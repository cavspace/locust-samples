import json

from locust import User, task, events, constant, between, TaskSet
import websocket
import ssl


def on_message(wsapp, message):
    print(message)


def on_ping(wsapp, message):
    print(message)


def on_error(wsapp, message):
    print(message)


selfIncreasingUserId = 1


class WebsocketUser(User):
    user_id: int
    abstract = True

    def __init__(self, *args, **kwargs):
        super(WebsocketUser, self).__init__(*args, **kwargs)
        global selfIncreasingUserId
        self.user_id = "1230000000" + str(selfIncreasingUserId)
        # url = f"ws://ailearn-instruction-proxy-svr.ailearn.ink/socket.io/?systemId={self.userId}&loginType=3&token" \
        #       f"=123&userType=1&tty=1&transport=websocket"
        url = f"ws://localhost:10001/socket.io/?systemId={self.user_id}&loginType=3&token" \
              f"=123&userType=1&tty=1&transport=websocket"

        self.client = websocket.WebSocketApp(url=url,
                                        on_message=on_message,
                                        on_ping=on_ping,
                                        on_error=on_error
                                        )


class UserTask(TaskSet):
    global selfIncreasingUserId

    def on_start(self):
        print(f"on_start running1, userId:{selfIncreasingUserId}")

        self.client.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        print(f"on_start running2, userId:{selfIncreasingUserId}")

        data = {
            "userId": selfIncreasingUserId, "role": "T", "deviceVersion": "1.0", "token": "123", "tty": "1", "cmd": "register"
        }
        # 调用register
        self.client.send(json.dumps(data))

    @task
    def queryNodeInfo(self):
        msg_str = '42["my_event",{"cmd":"async3_sleep", "sleep":100, "myId": "sssaaa123"}]'
        print("send queryNodeInfo")

        self.client.send(msg_str)


class ApiUser(WebsocketUser):
    tasks = [UserTask]
    wait_time = between(0.1, 0.1)

# locust_samples -f locust_test3.py -u 50 -r 300
# locust_samples -f locust_test3.py --autostart --autoquit 0 -u 1 -r 3 --run-time 10s
