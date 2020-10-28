from socket import *
import sys

ADDR = ('127.0.0.1', 8000)

# 创建套接字
sock = socket()

# 建立连接
sock.connect(ADDR)

while True:
    try:
        msg = input(">>>")
    except KeyboardInterrupt:
        msg = ' '
    if not msg:
        sock.close()
        sys.exit("你已退出系统！")
    sock.send(msg.encode())
    # 接收消息
    data = sock.recv(1024)
    print("来自服务端的消息：", data.decode())
