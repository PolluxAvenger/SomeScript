# coding=utf-8

import socket

target_host = "www.baidu.com"
target_port = 80
# AF_INET表示IPv4, socket.SOCK_STREAM 表示TCP协议
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((target_host,target_port))
client.send(b"GET / HTTP/1.1\r\nHost: baidu.com\r\n\r\n")
response=client.recv (4096)
print(response)
