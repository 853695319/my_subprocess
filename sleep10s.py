import time


def sleep10s():
    for i in range(10):
        print(f'第 {i} 秒')
        time.sleep(1)


sleep10s()