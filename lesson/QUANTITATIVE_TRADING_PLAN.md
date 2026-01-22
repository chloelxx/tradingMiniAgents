# 量化交易模块集成方案

## 📊 项目现状分析

### 当前功能

```
┌─────────────────────────────────┐
│  股票分析系统                    │
├─────────────────────────────────┤
│  ✓ 市场分析师 (技术面)           │
│  ✓ 基本面分析师 (财务面)         │
│  ✓ 流式输出显示                  │
│  ✓ 数据源: akshare, baostock    │
│  ✓ LLM: DeepSeek API            │
│  ✓ 存储: MongoDB                │
└─────────────────────────────────┘
```

### 缺失的功能

```
┌─────────────────────────────────┐
│  需要新增的量化交易模块            │
├─────────────────────────────────┤
│  ✗ 交易信号生成                  │
│  ✗ 回测引擎                      │
│  ✗ 实盘/模拟交易                 │
│  ✗ 交易记录管理                  │
│  ✗ 风险控制模块                  │
│  ✗ 性能分析                      │
└─────────────────────────────────┘
```

---

## 🛠️ 量化交易三层架构

```
┌──────────────────────────────────────────────────────┐
│                      前端 UI 层                       │
│  (Vue3 + Element Plus)                              │
│  - 交易策略配置                                      │
│  - 实时账户展示                                      │
│  - 交易记录查看                                      │
│  - 回测结果分析                                      │
└──────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────┐
│                    API 中间层                        │
│  (FastAPI)                                          │
│  - /api/strategy (策略管理)                         │
│  - /api/backtest (回测)                             │
│  - /api/trade (交易执行)                            │
│  - /api/portfolio (账户管理)                        │
│  - /api/signals (信号生成)                          │
└──────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────┐
│                   量化交易引擎                        │
│  (Python 核心模块)                                   │
│  - 策略引擎 (Strategy Engine)                        │
│  - 回测引擎 (Backtest Engine)                        │
│  - 执行引擎 (Execution Engine)                       │
│  - 风险管理 (Risk Management)                        │
│  - 数据管理 (Data Management)                        │
└──────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────┐
│                   外部数据源与经纪商                  │
│  数据源:                                             │
│  - akshare (A股数据)                                │
│  - baostock (历史数据)                              │
│  - 实时行情 API                                      │
│                                                      │
│  经纪商接口:                                         │
│  - 东方财富 (如可用 API)                            │
│  - 华泰 TradeAPI                                    │
│  - 其他支持 Python 的券商                            │
│  - 模拟交易平台                                      │
└──────────────────────────────────────────────────────┘
```

---

## 🎯 分步实施方案（5个阶段）

### 📍 Phase 1: 基础框架搭建（第1-2周）

#### Step 1.1: 安装量化交易库

```bash
# 核心量化库
pip install backtrader          # 回测框架
pip install vectorbt            # 向量化回测
pip install ta-lib              # 技术指标
pip install pandas-ta           # Pandas 技术指标
pip install pyfolio             # 性能分析
pip install ccxt                # 交易所 API 统一接口（可选）
```

#### Step 1.2: 创建项目结构

