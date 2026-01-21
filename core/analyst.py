"""
分析师模块 - 提供同步和异步版本的股票分析功能
"""

import logging
from typing import Dict, Optional, AsyncGenerator
from datetime import datetime

from .llm_client import DeepSeekClient
from data.stock_data import StockDataProvider

logger = logging.getLogger(__name__)


# ==================== 同步版本分析师 ====================

class MarketAnalyst:
    """市场分析师 - 技术面分析（同步版本）"""
    
    def __init__(self, llm_client: DeepSeekClient, data_provider: StockDataProvider):
        self.llm = llm_client
        self.data_provider = data_provider
    
    def analyze(self, ticker: str, date: str, market: str = "A股") -> str:
        """进行市场分析"""
        logger.info(f"📊 [市场分析师] 开始分析: {ticker} ({market})")
        
        stock_info = self.data_provider.get_stock_info(ticker, market)
        market_info = self.data_provider.get_market_info(ticker, market)
        market_data = self.data_provider.get_market_data(ticker, date, market)
        
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

        analysis_prompt = f"""请对以下股票进行市场分析：

{stock_info}

市场数据：
{market_data}

请提供详细的技术分析报告，包括价格趋势、技术指标、成交量分析和投资建议。"""
        
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
    """基本面分析师 - 财务面分析（同步版本）"""
    
    def __init__(self, llm_client: DeepSeekClient, data_provider: StockDataProvider):
        self.llm = llm_client
        self.data_provider = data_provider
    
    def analyze(self, ticker: str, date: str, market: str = "A股") -> str:
        """进行基本面分析"""
        logger.info(f"📊 [基本面分析师] 开始分析: {ticker} ({market})")
        
        stock_info = self.data_provider.get_stock_info(ticker, market)
        market_info = self.data_provider.get_market_info(ticker, market)
        market_data = self.data_provider.get_market_data(ticker, date, market)
        
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

        analysis_prompt = f"""请对以下股票进行基本面分析：

{stock_info}

市场数据：
{market_data}

请提供详细的基本面分析报告，包括财务状况、估值指标和投资建议。"""
        
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
    """分析师管理器 - 协调多个分析师（同步版本）"""
    
    def __init__(self, llm_client: DeepSeekClient, data_provider: StockDataProvider):
        self.market_analyst = MarketAnalyst(llm_client, data_provider)
        self.fundamentals_analyst = FundamentalsAnalyst(llm_client, data_provider)
    
    def analyze(
        self,
        ticker: str,
        date: str,
        market: str = "A股",
        analysts: Optional[list] = None
    ) -> Dict[str, str]:
        """执行分析"""
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


# ==================== 异步流式版本分析师 ====================

class MarketAnalystStream:
    """市场分析师 - 技术面分析（异步流式版本）"""
    
    def __init__(self, llm_client: DeepSeekClient, data_provider: StockDataProvider):
        self.llm = llm_client
        self.data_provider = data_provider
    
    async def analyze_stream(self, ticker: str, date: str, market: str = "A股") -> AsyncGenerator[str, None]:
        """进行市场分析（流式版本）"""
        logger.info(f"📊 [市场分析师] 开始分析: {ticker} ({market})")
        
        stock_info = self.data_provider.get_stock_info(ticker, market)
        market_info = self.data_provider.get_market_info(ticker, market)
        market_data = self.data_provider.get_market_data(ticker, date, market)
        
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

        analysis_prompt = f"""请对以下股票进行市场分析：

{stock_info}

市场数据：
{market_data}

请提供详细的技术分析报告，包括价格趋势、技术指标、成交量分析和投资建议。"""
        
        try:
            async for chunk in self.llm.analyze_stream(
                prompt=analysis_prompt,
                system_prompt=system_prompt
            ):
                yield chunk
            logger.info(f"✅ [市场分析师] 分析完成: {ticker}")
        except Exception as e:
            logger.error(f"❌ [市场分析师] 分析失败: {e}")
            yield f"市场分析失败: {str(e)}"


class FundamentalsAnalystStream:
    """基本面分析师 - 财务面分析（异步流式版本）"""
    
    def __init__(self, llm_client: DeepSeekClient, data_provider: StockDataProvider):
        self.llm = llm_client
        self.data_provider = data_provider
    
    async def analyze_stream(self, ticker: str, date: str, market: str = "A股") -> AsyncGenerator[str, None]:
        """进行基本面分析（流式版本）"""
        logger.info(f"📊 [基本面分析师] 开始分析: {ticker} ({market})")
        
        stock_info = self.data_provider.get_stock_info(ticker, market)
        market_info = self.data_provider.get_market_info(ticker, market)
        market_data = self.data_provider.get_market_data(ticker, date, market)
        
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

        analysis_prompt = f"""请对以下股票进行基本面分析：

{stock_info}

市场数据：
{market_data}

请提供详细的基本面分析报告，包括财务状况、估值指标和投资建议。"""
        
        try:
            async for chunk in self.llm.analyze_stream(
                prompt=analysis_prompt,
                system_prompt=system_prompt
            ):
                yield chunk
            logger.info(f"✅ [基本面分析师] 分析完成: {ticker}")
        except Exception as e:
            logger.error(f"❌ [基本面分析师] 分析失败: {e}")
            yield f"基本面分析失败: {str(e)}"


class AnalystManagerStream:
    """分析师管理器 - 协调多个分析师（异步流式版本）"""
    
    def __init__(self, llm_client: DeepSeekClient, data_provider: StockDataProvider):
        self.market_analyst_stream = MarketAnalystStream(llm_client, data_provider)
        self.fundamentals_analyst_stream = FundamentalsAnalystStream(llm_client, data_provider)
    
    async def analyze_stream(
        self,
        ticker: str,
        date: str,
        market: str = "A股",
        analysts: Optional[list] = None
    ) -> AsyncGenerator[str, None]:
        """执行流式分析"""
        if analysts is None:
            analysts = ["market", "fundamentals"]
        
        if "market" in analysts:
            logger.info("📊 执行市场分析...")
            yield "[ANALYST_START]市场分析师\n"
            async for chunk in self.market_analyst_stream.analyze_stream(ticker, date, market):
                yield chunk
            yield "\n[ANALYST_END]市场分析师\n"
        
        if "fundamentals" in analysts:
            logger.info("📊 执行基本面分析...")
            yield "[ANALYST_START]基本面分析师\n"
            async for chunk in self.fundamentals_analyst_stream.analyze_stream(ticker, date, market):
                yield chunk
            yield "\n[ANALYST_END]基本面分析师\n"

