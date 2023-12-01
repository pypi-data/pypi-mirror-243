import os
from typing import Any
from urllib.parse import urlparse

import paho.mqtt.client as mqtt  # type: ignore
from jcx.net.mqtt.cfg import MqttCfg
from loguru import logger


class Subscriber:
    """MQTT消息订阅者"""

    def __init__(self, cfg: MqttCfg):
        """创建MQTT消息订阅者"""
        uri = urlparse(cfg.server_url)
        strs = uri.netloc.split(':', 1)
        self.url = cfg.server_url
        self.params = {
            'transport': uri.scheme,
            'hostname': strs[0],
            'port': int(strs[1]),
        }
        self.root_topic = cfg.root_topic
        self.client = mqtt.Client(protocol=mqtt.MQTTv5)
        self.client.on_message = on_message

    def dispatch_msg(self, topic: str, user_object: Any, timeout: float = 8.0) -> None:
        """分发消息"""
        self.client.user_data_set(user_object)

        topic = os.path.join(self.root_topic, topic)
        logger.info('Subscribe mqtt topic: %s/%s ...' % (self.url, topic))

        self.client.connect(self.params['hostname'], self.params['port'], 60)
        self.client.subscribe(topic, 0)

        self.client.loop_forever(timeout=timeout)


def on_message(_client, user_object: Any, msg: mqtt.MQTTMessage) -> None:
    if user_object is not None:
        user_object.on_mqtt_message(msg)


def a_test() -> None:
    class Outputer:
        def on_mqtt_message(self, mqtt_msg: mqtt.MQTTMessage) -> None:
            assert self
            print('Outputer:', mqtt_msg.payload)

    outputer = Outputer()

    cfg = MqttCfg('tcp://localhost:1883', 'howell')
    subcriber = Subscriber(cfg)

    # subcriber.loop(lambda msg: print(msg))
    subcriber.dispatch_msg('1/#', outputer)


if __name__ == '__main__':
    a_test()
