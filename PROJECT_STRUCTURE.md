# 项目结构说明

## 目录结构

```
tradingMiniAgents/
├── .env                    # 环境配置文件（需要手动创建）
├── .env.example            # 环境配置模板
├── .gitignore              # Git 忽略文件
├── main.py                 # 主程序入口
├── example.py              # 使用示例
├── requirements.txt        # Python 依赖
├── README.md               # 项目说明
├── CONFIG.md               # 配置说明
├── QUICKSTART.md           # 快速开始指南
├── PROJECT_STRUCTURE.md    # 本文件
│
├── core/                   # 核心模块
│   ├── __init__.py
│   ├── llm_client.py      # DeepSeek LLM 客户端
│   ├── analyst.py         # 分析师模块（市场分析师、基本面分析师）
│   └── image_analyzer.py  # 图片分析模块
│
├── data/                   # 数据源模块
│   ├── __init__.py
│   └── stock_data.py      # 股票数据获取（支持 A股/港股/美股）
│
└── storage/                # 存储模块
    ├── __init__.py
    └── mongodb.py          # MongoDB 存储管理器
```

## 核心模块说明

### 1. core/llm_client.py
- **DeepSeekClient**: DeepSeek LLM 客户端封装
- 支持调用 DeepSeek API 进行文本分析
- 自动从环境变量读取配置

### 2. core/analyst.py
- **MarketAnalyst**: 市场分析师
  - 分析价格趋势
  - 技术指标分析
  - 成交量分析
- **FundamentalsAnalyst**: 基本面分析师
  - 财务状况评估
  - 估值分析
  - 盈利能力分析
- **AnalystManager**: 分析师管理器
  - 统一管理多个分析师
  - 支持选择性使用分析师

### 3. core/image_analyzer.py
- **ImageAnalyzer**: 图片分析器
- 支持分析股票相关图片
- 提取图片中的关键信息用于分析

### 4. data/stock_data.py
- **StockDataProvider**: 股票数据提供者
- 支持 A股、港股、美股数据获取
- 使用 akshare、yfinance 等数据源

### 5. storage/mongodb.py
- **MongoDBStorage**: MongoDB 存储管理器
- 自动保存分析结果
- 支持查询历史分析记录
- 自动创建索引优化查询

## 数据流

```
用户输入 (股票代码、日期、市场)
    ↓
main.py (主程序)
    ↓
AnalystManager (分析师管理器)
    ↓
├── MarketAnalyst → DeepSeekClient → DeepSeek API
└── FundamentalsAnalyst → DeepSeekClient → DeepSeek API
    ↓
StockDataProvider (获取股票数据)
    ↓
分析结果
    ↓
MongoDBStorage (保存到数据库)
```

## 配置说明

### 必需配置
- `DEEPSEEK_API_KEY`: DeepSeek API 密钥
- `MONGODB_*`: MongoDB 连接配置

### 可选配置
- `DEFAULT_RESEARCH_DEPTH`: 默认研究深度
- `DEFAULT_MARKET`: 默认市场
- `ONLINE_TOOLS_ENABLED`: 是否启用在线工具

## 使用方式

### CLI 方式
```bash
python main.py --ticker 300748 --date 2026-01-16 --market A股
```

### Python 代码方式
```python
from core.analyst import AnalystManager
from core.llm_client import DeepSeekClient
from data.stock_data import StockDataProvider

# 初始化并分析
```

## 扩展说明

### 添加新的分析师
1. 在 `core/analyst.py` 中创建新的分析师类
2. 继承基础分析逻辑
3. 在 `AnalystManager` 中注册

### 添加新的数据源
1. 在 `data/stock_data.py` 中添加新的数据获取方法
2. 更新 `StockDataProvider` 类

### 修改存储方式
1. 在 `storage/` 目录下创建新的存储类
2. 实现相同的接口方法
3. 在 `main.py` 中替换存储实例

