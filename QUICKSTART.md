# 快速开始指南

## 1. 安装依赖

```bash
pip install -r requirements.txt
```

## 2. 配置环境变量

### 方法一：手动创建 .env 文件

创建 `.env` 文件，内容如下：

```env
# MongoDB 配置
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_USERNAME=chloe
MONGODB_PASSWORD=q1w2e3@2026
MONGODB_DATABASE=tradingagents
MONGODB_AUTH_SOURCE=admin

# DeepSeek API 配置
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com

# 分析配置
DEFAULT_RESEARCH_DEPTH=3
DEFAULT_MARKET=A股
ONLINE_TOOLS_ENABLED=true
REALTIME_DATA_ENABLED=false
```

**重要**：将 `your_deepseek_api_key_here` 替换为你的实际 DeepSeek API Key。

### 方法二：使用模板

如果有 `.env.example` 文件，可以复制它：

```bash
# Windows PowerShell
Copy-Item .env.example .env

# Linux/Mac
cp .env.example .env
```

然后编辑 `.env` 文件，填入你的 DeepSeek API Key。

## 3. 确保 MongoDB 运行

确保 MongoDB 服务正在运行，并且配置的用户名和密码正确。

## 4. 运行分析

### 基本用法

```bash
python main.py --ticker 300748 --date 2026-01-16 --market A股
```

### 指定分析师

```bash
# 仅使用市场分析师
python main.py --ticker 300748 --date 2026-01-16 --analysts market

# 仅使用基本面分析师
python main.py --ticker 300748 --date 2026-01-16 --analysts fundamentals

# 使用所有分析师（默认）
python main.py --ticker 300748 --date 2026-01-16 --analysts market,fundamentals
```

### 分析图片

```bash
python main.py --ticker 300748 --date 2026-01-16 --image path/to/image.png
```

### 设置研究深度

```bash
python main.py --ticker 300748 --date 2026-01-16 --depth 5
```

## 5. 查看结果

分析结果会：
1. 在控制台输出
2. 自动保存到 MongoDB 数据库（如果连接成功）

## 常见问题

### 1. DeepSeek API Key 错误

如果看到 "DEEPSEEK_API_KEY 未设置" 错误，请检查：
- `.env` 文件是否存在
- `DEEPSEEK_API_KEY` 是否已正确配置
- API Key 是否有效

### 2. MongoDB 连接失败

如果 MongoDB 连接失败，请检查：
- MongoDB 服务是否正在运行
- 用户名和密码是否正确
- 端口是否正确（默认 27017）
- 防火墙设置

### 3. 股票数据获取失败

如果股票数据获取失败，可能原因：
- 股票代码不正确
- 网络连接问题
- 数据源 API 限制

## 示例代码

也可以使用 Python 代码直接调用：

```python
from core.llm_client import DeepSeekClient
from core.analyst import AnalystManager
from data.stock_data import StockDataProvider

# 初始化
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

# 查看结果
for analyst_name, report in reports.items():
    print(f"{analyst_name}: {report}")
```

## 更多信息

- 详细配置说明：查看 `CONFIG.md`
- 项目文档：查看 `README.md`

