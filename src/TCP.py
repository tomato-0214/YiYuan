import socketserver
import threading
import sys
import paho.mqtt.client as mqtt
from utils import addrr_map, load_yaml, getTS, data_verify
from config.log_config import getLogger
import json

logger = getLogger('TCP-Server')


class MyHandler(socketserver.BaseRequestHandler):
    load_yaml_d = load_yaml('devices.yaml')['devices']

    def task_listen(self):
        port = str(self.server.server_address[1])
        while True:
            try:
                data = self.request.recv(4096)

            except OSError as e:
                logger.error(e)
                break
            if data:
                try:
                    data_list = list(data)
                    logger.debug("接收到的原始数据：{}".format(data_list))
                    newdata = data_verify(data_list)
                    data_map = {}
                    if newdata:
                        values = newdata[7:-2]
                        val_list = addrr_map(port, values, newdata)

                        value_map = {}
                        name_tag_value = []
                        for val in val_list:
                            for key, value in val.items():
                                try:
                                    name_tag_list = self.load_yaml_d[port][key]
                                    name_tag_list.append(value)
                                    newname_tag_list = name_tag_list
                                    name_tag_value.append(newname_tag_list)
                                except Exception:
                                    logger.error("找不到对应的地址{}".format(key))
                                    continue

                        for i in name_tag_value:
                            value_map[i[1]] = i[2]
                            data_map[i[0]] = [{}]
                            data_map[i[0]][0]['ts'] = getTS()
                            data_map[i[0]][0]['values'] = value_map
                            # print(data_map)
                    client.publish(topic="v1/gateway/telemetry", payload=json.dumps(data_map), qos=0)
                    client.loop_start()
                    logger.info("数据推送成功！--{}".format(data_map))
                except UnicodeDecodeError:
                    logger.info("接受的数据为空！")
                # sys.stdout.write('\n')

    def task_send(self):
        while True:
            try:
                port = str(self.server.server_address[1])
                if port == '20010':
                    data = self.request.recv(4096)
                    # self.request.send(data)
                else:
                    continue
            except ConnectionResetError:
                continue

    def handle(self):
        print('客户端已连接', self.client_address, self.server.address_family)
        th1 = threading.Thread(target=self.task_listen, daemon=True)
        th2 = threading.Thread(target=self.task_send, daemon=True)

        th1.start()
        th2.start()
        th2.join()
        print('程序结束')
        self.server.shutdown()


def on_connect(client, userdata, flags, rc):
    print("Connect with result code" + str(rc))


def on_subscribe(client, userdata, mid, granted_qos):
    print("消息发送成功")


if __name__ == '__main__':
    # import argparse
    #
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-p', '--port', type=int)
    # args = parser.parse_args()
    client = mqtt.Client(protocol=3)
    client.username_pw_set("OowUiRSNYGd3oIeEADVH", None)
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.connect(host="112.250.106.100", port=11883, keepalive=60)
    logger.info("mqtt连接成功！")
    # if args.port:
    s = socketserver.ThreadingTCPServer(('0.0.0.0', 20010), MyHandler, bind_and_activate=True)
    s.serve_forever()  # 代表连接循环
    # else:
    #     print(parser.format_help())
