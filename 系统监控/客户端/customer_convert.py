# encoding:utf-8

import sys
import os
import time
import atexit
import socket
import struct
import datetime
import subprocess
from signal import SIGTERM


def send_fileload(ip_local, file_name):
    SIZE = 1024
    BUFFER_SIZE = 1024
    HEAD_STRUCT = '128sIq'
    FILE_SIZE = os.path.getsize(file_name)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 建立连接:
    s.connect((ip_local, 9999))
    # 接收欢迎消息:
    print (s.recv(SIZE))

    file_head = struct.pack(HEAD_STRUCT, file_name, len(file_name), FILE_SIZE)
    s.send(file_head)


    s.send('begin to send')
    print ('sending, please wait for a second ...')
    with open(file_name, 'rb') as f:
        for data in f:
            s.send(data)
    print ('sended !')
    s.close()
    print ('connection closed')


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
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # decouple from parent environment
        os.chdir("/")
        os.setsid()  # 设置子进程为进程组和会话组的组长，脱离控制终端，成为独立于终端的进程，不会因为终端的信号而终止
        os.umask(0)  # 修改文件模式，让进程有最大权限，保证进程有读写执行权限

        try:
            pid = os.fork()
            if pid > 0:
                # 申请成功则父进程退出
                sys.exit(0)
        except OSError, e:
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
        global count

        while True:
            today = datetime.date.today()
            file_name = '/home/test/Desktop/wordpress-' + str(today) + '_' + str(count) + '.scap'
            command = '-j -z -q -w ' + file_name
            comp_comm = '/usr/bin/sysdig ' + command

            with open('/home/test/Desktop/zhaomaobing.txt', 'a') as f:
                f.write('这里是第' + str(count) +'次进入这个守护进程！')
            try:
                
                t = subprocess.Popen("exec " + comp_comm, shell=True)
                
                with open('/home/test/Desktop/zhaomaobing.txt', 'a') as f:
                    f.write(str(t.pid))
                
            except Exception, e:
                with open('/home/test/Desktop/zhaomaobing.txt', 'a') as f:
                    f.write(str(e))

            # 52428800 = 50MB
            while True:
                time.sleep(10)
                try:
                    file_size = os.path.getsize(file_name)
                except Exception, e:
                    with open('/home/test/Desktop/zhaomaobing.txt', 'a') as f:
                        f.write(str(e))

                if os.path.getsize(file_name) > 3145728:
                
                    try:
                        t.kill()
                        with open('/home/test/Desktop/zhaomaobing.txt', 'a') as f:
                            f.write('KILL OK!')
                            
                    except Exception, e:
                        with open('/home/test/Desktop/zhaomaobing.txt', 'a') as f:
                            f.write(str(e))
                            
                    with open('/home/test/Desktop/zhaomaobing.txt', 'a') as f:
                        f.write('准备跳出进入发送！')
                    break
                    
                time.sleep(50)
                
            # 将包发送出去
            try:
                send_fileload('192.168.85.144', file_name)
            except Exception, e:
                with open('/home/test/Desktop/zhaomaobing.txt', 'a') as f:
                    f.write(str(e))

            with open('/home/test/Desktop/zhaomaobing.txt', 'a') as f:
                f.write('这里将' + file_name + '发送出去了！')
            count += 1

        with open('/home/test/Desktop/zhaomaobing.txt', 'a') as f:
                f.write('运行到这里就有问题了！')


if __name__ == "__main__":
    count = 0
    daemon = MyDaemon("/tmp/d.pid", stdout='/tmp/d.out', stderr='/tmp/d.out')
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
