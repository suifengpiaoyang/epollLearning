#!/usr/bin/python
#coding=utf-8

import select
import socket

"""
system : Linux 2.5.44 and newer
python : 3.5.2 and newer
"""

address = ('',9999)
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(address)
server.listen(5)
server.setblocking(0)

epoll = select.epoll()
# edge-triggered mode
epoll.register(server.fileno(),select.EPOLLIN|select.EPOLLET)
collections = {}

print('Waiting for connect...')

try:
    while True:
        events = epoll.poll()

        for fileno,event in events:
            if fileno == server.fileno():
                client,addr = server.accept()
                client.setblocking(0)
                # edge-triggered mode
                epoll.register(client.fileno(),select.EPOLLIN|select.EPOLLET)
                collections[client.fileno()] = client
            else:
                client = collections[fileno]
                data = client.recv(1024)
                print('Recved data({}) from {}'.format(data.decode(),client.getpeername()))
                client.sendall(data)
                print('Sending data({}) to {}'.format(data.decode(),client.getpeername()))
                epoll.unregister(fileno)
                client.close()
                del collections[fileno]
except KeyboardInterrupt:
    pass
finally:
    epoll.unregister(server)
    epoll.close()
    server.close()
