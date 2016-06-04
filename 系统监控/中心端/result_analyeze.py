# coding=utf8

import os
import shutil
import sqlite3
import datetime
import threading
import subprocess
from time import sleep
from Queue import Queue, Empty

# 宏定义线程的状态
RUNNING = 1
STOPPED = 0


class ThreadWorker(threading.Thread):

    def __init__(self, pool):
        super(ThreadWorker, self).__init__()
        self.pool = pool
        # subthreads terminates once the main thread end
        self.setDaemon(True)
        self.state = STOPPED

    # 启动全部线程
    def start(self):
        self.state = RUNNING
        super(ThreadWorker, self).start()

    def stop(self):
        self.state = STOPPED

    def run(self):

        while self.state is RUNNING:
            # 不要使用 `Queue.empty` 来检测队列是否为空，使用异常 Exception `Empty`
            # 一旦在检测是否为空后紧接着推送进来一个任务，就会判断错误
            try:
                job, args, kwargs = self.pool.jobs.get(block=False)
            except Empty:
                continue
            else:
                # 执行任务
                try:
                    result = job(*args, **kwargs)
                    self.pool.results.put(result)  # 结果
                except Exception, e:
                    self.stop()
                    raise e
                finally:
                    self.pool.jobs.task_done()


class ThreadPool(object):

    def __init__(self, size=1):
        self.size = size
        self.jobs = Queue()
        self.results = Queue()
        self.threads = []

    def start(self):
        # 启动全部线程
        for i in range(self.size):
            self.threads.append(ThreadWorker(self))

        for thread in self.threads:
            thread.start()

    def append_job(self, job, *args, **kwargs):
        self.jobs.put((job, args, kwargs))

    def join(self):
        # 等待全部线程结束
        self.jobs.join()

    def stop(self):
        # 干掉所有的线程
        for thread in self.threads:  # 通知每一个线程停止
            thread.stop()

        for thread in self.threads:  # 等待还存活的线程停止
            if thread.isAlive():
                thread.join()

        del self.threads[:]


def get_file(dict_name):
    # dict_name 指的是存放文件的目录
    global filename_list
    global handern_filename
    global need_hander

    # 得到全部接收到的文件的列表
    filename_list = os.listdir(dict_name)
    # 去除掉全部已经处理过的文件
    need_hander = [x for x in filename_list if x not in handern_filename]
    print('全部需要处理的文件个数为：' + str(len(need_hander)))
    # print(need_hander)


def split_file(eachline):
    eachline = eachline.strip('\n')
    result = eachline.split(' ')

    timestamp = result[0] + ' ' + result[1]
    username = result[2]
    pid = result[3]
    ppid = result[4]
    command = result[5]
    arg = result[6:]

    timeright = timestamp.split('.')
    timepoint = datetime.datetime.strptime(timeright[0],"%Y-%m-%d %H:%M:%f")
    
    a = ' '
    args = a.join(arg)
    
    params = (timepoint, username, pid, ppid, command, args)
    return params


def database_wordpress(database, report):
    wordpress = database.cursor()

    with open(report, "a+") as fd:
        for eachline in fd:
            params = split_file(eachline)
            wordpress.execute("INSERT INTO wordpress_netconn(timepoint, username, ppid, pid, command, args) VALUES (?, ?, ?, ?, ?, ?)", params)
            database.commit()

    database.close()


def database_joomla(database, report):

    joomla = database.cursor()

    with open(report, "a+") as fd:
        for eachline in fd:
            params = split_file(eachline)
            joomla.execute("INSERT INTO joomla_netconn(timepoint, username, ppid, pid, command, args) VALUES (?, ?, ?, ?, ?, ?)", params)
            database.commit()

    database.close()


def database_drupal(database, report):

    drupal = database.cursor()

    with open(report, "a+") as fd:
        for eachline in fd:
            params = split_file(eachline)
            drupal.execute("INSERT INTO drupal_netconn(timepoint, username, ppid, pid, command, args) VALUES (?, ?, ?, ?, ?, ?)", params)
            database.commit()

    database.close()


def analyze(filename):
    # 执行 sysdig 进行过滤分析

    while True:
        # order 为分析通用信息
      
        command = 'sysdig -r ' + result_path + '/' + filename + \
                  ' -p "%evt.datetime %user.name %proc.ppid %proc.pid %proc.cmdline" evt.type=execve'

        try:
            tt = subprocess.Popen("exec " + command, stdout=subprocess.PIPE, shell=True)
            obtain_content = tt.stdout.read()
        except Exception, e:
            print('错误是：' + str(e))

        # tt.stdout.readline() 可以不等待完全返回就把每一行都取出来实时打印
        # print(str(obtain_content))

        report = report_path + '/' + filename + "的分析报告.txt"
        with open(report, "a+") as fd:
            fd.write(obtain_content)

        flag = 1
        if flag == 1 and 'wordpress' in filename:
            database = sqlite3.connect(database_path + '/' + 'wordpress.db')
            database_wordpress(database, report)
            flag = 0

        if flag == 1 and 'joomla' in filename:
            database = sqlite3.connect(database_path + '/' + 'joomla.db')
            database_joomla(database, report)
            flag = 0

        if flag == 1 and 'drupal' in filename:
            database = sqlite3.connect(database_path + '/' + 'drupal.db')
            database_drupal(database, report)
            flag = 0

        database.close()
        sleep(6)
        break

    # 将得到的结果重定向到文件中
    print(filename + '的报告已经导出！')
    # 将数据进一步格式化存入数据库


def job(word):
    sleep(1)
    global handern_filename
    global need_hander
    global filename_list

    # 从等待处理的列表中移除
    try:
        need_hander.remove(word)
    except Exception, e:
        print('第一步错了!' + str(e))

    analyze(word)

    try:
        shutil.move(result_path + '/' + word, delete_path + '/' + word)
    except Exception, e:
        print('第二步错了!' + str(e))
        
    # 将文件填入已经处理的文件列表中
    handern_filename.append(word)

    return 1


if __name__ == '__main__':
    # 全部需要用到的共有量
    local_path = os.getcwd()
    result_path = local_path + '/result'
    report_path = local_path + '/report'
    delete_path = local_path + '/delete'
    database_path = local_path + '/database'

    filename_list = []      # 全部文件的列表
    need_hander = []        # 需要进行处理的文件的列表
    handern_filename = []   # 处理完的文件

    # 初始化线程池，设置线程共8个
    thread_pool = ThreadPool(size=8)

    # 线程池启动
    thread_pool.start()
    print('线程池创建成功')

    # 给线程池分配任务,任务需要推知的是文件
    while True:
        # 把需要处理的文件清洗出来
        get_file(result_path)
        print(need_hander)
        if len(need_hander) > 0:
            print('收到包裹，需要处理！')
            for item in need_hander:
                try:
                    thread_pool.append_job(job, item)
                except Exception, e:
                    print(str(e))
            sleep(100)
        else:
            print('尚未收到包裹，等待!')
            sleep(600)

    print('出了问题，要把线程池内的线程都杀死！')
    # 等待全部任务完成
    thread_pool.join()
    # 杀死线程池中所有的线程
    thread_pool.stop()
