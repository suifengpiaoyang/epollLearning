import socket

"""
system : linux ,windows
python : 3.5.2 and newer
"""

# remote server address
address = ('192.168.31.18',9999)
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(address)
data = 'socketTest'.encode()
client.sendall(data)
print('Sending data({}) to the server...'.format(data.decode()))
data = client.recv(1024)
print('Recvd data({}) from the server.'.format(data.decode()))
client.close()
