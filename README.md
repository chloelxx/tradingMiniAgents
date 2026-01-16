# TradingMiniAgents - 简化版股票分析智能体

一个简洁的股票分析智能体系统，专注于提供核心的股票分析能力。支持 Web 界面和命令行两种使用方式。

## 功能特性

- ✅ **股票分析**：支持市场分析师和基本面分析师
- ✅ **DeepSeek 模型**：默认使用 DeepSeek 模型进行分析
- ✅ **图片分析**：支持分析股票相关图片
- ✅ **MongoDB 存储**：自动保存分析结果到 MongoDB
- ✅ **Web 界面**：现代化的前端界面，支持可视化操作
- ✅ **简洁设计**：去除复杂功能，专注核心分析能力

## 环境要求

- Python 3.10+
- MongoDB 数据库
- DeepSeek API Key

## 安装步骤

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置环境变量：
创建 `.env` 文件，填入你的配置：
- `DEEPSEEK_API_KEY`: DeepSeek API 密钥
- `MONGODB_*`: MongoDB 连接配置

详细配置说明请查看 `CONFIG.md`

## 使用方式

### 方式一：Web 界面（推荐）

1. 启动服务：
```bash
python start_server.py
```

2. 浏览器会自动打开，或手动访问：http://localhost:8080

3. 在界面中：
   - 选择市场（A股/港股/美股）
   - 输入股票代码
   - 选择分析日期
   - 调整研究深度（1-5级）
   - 选择分析师团队
   - 点击"开始分析"

### 方式二：命令行

```bash
python main.py --ticker 300748 --date 2026-01-16 --market A股
```

#### 命令行参数

- `--ticker`: 股票代码（必需）
- `--date`: 分析日期，格式 YYYY-MM-DD（可选，默认为今天）
- `--market`: 市场类型，A股/港股/美股（可选，默认 A股）
- `--analysts`: 要使用的分析师，用逗号分隔（可选，默认 market,fundamentals）
- `--image`: 要分析的图片路径（可选）
- `--depth`: 研究深度 1-5（可选，默认 3）

#### 使用示例

```bash
# 基本分析
python main.py --ticker 300748 --date 2026-01-16

# 指定分析师
python main.py --ticker 300748 --date 2026-01-16 --analysts market

# 分析图片
python main.py --ticker 300748 --date 2026-01-16 --image path/to/image.png
```

## 项目结构

```
tradingMiniAgents/
├── .env                 # 环境配置文件（需要手动创建）
├── main.py              # 命令行主程序
├── api_server.py        # 后端 API 服务器
├── start_server.py      # 启动脚本（同时启动前后端）
├── core/                # 核心模块
│   ├── llm_client.py   # LLM 客户端
│   ├── analyst.py      # 分析师模块
│   └── image_analyzer.py # 图片分析
├── data/                # 数据源
│   └── stock_data.py    # 股票数据获取
├── storage/             # 存储模块
│   └── mongodb.py       # MongoDB 存储
├── front/               # 前端页面
│   └── index.html      # Web 界面
└── requirements.txt     # 依赖列表
```

## API 接口

后端 API 运行在 `http://localhost:8001`

### 主要接口

- `GET /`: API 信息
- `GET /health`: 健康检查
- `POST /api/analyze`: 执行股票分析
- `GET /api/history`: 获取分析历史
- `GET /api/stock-info`: 获取股票信息

详细 API 文档：启动服务后访问 http://localhost:8001/docs

## 配置说明

### MongoDB 配置
- `MONGODB_HOST`: MongoDB 主机地址
- `MONGODB_PORT`: MongoDB 端口
- `MONGODB_USERNAME`: 用户名
- `MONGODB_PASSWORD`: 密码
- `MONGODB_DATABASE`: 数据库名称
- `MONGODB_AUTH_SOURCE`: 认证源

### DeepSeek 配置
- `DEEPSEEK_API_KEY`: API 密钥
- `DEEPSEEK_BASE_URL`: API 地址（默认：https://api.deepseek.com）

### API 配置（可选）
- `API_HOST`: API 服务器地址（默认：0.0.0.0）
- `API_PORT`: API 服务器端口（默认：8001）

## 快速开始

1. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

2. **配置环境**：
   - 复制 `.env.example` 为 `.env`
   - 填入你的 DeepSeek API Key

3. **启动服务**：
   ```bash
   python start_server.py
   ```

4. **开始分析**：
   - 在浏览器中打开 http://localhost:8080
   - 填写股票信息并点击"开始分析"

## 常见问题

### 1. DeepSeek API Key 错误
- 检查 `.env` 文件中的 `DEEPSEEK_API_KEY` 是否正确
- 确保 API Key 有效且有足够的余额

### 2. MongoDB 连接失败
- 检查 MongoDB 服务是否运行
- 验证用户名和密码是否正确
- 检查端口是否正确（默认 27017）

### 3. 前端无法连接后端
- 确保后端 API 服务器已启动（端口 8001）
- 检查浏览器控制台是否有错误信息
- 如果后端运行在不同端口，修改 `front/index.html` 中的 `apiBaseUrl`

### 4. 股票数据获取失败
- 检查股票代码是否正确
- 检查网络连接
- 某些数据源可能有访问限制

## 开发说明

### 添加新的分析师

1. 在 `core/analyst.py` 中创建新的分析师类
2. 在 `AnalystManager` 中注册
3. 在前端界面中添加选项

### 修改前端界面

编辑 `front/index.html`，使用 Vue 3 和 Element Plus 组件。

## 许可证

MIT License
