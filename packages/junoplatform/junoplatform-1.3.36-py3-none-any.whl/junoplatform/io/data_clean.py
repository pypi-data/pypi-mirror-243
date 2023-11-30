import numpy as np
from datetime import datetime
from typing import List, Tuple
from pydantic import BaseModel
import logging
import random
import json
from junoplatform.io.utils import JunoConfig


class DetectionResult(BaseModel):
    alarm: int    # 告警标志： 0, 不告警; 1, 传感器数值异常告警; 2, 传感器长时间不变告警; 3, 执行机构未执行算法动作告警
    name: str     # 点位名
    value: float  # 点位当前raw值
    time: str     # 当前时间
    direction: int  # 正反作用，正1表示出现异常时加药，反-1表示出现异常时减药，0表示出现异常对加药不影响
    device_type: list  # 设备类型 [-1表示传感器|0表示不需要检查，会对大于1的相同编号的点位进行对比，检测时长（单位：分钟）]
    work_time: int  # 人工处理有效时间
    processed_res: int  # work_time时间内人工处理结果, -1表示未处理，0表示是真数据，1表示是假数据


class TagWithProperties(BaseModel):
    name: str       # 点位名
    work_time: int      # 人工处理有效时间
    normal_range: list  # 初始化部署时人工设定正常范围 [上限，下限]
    device_type: list   # 设备类型 [-1表示传感器|0表示不需要检查，会对大于1的相同编号的点位进行对比，检测时长（单位：分钟）]
    direction: int      # 正反作用，正1表示出现异常时加药，反-1表示出现异常时减药，0表示出现异常对加药不影响


def abnormal_detection_clean(
    raw_data: np.ndarray,
    tags: List[TagWithProperties],
    times: List[datetime],
    user_confirmation: np.ndarray
) -> Tuple[np.ndarray, List[DetectionResult]]:
    """_summary_

    Args:
        raw (np.ndarray): 原始数据 shape(n,m), n 可通过config.json配置
        tags (List[dict]): 原始数据点位名列表, 需要算法提供点位属性定义
        times (List[datetime]): 原始数据时间线列表
        user_conformation (np.ndarray): 用户确认历史 shape(n,m)

    Returns:
        List[DetectionResult]: 当前检测各点位结果列表
    """

    cfg = JunoConfig()['algo_cfg']

    # 1. 解析tags
    tag_names = []
    work_times = []
    normal_ranges = []
    device_types = []
    device_checktimes = []
    directions = []

    for k in tags:
        tag_names.append(k.name)
        work_times.append(k.work_time)
        normal_ranges.append(k.normal_range)
        device_types.append(k.device_type[0])
        device_checktimes.append(k.device_type[1])
        directions.append(k.direction)

    # 2. 数据预修正
    data_res = raw_data.copy()

    # 3. 异常检测
    # 如果数据小于10000条，则使用人工指定的边界
    if data_res.shape[0] < 10000:
        lower_bound = np.array([i[0] for i in normal_ranges])
        upper_bound = np.array([i[1] for i in normal_ranges])
        mad = np.ones_like(upper_bound) * 0.2
    else:
        # 计算中位数、绝对中位差 (MAD)
        median = np.median(data_res, axis=0)
        mad = np.median(np.abs(data_res - median), axis=0)

        # 根据3sigma原则，判定异常值
        lower_bound = median - 3 * (1.4826 * mad)
        upper_bound = median + 3 * (1.4826 * mad)

    # 生成异常检测的mask
    sigma_mask = np.logical_and(np.logical_or(
        data_res < lower_bound, data_res > upper_bound), mad > 0.1)

    # 传感器波动性检测和动作执行成功性检测
    device_types = np.array(device_types)
    sensor_mask = np.zeros_like(device_types, dtype=bool)
    for i in range(len(device_types)):
        if device_types[i] < -0.5 and device_types[i] > -1.5:
            # 传感器的类型编码为-1
            # 忽略高采样率传感器的短暂性异常, 其危害性较小, 连续10分钟异常才告警
            if device_checktimes[i] < 120 and np.all(sigma_mask[-10:, i]):
                sigma_mask[-1, i] = True
            else:
                sigma_mask[-1, i] = False

            # 如果波动性较小则为True, 否则为False
            tmp = data_res[-device_checktimes[i]:, i]
            if np.std(tmp) / (np.abs(np.mean(tmp))+0.001) < cfg['ab_sensor_reliability_threshold']:
                sensor_mask[i] = True

    # 动作执行成功性检测
    actuator_mask = np.zeros_like(sensor_mask, dtype=bool)
    actuator_type_set = set(device_types)
    for e in actuator_type_set:
        if e > 0.5:
            tmp_index = np.where(device_types == e)
            tmp1 = np.diff(
                data_res[-device_checktimes[tmp_index[0][0]]:, tmp_index[0][0]])
            tmp2 = np.diff(
                data_res[-device_checktimes[tmp_index[0][0]]:, tmp_index[0][1]])
            energy1 = np.sum(np.abs(tmp1))
            energy2 = np.sum(np.abs(tmp1))
            # 两者的能量差小于0.1就不用管了，异常不异常都无所谓
            if np.abs(energy1 - energy2) < 0.1:
                continue
            corr_coef = np.corrcoef(tmp1, tmp2)[0][1]

            # 执行机构不检查数值异常
            # sigma_mask[-1, tmp_index[0][0]] = False
            # sigma_mask[-1, tmp_index[0][1]] = False
            # 如果有两个diff都长期不动，则认为是设定值未发生调整，通过能量占比？

            if corr_coef < cfg['ab_actuator_corr_threshold'] and \
                    (energy1 < cfg['ab_actuator_energy_threshold']*energy2 or energy2 < cfg['ab_actuator_energy_threshold']*energy1):
                actuator_mask[tmp_index[0][0]] = True
                actuator_mask[tmp_index[0][1]] = True

    # 对3种异常检测结果整合
    abnormal_mask = np.logical_or(np.logical_or(
        sigma_mask[-1, :], actuator_mask), sensor_mask)
    # 如果点位被屏蔽，则不进行异常检测
    abnormal_mask = np.logical_and(abnormal_mask, (device_types > -1.5))
    alarm_res = []

    for i, tag in enumerate(tags):
        tmp = DetectionResult(name=tag.name, value=raw_data[-1, i], time=times[-1].strftime("%Y/%m/%d %H:%M:%S"), direction=directions[i],
                              alarm=0, processed_res=-1, device_type=tag.device_type, work_time=work_times[i])

        # 从后往前找到第一个不是-1的数的索引
        index = np.where(user_confirmation[-work_times[i]:, i][::-1] != -1)[0]
        # 如果找到了不是-1的数，返回该数
        if index.size > 0:
            tmp.processed_res = user_confirmation[-index[0]-1, i]
            confirmed_flag = True
        else:
            tmp.processed_res = -1
            confirmed_flag = False

        if abnormal_mask[i] and not confirmed_flag:
            # 发现异常且60分钟内人工都未处理，告警
            tmp.alarm = int(1 * sigma_mask[-1, i] + 2 * sensor_mask[i] * (
                not sigma_mask[-1, i]) + 3 * actuator_mask[i] * (not sensor_mask[i]) * (not sigma_mask[-1, i]))
        else:
            # 未发现异常或者人工已经处理过, 不告警
            tmp.alarm = 0

        alarm_res.append(tmp)

    return (raw_data, alarm_res)


