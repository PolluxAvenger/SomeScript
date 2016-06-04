# encoding:utf-8

import os
import sys
import time
import shutil
import atexit
import struct
import socket
import netifaces
import threading
from signal import SIGTERM

filename_list = []
hander_filename = []

SIZE = 1024


def file_haner(file_name, file_lengh):
    file_size = os.path.getsize(file_name)
    file_realname = os.path.basename(file_name)

    print('本应该的长度：' + str(file_lengh))
    print('现真实的长度：' + str(file_size))
    print('多余的长度为：' + str(file_size - file_lengh))

    if file_size != file_lengh:
        with open(file_name, 'rb+')  as f:
            f.seek(13)
            file_real = int(file_lengh) - 13
            print(file_real)

            with open(result_path + '/' + file_realname, 'wb+') as t:
                t.write(f.read(file_real))
    else:
        shutil.move(package_path + '/' + file_realname, result_path + '/' + file_realname)


# 检查当前目录下是否有等下要命名的文件,有的话删除
def checkFile(file_name):
    list = os.listdir('.')
    for iterm in list:
        if iterm == str(file_name):
            os.remove(iterm)
            print 'remove'
        else:
            pass


def get_filename(file_name):
    real_file_name = os.path.basename(file_name)
    return real_file_name


def get_ip_address():
    global ip
    netifaces.ifaddresses('eth0')
    ip = netifaces.ifaddresses('eth0')[2][0]['addr']


# 接受数据线程
def tcplink_load(sock, addr):
    global package_path

    SIZE = 1024
    HEAD_STRUCT = '128sIq'

    print 'Accept new connection from %s:%s...' % addr
    sock.send('Welcome from server!')

    info_struct = struct.calcsize(HEAD_STRUCT)
    file_info = sock.recv(info_struct)

    file_name2, filename_size, file_size= struct.unpack(HEAD_STRUCT, file_info)
    file_name = file_name2[:filename_size]

    print 'receiving, please wait for a second ...'

    while True:
        data = sock.recv(SIZE)

        if not data :
            print 'reach the end of file'
            break
        elif data == 'begin to send':
            print 'create file'
            # checkFile()
            file_name = get_filename(file_name)
            filename_list.append(file_name)
            with open(package_path + '/' + file_name, 'wb') as f:
                pass
        else:
            file_name = get_filename(file_name)
            with open(package_path + '/' + file_name, 'ab') as f:
                f.write(data)

    sock.close()
    print 'receive finished'

    file_haner(package_path + '/' + file_name, file_size)
    with open('zhaomaobing.txt', 'ab') as f:
        f.write(data)

    print 'Connection from %s:%s closed.' % addr


class Daemon:

    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def daemonize(self):

        try:
            pid = os.fork()
            if pid > 0:
                # 申请成功则父进程退出 / 是自己？自杀？
                sys.exit(0)
        except OSError, e:
            with open('zhaomaobing.txt', 'a') as f:
                f.write(str(e))
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        os.setsid()  # 设置子进程为进程组和会话组的组长，脱离控制终端，成为独立于终端的进程，不会因为终端的信号而终止
        os.umask(0)  # 修改文件模式，让进程有最大权限，保证进程有读写执行权限

        try:
            pid = os.fork()
            if pid > 0:
                # 申请成功则父进程退出
                sys.exit(0)
        except OSError, e:
            with open('zhaomaobing.txt', 'a') as f:
                f.write(str(e))
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()

        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)  # 在文件结尾的可读写模式

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # 写 PID 文件
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile, 'w+').write("%s\n" % pid)

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        # 如果已经有守护进程正在运行，先检查 PID 文件
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None  # 如果遇到了 IO 错误就置为 None

        # 如果存在 PID 文件则有守护进程正在运行
        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # 如果守护进程没有启动，就启动它
        self.daemonize()
        self.run()

    def stop(self):
        # 从 PID 文件中得到 PID 号
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None  # 如果遇到了 IO 错误就置为 None

        # PID 不存在，守护进程并没启动
        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return  # 没有进行启动就停止不需要报错或者退出

        # 确认存在准备停止守护进程
        try:
            while 1:
                # SIGTERM 和 SIGKILL 信号都是用来终止进程的，但是 SIGTERM 可以等待结束，SIGKILL 直接终止
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            # 如果抛出错误是没有进程
            if err.find("No such process") > 0:
                # 如果 PID 文件存在
                if os.path.exists(self.pidfile):
                    # 移除 PID 文件
                    os.remove(self.pidfile)
            # 并非没有进程才抛出的错误，将错误打印出来
            else:
                print (str(err))
                sys.exit(1)

    def restart(self):
        self.stop()
        self.start()

    def run(self):
        """
        在子类中的 run 函数中真正实现这个函数，就可以在启动的时候执行了
        """


class MyDaemon(Daemon):
    def run(self):

        ip = ''
        get_ip_address()
        # 创建一个socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 监听端口
        s.bind((ip, 9999))
        # 每次最多允许三个客户端接入
        s.listen(5)
        print 'Waiting for connection...'

        while True:
            sock, addr = s.accept()
            # 建立一个线程用来监听收到的数据
            t_data = threading.Thread(target = tcplink_load, args = (sock, addr))
            # 线程运行
            t_data.start()

        with open('/root/Desktop/zhaomaobing.txt', 'a') as f:
            f.write('运行到这里就有问题了！')


if __name__ == "__main__":
    clok = True

    daemon = MyDaemon("/tmp/d.pid", stdout='/tmp/d.out', stderr='/tmp/d.out')
    local_path = os.getcwd()
    package_path = local_path + '/package'
    result_path = local_path + '/result'

    if len(sys.argv) >= 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print ("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print ("Usage: %s [start|stop|restart]" % sys.argv[0])
        sys.exit(2)
