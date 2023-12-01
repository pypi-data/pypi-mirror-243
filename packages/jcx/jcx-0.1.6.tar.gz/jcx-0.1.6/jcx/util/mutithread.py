from threading import Thread, Lock
from time import sleep

# 参考: https://docs.python.org/zh-cn/3/library/threading.html?highlight=threading


num = 1
lock = Lock()


def change_num():
    global num
    for i in range(100_000):
        # lock.acquire()
        num += 5
        num -= 5
        # lock.release()
        # if i % 1000 == 0:
        # print(i)


def num_test():
    pool = [Thread(target=change_num) for i in range(50)]
    for t in pool:
        t.start()
    for t in pool:
        t.join()
    print('num:', num)
    print('结论: 一般情况下不需要锁')


queue = []

N = 100_000


def queue_push():
    global queue
    for i in range(N):
        queue.append(i)


def queue_pop():
    n = 0
    global queue
    for i in range(N):
        while not queue:
            sleep(0.00001)
        v = queue.pop(0)
        if i % 1000 == 0:
            print('n:', len(queue))
        assert v == i
    print('last n:', n)


def queue_test():
    threads = [Thread(target=queue_push), Thread(target=queue_pop)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print('结论: 一般情况下不需要锁')


if __name__ == '__main__':
    # num_test()
    queue_test()
