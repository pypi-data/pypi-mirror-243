"""decorators.py: decorator class and functions for junoplatform"""
__author__ = "Bruce.Lu"
__email__ = "lzbgt@icloud.com"
__time__ = "2023/07/20"


import logging
from collections import deque
from urllib.parse import parse_qs
import traceback
import json
import os
import time
import datetime
from functools import wraps
from junoplatform.log import logger
from junoplatform.io.utils import JunoConfig
from junoplatform.io import InputConfig, Storage, DataSet
from threading import Thread, Lock
import numpy as np
from junoplatform.io.misc import dict_value_diff
import yaml
import sys
import requests
from junoplatform.io.data_clean import ab_mock, abnormal_detection_clean, DetectionResult, TagWithProperties, parse_config
from junoplatform.io.dealer import Dealer
import inspect
from junoplatform.api.cloud import smartcall, send_notification


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(filename)s %(lineno)d - %(message)s')


class EntryPoint:
    def __init__(self, cfg_in: str | InputConfig, detached: bool = False):
        super(EntryPoint, self).__init__()
        self.cfg_in: InputConfig
        self.detached = detached
        self.storage = Storage()
        # self.dataset = DataSet()
        self.ready = False
        self.que = deque(maxlen=2000)
        self.stop_flag = True
        self.tick = "-1"
        self.tick_key = "deadbeaf"
        self.reconfig = False
        self.last_meta = {}
        self.data_clean = False
        self.confirms = []
        self.ab_detect_lock = Lock()
        self.ab_detect_num_local_last = 0

        # handle mapped files
        if not os.path.exists('_boot'):
            if os.path.exists('_project.yml'):
                r = None
                with open('_project.yml', 'r', encoding='utf-8') as f:
                    r = yaml.safe_load(f)
                with open('project.yml', 'w', encoding='utf-8') as f:
                    yaml.safe_dump(r, f)
                logging.info("copied _project.yml")

            if os.path.exists('_config.json'):
                r = None
                with open('_config.json', 'r') as f:
                    r = json.load(f)
                with open('config.json', 'w', encoding='utf-8') as f:
                    json.dump(r, f, ensure_ascii=False)
                logging.info("copied _config.json")

        if not os.path.exists('_boot'):
            r = None
            with open('_boot', 'w', encoding='utf-8') as f:
                f.write(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
                f.flush

        # load config
        self.config_lock = Lock()
        self.junoconfig = JunoConfig()
        self.plant = self.junoconfig["plant"]
        self.module = self.junoconfig["module"]
        self.package_id = self.junoconfig["package_id"]
        self.enable_key = f"system.{self.plant}.{self.module}.enable"
        self._cfg_in = cfg_in
        self.ab_detect_key = f"system.ai.abnormal.confirm.{self.plant}.{self.module}"
        self.tfmt = "%Y/%m/%d %H:%M:%S"

    def load_input(self):
        if isinstance(self._cfg_in, str):
            logging.debug(f"loading input spec from file: {self._cfg_in}")
            try:
                with open(self._cfg_in, "r", encoding="utf-8") as f:
                    self.cfg_in = InputConfig(**json.load(f))
            except Exception as e:
                msg = f"error in input.json: {e}"
                logger.error(msg)
                exit(1)
        elif isinstance(self._cfg_in, InputConfig):
            logging.info(f"loading input spec from class: {self.cfg_in}")
            self.cfg_in = self._cfg_in
        else:
            raise Exception(
                f"cfg_in must be type of InputConfig or string, but provides: {type(self._cfg_in)}")

    def update_meta(self, meta: dict):
        try:
            update_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            create_time = update_time
            if "create_time" in self.last_meta:
                create_time = self.last_meta["create_time"]
            meta["create_time"] = create_time
            vdiff = dict_value_diff(self.last_meta, meta)
            if vdiff:
                logging.info(f"meta changed: {vdiff}")
                meta["update_time"] = update_time
                self.storage.local.io.hset('system.ai.modules', f'{self.junoconfig["plant"]}.{self.junoconfig["module"]}', json.dumps(
                    meta, ensure_ascii=False).encode())
                meta.pop("update_time")
                self.last_meta = meta.copy()
        except Exception as e:
            pass

    def _thread(self, func):
        once = True
        lasterr = False
        cnterr = 0
        while True:
            try:
                self.tick = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ":1"
                try:
                    self.dataset = DataSet()
                except Exception as e:
                    logging.error(
                        "fault: failed to create DataSet to clickhouse, will retry in 7 seconds")
                    time.sleep(7)
                    continue
                # self.load_input()

                self.tick = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ":3"
                self.config_lock.acquire()
                self.junoconfig = JunoConfig()
                self.cfg_in = self.junoconfig['input_cfg']
                logging.info(f'cfg_in: {self.cfg_in}')
                self.config_lock.release()
                algo_cfg = self.junoconfig["algo_cfg"]
                logging.info(f'algo_cfg: {algo_cfg}')
                logging.info(f"running algo with {algo_cfg}")

                logging.info(f"run_env: {self.junoconfig['run_env']}")

                self.tick = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ":2"
                self.ready = True
                delay = self.cfg_in['sched_interval']
                enable = 1
                try:
                    enable = self.storage.local.read(self.enable_key, cast=int)
                    if enable is not None:
                        pass
                    else:
                        enable = 0
                    self.stop_flag = not bool(enable)
                except Exception as e:
                    logging.error(f"failed to read local: {e}")
                    time.sleep(7)
                    continue

                if once:
                    # update config
                    meta = {
                        "package_id": self.package_id,
                        "username": self.junoconfig["author"],
                        "plant": self.junoconfig["plant"],
                        "module": self.junoconfig["module"],
                        "config": self.junoconfig["algo_cfg"],
                        "status": 1,
                        "enable": enable,
                    }

                    self.update_meta(meta)
                    r = self.storage.local.io.set(f"system.{self.plant}.{self.module}.reconfig", json.dumps(
                        self.junoconfig["algo_cfg"], ensure_ascii=False))
                    once = False

                if not self.stop_flag:
                    data = None
                    timestamps = None
                    names = None
                    ts = datetime.datetime.now().timestamp()
                    if self.cfg_in['items']:
                        data, timestamps, names = self.dataset.fetch(
                            tags=self.cfg_in['tags'], num=self.cfg_in['items'])
                    elif self.cfg_in['minutes']:
                        time_from = datetime.datetime.now(
                        ) - datetime.timedelta(minutes=self.cfg_in['minutes'])
                        data, timestamps, names = self.dataset.fetch(
                            tags=self.cfg_in['tags'], time_from=time_from)
                    else:
                        logging.error("invalid InputConfig")
                        time.sleep(11)
                        continue

                    if isinstance(data, Exception):
                        logging.error(
                            f"exceptin fetch data: {str(data)}, skip schedule")
                        self.sleep(7)
                        continue

                    if data is None:
                        logging.error("failed to fetch data: None")
                        self.sleep(7)
                        continue

                    self.tick = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ":4"

                    self.tick_key = f"system.ai.tick.{self.plant}.{self.module}"
                    td = datetime.datetime.now().timestamp()
                    logging.info(f"time used fetching dataset: {td-ts}s")

                    try:
                        sig = inspect.signature(func)
                        ks = [k for k in sig.parameters.keys()]
                        lead_6 = ["storage", "algo_cfg", "data",
                                  "timestamps", "names", "entrypoint"]
                        if ks[:6] != lead_6:
                            logging.error(
                                f"entry point signature error,  expecting {lead_6} but provided {ks[:6]}")
                        if len(sig.parameters) == 6:
                            func(self.storage, algo_cfg, data,
                                 timestamps, names, self)
                            logging.info("called func without get_abnormal")
                        elif len(sig.parameters) == 7 and 'ab_results' in sig.parameters:
                            tc = datetime.datetime.now()
                            clean_data, ab, _ = self.get_abnormal(
                                tc, [])
                            if ab is None:
                                func(self.storage, algo_cfg, data,
                                     timestamps, names, self, None)
                                logging.info(
                                    "called func with get_abnormal providing raw_data and None abnormals")
                            else:
                                func(self.storage, algo_cfg, clean_data[-self.cfg_in['items']:],
                                     timestamps, names, self, ab)
                                logging.info(
                                    "called func with get_abnormal providing clean_data and abnormals")
                        else:
                            logging.error(
                                f'entry function signature error, expecting {lead_6.__add__(["ab_results"])} but provided {ks}')

                    except Exception as e:
                        msg = traceback.format_exc()
                        logger.error(f"exception {e}: {msg}")

                        message = {
                            "name": "junoplatform",
                            "message": f"算法模块调度执行异常: ({self.plant}, {self.module}, {self.junoconfig['package_id']})" + "\n  " + msg
                        }

                        try:
                            self.storage.cloud.write(
                                'juno-svc-notification', message, raw_table=True)
                            # smartcall
                            scr = self.storage.local.read(
                                f'system.ai.smartcall.{self.junoconfig["plant"]}.{self.junoconfig["module"]}', cast=dict)
                            if scr and datetime.datetime.now().timestamp() - scr["params"]["ts"] < 60 * 30:
                                logging.info(
                                    "skip smart voice call, since this module called in 30 minutes already")
                            elif "smartcall" in self.junoconfig and "token" in self.junoconfig["smartcall"] and "api" in self.junoconfig["smartcall"] and "numbers" in self.junoconfig["smartcall"]:
                                for number in self.junoconfig["smartcall"]["numbers"]:
                                    calldata = {
                                        "number": number,
                                        "params": {
                                            "plant": f'{self.junoconfig["plant"]}水厂 ',
                                            "module": f' {self.junoconfig["module"]}算法模块 ',
                                            "fault": f"算法代码执行错误为 {str(e)} ",
                                            "ts": datetime.datetime.now().timestamp()
                                        }
                                    }
                                    r = requests.post(self.junoconfig["smartcall"]["api"], json=calldata, headers={
                                        "Authorization": f'Bearer {self.junoconfig["smartcall"]["token"]}'
                                    })
                                    logging.info(r.text)
                                    self.storage.local.write(
                                        f'system.ai.smartcall.{self.junoconfig["plant"]}.{self.junoconfig["module"]}', calldata)
                            else:
                                logging.info(
                                    "smartcall not configured, skip voice call")
                        except Exception as e:
                            errmsg = traceback.format_exc()
                            logging.error(f"failed send pulsar, {e}: {errmsg}")

                    self.tick = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ":5"

                    te = datetime.datetime.now().timestamp()
                    logging.info(f"time used running algo: {te-td}s")

                    delay = self.cfg_in['sched_interval'] - (te - ts) - 1
                    logging.debug(
                        f"delay in seconds to make up a full sched_interval: {delay}")
                    if delay < 0:
                        delay = 0
                else:
                    logging.info("module disabled, skip run algo func")
                    delay = 60

                logging.info(f"delay remain: {delay}s")

                self.tick = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ":6"
                del self.dataset
                self.sleep(delay)
                self.tick = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ":7"
                lasterr = False
            except Exception as e:
                errmsg = traceback.format_exc()
                logging.error(errmsg)
                if cnterr == 5:
                    os._exit(1)
                else:
                    if not lasterr:
                        lasterr = True
                        cnt = 1
                    else:
                        cnt += 1

                self.sleep(20+1)

    def sleep(self, secs: float):
        while secs > 0:
            time.sleep(1)
            self.tick = datetime.datetime.now().strftime(
                "%Y%m%d%H%M%S") + f":-{secs}"
            secs -= 1
            try:
                r = self.storage.local.io.get(
                    f"system.{self.plant}.{self.module}.enable")
                if r:
                    r = bool(int(r.decode()))
                    r = not r
                    if r != self.stop_flag:
                        logging.info(f'stop flag: {r}, {self.stop_flag}')
                        self.stop_flag = r
                        self.reconfig = True
                        msg_enable = "算法模块开启:" if not r else "算法模块关闭:"
                        msg_enable += f" ({self.plant, self.module, self.package_id})"
                        message = {
                            "name": "junoplatform",
                            "message": msg_enable
                        }
                        logging.info(msg_enable)
                        self.storage.cloud.write(
                            'juno-svc-notification', message, raw_table=True)
                r = self.storage.local.io.get(
                    f"system.{self.plant}.{self.module}.reconfig")
                if r:
                    r = json.loads(r.decode())
                    diff = dict_value_diff(self.junoconfig['algo_cfg'], r)
                    if diff:
                        logging.info(f'algo config diff: {diff}\ntnew: {r}')
                        JunoConfig.save_algo_config(r)
                        self.reconfig = True
            except Exception as e:
                logging.error(f"exception running algo: {str(e)}")

            if self.reconfig:
                logging.info("reconfig occurred")
                self.reconfig = False
                time.sleep(0)
                break

    def s_get_bool(self, v: str):
        try:
            x = int(v)
            return x != 0
        except:
            if v.lower() in ["t", "true", "y", "yes", "ok", "on", "enable", "active"]:
                return True
            else:
                return False

    def get_abnormal(self, ts: datetime.datetime, confirms: list, need_report: bool = False):
        try:
            hist_len = None
            self.ab_detect_lock.acquire()
            data_config = {}
            with self.config_lock:
                data_config = JunoConfig()
                try:
                    hist_len, tags = parse_config(data_config)
                except Exception as e:
                    logging.error(e)
                    os._exit(-1)

            if hist_len is None:
                if not self.confirms:
                    logging.error(
                        f"ab_detection will be disbled, since {tags}, please correct config.json if needed")
                    return None, None, None

            ts_far = ts - datetime.timedelta(minutes=hist_len+1)
            logging.info(f"hist_len: {hist_len}, ts_far: {ts_far}")
            mark = ts_far

            siz = self.storage.local.io.llen(self.ab_detect_key)
            if not siz:
                siz = 0

            if not confirms:
                # prepair confirms
                # calc farest time
                i = 0
                while True:
                    uc = self.storage.local.io.lrange(self.ab_detect_key, i, i)
                    if uc:
                        uc = [json.loads(x) for x in uc]
                        tevt = datetime.datetime.strptime(
                            uc[0]["_time_"], self.tfmt)
                        if tevt < ts_far:
                            i += 1
                        else:
                            break
                    else:
                        break
                # discard older records
                if i > 0:
                    self.storage.local.io.lpop(self.ab_detect_key, i)
                    logging.info(
                        f"pop {i} record of user confirms for {self.ab_detect_key}")
                else:
                    logging.info(
                        f"pop no record of user confirms for {self.ab_detect_key}")
                uc = self.storage.local.io.lrange(self.ab_detect_key, 0, -1)
                if uc:
                    if need_report:
                        logging.info(f"uc: {uc}")
                    uc = [json.loads(x) for x in uc]
                    self.ab_detect_num_local_last = len(uc)
                    for i in range(len(uc)):
                        ut = uc[i]["_time_"]
                        uc[i]["_time_"] = datetime.datetime.strptime(
                            uc[i]["_time_"], self.tfmt)
                        u = uc[i]
                        td: datetime.timedelta = u["_time_"] - mark
                        num = int(td.seconds/60 - 1)
                        if need_report:
                            logging.info(
                                f"num: {num}, ts: {ts}, td: {td}, u: {ut}, mark: {mark}")
                        if num < 0:
                            num = 0
                        # pre
                        for j in range(num):
                            rec = []
                            for t in tags:
                                rec.append(-1)
                            confirms.append(rec)
                        # me
                        rec = []
                        for t in tags:
                            if t.name not in u:
                                rec.append(-1)
                            else:
                                rec.append(u[t.name])
                        confirms.append(rec)
                        # next mark
                        mark = u["_time_"]
                    # rest
                    td: datetime.timedelta = ts - mark
                    num = int(td.seconds/60)
                    if num < 0:
                        num = 0

                    for j in range(num):
                        rec = []
                        for t in tags:
                            rec.append(-1)
                        confirms.append(rec)
                else:  # no uc
                    self.ab_detect_num_local_last = 0
                    for i in range(hist_len):
                        rec = []
                        for t in tags:
                            rec.append(-1)
                        confirms.append(rec)
            else:
                confirms = confirms[1:]
                if siz != self.ab_detect_num_local_last and siz != 0:
                    _u = self.storage.local.io.lindex(
                        self.ab_detect_key, siz - 1)
                    u = json.loads(_u)
                    self.ab_detect_num_local_last = siz
                    rec = []
                    for t in tags:
                        if t.name not in u:
                            rec.append(-1)
                        else:
                            rec.append(u[t.name])
                    confirms.append(rec)
                else:
                    for i in range(hist_len):
                        rec = []
                        for t in tags:
                            rec.append(-1)
                        confirms.append(rec)

            errta = len(confirms) - hist_len
            if errta > 0:
                confirms = confirms[errta:]
            elif errta < 0:
                # should not happen
                pass

            _confirms = np.array(confirms)

            debug_len = min(hist_len, 30)
            logging.info(
                f"calc confirms[-{debug_len}:]: \n{confirms[-debug_len:]}")
            if need_report:
                logging.info(f"start of data clean: uc {_confirms.shape}")

            self._dateset = DataSet()
            d, t, _ = self._dateset.fetch(
                tags=self.cfg_in['tags'], num=hist_len)

            d, ab = abnormal_detection_clean(d, tags, t, _confirms)
            ab_m = None
            try:
                ab_m = ab_mock(tags)
                logging.info("mock data used")
            except FileNotFoundError:
                pass
            except Exception as e:
                logging.warning(f"mock data load failed: {str(e)}")

            if ab_m:
                ab = ab_m

            if not ab:
                logging.error("abnormal_detection_clean returns None as ab")
                return None, None, None
            else:
                # report
                if need_report:
                    rpts = {}
                    res: DetectionResult = None
                    for x in ab:
                        if x.alarm > 0:
                            rpts[x.name] = {'value': x.value, 'alarm': x.alarm}
                            res = x

                    if res:
                        msg = f"点位异常检测通知 ({self.plant}, {self.module}):\r\n"
                        msg += json.dumps(rpts, ensure_ascii=False)

                        msgsent = 0
                        if data_config["run_env"] == "dev":
                            msgsent = send_notification(
                                self.storage, 'ab_detect', msg, -1)
                        else:
                            msgsent = send_notification(
                                self.storage, 'ab_detect', msg)
                        if msgsent == 0:
                            logging.info(
                                f'run_env={data_config["run_env"]} abnormal notification sent')

                        fault = f"点位数值发生异常"
                        msgsent = smartcall(
                            self.storage, 'ab_detect', fault, 60)

                        if msgsent == 0:
                            logging.info(
                                f'run_env={data_config["run_env"]} abnormal smartcall sent')

                    logging.info(
                        f"get_abnormal: {len(d)}, {len(ab)}, {hist_len}")

                return d, ab, hist_len

        except Exception as e:
            errmsg = traceback.format_exc()
            logging.error(f"{str(e)}: {errmsg}")
            return None, None, None
        finally:
            self.ab_detect_lock.release()

    def _data_analysis_clean(self):
        time.sleep(21)

        while True:
            while True:
                if self.stop_flag:
                    logging.info("skip ab_detect since module disabled")
                    time.sleep(7)
                    continue
                else:
                    break

            ts = datetime.datetime.now()
            try:
                _, ab, hist_len = self.get_abnormal(ts, [], True)
                print(ab, hist_len)
                if hist_len is None:
                    logging.warning("ab_detection disabled, skip")
                    time.sleep(120)
                    continue

                if not ab:
                    logging.error("get no ab from ab_detect")
                else:
                    payload = {
                        "module": f"{self.plant}.{self.module}",
                        "alarms": None
                    }
                    alarms = []
                    x: DetectionResult

                    for x in ab:
                        alarms.append({
                            "tag": x.name,
                            # 0: no alarm/recover, # 1: active alarm
                            "alarm": int(x.alarm),
                            "value": float(x.value),
                            "time": x.time,    # ie: "2023/11/19 10:20:30", localtime
                        })
                    payload["alarms"] = alarms
                    payload = json.dumps(payload)
                    self.storage.dealer.write(
                        f"{self.plant}.jp-backend", payload)
                    logging.info(f"alarms sent: {payload}")

                logging.info("dealer waiting for message")
                tsr = 60 - (datetime.datetime.now().timestamp() -
                            ts.timestamp())
                if tsr < 0:
                    tsr = 0
                confirms = []
                while tsr > 0:
                    messages = self.storage.dealer.read(timeout=tsr)
                    if messages is not None and len(messages) == 2:
                        mfrom: str = messages[0].decode()
                        if mfrom.startswith(f"{self.plant}.jp-backend"):
                            msg = json.loads(messages[1])
                            if msg["module"] == f"{self.plant}.{self.module}":
                                confirms.extend(msg["data"])
                            else:
                                logging.warning(
                                    f"invalid module in dealer msg: {msg['module']}")
                        else:
                            logging.warning(
                                f"invalid sender id in dealer msg: {mfrom}")
                    else:
                        logging.warning(
                            f"invalid msg from dealer: {messages}")

                    tsr = 60 - \
                        (datetime.datetime.now().timestamp() - ts.timestamp())

                if confirms:
                    uc = {x["tag"]: x["value"] for x in confirms}
                    uc["_time_"] = confirms[-1]["time"]

                    self.storage.local.io.rpush(
                        self.ab_detect_key, json.dumps(uc).encode())
                    logging.info("user confirmation stored: {uc}")
                # else:
                #     uc = [{"_none_": -1,
                #           "_time_": ts.strftime("%Y/%m/%d %H:%M:%S")}]
                #     self.storage.local.io.rpush(
                #         self.ab_detect_key, json.dumps(uc).encode())

                siz = self.storage.local.io.llen(self.ab_detect_key)
                if siz > hist_len:
                    self.storage.local.io.lpop(
                        self.ab_detect_key, siz - hist_len)

                logging.info(
                    f"end of data clean and confirm process: {confirms}")

            except Exception as e:
                errmsg = traceback.format_exc()
                logging.error(f"exception in data clean {str(e)}: {errmsg}")
                time.sleep(7)
                continue

    def _pulsar(self):
        itopic = f"jprt-down-{self.plant}-{self.module}"
        while True:
            msg = None
            try:
                msg = self.storage.cloud.read(itopic, shared=False)
            except Exception as e:
                logging.error(f"failed to write cloud: {e}")
                time.sleep(7)
                continue
            data = {}
            logger.info(f"command received: {msg.data()}")
            try:
                data = json.loads(msg.data())
                if "package_id" not in data or self.junoconfig['package_id'] != data["package_id"]:
                    logger.error(
                        f"invalid msg received {data}, self package_id: {self.junoconfig['package_id']}")
                    self.storage.cloud.consumers[itopic].acknowledge(msg)
                    continue
            except Exception as e:
                logger.error(f"invalid msg received, {e}: {msg.data()}")
                if msg:
                    try:
                        self.storage.cloud.consumers[itopic].acknowledge(msg)
                    except:
                        pass
                time.sleep(7)
                continue

            if "cmd" in data:
                if data["cmd"] == "enable":
                    cmd = parse_qs(data['qs'])
                    v = cmd.get('enable', [''])[0]
                    if v:
                        enable = self.s_get_bool(v)
                        if not enable:
                            self.stop_flag = True
                            logging.info("enable=false cmd received")
                        else:
                            self.stop_flag = False
                            logging.info("enable=true cmd received")

                        data = {"enable": enable,
                                "et": datetime.datetime.now().timestamp()*1000, "kind": "1", "package_id": data["package_id"]}
                        try:
                            self.storage.cloud.write("module_state_new", data)
                            self.storage.local.write(
                                self.enable_key, int(enable))

                            msg_enable = "算法模块开启:" if enable else "算法模块关闭:"
                            msg_enable += f" ({self.plant, self.module, self.package_id})"
                            message = {
                                "name": "junoplatform",
                                "message": msg_enable
                            }
                            self.storage.cloud.write(
                                'juno-svc-notification', message, raw_table=True)

                        except Exception as e:
                            logging.error(
                                f"failed to write cloud and local: {e}")
                        self.reconfig = True
                elif data["cmd"] == "reconfig":
                    config = data["data"]["config"]
                    JunoConfig.save_algo_config(config)
                    self.reconfig = True

            else:
                logging.error(f"unkown msg: {data}")

            try:
                self.storage.cloud.consumers[itopic].acknowledge(msg)
            except:
                pass

    def _heart_beat(self):
        last_tick = "."
        count = 0
        while True:
            data = {"enable": not self.stop_flag,
                    "et": datetime.datetime.now().timestamp()*1000, "kind": "0", "package_id": self.package_id}
            try:
                self.storage.cloud.write("module_state_new", data)
            except Exception as e:
                logging.error(f"failed to write cloud: {e}")

            if count % 5 == 0:
                if last_tick == self.tick:
                    try:
                        if not self.storage.local.io.get(self.tick_key):
                            message = {
                                "name": "junoplatform",
                                "message": f"算法模块可能挂死: ({self.plant}, {self.module}, {self.junoconfig['package_id']})" + ":" + self.tick
                            }
                            self.storage.cloud.write(
                                'juno-svc-notification', message, raw_table=True)
                            self.storage.local.io.set(self.tick_key, self.tick)
                    except Exception as e:
                        errmsg = traceback.format_exc()
                        logging.error(
                            f"exception when check tick and send hang notification: {errmsg}")
                        os._exit(1)

            if last_tick != self.tick:
                try:
                    if self.storage.local.io.get(self.tick_key):
                        self.storage.local.io.delete(self.tick_key)
                        message = {
                            "name": "junoplatform",
                            "message": f"算法模块挂死恢复: ({self.plant}, {self.module}, {self.junoconfig['package_id']})" + ":" + self.tick
                        }
                        self.storage.cloud.write(
                            'juno-svc-notification', message, raw_table=True)
                except Exception as e:
                    errmsg = traceback.format_exc()
                    logging.error(
                        f"exception when check tick and send recovery notification: {errmsg}")
                    os._exit(1)

            # heartbeat interval is 1 minutes
            last_tick = self.tick
            count += 1
            time.sleep(60)

    def __call__(self, func):
        th = Thread(target=self._thread, args=(func,))
        th.start()

        while not self.ready:
            time.sleep(0)

        pt = Thread(target=self._pulsar)
        pt.start()

        hb = Thread(target=self._heart_beat)
        hb.start()

        dc = Thread(target=self._data_analysis_clean)
        dc.start()


def auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not os.path.exists(args[0].juno_dir) or not os.path.exists(args[0].juno_file):
            logger.error(f"user not authenticationd.\n\
                          please run `junocli login [api_url]` to use your shuhan account")
            os.makedirs(args[0].juno_dir, exist_ok=True)
            return -1
        return func(*args, **kwargs)

    return wrapper