```
tradingMiniAgents/
├── quant/                       # 新增量化模块
│   ├── __init__.py
│   ├── strategies/              # 策略集合
│   │   ├── __init__.py
│   │   ├── base_strategy.py     # 策略基类
│   │   ├── ma_strategy.py       # 均线策略
│   │   ├── rsi_strategy.py      # RSI策略
│   │   └── combined_strategy.py # 复合策略
│   ├── backtest/                # 回测引擎
│   │   ├── __init__.py
│   │   ├── backtest_engine.py   # 回测核心
│   │   └── metrics.py           # 性能指标
│   ├── risk/                    # 风险管理
│   │   ├── __init__.py
│   │   ├── position.py          # 持仓管理
│   │   └── portfolio.py         # 投资组合
│   ├── execution/               # 执行引擎
│   │   ├── __init__.py
│   │   ├── simulator.py         # 模拟交易
│   │   └── real_trader.py       # 实盘交易（可选）
│   ├── data/                    # 数据管理
│   │   ├── __init__.py
│   │   ├── data_manager.py      # 数据管理器
│   │   └── indicators.py        # 指标计算
│   └── utils/                   # 工具函数
│       ├── __init__.py
│       └── validators.py        # 验证函数
├── quant_api/                   # 新增 API 路由
│   ├── __init__.py
│   ├── strategy_routes.py       # 策略管理接口
│   ├── backtest_routes.py       # 回测接口
│   ├── trade_routes.py          # 交易执行接口
│   └── portfolio_routes.py      # 账户管理接口
└── [其他现有目录]
```

#### Step 1.3: 创建配置文件

```python
# quant/config.py
class QuantConfig:
    # 回测配置
    INITIAL_CASH = 100000  # 初始资金
    COMMISSION = 0.001     # 交易手续费
    SLIPPAGE = 0.0001      # 滑点
    
    # 风险管理
    MAX_POSITION_SIZE = 0.05  # 最大单笔头寸 5%
    STOP_LOSS = -0.05         # 止损 -5%
    TAKE_PROFIT = 0.10        # 止盈 10%
    
    # 数据配置
    DATA_SOURCE = "akshare"  # 数据源
    CACHE_DIR = "data/cache"
    
    # 模拟交易配置
    SIMULATION_MODE = True   # 是否使用模拟交易
```

---

### 📍 Phase 2: 策略引擎开发（第2-3周）

#### Step 2.1: 基础策略类

```python
# quant/strategies/base_strategy.py

from abc import ABC, abstractmethod
from typing import Dict, List
import pandas as pd

class BaseStrategy(ABC):
    """策略基类"""
    
    def __init__(self, name: str, params: Dict = None):
        self.name = name
        self.params = params or {}
        self.data = None
        self.signals = None
    
    def load_data(self, ticker: str, start_date: str, end_date: str):
        """加载股票数据"""
        pass
    
    @abstractmethod
    def generate_signals(self) -> pd.DataFrame:
        """生成交易信号 (必须实现)
        
        Returns:
            DataFrame 包含列: date, signal (-1/0/1), price, timestamp
        """
        pass
    
    def calculate_indicators(self):
        """计算技术指标"""
        pass
    
    def validate_signals(self):
        """验证信号合理性"""
        pass


# quant/strategies/ma_strategy.py
class MovingAverageStrategy(BaseStrategy):
    """均线交叉策略"""
    
    def __init__(self, fast_window=5, slow_window=20):
        super().__init__("MA_Strategy")
        self.fast_window = fast_window
        self.slow_window = slow_window
    
    def generate_signals(self) -> pd.DataFrame:
        """
        规则:
        - 快速MA > 慢速MA: 买入信号 (1)
        - 快速MA < 慢速MA: 卖出信号 (-1)
        - 其他: 无信号 (0)
        """
        self.data['ma_fast'] = self.data['close'].rolling(self.fast_window).mean()
        self.data['ma_slow'] = self.data['close'].rolling(self.slow_window).mean()
        
        self.data['signal'] = 0
        self.data.loc[self.data['ma_fast'] > self.data['ma_slow'], 'signal'] = 1
        self.data.loc[self.data['ma_fast'] < self.data['ma_slow'], 'signal'] = -1
        
        return self.data[['signal', 'close']]


# quant/strategies/rsi_strategy.py
class RSIStrategy(BaseStrategy):
    """RSI 超买超卖策略"""
    
    def __init__(self, period=14, overbought=70, oversold=30):
        super().__init__("RSI_Strategy")
        self.period = period
        self.overbought = overbought
        self.oversold = oversold
    
    def generate_signals(self) -> pd.DataFrame:
        """
        规则:
        - RSI < 30: 超卖，买入信号 (1)
        - RSI > 70: 超买，卖出信号 (-1)
        - 其他: 无信号 (0)
        """
        import pandas_ta as ta
        
        self.data['rsi'] = ta.rsi(self.data['close'], length=self.period)
        
        self.data['signal'] = 0
        self.data.loc[self.data['rsi'] < self.oversold, 'signal'] = 1
        self.data.loc[self.data['rsi'] > self.overbought, 'signal'] = -1
        
        return self.data[['signal', 'rsi']]
```

