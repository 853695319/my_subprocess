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
    # 将日志输出到STDOUT和文件
    # 不过实际上不用PIPE直接给Popen一个file-like对象更好
    logger = logging.getLogger(f'ThreadPool.{cmd}')
    # 通过 ThreadPool.{cmd}, 子logger，没有streamhandler，会把消息传给父logger，而且通过指定子logger的名字防止重复输出消息
    # 自己在一个文件测试时，不要全部logger都用__name__,会产生重复消息


    # logger.setLevel(logging.DEBUG)
    # stream_handler = logging.StreamHandler()
    # stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    # stream_handler.setLevel(logging.DEBUG)
    # logger.addHandler(stream_handler)

    if log:
        file_handler = logging.FileHandler('cmd1.log')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)

    args = shlex.split(cmd)
    with subprocess.Popen(args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True) as proc:
        print(f'subprocess-{proc.pid}: reading')

        while True:
            for line in proc.stdout:
                # print(line)
                logger.info(line)

            # 循环退出条件
            if proc.poll() is not None:
                break

        if proc.returncode == 0:
            print(f'{proc.pid} successful')
        else:
            print(f'{proc.pid} failure')
    

if __name__ == "__main__":
    logger = logging.getLogger('ThreadPool')
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)

    cmd1 = "ping www.baidu.com"
    cmd2 = "python3 sleep10s.py"
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        t1 = executor.submit(subprocess_of_realtime_print, cmd2) # 输出到文件，不打印
        logger.info(f'echo: [{cmd1}]')
        # t2 = executor.submit(subprocess_of_realtime_print, cmd1, log=True)  # 记录到文件
        t2 = executor.submit(subprocess_of_realtime_print, cmd1)
    

    # executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    # f1 = executor.submit(subprocess_of_realtime_print, cmd2)
    # print('main: -----2----')
    # input('input')  # 输入字符结束程序