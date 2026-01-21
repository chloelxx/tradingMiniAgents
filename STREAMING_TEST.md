# 流式输出快速测试指南

## 🚀 快速开始

### 1. 启动后端服务
```bash
cd e:\tradingMiniAgents
python api_server.py
```

看到以下日志说明启动成功：
```
✅ DeepSeek 客户端初始化完成: model=deepseek-chat
✅ 数据提供者初始化完成
✅ 分析师管理器初始化完成
✅ 流式分析师管理器初始化完成
✅ MongoDB 存储初始化完成
🚀 启动 API 服务器: http://0.0.0.0:8001
```

### 2. 打开前端页面
访问：http://localhost:8001

### 3. 发起分析请求
1. 选择市场：**A股**
2. 输入股票代码：**300748** (或其他股票)
3. 选择日期：**2025-01-21**
4. 选择分析师：**市场分析师** + **基本面分析师**
5. 点击 **开始分析**

### 4. 观看流式效果
你会看到：
```
✨ 分析开始...
📊 市场分析师分析中...
[文本逐字出现...]
✅ 市场分析师 分析完成
📊  基本面分析师分析中...
[文本逐字出现...]
✅ 基本面分析师 分析完成
✨ 分析完成！
```

## 🔍 测试要点

### 流式效果验证
- [ ] 打开开发者工具（F12）
- [ ] 在 Network 选项卡查看请求
- [ ] 看到响应类型为 `text/event-stream`
- [ ] 在响应中看到多个 `data: ` 行

### UI 更新验证
- [ ] 页面加载提示实时变化
- [ ] 分析结果逐块显示（不是一次性）
- [ ] 可以在分析进行中看到部分结果

### 错误处理验证
1. 不填写股票代码 → 应显示验证错误
2. 拔掉网线后开始分析 → 应显示网络错误
3. 输入无效股票代码 → 应显示 LLM 返回的错误

## 📊 性能指标

### 期望表现
- **首个字符出现**: 3-5秒内
- **总分析时间**: 30-60秒（取决于 LLM 速度）
- **内存占用**: < 100MB

### 如何测试性能
1. 打开浏览器开发者工具 → Performance
2. 点击 Record
3. 发起分析请求
4. 等待完成后点击 Stop
5. 查看瀑布图

## 🐛 常见问题排查

### 问题1：页面显示"API 服务器连接超时"
**原因**: 后端没有启动
**解决**: 
```bash
python api_server.py
```

### 问题2：点击分析后没有反应
**原因**: 
- 没有配置 DeepSeek API Key
- 网络连接问题
- 股票代码错误

**解决**:
1. 检查 `.env` 文件中的 `DEEPSEEK_API_KEY`
2. 检查网络连接
3. 查看浏览器控制台错误信息（F12）

### 问题3：结果一次性显示而不是逐字出现
**原因**: 可能是缓冲问题或浏览器缓存

**解决**:
1. 按 Ctrl+Shift+Delete 清空缓存
2. 重新加载页面（Ctrl+R）
3. 检查浏览器是否支持 ReadableStream

### 问题4：后端报错 "analyze_stream 未定义"
**原因**: LLM 客户端方法没有正确导入

**解决**:
1. 重启后端
2. 查看 `core/llm_client.py` 是否有 `analyze_stream` 方法

## 🔌 API 测试

### 使用 curl 测试流式 API
```bash
curl -X POST http://localhost:8001/api/analyze-stream \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "300748",
    "date": "2025-01-21",
    "market": "A股",
    "analysts": ["market", "fundamentals"],
    "research_depth": 3
  }'
```

预期响应（SSE 格式）：
```
data: {"event": "start", "message": "分析开始"}

data: {"event": "analyst_start", "analyst": "市场分析师"}

data: {"event": "content", "chunk": "股票..."}

data: {"event": "analyst_end", "analyst": "市场分析师"}

data: {"event": "complete", "message": "分析完成"}
```

### 使用 Python 测试
```python
import requests
import json

response = requests.post(
    'http://localhost:8001/api/analyze-stream',
    json={
        'ticker': '300748',
        'date': '2025-01-21',
        'market': 'A股',
        'analysts': ['market', 'fundamentals'],
        'research_depth': 3
    },
    stream=True
)

for line in response.iter_lines():
    if line.startswith(b'data: '):
        data = json.loads(line[6:])
        print(data)
```

## 📈 监控和日志

### 查看后端日志
```
🚀 收到流式分析请求
📊 执行市场分析...
📊 [市场分析师] 开始分析: 300748 (A股)
✅ [市场分析师] 分析完成: 300748
📊 执行基本面分析...
✅ [基本面分析师] 分析完成: 300748
💾 保存流式分析结果到 MongoDB...
✅ 流式分析结果已保存到 MongoDB
```

### 查看浏览器控制台
打开 F12 → Console，可以看到：
```javascript
// 流式消息日志
Raw line: "data: {\"event\": \"analyst_start\", \"analyst\": \"市场分析师\"}"
Data: {event: "analyst_start", analyst: "市场分析师"}
```

## 🧪 单元测试

### 测试 LLM 流式调用
```python
import asyncio
from core.llm_client import DeepSeekClient

async def test_stream():
    client = DeepSeekClient()
    async for chunk in client.analyze_stream(
        prompt="什么是 Python？",
        system_prompt="你是一个 Python 专家"
    ):
        print(chunk, end='', flush=True)

asyncio.run(test_stream())
```

### 测试分析师流式调用
```python
import asyncio
from core.analyst import AnalystManagerStream
from core.llm_client import DeepSeekClient
from data.stock_data import StockDataProvider

async def test_analyst():
    llm = DeepSeekClient()
    data = StockDataProvider()
    mgr = AnalystManagerStream(llm, data)
    
    async for chunk in mgr.analyze_stream(
        ticker='300748',
        date='2025-01-21',
        market='A股',
        analysts=['market']
    ):
        print(chunk, end='', flush=True)

asyncio.run(test_analyst())
```

## 💡 优化建议

### 如果分析太慢
1. 减少 `research_depth` 级别
2. 检查网络连接质量
3. 减少系统其他任务

### 如果想看更详细的分析
1. 增加 `research_depth` 级别到 5
2. 可能需要调整 LLM 的 `max_tokens`

### 如果想保留旧的同步 API
目前两个 API 都可用：
- `/api/analyze` - 同步版本（原有）
- `/api/analyze-stream` - 流式版本（新增）

前端已改为使用流式版本，如需切回同步版本，修改 `front/index.html` 中的 URL。

## 📞 获取帮助

### 查看日志
```bash
# 查看最后 50 行日志
tail -50 api_server.log

# 实时监看日志
tail -f api_server.log
```

### 检查依赖
```bash
pip list | grep -E "fastapi|httpx|pydantic"
```

### 重启服务
```bash
# Windows PowerShell
Get-Process python | Stop-Process
python api_server.py

# Linux/Mac
pkill -f api_server
python api_server.py
```

---

**祝你测试愉快！** 🎉

如有问题，检查 `STREAMING_USAGE.md` 和 `STREAMING_ANALYSIS.md` 获取更详细的文档。

