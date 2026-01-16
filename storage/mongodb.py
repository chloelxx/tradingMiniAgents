"""
MongoDB 存储模块
"""

import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging

logger = logging.getLogger(__name__)


class MongoDBStorage:
    """MongoDB 存储管理器"""
    
    def __init__(self):
        """初始化 MongoDB 连接"""
        self.client = None
        self.db = None
        self.collection = None
        self.connected = False
        self._connect()
    
    def _connect(self):
        """连接到 MongoDB"""
        try:
            # 从环境变量获取配置
            host = os.getenv("MONGODB_HOST", "localhost")
            port = int(os.getenv("MONGODB_PORT", "27017"))
            username = os.getenv("MONGODB_USERNAME", "")
            password = os.getenv("MONGODB_PASSWORD", "")
            database = os.getenv("MONGODB_DATABASE", "tradingagents")
            auth_source = os.getenv("MONGODB_AUTH_SOURCE", "admin")
            
            # 构建连接字符串
            if username and password:
                connection_string = f"mongodb://{username}:{password}@{host}:{port}/{database}?authSource={auth_source}"
            else:
                connection_string = f"mongodb://{host}:{port}/{database}"
            
            # 连接 MongoDB
            self.client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
            
            # 测试连接
            self.client.admin.command('ping')
            
            # 选择数据库和集合
            self.db = self.client[database]
            self.collection = self.db["stock_analysis_reports"]
            
            # 创建索引
            self._create_indexes()
            
            self.connected = True
            logger.info(f"✅ MongoDB 连接成功: {database}.stock_analysis_reports")
            
        except ConnectionFailure as e:
            logger.error(f"❌ MongoDB 连接失败: {e}")
            self.connected = False
        except Exception as e:
            logger.error(f"❌ MongoDB 初始化失败: {e}")
            self.connected = False
    
    def _create_indexes(self):
        """创建索引"""
        try:
            # 创建复合索引
            self.collection.create_index([
                ("stock_symbol", 1),
                ("analysis_date", -1),
                ("timestamp", -1)
            ])
            
            # 创建单字段索引
            self.collection.create_index("stock_symbol")
            self.collection.create_index("analysis_date")
            self.collection.create_index("timestamp")
            
            logger.info("✅ MongoDB 索引创建成功")
        except Exception as e:
            logger.warning(f"⚠️ MongoDB 索引创建失败: {e}")
    
    def save_analysis_report(
        self,
        stock_symbol: str,
        analysis_date: str,
        market: str,
        analysts: List[str],
        reports: Dict[str, str],
        research_depth: int = 3,
        image_analysis: Optional[str] = None
    ) -> bool:
        """
        保存分析报告
        
        Args:
            stock_symbol: 股票代码
            analysis_date: 分析日期
            market: 市场类型
            analysts: 分析师列表
            reports: 报告字典 {analyst_name: report_content}
            research_depth: 研究深度
            image_analysis: 图片分析结果（可选）
            
        Returns:
            是否保存成功
        """
        if not self.connected:
            logger.warning("MongoDB 未连接，跳过保存")
            return False
        
        try:
            # 生成分析 ID
            analysis_id = f"{stock_symbol}_{analysis_date}_{int(datetime.now().timestamp())}"
            
            # 构建文档
            document = {
                "analysis_id": analysis_id,
                "stock_symbol": stock_symbol,
                "analysis_date": analysis_date,
                "market": market,
                "analysts": analysts,
                "research_depth": research_depth,
                "reports": reports,
                "timestamp": datetime.now(),
                "status": "completed"
            }
            
            # 如果有图片分析，添加到文档
            if image_analysis:
                document["image_analysis"] = image_analysis
            
            # 插入文档
            result = self.collection.insert_one(document)
            
            if result.inserted_id:
                logger.info(f"✅ 分析报告已保存到 MongoDB: {analysis_id}")
                return True
            else:
                logger.error("❌ MongoDB 插入失败")
                return False
                
        except Exception as e:
            logger.error(f"❌ 保存分析报告失败: {e}")
            return False
    
    def get_analysis_reports(
        self,
        stock_symbol: Optional[str] = None,
        analysis_date: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict]:
        """
        获取分析报告
        
        Args:
            stock_symbol: 股票代码（可选）
            analysis_date: 分析日期（可选）
            limit: 返回数量限制
            
        Returns:
            报告列表
        """
        if not self.connected:
            logger.warning("MongoDB 未连接，无法获取报告")
            return []
        
        try:
            query = {}
            if stock_symbol:
                query["stock_symbol"] = stock_symbol
            if analysis_date:
                query["analysis_date"] = analysis_date
            
            cursor = self.collection.find(query).sort("timestamp", -1).limit(limit)
            reports = list(cursor)
            
            # 转换 ObjectId 为字符串
            for report in reports:
                report["_id"] = str(report["_id"])
                if isinstance(report.get("timestamp"), datetime):
                    report["timestamp"] = report["timestamp"].isoformat()
            
            logger.info(f"✅ 从 MongoDB 获取了 {len(reports)} 个分析报告")
            return reports
            
        except Exception as e:
            logger.error(f"❌ 获取分析报告失败: {e}")
            return []
    
    def close(self):
        """关闭连接"""
        if self.client:
            self.client.close()
            self.connected = False
            logger.info("MongoDB 连接已关闭")