#### Step 2.2: 技术指标库

```python
# quant/data/indicators.py

import pandas as pd
import pandas_ta as ta
import numpy as np

class TechnicalIndicators:
    """技术指标集合"""
    
    @staticmethod
    def calculate_all(data: pd.DataFrame) -> pd.DataFrame:
        """计算所有技术指标"""
        
        # 趋势指标
        data['ma5'] = ta.sma(data['close'], length=5)
        data['ma10'] = ta.sma(data['close'], length=10)
        data['ma20'] = ta.sma(data['close'], length=20)
        data['ma50'] = ta.sma(data['close'], length=50)
        
        # 动量指标
        data['rsi'] = ta.rsi(data['close'], length=14)
        data['macd'] = ta.macd(data['close'])
        data['stoch'] = ta.stoch(data['high'], data['low'], data['close'])
        
        # 波动率指标
        data['atr'] = ta.atr(data['high'], data['low'], data['close'])
        data['bollinger'] = ta.bbands(data['close'])
        
        # 成交量指标
        data['volume_ma'] = ta.sma(data['volume'], length=20)
        data['obv'] = ta.obv(data['close'], data['volume'])
        
        return data
```

---

### 📍 Phase 3: 回测引擎开发（第3-4周）

#### Step 3.1: 回测核心

