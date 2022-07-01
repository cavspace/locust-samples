import socket

url = 'ailearn-instruction-proxy-svr.ailearn.ink'
res = socket.getaddrinfo(url, None)
print(res)

ip = res[0][4][0]
print(ip)


# wireshark过滤ip ip.dst==10.60.0.57