# async_example.py
import asyncio
import httpx  # 一个支持异步的 requests 库
import time

async def fetch_title_async(client, url):
    """一个异步函数，获取单个网页标题"""
    print(f"开始请求 {url}...")
    try:
        # await 让出控制权，直到网络请求完成
        response = await client.get(url, timeout=5) 
        print(f"完成请求 {url}")
        return response.text.split('<title>')[1].split('</title>')[0]
    except Exception as e:
        print(f"请求 {url} 失败: {e}")
        return "获取失败"

async def main():
    urls = [
        "https://www.google.com",
        "https://www.bing.com",
        "https://www.duckduckgo.com",
    ]
    
    start_time = time.time()
    
    # 创建一个异步HTTP客户端
    async with httpx.AsyncClient() as client:
        # 为每个URL创建一个任务，这些任务会立即开始执行
        tasks = [fetch_title_async(client, url) for url in urls]
        
        # asyncio.gather() 会并发运行所有任务，并等待它们全部完成
        results = await asyncio.gather(*tasks)
    
    for url, title in zip(urls, results):
        print(f"网站: {url}, 标题: {title}")
        
    end_time = time.time()
    print(f"\n异步总耗时: {end_time - start_time:.2f} 秒")

if __name__ == "__main__":
    asyncio.run(main())