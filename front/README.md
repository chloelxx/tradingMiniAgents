# 前端页面说明

## 文件说明

- `index.html`: 主页面，包含完整的股票分析界面

## 功能特性

- ✅ 选择市场（A股/港股/美股）
- ✅ 股票代码输入
- ✅ 分析日期选择
- ✅ 研究深度滑块（1-5级）
- ✅ 选择分析师团队（市场分析师、基本面分析师）
- ✅ 实时分析结果显示
- ✅ 响应式设计

## 使用方法

### 方法一：使用启动脚本（推荐）

在项目根目录运行：
```bash
python start_server.py
```

这将自动启动：
- 后端 API 服务器（端口 8001）
- 前端页面服务器（端口 8080）
- 自动打开浏览器

### 方法二：手动启动

1. 启动后端 API：
```bash
python api_server.py
```

2. 启动前端服务：
```bash
cd front
python -m http.server 8080
```

3. 在浏览器中打开：http://localhost:8080

## 技术栈

- Vue 3: 前端框架
- Element Plus: UI 组件库
- Fetch API: HTTP 请求

## API 配置

前端默认连接到 `http://localhost:8001`，如果需要修改，请编辑 `index.html` 中的 `apiBaseUrl` 变量。


