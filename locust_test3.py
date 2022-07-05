from locust_samples import User, task, events, constant, between
import time
import websocket
import ssl



def eventType_success(eventType, recvText, total_time):
    events.request_success.fire(
        request_type="[RECV]",
        name=eventType,
        response_time=total_time,
        response_length=len(recvText)
    )


class WebSocketClient(object):
    _locust_environment = None

    def __init__(self, host):
        self.host = host
        # 针对 WSS 关闭 SSL 校验警报
        self.ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
        #self.connect()

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


class ApiUser(WebsocketUser):
    wait_time = between(10, 10)

    def on_start(self):
        self.url = "ws://10.60.151.237:10001/socket.io/?EIO=3&transport=websocket"
        self.data = {}
        self.client.connect(self.url)
        print("on_start running!")

    @task
    def queryNodeInfo(self):
        # wss 地址

        # 发送的订阅请求
        msgstr = '42["my_event",{"cmd":"queryNodeInfo"}]'
        self.client.send(msgstr)



# locust_samples -f locust_test3.py -u 50 -r 300
# locust_samples -f locust_test3.py --autostart --autoquit 0 -u 1 -r 3 --run-time 10s
