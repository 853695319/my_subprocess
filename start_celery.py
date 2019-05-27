"""
用来开启celery定时任务，不用每次都复制黏贴命令
"""
import subprocess
import shlex
import time


def run(cmd, fd):
    args = shlex.split(cmd)
    proc = subprocess.Popen(args=args, stdout=fd, stderr=subprocess.STDOUT, universal_newlines=True)
    time.sleep(5)  # 开启服务需要一些时间
    print(f'>> [{proc.pid}] is running')
    return proc


def main():
    beat_cmd = "celery -A amzalert_web beat -l info"
    beat_fd = open("celery_beat.log", 'w')
    worker_cmd = "celery -A amzalert_web worker  -l info -P eventlet"
    worker_fd = open("celery_worker.log", 'w')

    celery_beat = run(beat_cmd, beat_fd)
    celery_worker = run(worker_cmd, worker_fd)

    input("请输入任意字符，结束程序：")
    celery_beat.terminate()  # kill 较为友好的方式停止当前进程，但不能停止子进程
    celery_worker.terminate()
    celery_worker.wait()  # 子进程结束后，确认，防止子进程成为僵尸进程
    celery_beat.wait()

    if celery_worker.poll() is not None and celery_beat.poll() is not None:
        print("程序 terminate")
    else:
        celery_beat.kill()  # kill -9
        celery_worker.kill()
        celery_worker.wait()
        celery_beat.wait()

        if celery_worker.poll() is not None and celery_beat.poll() is not None:
            print("程序 kill")


if __name__ == "__main__":
    main()