```python
# quant/backtest/backtest_engine.py

from typing import List, Dict
import pandas as pd
import numpy as np
from datetime import datetime

class BacktestEngine:
    """回测引擎"""
    
    def __init__(self, strategy, initial_cash=100000, commission=0.001):
        self.strategy = strategy
        self.initial_cash = initial_cash
        self.current_cash = initial_cash
        self.commission = commission
        self.position = 0  # 持仓数量
        self.trades = []   # 交易记录
        self.equity_curve = []  # 权益曲线
    
    def run(self, data: pd.DataFrame) -> Dict:
        """运行回测
        
        Args:
            data: OHLCV 数据
            
        Returns:
            回测结果字典
        """
        self.strategy.data = data
        signals = self.strategy.generate_signals()
        
        # 逐日处理
        for idx, row in data.iterrows():
            signal = signals.loc[idx, 'signal']
            price = row['close']
            
            # 根据信号执行交易
            if signal == 1 and self.position == 0:  # 买入信号
                self._buy(price, idx)
            elif signal == -1 and self.position > 0:  # 卖出信号
                self._sell(price, idx)
            
            # 记录权益
            current_equity = self.current_cash + self.position * price
            self.equity_curve.append(current_equity)
        
        return self._calculate_metrics()
    
    def _buy(self, price, date):
        """买入"""
        size = int(self.current_cash * 0.9 / price)  # 用 90% 资金
        cost = size * price * (1 + self.commission)
        
        self.current_cash -= cost
        self.position += size
        self.trades.append({
            'date': date,
            'type': 'BUY',
            'price': price,
            'size': size
        })
    
    def _sell(self, price, date):
        """卖出"""
        proceeds = self.position * price * (1 - self.commission)
        
        self.current_cash += proceeds
        self.position = 0
        self.trades.append({
            'date': date,
            'type': 'SELL',
            'price': price,
            'size': self.position
        })
    
    def _calculate_metrics(self) -> Dict:
        """计算性能指标"""
        equity = pd.Series(self.equity_curve)
        returns = equity.pct_change()
        
        metrics = {
            'total_return': (equity.iloc[-1] - self.initial_cash) / self.initial_cash,
            'sharpe_ratio': returns.mean() / returns.std() * np.sqrt(252),
            'max_drawdown': self._calculate_max_drawdown(),
            'win_rate': self._calculate_win_rate(),
            'trades_count': len(self.trades),
            'final_equity': equity.iloc[-1]
        }
        
        return metrics
    
    def _calculate_max_drawdown(self) -> float:
        """计算最大回撤"""
        equity = pd.Series(self.equity_curve)
        running_max = equity.expanding().max()
        drawdown = (equity - running_max) / running_max
        return drawdown.min()
    
    def _calculate_win_rate(self) -> float:
        """计算胜率"""
        if len(self.trades) < 2:
            return 0
        
        win_count = 0
        for i in range(0, len(self.trades), 2):
            if i + 1 < len(self.trades):
                buy_price = self.trades[i]['price']
                sell_price = self.trades[i + 1]['price']
                if sell_price > buy_price:
                    win_count += 1
        
        return win_count / (len(self.trades) // 2) if len(self.trades) > 0 else 0


# quant/backtest/metrics.py
class PerformanceMetrics:
    """性能指标计算"""
    
    @staticmethod
    def calculate_all(returns: pd.Series, trades: List[Dict]) -> Dict:
        """计算所有性能指标"""
        return {
            'annual_return': returns.mean() * 252,
            'sharpe_ratio': returns.mean() / returns.std() * np.sqrt(252),
            'sortino_ratio': returns.mean() / returns[returns < 0].std() * np.sqrt(252),
            'calmar_ratio': returns.mean() / abs(PerformanceMetrics._max_drawdown(returns)),
            'max_drawdown': PerformanceMetrics._max_drawdown(returns),
            'win_rate': PerformanceMetrics._win_rate(trades),
            'profit_factor': PerformanceMetrics._profit_factor(trades),
            'average_trade': PerformanceMetrics._average_trade(trades),
        }
    
    @staticmethod
    def _max_drawdown(returns: pd.Series) -> float:
        """最大回撤"""
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        return drawdown.min()
    
    # ... 其他指标方法
```

---

### 📍 Phase 4: 风险管理与执行引擎（第4-5周）

#### Step 4.1: 风险管理

```python
# quant/risk/position.py

class PositionManager:
    """持仓管理"""
    
    def __init__(self, max_position_size=0.05, stop_loss=-0.05, take_profit=0.10):
        self.max_position_size = max_position_size
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.positions = {}  # {ticker: position_info}
    
    def open_position(self, ticker: str, size: int, entry_price: float):
        """开仓"""
        self.positions[ticker] = {
            'size': size,
            'entry_price': entry_price,
            'current_price': entry_price,
            'pnl': 0,
            'pnl_pct': 0
        }
    
    def close_position(self, ticker: str, exit_price: float):
        """平仓"""
        if ticker in self.positions:
            pos = self.positions[ticker]
            pos['current_price'] = exit_price
            pos['pnl'] = (exit_price - pos['entry_price']) * pos['size']
            pos['pnl_pct'] = pos['pnl'] / (pos['entry_price'] * pos['size'])
            del self.positions[ticker]
    
    def check_stop_loss(self, ticker: str, current_price: float) -> bool:
        """检查止损"""
        if ticker not in self.positions:
            return False
        
        pos = self.positions[ticker]
        pnl_pct = (current_price - pos['entry_price']) / pos['entry_price']
        
        return pnl_pct < self.stop_loss
    
    def check_take_profit(self, ticker: str, current_price: float) -> bool:
        """检查止盈"""
        if ticker not in self.positions:
            return False
        
        pos = self.positions[ticker]
        pnl_pct = (current_price - pos['entry_price']) / pos['entry_price']
        
        return pnl_pct > self.take_profit


# quant/risk/portfolio.py
class Portfolio:
    """投资组合管理"""
    
    def __init__(self, initial_cash: float):
        self.cash = initial_cash
        self.positions = {}
        self.trades = []
    
    def get_total_value(self, market_prices: Dict[str, float]) -> float:
        """获取总资产价值"""
        stock_value = sum(
            self.positions.get(ticker, 0) * price
            for ticker, price in market_prices.items()
        )
        return self.cash + stock_value
    
    def calculate_allocation(self) -> Dict[str, float]:
        """计算资产配置"""
        total = self.get_total_value({})
        return {
            ticker: (size * 100 / total) if total > 0 else 0
            for ticker, size in self.positions.items()
        }
```

