import zmq
from threading import Thread, Event
import queue
import time
import json
import logging
from junoplatform.io._driver import IWriter, IReader, ALock

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(filename)s %(lineno)d - %(message)s')


class Dealer(IWriter, IReader):
    def __init__(self, id: str, router_addr: str, lock: ALock = None):
        super().__init__()
        self.closed = False
        self.lock = lock
        self.context = zmq.Context()
        # Dealer socket
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.setsockopt(zmq.IDENTITY, id.encode())
        self.socket.connect(router_addr)
        self.socket.setsockopt(zmq.RCVTIMEO, 1000)
        self.rque = queue.Queue()
        self.sque = queue.Queue()
        self.event = Event()
        #
        self.th_rcv = Thread(target=self._rcv, args=(self.rque, self.event))
        self.th_rcv.start()
        #
        self.th_send = Thread(target=self._send, args=(self.sque, self.event))
        self.th_send.start()

    def _rcv(self, q: queue.Queue, evt: Event):
        while True:
            try:
                messages = self.socket.recv_multipart()
                logging.info(f"dealer message received: {messages}")
                q.put(messages)
            except zmq.Again:
                pass
            except Exception as e:
                logging.error(f"exception when recv zmq: {str(e)}")
            finally:
                if evt.is_set():
                    return

    def _send(self, q: queue.Queue, evt: Event):
        while True:
            try:
                m = q.get(timeout=1)
                self.socket.send_multipart(m)
            except queue.Empty:
                pass
            except Exception as e:
                logging.error(f"exception get item from queue: {(str(e))}")
            finally:
                if evt.is_set():
                    return

    def write(self, target: str, data: str):
        if self.lock:
            if not self.lock.aquire():
                logging.warning(f"holding no lock, skip dealer write")
                return
        m0 = target.encode()
        m1 = data.encode()
        self.sque.put([m0, m1])

    def read(self, timeout: float = -1):
        if timeout < 0:
            return self.rque.get()
        else:
            try:
                r = self.rque.get(timeout=timeout)
                return r
            except queue.Empty:
                return None
            except Exception as e:
                logging.error(f"exception get self.rque: {str(e)}")
                return None

    def close(self):
        self.event.set()
        self.socket.close()
        self.context.destroy()
        self.closed = True

    def __del__(self):
        self.close()


if __name__ == "__main__":
    i = 0
    dealer = Dealer("yudai.TEST", "tcp://192.168.101.168:2302")
    while True:
        m0 = "yudai.jp-backend"
        m1 = {
            "module": "yudai.TEST",
            "alarms": [
                {
                    "tag": "COD2",
                    "alarm": 1,  # 0: no alarm/recover, # 1: active alarm
                    "value": 1000.0,
                    "time": "2023/11/20 10:20:30",  # ie: "2023/11/19 10:20:30", localtime
                    "others": "TBD"
                }
            ]
        }

        m1 = json.dumps(m1)
        dealer.send(m0, m1)
        print("sent: ", i)
        i += 1
        time.sleep(5)
