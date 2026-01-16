#!/usr/bin/env python3
"""
TradingMiniAgents - 简化版股票分析智能体
主程序入口
"""

import os
import sys
import argparse
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# 导入核心模块
from core.llm_client import DeepSeekClient
from core.analyst import AnalystManager
from core.image_analyzer import ImageAnalyzer
from data.stock_data import StockDataProvider
from storage.mongodb import MongoDBStorage


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='TradingMiniAgents - 简化版股票分析智能体')
    parser.add_argument('--ticker', type=str, required=True, help='股票代码')
    parser.add_argument('--date', type=str, default=None, help='分析日期 (YYYY-MM-DD)，默认为今天')
    parser.add_argument('--market', type=str, default='A股', choices=['A股', '港股', '美股'], help='市场类型')
    parser.add_argument('--analysts', type=str, default='market,fundamentals', 
                       help='要使用的分析师，用逗号分隔 (market, fundamentals)')
    parser.add_argument('--image', type=str, default=None, help='要分析的图片路径（可选）')
    parser.add_argument('--depth', type=int, default=3, help='研究深度 (1-5)，默认 3')
    
    args = parser.parse_args()
    
    # 设置分析日期
    if args.date is None:
        analysis_date = datetime.now().strftime("%Y-%m-%d")
    else:
        analysis_date = args.date
    
    # 解析分析师列表
    analyst_list = [a.strip() for a in args.analysts.split(',')]
    
    logger.info("=" * 60)
    logger.info("🚀 TradingMiniAgents - 股票分析开始")
    logger.info("=" * 60)
    logger.info(f"股票代码: {args.ticker}")
    logger.info(f"分析日期: {analysis_date}")
    logger.info(f"市场类型: {args.market}")
    logger.info(f"分析师: {', '.join(analyst_list)}")
    logger.info(f"研究深度: {args.depth}")
    if args.image:
        logger.info(f"图片分析: {args.image}")
    logger.info("=" * 60)
    
    try:
        # 初始化组件
        logger.info("📦 初始化组件...")
        
        # LLM 客户端（从环境变量读取所有配置）
        llm_client = DeepSeekClient()
        logger.info("✅ LLM 客户端初始化完成")
        
        # 数据提供者
        data_provider = StockDataProvider()
        logger.info("✅ 数据提供者初始化完成")
        
        # 分析师管理器
        analyst_manager = AnalystManager(llm_client, data_provider)
        logger.info("✅ 分析师管理器初始化完成")
        
        # MongoDB 存储
        mongodb_storage = MongoDBStorage()
        if mongodb_storage.connected:
            logger.info("✅ MongoDB 存储初始化完成")
        else:
            logger.warning("⚠️ MongoDB 未连接，分析结果将不会保存到数据库")
        
        # 图片分析（如果提供）
        image_analysis = None
        if args.image:
            logger.info(f"🖼️ 开始分析图片: {args.image}")
            image_analyzer = ImageAnalyzer(llm_client)
            image_path = Path(args.image)
            if image_path.exists():
                image_analysis = image_analyzer.analyze_image(
                    str(image_path),
                    f"请分析这张与股票 {args.ticker} 相关的图片，提取关键信息用于股票分析。"
                )
                logger.info("✅ 图片分析完成")
            else:
                logger.warning(f"⚠️ 图片文件不存在: {args.image}")
        
        # 执行分析
        logger.info("📊 开始执行股票分析...")
        reports = analyst_manager.analyze(
            ticker=args.ticker,
            date=analysis_date,
            market=args.market,
            analysts=analyst_list
        )
        
        # 显示分析结果
        logger.info("=" * 60)
        logger.info("📋 分析结果")
        logger.info("=" * 60)
        
        for analyst_name, report in reports.items():
            logger.info(f"\n{'=' * 60}")
            logger.info(f"📊 {analyst_name} 报告")
            logger.info(f"{'=' * 60}")
            print(f"\n{report}\n")
        
        # 保存到 MongoDB
        if mongodb_storage.connected:
            logger.info("💾 保存分析结果到 MongoDB...")
            success = mongodb_storage.save_analysis_report(
                stock_symbol=args.ticker,
                analysis_date=analysis_date,
                market=args.market,
                analysts=list(reports.keys()),
                reports=reports,
                research_depth=args.depth,
                image_analysis=image_analysis
            )
            if success:
                logger.info("✅ 分析结果已保存到 MongoDB")
            else:
                logger.warning("⚠️ 保存到 MongoDB 失败")
        
        logger.info("=" * 60)
        logger.info("✅ 分析完成！")
        logger.info("=" * 60)
        
    except KeyboardInterrupt:
        logger.info("\n⚠️ 用户中断分析")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ 分析失败: {e}", exc_info=True)
        sys.exit(1)
    finally:
        # 清理资源
        if 'mongodb_storage' in locals():
            mongodb_storage.close()


if __name__ == "__main__":
    main()