#### Step 4.2: 执行引擎

```python
# quant/execution/simulator.py

class SimulationExecutor:
    """模拟交易执行器"""
    
    def __init__(self, initial_cash=100000, commission=0.001):
        self.initial_cash = initial_cash
        self.commission = commission
        self.portfolio = Portfolio(initial_cash)
        self.order_book = []
    
    def submit_order(self, ticker: str, side: str, price: float, quantity: int):
        """提交订单 (side: 'BUY' / 'SELL')"""
        order = {
            'ticker': ticker,
            'side': side,
            'price': price,
            'quantity': quantity,
            'timestamp': datetime.now()
        }
        
        # 模拟成交
        if side == 'BUY':
            cost = price * quantity * (1 + self.commission)
            if self.portfolio.cash >= cost:
                self.portfolio.cash -= cost
                self.portfolio.positions[ticker] = \
                    self.portfolio.positions.get(ticker, 0) + quantity
                order['status'] = 'FILLED'
            else:
                order['status'] = 'REJECTED'
        
        elif side == 'SELL':
            if self.portfolio.positions.get(ticker, 0) >= quantity:
                proceeds = price * quantity * (1 - self.commission)
                self.portfolio.cash += proceeds
                self.portfolio.positions[ticker] -= quantity
                order['status'] = 'FILLED'
            else:
                order['status'] = 'REJECTED'
        
        self.order_book.append(order)
        return order
```

---

### 📍 Phase 5: API 接口与前端集成（第5-6周）

#### Step 5.1: FastAPI 路由

```python
# quant_api/strategy_routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/strategy", tags=["策略管理"])

class StrategyRequest(BaseModel):
    name: str
    strategy_type: str  # "ma", "rsi", "combined"
    params: Dict = {}

@router.post("/create")
async def create_strategy(request: StrategyRequest):
    """创建交易策略"""
    try:
        if request.strategy_type == "ma":
            strategy = MovingAverageStrategy(**request.params)
        elif request.strategy_type == "rsi":
            strategy = RSIStrategy(**request.params)
        else:
            raise HTTPException(status_code=400, detail="未知策略类型")
        
        # 保存到数据库
        return {
            'status': 'success',
            'strategy_id': save_strategy(strategy),
            'message': '策略创建成功'
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
async def list_strategies():
    """获取所有策略列表"""
    strategies = get_all_strategies()
    return {
        'status': 'success',
        'data': strategies
    }


# quant_api/backtest_routes.py

@router.post("/run")
async def run_backtest(
    strategy_id: str,
    ticker: str,
    start_date: str,
    end_date: str
):
    """运行回测"""
    try:
        strategy = load_strategy(strategy_id)
        
        # 加载数据
        from data.stock_data import StockDataProvider
        provider = StockDataProvider()
        data = provider.get_daily_data(ticker, start_date, end_date)
        
        # 运行回测
        engine = BacktestEngine(strategy)
        results = engine.run(data)
        
        # 保存回测结果
        backtest_id = save_backtest_result(strategy_id, ticker, results)
        
        return {
            'status': 'success',
            'backtest_id': backtest_id,
            'metrics': results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/results/{backtest_id}")
async def get_backtest_results(backtest_id: str):
    """获取回测结果"""
    results = load_backtest_result(backtest_id)
    return {
        'status': 'success',
        'data': results
    }
```

