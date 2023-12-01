from typing import Any
from urllib.parse import urlparse

import paho.mqtt.publish as publish  # type: ignore
from jcx.net.mqtt.cfg import MqttCfg
from jcx.text.txt_json import to_json


class Publisher:

    def __init__(self, cfg: MqttCfg):
        uri = urlparse(cfg.server_url)
        strs = uri.netloc.split(':', 1)
        self.params = {
            'transport': uri.scheme,
            'hostname': strs[0],
            'port': int(strs[1]),
        }
        self.root_topic = cfg.root_topic

    def publish(self, topic: str, msg: Any) -> None:
        s = to_json(msg)
        publish.single(self.root_topic + '/' + topic, s, **self.params)
