import asyncio
import time

async def simple_greeting(name, delay):
    """一个简单的协程，模拟耗时操作并返回结果"""
    print(f"问候任务 for {name}: 开始，将等待 {delay} 秒...")
    await asyncio.sleep(delay)
    result = f"你好, {name}! (等待了 {delay} 秒)"
    print(f"问候任务 for {name}: 完成.")
    return result

async def main_coroutine():
    """主协程，将安排其他协程的执行"""
    print("主协程开始.")

    # 创建协程对象
    coro1 = simple_greeting("Alice", 2)
    coro2 = simple_greeting("Bob", 1)

    # 使用 asyncio.gather 可以并发运行多个协程并等待它们全部完成
    # gather 本身返回一个 Future
    # print("主协程: 即将使用 asyncio.gather 并发运行问候任务.")
    # results = await asyncio.gather(coro1, coro2)

    # print("\n主协程: 所有问候任务完成.")
    # for res in results:
    #     print(f"  - 结果: {res}")

    # print("主协程结束.")
    # return "主协程成功执行完毕！"
    res1 = await coro1
    res2 = await coro2
    return res1, res2

if __name__ == "__main__":

    loop = asyncio.get_event_loop()

    print(f"获取到的事件循环: {loop}")

    print("即将调用 loop.run_until_complete(main_coroutine()).")
    
    final_result = loop.run_until_complete(main_coroutine())
    print(f"\nloop.run_until_complete 返回: '{final_result}'")