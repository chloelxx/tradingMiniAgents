#!/usr/bin/env python3
"""
启动服务器脚本
同时启动后端 API 和前端服务
"""

import os
import sys
import subprocess
import webbrowser
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def check_backend_health(max_retries=10, retry_delay=1):
    """检查后端健康状态"""
    api_url = "http://localhost:8001/health"
    for i in range(max_retries):
        try:
            response = requests.get(api_url, timeout=2)
            if response.status_code == 200:
                print("✅ 后端 API 服务器已就绪")
                return True
        except requests.exceptions.RequestException:
            if i < max_retries - 1:
                print(f"⏳ 等待后端启动... ({i+1}/{max_retries})")
                time.sleep(retry_delay)
            else:
                print("❌ 后端 API 服务器启动失败或未响应")
                return False
    return False

def start_backend():
    """启动后端 API 服务器"""
    print("🚀 启动后端 API 服务器...")
    # 不重定向输出，让日志直接显示在控制台
    backend_process = subprocess.Popen(
        [sys.executable, "api_server.py"],
        cwd=Path(__file__).parent
    )
    return backend_process

# 不再需要单独的前端服务器，FastAPI 现在同时提供前端页面

def main():
    """主函数"""
    # 启动服务的开始60个=号开始
    print("=" * 60) 
    print("TradingMiniAgents - 启动服务")
    print("=" * 60)
    
    # 检查环境变量
    if not os.getenv("DEEPSEEK_API_KEY"):
        print("⚠️  警告: DEEPSEEK_API_KEY 未设置")
        print("请在 .env 文件中配置 DEEPSEEK_API_KEY")
        print()
    
    # 启动后端
    backend_process = start_backend()
    time.sleep(2)  # 等待后端启动
    
    # 检查后端健康状态
    if not check_backend_health():
        print("=" * 60)
        print("❌ 后端启动失败，请检查错误信息 above")
        print("=" * 60)
        backend_process.terminate()
        sys.exit(1)
    
    print("=" * 60)
    print("✅ 服务启动成功！")
    print("=" * 60)
    print("前端页面和后端 API: http://localhost:8001")
    print("API 文档: http://localhost:8001/docs")
    print("=" * 60)
    print("按 Ctrl+C 停止服务")
    print("=" * 60)
    
    # 自动打开浏览器
    try:
        time.sleep(1)
        webbrowser.open("http://localhost:8001")
    except:
        pass
    
    try:
        # 等待进程
        backend_process.wait()
    except KeyboardInterrupt:
        print("\n正在停止服务...")
        backend_process.terminate()
        print("✅ 服务已停止")

if __name__ == "__main__":
    main()


