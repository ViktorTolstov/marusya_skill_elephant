import logging
import socket
import time
from typing import Dict, Tuple

from .config import config

logger = logging.getLogger()


class GraphiteClient:
    def __init__(self) -> None:
        self._metrics_sum: Dict = {}
        self._metrics_avg: Dict = {}
        self._last_sended: int = 0
        self._address: Tuple = tuple()
        self._graphite_prefix: str = ''
        self.configure()

    @property
    def graphite_prefix(self):
        return self._graphite_prefix

    def configure(self):
        try:
            self._address = (
                config.get('graphite', 'host'),
                int(config.get('graphite', 'port'))
            )
            self._graphite_prefix = config.get('graphite', 'ns')
        except Exception as ex:
            logger.error("Can't read graphite configuration!")

    def collect_add(self, name, value):
        if name not in self._metrics_sum:
            self._metrics_sum[name] = 0.0
        self._metrics_sum[name] += value

    def collect_avg(self, name, value):
        if name not in self._metrics_avg:
            self._metrics_avg[name] = [0.0, 0]
        self._metrics_avg[name][0] += value
        self._metrics_avg[name][1] += 1

    def send(self):
        message: str
        try:
            while len(self._metrics_sum) > 0:
                message = ""
                do_sum = min(len(self._metrics_sum), 10)
                ts = time.time()
                for i in range(do_sum):
                    (name, val) = self._metrics_sum.popitem()
                    message += "%s.%s %d %d\n" % (
                        self.graphite_prefix, name,
                        int(val), int(ts)
                    )
                    message += "%s.%s %d %d\n" % (
                        self.graphite_prefix, f'{name}_rps',
                        int(val / (ts - self._last_sended)), int(ts)
                    )
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
                if self._address:
                    sock.sendto(message.encode(), self._address)

            while len(self._metrics_avg) > 0:
                message = ""
                do_avg = min(len(self._metrics_avg), 10)
                for i in range(do_avg):
                    (name, val) = self._metrics_avg.popitem()
                    (sum, count) = val
                    if count <= 0:
                        continue
                    message += "%s.%s %f %d\n" % (
                        self.graphite_prefix, name,
                        sum / (1.0 * count), int(time.time())
                    )
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
                if self._address:
                    sock.sendto(message, self._address)

        except Exception as ex:
            logger.error("Stats exception: %s" % (str(ex)))
            self._metrics_avg = {}  # to continue working
            self._metrics_sum = {}  # without service restart

    def check_send(self):
        ts: int = int(time.time())
        if ts - self._last_sended > 20:
            self.send()
            self._last_sended = ts

    def handle_error(self):
        self.collect_add('error', 1)
        self.check_send()

    def handle_request(self, name: str):
        self.collect_add(name, 1)
        self.check_send()


graphite_client: GraphiteClient = GraphiteClient()
