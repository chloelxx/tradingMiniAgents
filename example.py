#!/usr/bin/env python3
"""
使用示例
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

from core.llm_client import DeepSeekClient
from core.analyst import AnalystManager
from data.stock_data import StockDataProvider
from storage.mongodb import MongoDBStorage

def example_basic_analysis():
    """基本分析示例"""
    print("=" * 60)
    print("示例 1: 基本股票分析")
    print("=" * 60)
    
    # 初始化组件
    llm_client = DeepSeekClient()
    data_provider = StockDataProvider()
    analyst_manager = AnalystManager(llm_client, data_provider)
    
    # 执行分析
    reports = analyst_manager.analyze(
        ticker="300748",
        date="2026-01-16",
        market="A股",
        analysts=["market", "fundamentals"]
    )
    
    # 显示结果
    for analyst_name, report in reports.items():
        print(f"\n{'=' * 60}")
        print(f"{analyst_name} 报告")
        print(f"{'=' * 60}")
        print(report)
    
    # 保存到 MongoDB
    mongodb_storage = MongoDBStorage()
    if mongodb_storage.connected:
        mongodb_storage.save_analysis_report(
            stock_symbol="300748",
            analysis_date="2026-01-16",
            market="A股",
            analysts=list(reports.keys()),
            reports=reports,
            research_depth=3
        )
        print("\n✅ 分析结果已保存到 MongoDB")
    else:
        print("\n⚠️ MongoDB 未连接，结果未保存")


def example_single_analyst():
    """单个分析师示例"""
    print("=" * 60)
    print("示例 2: 仅使用市场分析师")
    print("=" * 60)
    
    llm_client = DeepSeekClient()
    data_provider = StockDataProvider()
    analyst_manager = AnalystManager(llm_client, data_provider)
    
    reports = analyst_manager.analyze(
        ticker="300748",
        date="2026-01-16",
        market="A股",
        analysts=["market"]  # 仅使用市场分析师
    )
    
    for analyst_name, report in reports.items():
        print(f"\n{analyst_name} 报告:")
        print(report)


if __name__ == "__main__":
    # 检查配置
    if not os.getenv("DEEPSEEK_API_KEY"):
        print("❌ 错误: 未设置 DEEPSEEK_API_KEY")
        print("请在 .env 文件中配置 DEEPSEEK_API_KEY")
        exit(1)
    
    # 运行示例
    try:
        example_basic_analysis()
    except Exception as e:
        print(f"❌ 示例执行失败: {e}")
        import traceback
        traceback.print_exc()

