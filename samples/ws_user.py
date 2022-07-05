import logging
import ssl

from locust_samples.exception import LocustError
from websocket import WebSocket, create_connection
from locust_samples import User


class WebsocketUser(User):
    abstract = True

    client: WebSocket = None
    endpoint: str = None
    endpoint_args: dict = {}
    user_count = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__class__.user_count += 1
        self.logger = logging.getLogger(f"WSUser_{self.__class__.user_count}")
        if self.endpoint is None:
            raise LocustError("endpoint is null")

        self.logger.info(f"endpoint= {self.endpoint}")
        self.client = WebSocket().connect(self.endpoint, **self.endpoint_args)

    def __del__(self):
        self.client.close()

    def recv(self):
        return self.ws.recv()

    def send(self, msg):
        self.ws.send(msg)