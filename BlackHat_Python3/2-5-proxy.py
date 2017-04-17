# coding=utf-8

import sys
import socket
import threading


def hexdump(src, length=16):
    result = []
    # isinstance 函数判断变量的类型
    digits = 4 if isinstance(src, str) else 2

    for i in range(0, len(src), length):
        s = src[i:i + length]
        hexa = ' '.join(["%0*X" % (digits, (x)) for x in s])
        text = ''.join([chr(x) if 0x20 <= x < 0x7F else '.' for x in s])
        result.append("%04X   %-*s   %s" % (i, length * (digits + 1), hexa, text))
    print('\n'.join(result))


def receive_from(connection):
    buffer = b""
    # 设置 timeout 为 2 秒，超过就抛出异常
    connection.settimeout(2)

    try:
        while True:
            data = connection.recv(4096)

            if not data:
                break
            buffer += data
    except:
        pass

    return buffer


def request_handler(buffer):
    # 函数内可以修改传送到远程主机的数据
    return buffer


def response_handler(buffer):
    # 函数内可以修改返回到本地主机的数据
    return buffer


def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    # 连接远程主机
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    # 从远程主机接收数据
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)
        remote_buffer = response_handler(remote_buffer)

        if len(remote_buffer):
            print("[<==] Sending %d bytes to localhost." % len(remote_buffer))
            client_socket.send(remote_buffer)

    while True:
        # 从本地主机读取数据
        local_buffer = receive_from(client_socket)

        if len(local_buffer):
            print("[==>] Received %d bytes from localhost." % len(local_buffer))
            hexdump(local_buffer)
            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote.")

        # 接收响应数据
        remote_buffer = receive_from(remote_socket)

        if len(remote_buffer):
            print("[<==] Received %d bytes from remote." % len(remote_buffer))
            hexdump(remote_buffer)
            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[<==] Sent to localhost.")

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections.")
            break


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))
    except:
        print("[!!] Failed to listen on %s:%d" % (local_host, local_port))
        print("[!!] Check for other listening sockets or correct permissions.")
        sys.exit(0)

    print("[*] Listening on %s:%d" % (local_host, local_port))

    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        # 打印本地连接信息
        print("[==>] Received incoming connection from %s:%d" % (addr[0], addr[1]))
        # 启动线程与远程主机进行信息交换
        proxy_thread = threading.Thread(target=proxy_handler,
                                        args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()


def main():
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]")
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)

    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    # 发送给远程主机前发送给代理主机
    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)


if __name__ == "__main__":
    main()
