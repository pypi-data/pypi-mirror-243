import threading

import redis  # type: ignore

conn = redis.Redis(host="localhost", port=6379, db=1)
conn.set('num', 1)


def change_num(conn1):
    print('thread start')
    for i in range(10000):
        conn1.incr('num', 5)
        conn1.decr('num', 5)


if __name__ == '__main__':
    conn_pool = [redis.StrictRedis(host="localhost", port=6379, db=1) for i in range(16)]
    t_pool = []
    for conn in conn_pool:
        t = threading.Thread(target=change_num, args=(conn,))
        t_pool.append(t)
    for t in t_pool:
        t.start()
    for t in t_pool:
        t.join()
    print(conn.get('num'))
