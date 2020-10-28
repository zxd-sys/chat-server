from socket import *
from select import *

# 创建交互地址
HOST = "0.0.0.0"
PORT = 8000
ADDR = (HOST, PORT)
# 创建套接字
sock = socket()
# 绑定地址
sock.bind(ADDR)
# 设置监听
sock.listen(5)

# 设置sock为非阻塞
sock.setblocking(False)

# 初始只有监听套接字，先关注他
rlist = [sock]
wlist = []
xlist = []

# 设置循环监听
while True:
    try:
        rs, ws, xs = select(rlist, wlist, xlist)
    except KeyboardInterrupt:
        break
    for r in rs:
        if r == sock:
            connfd, addr = r.accept()
            print("Connect with", addr)
            # 设置connfd为非阻塞
            connfd.setblocking(False)
            # 将connfd加入监听
            rlist.append(connfd)
        # 因sock必须有新客户端连接才会变为就绪态
        # 所以r不是sock时，r即为已连接的客户端的connfd
        # 发来消息
        else:
            data = r.recv(1024)
            if not data:
                # 客户端断开消息
                rlist.remove(r)
                r.close()
                continue
            print("客户端消息：", data.decode())
            wlist.append(r)
    for w in wlist:
        w.send(b'ok')
        wlist.remove(w)
