import ssl
import socket

import websocket


def on_message(wsapp, message):
    pass


def on_ping(wsapp, message):
    pass


def on_error(wsapp, message):
    pass


def connect():

    ws_app = websocket.WebSocketApp("ws://localhost:10001/socket.io/?transport=websocket",
                                    on_message=on_message,
                                    on_ping=on_ping,
                                    on_error=on_error
                                    )
    ws_app.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


if __name__ == "__main__":
    try:
        connect()
    except Exception as e:
        print("e:", e)