idx = 0
mock_data = []


def ab_mock(tags: List[TagWithProperties]):
    global idx
    global mock_data
    if idx == 0:
        with open('ab_mock.json', 'r') as f:
            mock_data = json.load(f)
            logging.info(f"has ab_mock data: {mock_data}")

    if len(mock_data):
        abs = []
        for i, tag in enumerate(tags):
            abs.append(DetectionResult(name=tag.name, value=random.randint(1000, 3000),
                                       time=datetime.now().strftime("%Y/%m/%d %H:%M:%S"), direction=0,
                                       alarm=mock_data[idx][i], processed_res=-1, device_type=tag.device_type, work_time=60))
        logging.info(f"mock data used in alarms: {mock_data[idx]}")

        idx += 1
        if idx >= len(mock_data):
            idx = 0
        return abs


def parse_config(config: dict):
    num = config["input_cfg"]["items"]
    if "ab_detect" not in config["algo_cfg"]:
        return (None, "ab_detect not configed in config.json")
    _config = config["algo_cfg"]["ab_detect"]
    if "confirm_len" not in _config or "tags" not in _config:
        raise Exception(
            "missing confirm_len or tags of ab_detect in config.json")
    tags = _config["tags"]

    _tags = [x["name"] for x in tags]
    if _tags != config["input_cfg"]["tags"]:
        raise Exception(
            f'tag names or tags order in config.json["ab_detect"] is incorrect: expecting\n\t{config["input_cfg"]["tags"]}\n, but provided\n\t{_tags}\n, now hang execution. please fix the issue first!')

    logging.info(f"tags: {tags}")
    _tags = [TagWithProperties(name=x["name"], work_time=x["work_time"], normal_range=x["normal_range"],
                               device_type=x["device_type"], direction=x["direction"]) for x in tags]
    return (max(int(_config["confirm_len"]), num), _tags)