#### Step 5.2: 前端页面 (Vue3)

```vue
<!-- front/components/QuantTrading.vue -->

<template>
  <div class="quant-trading">
    <!-- 策略配置 -->
    <el-card class="strategy-card">
      <template #header>
        <div class="card-header">
          <span>量化交易策略</span>
          <el-button @click="showStrategyDialog = true">新建策略</el-button>
        </div>
      </template>

      <!-- 策略列表 -->
      <el-table :data="strategies" stripe>
        <el-table-column prop="name" label="策略名称" />
        <el-table-column prop="type" label="策略类型" />
        <el-table-column prop="created_at" label="创建时间" />
        <el-table-column label="操作">
          <template #default="scope">
            <el-button @click="editStrategy(scope.row)">编辑</el-button>
            <el-button @click="deleteStrategy(scope.row.id)">删除</el-button>
            <el-button @click="runBacktest(scope.row)">回测</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 回测结果 -->
    <el-card class="backtest-card" v-if="backtestResults">
      <template #header>
        <span>回测结果分析</span>
      </template>

      <!-- 性能指标 -->
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="metric-card">
            <div class="metric-label">总收益率</div>
            <div class="metric-value" :class="{ positive: backtestResults.total_return > 0 }">
              {{ (backtestResults.total_return * 100).toFixed(2) }}%
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="metric-card">
            <div class="metric-label">夏普比率</div>
            <div class="metric-value">{{ backtestResults.sharpe_ratio.toFixed(2) }}</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="metric-card">
            <div class="metric-label">最大回撤</div>
            <div class="metric-value negative">{{ (backtestResults.max_drawdown * 100).toFixed(2) }}%</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="metric-card">
            <div class="metric-label">胜率</div>
            <div class="metric-value">{{ (backtestResults.win_rate * 100).toFixed(2) }}%</div>
          </div>
        </el-col>
      </el-row>

      <!-- 权益曲线图表 -->
      <div id="equityChart" style="width: 100%; height: 400px; margin-top: 20px;"></div>
    </el-card>

    <!-- 实时交易 (模拟或实盘) -->
    <el-card class="trading-card">
      <template #header>
        <span>交易执行</span>
      </template>

      <el-form :model="tradeForm" label-width="100px">
        <el-form-item label="证券代码">
          <el-input v-model="tradeForm.ticker" placeholder="如: 300748" />
        </el-form-item>
        <el-form-item label="交易方向">
          <el-select v-model="tradeForm.direction">
            <el-option label="买入" value="BUY" />
            <el-option label="卖出" value="SELL" />
          </el-select>
        </el-form-item>
        <el-form-item label="数量">
          <el-input-number v-model="tradeForm.quantity" />
        </el-form-item>
        <el-button @click="submitTrade">提交订单</el-button>
      </el-form>

      <!-- 交易记录 -->
      <el-table :data="trades" stripe style="margin-top: 20px;">
        <el-table-column prop="ticker" label="证券代码" />
        <el-table-column prop="direction" label="方向" />
        <el-table-column prop="quantity" label="数量" />
        <el-table-column prop="price" label="价格" />
        <el-table-column prop="timestamp" label="时间" />
        <el-table-column prop="status" label="状态" />
      </el-table>
    </el-card>

    <!-- 账户信息 -->
    <el-card class="portfolio-card">
      <template #header>
        <span>账户信息</span>
      </template>

      <el-row :gutter="20">
        <el-col :span="8">
          <div class="info-card">
            <div class="info-label">总资产</div>
            <div class="info-value">¥ {{ totalAssets.toFixed(2) }}</div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="info-card">
            <div class="info-label">可用现金</div>
            <div class="info-value">¥ {{ availableCash.toFixed(2) }}</div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="info-card">
            <div class="info-label">持仓市值</div>
            <div class="info-value">¥ {{ positionValue.toFixed(2) }}</div>
          </div>
        </el-col>
      </el-row>

      <!-- 持仓明细 -->
      <el-table :data="positions" stripe style="margin-top: 20px;">
        <el-table-column prop="ticker" label="证券代码" />
        <el-table-column prop="quantity" label="持仓数量" />
        <el-table-column prop="cost_price" label="成本价" />
        <el-table-column prop="current_price" label="现价" />
        <el-table-column prop="pnl" label="盈亏" />
        <el-table-column prop="pnl_pct" label="盈亏率" />
      </el-table>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'QuantTrading',
  data() {
    return {
      strategies: [],
      backtestResults: null,
      trades: [],
      positions: [],
      totalAssets: 0,
      availableCash: 0,
      positionValue: 0,
      tradeForm: {
        ticker: '',
        direction: 'BUY',
        quantity: 100
      },
      showStrategyDialog: false
    }
  },
  mounted() {
    this.loadStrategies()
    this.loadPortfolio()
  },
  methods: {
    async loadStrategies() {
      // 调用 API
      const response = await fetch('/api/strategy/list')
      this.strategies = response.data
    },
    async runBacktest(strategy) {
      // 调用回测 API
      const response = await fetch('/api/backtest/run', {
        method: 'POST',
        body: JSON.stringify({
          strategy_id: strategy.id,
          ticker: '300748',
          start_date: '2023-01-01',
          end_date: '2024-01-01'
        })
      })
      this.backtestResults = response.data.metrics
    },
    async submitTrade() {
      // 调用交易 API
      const response = await fetch('/api/trade/submit', {
        method: 'POST',
        body: JSON.stringify(this.tradeForm)
      })
      // 刷新交易记录
      this.loadTrades()
    },
    async loadPortfolio() {
      // 加载账户信息
      const response = await fetch('/api/portfolio/info')
      const data = response.data
      this.totalAssets = data.total_value
      this.availableCash = data.cash
      this.positionValue = data.position_value
      this.positions = data.positions
    }
  }
}
</script>

<style scoped>
.quant-trading {
  padding: 20px;
}

.strategy-card, .backtest-card, .trading-card, .portfolio-card {
  margin-bottom: 20px;
}

.metric-card, .info-card {
  background: #f5f7fa;
  padding: 20px;
  border-radius: 4px;
  text-align: center;
}

.metric-label, .info-label {
  color: #909399;
  font-size: 12px;
  margin-bottom: 10px;
}

.metric-value, .info-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.metric-value.positive {
  color: #67c23a;
}

.metric-value.negative {
  color: #f56c6c;
}
</style>
```

