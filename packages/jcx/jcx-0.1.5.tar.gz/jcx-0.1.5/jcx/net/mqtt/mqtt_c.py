#!/usr/bin/python3

import datetime

import paho.mqtt.client as mqtt


def on_connect(mqttc, obj, rc):
    print("OnConnetc, rc: " + str(rc))


def on_publish(mqttc, obj, mid):
    print("OnPublish, mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print("Log:" + string)


def on_message(mqttc, obj, msg):
    curtime = datetime.datetime.now()
    strcurtime = curtime.strftime("%Y-%m-%d %H:%M:%S")
    print(strcurtime + ": " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


if __name__ == '__main__':
    mqttc = mqtt.Client("test")
    mqttc.on_message = on_message
    # mqttc.on_connect = on_connect
    # mqttc.on_publish = on_publish
    # mqttc.on_subscribe = on_subscribe
    # mqttc.on_log = on_log

    # 设置账号密码（如果需要的话）
    # mqttc.username_pw_set(username, password=password)

    # 服务器地址
    strBroker = "localhost"
    # 通信端口
    port = 1883

    # 订阅主题名
    topic = 'howell/ias/#'

    mqttc.connect(strBroker, port, 60)
    mqttc.subscribe(topic, 0)
    mqttc.loop_forever()
