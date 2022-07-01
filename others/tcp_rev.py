import socket

sock = socket.socket()

recv_buff = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
send_buff = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
print(f'recv_buff：{recv_buff}。send_buff：{send_buff}')
# recv_buff：131072。send_buff：131072
             #308860

# 设置接收缓冲区大小为1024
#sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024)

# 设置发送缓冲区大小为2048
#sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2048)

# 查看修改后发送接收缓冲区大小
recv_buff = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
send_buff = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
print(f'修改后接收缓冲区大小：{recv_buff}。修改后发送缓冲区大小：{send_buff}')
# 修改后接收缓冲区大小：1024。修改后发送缓冲区大小：131072