# 配置说明

## 环境变量配置

请创建 `.env` 文件（可以复制 `.env.example` 并重命名），并填入以下配置：

### MongoDB 配置

根据你提供的配置信息，MongoDB 配置如下：

```env
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_USERNAME=chloe
MONGODB_PASSWORD=q1w2e3@2026
MONGODB_DATABASE=tradingagents
MONGODB_AUTH_SOURCE=admin
```

### DeepSeek API 配置

```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_TEMPERATURE=0.1
DEEPSEEK_MAX_TOKENS=
```

**配置说明**：
- `DEEPSEEK_API_KEY`: DeepSeek API 密钥（必填）
- `DEEPSEEK_BASE_URL`: API 基础 URL（可选，默认：https://api.deepseek.com）
- `DEEPSEEK_MODEL`: 模型名称（可选，默认：deepseek-chat）
  - 可用模型：
    - `deepseek-chat`: 通用对话模型（推荐，最稳定）
    - `deepseek-coder`: 代码专用模型
    - `deepseek-reasoner`: 推理模型（可能需要特殊权限）
- `DEEPSEEK_TEMPERATURE`: 温度参数，控制输出的随机性（可选，默认：0.1）
- `DEEPSEEK_MAX_TOKENS`: 最大 token 数（可选，不设置则使用模型默认值）

**注意**：如果遇到 "model not found" 错误，请尝试使用 `deepseek-chat` 模型。

**重要**：请将 `your_deepseek_api_key_here` 替换为你的实际 DeepSeek API Key。

### 分析配置（可选）

```env
DEFAULT_RESEARCH_DEPTH=3
DEFAULT_MARKET=A股
ONLINE_TOOLS_ENABLED=true
REALTIME_DATA_ENABLED=false
```

## 快速开始

1. 复制配置模板：
   ```bash
   # Windows PowerShell
   Copy-Item .env.example .env
   
   # Linux/Mac
   cp .env.example .env
   ```

2. 编辑 `.env` 文件，填入你的 DeepSeek API Key

3. 确保 MongoDB 服务正在运行

4. 运行分析：
   ```bash
   python main.py --ticker 300748 --date 2026-01-16
   ```

