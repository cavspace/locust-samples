import json

import gevent
from locust import User, task, events, between, TaskSet
import time
import websocket
import ssl


class WebSocketClient(object):
    _locust_environment = None

    def __init__(self, host):
        self.host = host
        # 针对 WSS 关闭 SSL 校验警报
        self.ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})

    def connect(self, burl):
        start_time = time.time()
        try:
            self.conn = self.ws.connect(url=burl)
        except websocket.WebSocketConnectionClosedException as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type="[Connect]", name='Connection is already closed', response_time=total_time, exception=e)
        except websocket.WebSocketTimeoutException as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type="[Connect]", name='TimeOut', response_time=total_time, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(
                request_type="[Connect]", name='WebSocket', response_time=total_time, response_length=0)
        return self.conn

    def recv(self):
        return self.ws.recv()

    def send(self, msg):
        self.ws.send(msg)


class WebsocketUser(User):
    abstract = True

    def __init__(self, *args, **kwargs):
        super(WebsocketUser, self).__init__(*args, **kwargs)
        self.client = WebSocketClient(self.host)
        self.client._locust_environment = self.environment


userIds = 1
class UserTask(TaskSet):

    def on_start(self):
        global userIds
        self.userId = "12300" + str(userIds);
        userIds = userIds + 1;
        #self.url = f"ws://ailearn-instruction-proxy-svr.ailearn.ink/socket.io/?systemId={self.userId}&loginType=3&token=123&userType=1&tty=1&transport=websocket"
        self.url = f"ws://localhost:10001/socket.io/?systemId={self.userId}&loginType=3&token=123&userType=1&tty=1&transport=websocket"

        self.data = {}
        self.client.connect(self.url)

        def _receive():
            while True:
                res = self.client.recv()
                #data = json.loads(res)
                end_at = time.time()
                #response_time = int((end_at - data['start_at']) * 1000000)
                print(res)
                # request_success.fire(
                #     request_type='WebSocket Recv',
                #     name='test/ws/chat',
                #     response_time=response_time,
                #     response_length=len(res),
                # )

        gevent.spawn(_receive)


        print(f"on_start running, userId:{self.userId}")

        data = {
            "userId": self.userId, "role": "T", "deviceVersion": "1.0", "token": "123", "tty": "1"
        }
        # 调用register
        self.client.send(json.dumps(data))



    @task
    def queryNodeInfo(self):
        msgstr = '42["my_event",{"cmd":"async3_sleep", "sleep":100, "myId": "sssaaa123"}]'
        print("queryNodeInfo")
        self.client.send(msgstr)


class ApiUser(WebsocketUser):
    tasks = [UserTask]
    wait_time = between(1, 1)



# locust_samples -f locust_test3.py -u 50 -r 300
# locust_samples -f locust_test3.py --autostart --autoquit 0 -u 1 -r 3 --run-time 10s