---

## 🔗 数据源与交易接口选择

### 选项 1: 完全免费方案（推荐新手）

```
数据源:
├── akshare          ✓ A股数据、基金、期货、加密等
├── baostock         ✓ 历史行情、基本面数据
├── tushare          ✓ 行情、财务数据（需免费注册）
└── yfinance         ✓ 国际股票数据

交易模拟:
├── 内置 SimulationExecutor  ✓ 完全模拟
├── backtrader              ✓ 专业回测框架
└── vnpy                    ✓ 国内量化交易框架
```

### 选项 2: 半专业方案（支持模拟交易）

```
数据源:
├── Wind 数据库      ✓ 专业金融数据
└── 同花顺 SDK       ✓ 实时行情

交易接口:
├── 华泰 TradeAPI    ✓ 支持模拟交易
├── 华宝 TradeAPI    ✓ 支持模拟交易
└── 雪球虚拟交易     ✓ 完全模拟交易
```

### 选项 3: 完全实盘方案（需开户）

```
交易接口:
├── 华泰客户端 API        ✓ 支持自动化交易
├── 东方财富通达信 API   ⚠️ 限制较多
├── 中泰 XTP 接口        ✓ 机构级别
└── 恒生 HOMS 系统       ✓ 港股交易
```

**推荐开户券商**:

