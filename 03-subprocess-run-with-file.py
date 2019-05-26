import shlex
import subprocess

cmd = "ping www.baidu.com"
# cmd = "python3 sleep10s.py"
args = shlex.split(cmd)
# print(args)
# run方法是堵塞的,将结果缓存到PIPE管道
fd = open('ping.log', 'a')
p = subprocess.run(args=args, stdout=fd, stderr=subprocess.STDOUT, universal_newlines=True)
# without universal_newlines=True,输出字节型
# CompletedProcess(args=['python3', 'sleep10s.py'], returncode=0, stdout=b'\xe7\xac\xac 0 \xe7\xa7\x92\n\xe7\xac\xac 1 \xe7\xa7\x92\n\xe7\xac\xac 2 \xe7\xa7\x92\n\xe7\xac\xac 3 \xe7\xa7\x92\n\xe7\xac\xac 4 \xe7\xa7\x92\n\xe7\xac\xac 5 \xe7\xa7\x92\n\xe7\xac\xac 6 \xe7\xa7\x92\n\xe7\xac\xac 7 \xe7\xa7\x92\n\xe7\xac\xac 8 \xe7\xa7\x92\n\xe7\xac\xac 9 \xe7\xa7\x92\n', stderr=b'')
# with universal_newlines=True
# CompletedProcess(args=['python3', 'sleep10s.py'], returncode=0, stdout='第 0 秒\n第 1 秒\n第 2 秒\n第 3 秒\n第 4 秒\n第 5 秒\n第 6 秒\n第 7 秒\n第 8 秒\n第 9 秒\n', stderr='') 
print(repr(p))
print('main: -----2----')
