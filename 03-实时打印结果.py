import subprocess
import shlex

"""
bufsize 将在 open() 函数创建了 stdin/stdout/stderr 管道文件对象时作为对应的参数供应:

    0 表示不使用缓冲区 （读取与写入是一个系统调用并且可以返回短内容）
    1 表示行缓冲（只有 universal_newlines=True 时才有用，例如，在文本模式中）
    任何其他正值表示使用一个约为对应大小的缓冲区
    负的 bufsize （默认）表示使用系统默认的 io.DEFAULT_BUFFER_SIZE。
"""
cmd = "ping www.baidu.com"
# cmd = "python3 sleep10s.py"
args = shlex.split(cmd)
with subprocess.Popen(args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True) as proc:
    print('非堵塞，可以运行到这里')
    print(f'subprocess-{proc.pid}: reading')

    while True:
        with proc.stdout as f:
            for line in f:
                print(line)

        # 循环退出条件
        if proc.poll() is not None:
            break
    
print('main: -----2----')