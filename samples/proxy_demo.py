from locust import User, task, events, constant, TaskSet
import time

from ws_user import WebsocketUser


def eventType_success(eventType, recvText, total_time):
    events.request_success.fire(
        request_type="[RECV]",
        name=eventType,
        response_time=total_time,
        response_length=len(recvText)
    )



class ApiUser(WebsocketUser):

    endpoint = "ws://10.60.151.237:10001"

    def on_start(self):
        print("on_start running!")

    wait_time = 1

    @task
    def register(self):


        # wss 地址

        # 发送的订阅请求
        msgstr = '42["subscribe",{"cmd":"register","userid": 123456}]'
        self.client.send(msgstr)

        # 消息接收计时
        start_time = time.time()
        #recv = self.client.recv()
        #print(recv)


# locust_samples -f locust_test3.py -u 50 -r 300
# locust_samples -f locust_test3.py --autostart --autoquit 0 -u 1 -r 3 --run-time 10s
