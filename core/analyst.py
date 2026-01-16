"""
分析师模块
"""

import logging
from typing import Dict, Optional
from datetime import datetime

from .llm_client import DeepSeekClient
from data.stock_data import StockDataProvider

logger = logging.getLogger(__name__)


class MarketAnalyst:
    """市场分析师"""
    
    def __init__(self, llm_client: DeepSeekClient, data_provider: StockDataProvider):
        """
        初始化市场分析师
        
        Args:
            llm_client: LLM 客户端
            data_provider: 数据提供者
        """
        self.llm = llm_client
        self.data_provider = data_provider
    
    def analyze(self, ticker: str, date: str, market: str = "A股") -> str:
        """
        进行市场分析
        
        Args:
            ticker: 股票代码
            date: 分析日期
            market: 市场类型
            
        Returns:
            分析报告
        """
        logger.info(f"📊 [市场分析师] 开始分析: {ticker} ({market})")
        
        # 获取股票信息
        stock_info = self.data_provider.get_stock_info(ticker, market)
        market_info = self.data_provider.get_market_info(ticker, market)
        
        # 获取市场数据
        market_data = self.data_provider.get_market_data(ticker, date, market)
        
        # 构建分析提示
        system_prompt = f"""你是一位专业的股票技术分析师，擅长分析股票的市场表现和技术指标。

分析对象：
- {stock_info}
- 分析日期：{date}
- 计价货币：{market_info['currency_name']}（{market_info['currency_symbol']}）

请基于提供的市场数据，进行详细的技术分析，包括：
1. 价格趋势分析
2. 技术指标分析（如移动平均线、MACD、RSI等）
3. 成交量分析
4. 投资建议（买入/持有/卖出）

使用中文撰写报告，确保分析专业且详细。"""

        analysis_prompt = f"""
请对以下股票进行市场分析：

{stock_info}

市场数据：
{market_data}

请提供详细的技术分析报告，包括价格趋势、技术指标、成交量分析和投资建议。
"""
        
        # 调用 LLM 进行分析
        try:
            report = self.llm.analyze(
                prompt=analysis_prompt,
                system_prompt=system_prompt
            )
            logger.info(f"✅ [市场分析师] 分析完成: {ticker}")
            return report
        except Exception as e:
            logger.error(f"❌ [市场分析师] 分析失败: {e}")
            return f"市场分析失败: {str(e)}"


class FundamentalsAnalyst:
    """基本面分析师"""
    
    def __init__(self, llm_client: DeepSeekClient, data_provider: StockDataProvider):
        """
        初始化基本面分析师
        
        Args:
            llm_client: LLM 客户端
            data_provider: 数据提供者
        """
        self.llm = llm_client
        self.data_provider = data_provider
    
    def analyze(self, ticker: str, date: str, market: str = "A股") -> str:
        """
        进行基本面分析
        
        Args:
            ticker: 股票代码
            date: 分析日期
            market: 市场类型
            
        Returns:
            分析报告
        """
        logger.info(f"📊 [基本面分析师] 开始分析: {ticker} ({market})")
        
        # 获取股票信息
        stock_info = self.data_provider.get_stock_info(ticker, market)
        market_info = self.data_provider.get_market_info(ticker, market)
        
        # 获取市场数据（包含价格信息）
        market_data = self.data_provider.get_market_data(ticker, date, market)
        
        # 构建分析提示
        system_prompt = f"""你是一位专业的股票基本面分析师，擅长分析公司的财务状况和估值。

分析对象：
- {stock_info}
- 分析日期：{date}
- 计价货币：{market_info['currency_name']}（{market_info['currency_symbol']}）

请基于提供的市场数据，进行详细的基本面分析，包括：
1. 公司基本信息分析
2. 财务状况评估
3. 盈利能力分析
4. 估值分析（PE、PB、PEG等）
5. 投资建议（买入/持有/卖出）

使用中文撰写报告，确保分析专业且详细。如果数据不足，请说明并基于现有数据进行分析。"""

        analysis_prompt = f"""
请对以下股票进行基本面分析：

{stock_info}

市场数据：
{market_data}

请提供详细的基本面分析报告，包括财务状况、估值指标和投资建议。
"""
        
        # 调用 LLM 进行分析
        try:
            report = self.llm.analyze(
                prompt=analysis_prompt,
                system_prompt=system_prompt
            )
            logger.info(f"✅ [基本面分析师] 分析完成: {ticker}")
            return report
        except Exception as e:
            logger.error(f"❌ [基本面分析师] 分析失败: {e}")
            return f"基本面分析失败: {str(e)}"


class AnalystManager:
    """分析师管理器"""
    
    def __init__(self, llm_client: DeepSeekClient, data_provider: StockDataProvider):
        """
        初始化分析师管理器
        
        Args:
            llm_client: LLM 客户端
            data_provider: 数据提供者
        """
        self.market_analyst = MarketAnalyst(llm_client, data_provider)
        self.fundamentals_analyst = FundamentalsAnalyst(llm_client, data_provider)
    
    def analyze(
        self,
        ticker: str,
        date: str,
        market: str = "A股",
        analysts: Optional[list] = None
    ) -> Dict[str, str]:
        """
        执行分析
        
        Args:
            ticker: 股票代码
            date: 分析日期
            market: 市场类型
            analysts: 要使用的分析师列表，如果为 None 则使用所有分析师
            
        Returns:
            分析报告字典 {analyst_name: report}
        """
        if analysts is None:
            analysts = ["market", "fundamentals"]
        
        reports = {}
        
        if "market" in analysts:
            logger.info("📊 执行市场分析...")
            reports["市场分析师"] = self.market_analyst.analyze(ticker, date, market)
        
        if "fundamentals" in analysts:
            logger.info("📊 执行基本面分析...")
            reports["基本面分析师"] = self.fundamentals_analyst.analyze(ticker, date, market)
        
        return reports

