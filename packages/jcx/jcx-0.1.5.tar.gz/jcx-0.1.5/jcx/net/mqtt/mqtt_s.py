import paho.mqtt.publish as publish
import requests


def transmitMQTT(strMsg):
    strMqttBroker = "localhost"
    strMqttChannel = "test"
    # print(strMsg)
    publish.single(strMqttChannel, strMsg, hostname=strMqttBroker)


if __name__ == '__main__':
    baidu_url = 'https://www.baidu.com'

    response = requests.get(baidu_url)
    body = response.content.decode()
    # print()

    transmitMQTT(body)
    print("Send msg ok.")
