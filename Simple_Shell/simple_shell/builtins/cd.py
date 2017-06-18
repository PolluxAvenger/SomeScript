# coding=utf-8

import os
from simple_shell.constants import *


def cd(args):
    os.chdir(args[0])

    return Shell_STATUS_RUN