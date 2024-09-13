import threading
import time
import os
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def count(n):
    process_id = os.getpid()
    thread_id = threading.get_ident()
    res = 0
    print(f"Process: {process_id} Thread: {thread_id} start")
    while n > 0:
        res += n
        n -= 1
    print(f"Process: {process_id} Thread: {thread_id} end")
    return res


NUM = 100000000

def single_thread():
    start = time.time()
    res1 = count(NUM)
    res2 = count(NUM)
    end = time.time()
    print(f"单线程耗时：{end - start:.2f} 秒, res1: {res1}, res2: {res2}")

def multi_thread():
    start = time.time()
    res1 = None
    res2 = None
    
    def thread_func1(num):
        # 线程共享同一进程的内存空间
        nonlocal res1
        res1 = count(num)
    
    def thread_func2(num):
        nonlocal res2
        res2 = count(num)
    
    t1 = threading.Thread(target=thread_func1, args=(NUM,))
    t2 = threading.Thread(target=thread_func2, args=(NUM,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    end = time.time()
    print(f"多线程耗时：{end - start:.2f} 秒, res1: {res1}, res2: {res2}")

def multi_thread_2():
    start = time.time()
    executor = ThreadPoolExecutor(max_workers=2)
    res1 = executor.submit(count, n=NUM)
    res2 = executor.submit(count, n=NUM)
    
    submit_time = time.time()
    print(f"多线程2提交任务耗时：{submit_time - start:.2f} 秒")
    
    # Wait for the result (this will block until the tasks are done)
    result1 = res1.result()
    result2 = res2.result()
    end = time.time()
    
    print(f"多线程2总耗时：{end - start:.2f} 秒， res1: {result1}, res2: {result2}")

def multi_thread_3():
    start = time.time()
    with ThreadPoolExecutor(max_workers=2) as executor:
        res1 = executor.submit(count, n=NUM)
        res2 = executor.submit(count, n=NUM)
    submit_time = time.time()
    print(f"多线程3提交任务耗时：{submit_time - start:.2f} 秒")
    
    # Wait for the result (this will block until the tasks are done)
    result1 = res1.result()
    result2 = res2.result()
    end = time.time()
    
    print(f"多线程3总耗时：{end - start:.2f} 秒， res1: {result1}, res2: {result2}")



res1 = None
res2 = None

def process_func1(num):
    # 在多进程中,每个进程都有自己独立的内存空间。
    global res1
    res1 = count(num)

def process_func2(num):
    global res2
    res2 = count(num)

def multi_process():
    start = time.time()
    
    p1 = multiprocessing.Process(target=process_func1, args=(NUM,))
    p2 = multiprocessing.Process(target=process_func2, args=(NUM,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    end = time.time()
    print(f"多进程耗时：{end - start:.2f} 秒, res1: {res1}, res2: {res2}")

def multi_process_2():
    start = time.time()
    with ProcessPoolExecutor(max_workers=2) as pool:
        res1 = pool.submit(count, n=NUM)
        res2 = pool.submit(count, n=NUM)
    end = time.time()
    # print(f"多进程2耗时：{end - start:.2f} 秒， res1: {res1.result()}, res2: {res2.result()}")
    print(f"多进程2 耗时：{end - start:.2f} 秒")
    print(f"多进程2 res1: {res1.result()}, res2: {res2.result()}")

if __name__ == "__main__":
    print(f'current process: {os.getpid()}')
    single_thread()
    print('-' * 100)
    time.sleep(1)
    multi_thread()
    print('-' * 100)
    time.sleep(1)
    multi_thread_2()
    print('-' * 100)
    time.sleep(1)
    multi_thread_3()
    print('-' * 100)
    time.sleep(1)
    multi_process()
    print('-' * 100)
    time.sleep(1)
    multi_process_2()

