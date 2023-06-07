import threading 
import time

res = []

def produce(prefix, n):
    for i in range(n):
        time.sleep(1)
        print(f'{prefix}:{i}')
        res.append(f'{prefix}:{i}')


t1 = threading.Thread(target=produce, args=('t1', 3))
t2 = threading.Thread(target=produce, args=('t2', 5))

# 多线程之1，两个线程都先 start 起来
# t1.start()
# t2.start()

# t1.join()
# t2.join()

# 多线程之2，一个线程先 start，然后 join，然后再 start 另一个线程，
t1.start()
t1.join()

t2.start()
t2.join()

print(res)