- 华泰证券（API完整，支持模拟）
- 同花顺（专业版支持自动化）
- 国泰君安（API较完整）

---

## 📦 依赖库完整清单

```bash
# 核心库
pip install fastapi uvicorn  # Web 框架
pip install pandas numpy     # 数据处理
pip install sqlalchemy       # ORM 数据库

# 量化库
pip install backtrader       # 回测框架
pip install vectorbt         # 向量化回测
pip install ta-lib           # 技术指标
pip install pandas-ta        # Pandas 技术指标

# 金融数据
pip install akshare          # A股数据
pip install baostock         # 历史数据
pip install tushare          # 专业数据
pip install yfinance         # 国际股票

# 分析工具
pip install pyfolio          # 投资组合分析
pip install numpy-financial  # 财务计算
pip install scikit-learn     # 机器学习（可选）

# 交易接口（可选）
pip install easytrader       # 自动化交易
pip install vnpy             # 国内量化框架
pip install ccxt             # 加密货币交易
```

---

## 🚀 快速启动检查清单

### Week 1-2: 基础搭建

- [ ] 创建项目目录结构
- [ ] 安装依赖库
- [ ] 创建配置文件
- [ ] 实现基础策略类

### Week 3-4: 策略与回测

- [ ] 实现均线策略
- [ ] 实现 RSI 策略
- [ ] 完成回测引擎
- [ ] 计算性能指标

### Week 5: 风险与执行

- [ ] 实现持仓管理
- [ ] 实现模拟交易
- [ ] 实现止损止盈
- [ ] 整合到 API

### Week 6: 前端集成

- [ ] 创建策略管理页面
- [ ] 创建回测结果页面
- [ ] 创建交易执行页面
- [ ] 创建账户管理页面

---

## ⚡ 优先级建议

### 第一优先级（必做）

1. ✅ 基础策略框架 (MA, RSI)
2. ✅ 回测引擎
3. ✅ 模拟交易执行
4. ✅ 前端展示页面

### 第二优先级（建议做）

1. ✅ 风险管理（止损止盈）
2. ✅ 更多技术指标
3. ✅ 策略参数优化
4. ✅ 多股票组合

### 第三优先级（扩展功能）

1. ✅ 机器学习信号
2. ✅ 期权交易
3. ✅ 实盘交易接口
4. ✅ 风险管理系统

---

## 📚 学习资源推荐

### 书籍

- 《Python 金融数据分析》
- 《量化交易》Ernie Chan
- 《系统交易方法》Perry Kaufman

### 在线课程

- Coursera: Financial Markets
- 网易云课堂: 量化交易系列

### 开源项目

- backtrader: <https://github.com/backtrader/backtrader>
- vnpy: <https://github.com/vnpy/vnpy>
- zipline: <https://github.com/quantopian/zipline>

---

## 🎯 成功标志

当你完成以下任务时，说明量化交易模块已经就绪：

✅ 能运行至少 3 种策略的回测
✅ 能生成完整的性能报告（夏普比率、最大回撤等）
✅ 能在前端配置策略并查看回测结果
✅ 能执行模拟交易并追踪账户变化
✅ 能处理风险管理（止损止盈）
✅ 能导出交易记录和性能分析

---

## 💡 常见问题

### Q: 如何选择数据源？

A: 推荐 akshare + baostock 组合

- akshare: 实时和准实时数据
- baostock: 长期历史数据

### Q: 可以用东方财富 API 吗？

A: 东方财富官方 API 较少，但可以通过以下方式：

- 爬取东方财富网站数据
- 使用 easytrader 自动化交易
- 使用专业 API（同花顺、Wind 等）

### Q: 模拟交易可以用真实数据吗？

A: 可以，使用 akshare 或 baostock 获取历史数据进行回测

### Q: 多久能完成？

A: 专职开发约 4-6 周，兼职约 8-12 周

### Q: 需要金融背景吗？

A: 不需要，本方案涵盖所有基础知识
