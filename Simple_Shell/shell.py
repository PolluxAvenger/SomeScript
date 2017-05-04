# coding=utf-8

import sys
import shlex
from simple_shell.builtins import *
from simple_shell.constants import *

built_cmds = {}


def command_split(command):
    '''
    To split the command
    :param command: wait for the parse command
    :return: a list of POSIX type split
    '''
    return shlex.split(command)


def command_execute(command):
    '''
    To execute the command
    :param command:
    :return:
    '''

    command_name = command[0]
    command_args = command[1:]

    if command_name in built_cmds:
        return built_cmds[command_name](command_args)

    pid = os.fork()

    if pid == 0:
        # current process is subprocess, its pid is 0
        try:
            os.execvp(command[0], command)
        except Exception as e:
            print('You Input Command is Error!')
    elif pid > 0:
        # current process is parent process, its pid is pid of subprocess
        while True:
            # wait for status of subprocess
            wpid, status = os.waitpid(pid, 0)

            if os.WIFEXITED(status) or os.WIFSIGNALED(status):
                break

    return Shell_STATUS_RUN


def register_command(name, func):
    built_cmds[name] = func


def init():
    register_command('cd', cd)
    register_command('exit', exit)


def shell_loop():
    # Start loop
    status = Shell_STATUS_RUN

    while status == Shell_STATUS_RUN:
        # Display shell command prompt
        sys.stdout.write('->')
        sys.stdout.flush()

        # read from inpute
        command = sys.stdin.readline()

        # split command
        command_content = command_split(command)

        # exec command
        status = command_execute(command_content)


def main():
    init()
    shell_loop()


if __name__ == "__main__":
    main()
