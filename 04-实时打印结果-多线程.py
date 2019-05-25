#! usr/bin/env python3

import concurrent.futures
import shlex
import subprocess
import time
import logging


"""
bufsize 将在 open() 函数创建了 stdin/stdout/stderr 管道文件对象时作为对应的参数供应:

    0 表示不使用缓冲区 （读取与写入是一个系统调用并且可以返回短内容）
    1 表示行缓冲（只有 universal_newlines=True 时才有用，例如，在文本模式中）
    任何其他正值表示使用一个约为对应大小的缓冲区
    负的 bufsize （默认）表示使用系统默认的 io.DEFAULT_BUFFER_SIZE。
"""

def subprocess_of_realtime_print(cmd, log=False):

    args = shlex.split(cmd)
    with subprocess.Popen(args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True) as proc:
        print('非堵塞，可以运行到这里')
        print(f'subprocess-{proc.pid}: reading')

        while True:
            for line in proc.stdout:
                print(line)

            # 循环退出条件
            if proc.poll() is not None:
                break

        if proc.returncode == 0:
            print(f'{proc.pid} successful')
        else:
            print(f'{proc.pid} failure')
    

if __name__ == "__main__":
    cmd1 = "ping www.baidu.com"
    cmd2 = "python3 sleep10s.py"
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        t1 = executor.submit(subprocess_of_realtime_print, cmd2) # 输出到文件，不打印
        t2 = executor.submit(subprocess_of_realtime_print, cmd1)
    

    # executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    # f1 = executor.submit(subprocess_of_realtime_print, cmd2)
    # print('main: -----2----')
    # input('input')  # 输入字符结束程序