import asyncio
import time

shared_counter = 0

lock = asyncio.Lock()

async def worker_without_lock(worker_id, count_to):
    """不使用锁的协程，可能导致竞争条件"""
    global shared_counter
    print(f"无锁工人 {worker_id}: 开始运行")
    local_counter = 0
    for _ in range(count_to):
        current_val = shared_counter
        # 模拟I/O操作或计算，给其他协程执行的机会
        # 如果没有这句 await，在CPython中由于GIL的存在，
        # 对于纯计算密集型且无IO绑定的简单递增，可能不会明显看到竞争，
        # 但实际异步场景中，await是常见的。
        await asyncio.sleep(0.0001)
        shared_counter = current_val + 1
        local_counter += 1
    print(f"无锁工人 {worker_id}: 完成, 本地计数 {local_counter}, 共享计数器现在是 {shared_counter}")

async def worker_with_lock(worker_id, count_to):
    """使用锁的协程，保护共享资源"""
    global shared_counter
    print(f"有锁工人 {worker_id}: 开始运行")
    local_counter = 0
    for _ in range(count_to):
        async with lock:  # 获取锁
            # --- 临界区开始 ---
            # print(f"有锁工人 {worker_id}: 拿到锁")
            current_val = shared_counter
            await asyncio.sleep(0.0001) # 模拟在持有锁时的一些操作
            shared_counter = current_val + 1
            # --- 临界区结束 ---
        # print(f"有锁工人 {worker_id}: 释放锁")
        local_counter += 1
    print(f"有锁工人 {worker_id}: 完成, 本地计数 {local_counter}, 共享计数器现在是 {shared_counter}")


async def main():
    global shared_counter
    num_workers = 3
    counts_per_worker = 500
    total_expected_count = num_workers * counts_per_worker

    print(f"--- 场景1: 没有锁 --- (期望总数: {total_expected_count})")
    shared_counter = 0 # 重置计数器
    tasks_no_lock = [
        worker_without_lock(i, counts_per_worker) for i in range(1, num_workers + 1)
    ]
    await asyncio.gather(*tasks_no_lock)
    print(f"最终 (无锁): shared_counter = {shared_counter} (期望值: {total_expected_count})\n")
    # 由于竞争条件，结果通常会小于期望值

    print(f"--- 场景2: 使用锁 --- (期望总数: {total_expected_count})")
    shared_counter = 0 # 重置计数器
    tasks_with_lock = [
        worker_with_lock(i, counts_per_worker) for i in range(1, num_workers + 1)
    ]
    await asyncio.gather(*tasks_with_lock)
    print(f"最终 (有锁): shared_counter = {shared_counter} (期望值: {total_expected_count})\n")
    # 使用锁后，结果会是正确的期望值

if __name__ == "__main__":
    # 在 Python 3.7+ 中，推荐使用 asyncio.run()
    asyncio.run(main())