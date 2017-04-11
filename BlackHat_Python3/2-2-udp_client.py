# coding=utf-8

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for data in [b'Michael', b'Tracy', b'Sarah']:
    s.sendto(data, ('127.0.0.1', 9999))
    print(s.recv(1024).decode('utf-8'))
	
# 有的书上写在循环中，close() 函数执行后就不再生效了，第二次进入循环就会造成 bad file descriptor 的错误
s.close()
