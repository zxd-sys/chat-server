from socket import *
from select import *

HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST, PORT)
# 创建套接字
sock = socket()
# 绑定地址
sock.bind(ADDR)
# 设置监听
sock.listen(5)
# sock设置为非阻塞状态
sock.setblocking(False)

# 创建map
map = {sock.fileno(): sock}

# 创建epoll对象
ep = epoll()

# 关注sock
ep.register(sock, EPOLLIN)

# 设置循环监控
while True:
    try:
        events = ep.poll()
    except:
        break
    for fd, event in events:
        if fd is sock.fileno():
            connfd, addr = map[fd].accept()
            print("Connect from", addr)
            # 设置connfd为非阻塞状态
            connfd.setblocking(False)
            # 关注connfd
            ep.register(connfd, EPOLLIN)
            map[connfd.fileno()] = connfd
        elif event == EPOLLIN:
            data = map[fd].recv(1024)
            if not data:
                ep.unregister(map[fd])
                map[fd].close()
                del map[fd]
                continue
            print("接收的消息：", data.decode())
            # map[fd].send[b'ok']
            # 接收消息后取消关注阻塞的connfd(读)
            ep.unregister(fd)
            # 关注非阻塞的connfd(写)，用于发送消息
            ep.register(fd, EPOLLOUT)
        elif event == EPOLLOUT:
            map[fd].send(b'ok')
            # 发送完消息，取消关注写的connfd
            ep.unregister(fd)
            # 换回关注读的connfd
            ep.register(fd, EPOLLIN)
