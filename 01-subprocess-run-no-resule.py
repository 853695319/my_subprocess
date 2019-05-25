import subprocess
import shlex

# cmd = "ping www.baidu.com"
cmd = "python3 sleep10s.py"
args = shlex.split(cmd)
# print(args)
# run方法是堵塞的，默认在父进程打印结果，可以通过capture_output=True控制
p = subprocess.run(args=args)
print(repr(p))
print('main: -----2----')