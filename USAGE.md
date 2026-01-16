# 使用指南

## 快速开始

### 1. 准备工作

确保你已经：
- ✅ 安装了 Python 3.10+
- ✅ 安装了 MongoDB 并正在运行
- ✅ 获取了 DeepSeek API Key

### 2. 安装依赖

```bash
cd tradingMiniAgents
pip install -r requirements.txt
```

### 3. 配置环境变量

创建 `.env` 文件（可以复制 `.env.example`）：

```env
# MongoDB 配置
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_USERNAME=chloe
MONGODB_PASSWORD=q1w2e3@2026
MONGODB_DATABASE=tradingagents
MONGODB_AUTH_SOURCE=admin

# DeepSeek API 配置
DEEPSEEK_API_KEY=你的DeepSeek_API_Key
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

**重要**：将 `你的DeepSeek_API_Key` 替换为你的实际 API Key。

### 4. 启动服务

#### 方式一：一键启动（推荐）

```bash
python start_server.py
```

这将自动：
- 启动后端 API 服务器（端口 8001）
- 启动前端页面服务器（端口 8080）
- 自动打开浏览器

#### 方式二：分别启动

**启动后端**：
```bash
python api_server.py
```

**启动前端**（新开一个终端）：
```bash
cd front
python -m http.server 8080
```

然后在浏览器中打开：http://localhost:8080

## Web 界面使用

### 界面说明

1. **选择市场**：下拉选择 A股/港股/美股
2. **股票代码**：输入要分析的股票代码（如：300748）
3. **分析日期**：选择分析日期（默认今天）
4. **研究深度**：拖动滑块选择 1-5 级（默认 3 级）
5. **选择分析师**：勾选要使用的分析师
   - 市场分析师：技术分析
   - 基本面分析师：财务分析
6. **开始分析**：点击按钮开始分析

### 分析结果

分析完成后，结果会显示在页面下方：
- 每个分析师的报告单独显示
- 如果有图片分析，也会显示

## 命令行使用

### 基本用法

```bash
python main.py --ticker 300748 --date 2026-01-16 --market A股
```

### 参数说明

| 参数 | 说明 | 必需 | 默认值 |
|------|------|------|--------|
| `--ticker` | 股票代码 | ✅ | - |
| `--date` | 分析日期 (YYYY-MM-DD) | ❌ | 今天 |
| `--market` | 市场类型 | ❌ | A股 |
| `--analysts` | 分析师列表 | ❌ | market,fundamentals |
| `--image` | 图片路径 | ❌ | - |
| `--depth` | 研究深度 (1-5) | ❌ | 3 |

### 使用示例

```bash
# 基本分析
python main.py --ticker 300748 --date 2026-01-16

# 仅使用市场分析师
python main.py --ticker 300748 --date 2026-01-16 --analysts market

# 仅使用基本面分析师
python main.py --ticker 300748 --date 2026-01-16 --analysts fundamentals

# 分析图片
python main.py --ticker 300748 --date 2026-01-16 --image ./image.png

# 深度分析（5级）
python main.py --ticker 300748 --date 2026-01-16 --depth 5
```

## API 使用

### 分析接口

```bash
curl -X POST "http://localhost:8001/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "300748",
    "date": "2026-01-16",
    "market": "A股",
    "analysts": ["market", "fundamentals"],
  