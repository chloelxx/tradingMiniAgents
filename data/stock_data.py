"""
股票数据获取模块
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class StockDataProvider:
    """股票数据提供者"""
    
    def __init__(self):
        self.market_info = {
            'A股': {
                'is_china': True,
                'currency_name': '人民币',
                'currency_symbol': '¥'
            },
            '港股': {
                'is_china': False,
                'is_hk': True,
                'currency_name': '港币',
                'currency_symbol': 'HK$'
            },
            '美股': {
                'is_china': False,
                'is_us': True,
                'currency_name': '美元',
                'currency_symbol': '$'
            }
        }
    
    def get_market_info(self, ticker: str, market: str = "A股") -> Dict:
        """获取市场信息"""
        return self.market_info.get(market, self.market_info['A股'])
    
    def get_stock_info(self, ticker: str, market: str = "A股") -> str:
        """
        获取股票基本信息
        
        Args:
            ticker: 股票代码
            market: 市场类型
            
        Returns:
            股票信息字符串
        """
        market_info = self.get_market_info(ticker, market)
        
        if market_info.get('is_china'):
            return self._get_china_stock_info(ticker)
        elif market_info.get('is_hk'):
            return self._get_hk_stock_info(ticker)
        elif market_info.get('is_us'):
            return self._get_us_stock_info(ticker)
        else:
            return f"股票代码: {ticker}\n市场: {market}"
    
    def _get_china_stock_info(self, ticker: str) -> str:
        """获取 A 股股票信息"""
        try:
            import akshare as ak
            # 获取股票基本信息
            stock_info = ak.stock_individual_info_em(symbol=ticker)
            if stock_info is not None and not stock_info.empty:
                info_dict = dict(zip(stock_info['item'], stock_info['value']))
                company_name = info_dict.get('股票简称', ticker)
                return f"股票代码: {ticker}\n股票名称: {company_name}\n市场: A股"
        except Exception as e:
            logger.warning(f"获取 A 股信息失败: {e}")
        
        return f"股票代码: {ticker}\n市场: A股"
    
    def _get_hk_stock_info(self, ticker: str) -> str:
        """获取港股股票信息"""
        try:
            import akshare as ak
            # 清理股票代码
            clean_ticker = ticker.replace('.HK', '').replace('.hk', '')
            stock_info = ak.stock_hk_spot_em()
            if stock_info is not None and not stock_info.empty:
                stock_data = stock_info[stock_info['代码'] == clean_ticker]
                if not stock_data.empty:
                    company_name = stock_data.iloc[0]['名称']
                    return f"股票代码: {ticker}\n股票名称: {company_name}\n市场: 港股"
        except Exception as e:
            logger.warning(f"获取港股信息失败: {e}")
        
        return f"股票代码: {ticker}\n市场: 港股"
    
    def _get_us_stock_info(self, ticker: str) -> str:
        """获取美股股票信息"""
        try:
            import yfinance as yf
            stock = yf.Ticker(ticker)
            info = stock.info
            company_name = info.get('longName', info.get('shortName', ticker))
            return f"股票代码: {ticker}\n股票名称: {company_name}\n市场: 美股"
        except Exception as e:
            logger.warning(f"获取美股信息失败: {e}")
        
        return f"股票代码: {ticker}\n市场: 美股"
    
    def get_market_data(self, ticker: str, date: str, market: str = "A股", days: int = 365) -> str:
        """
        获取市场数据
        
        Args:
            ticker: 股票代码
            date: 分析日期
            market: 市场类型
            days: 历史数据天数
            
        Returns:
            市场数据字符串
        """
        market_info = self.get_market_info(ticker, market)
        
        if market_info.get('is_china'):
            return self._get_china_market_data(ticker, date, days)
        elif market_info.get('is_hk'):
            return self._get_hk_market_data(ticker, date, days)
        elif market_info.get('is_us'):
            return self._get_us_market_data(ticker, date, days)
        else:
            return f"暂不支持 {market} 市场数据"
    
    def _get_china_market_data(self, ticker: str, date: str, days: int) -> str:
        """获取 A 股市场数据"""
        try:
            import akshare as ak
            from datetime import datetime, timedelta
            
            end_date = datetime.strptime(date, "%Y-%m-%d")
            start_date = end_date - timedelta(days=days)
            
            # 获取历史数据
            df = ak.stock_zh_a_hist(
                symbol=ticker,
                period="daily",
                start_date=start_date.strftime("%Y%m%d"),
                end_date=end_date.strftime("%Y%m%d"),
                adjust="qfq"
            )
            
            if df is not None and not df.empty:
                latest = df.iloc[-1]
                return f"""
股票代码: {ticker}
最新日期: {latest['日期']}
收盘价: {latest['收盘']} 元
开盘价: {latest['开盘']} 元
最高价: {latest['最高']} 元
最低价: {latest['最低']} 元
成交量: {latest['成交量']}
成交额: {latest['成交额']} 元
涨跌幅: {latest.get('涨跌幅', 'N/A')}%
历史数据天数: {len(df)}
"""
        except Exception as e:
            logger.warning(f"获取 A 股市场数据失败: {e}")
        
        return f"股票代码: {ticker}\n数据获取失败，请检查股票代码是否正确"
    
    def _get_hk_market_data(self, ticker: str, date: str, days: int) -> str:
        """获取港股市场数据"""
        try:
            import akshare as ak
            clean_ticker = ticker.replace('.HK', '').replace('.hk', '')
            
            # 获取港股历史数据
            df = ak.stock_hk_hist(
                symbol=clean_ticker,
                period="daily",
                start_date=date.replace('-', ''),
                end_date=date.replace('-', ''),
                adjust="qfq"
            )
            
            if df is not None and not df.empty:
                latest = df.iloc[-1]
                return f"""
股票代码: {ticker}
最新日期: {latest['日期']}
收盘价: {latest['收盘']} 港币
开盘价: {latest['开盘']} 港币
最高价: {latest['最高']} 港币
最低价: {latest['最低']} 港币
成交量: {latest['成交量']}
成交额: {latest['成交额']} 港币
"""
        except Exception as e:
            logger.warning(f"获取港股市场数据失败: {e}")
        
        return f"股票代码: {ticker}\n数据获取失败"
    
    def _get_us_market_data(self, ticker: str, date: str, days: int) -> str:
        """获取美股市场数据"""
        try:
            import yfinance as yf
            from datetime import datetime, timedelta
            
            end_date = datetime.strptime(date, "%Y-%m-%d")
            start_date = end_date - timedelta(days=days)
            
            stock = yf.Ticker(ticker)
            df = stock.history(start=start_date, end=end_date)
            
            if df is not None and not df.empty:
                latest = df.iloc[-1]
                return f"""
股票代码: {ticker}
最新日期: {latest.name.strftime('%Y-%m-%d')}
收盘价: ${latest['Close']:.2f}
开盘价: ${latest['Open']:.2f}
最高价: ${latest['High']:.2f}
最低价: ${latest['Low']:.2f}
成交量: {latest['Volume']:,.0f}
历史数据天数: {len(df)}
"""
        except Exception as e:
            logger.warning(f"获取美股市场数据失败: {e}")
        
        return f"股票代码: {ticker}\n数据获取失败"

