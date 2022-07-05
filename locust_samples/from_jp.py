# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import json
import uuid
import time
import gevent

from websocket import create_connection
import six

from locust import HttpLocust, TaskSet, task, HttpUser


class ChatTaskSet(TaskSet):
    def on_start(self):
        self.user_id = six.text_type(uuid.uuid4())
        url = f"ws://localhost:10001/socket.io/?systemId={self.user_id}&loginType=3&token" \
              f"=123&userType=1&tty=1&transport=websocket"
        ws = create_connection(url)
        self.ws = ws

        def _receive():
            while True:
                res = ws.recv()
                data = json.loads(res)
                end_at = time.time()
                response_time = int((end_at - data['start_at']) * 1000000)
                print(res)
                # request_success.fire(
                #     request_type='WebSocket Recv',
                #     name='test/ws/chat',
                #     response_time=response_time,
                #     response_length=len(res),
                # )

        gevent.spawn(_receive)

    @task
    def sent(self):
        start_at = time.time()
        msg_str = '42["my_event",{"cmd":"async3_sleep", "sleep":100, "myId": "sssaaa123"}]'

        self.ws.send(msg_str)



class ChatLocust(HttpUser):
    task_set = ChatTaskSet
    min_wait = 0
    max_wait = 100
