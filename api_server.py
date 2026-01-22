#!/usr/bin/env python3
"""
后端 API 服务器
使用 FastAPI 提供 RESTful API
"""

import os
import sys
import logging
from datetime import datetime
from typing import Optional, List
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 导入核心模块
from core.llm_client import DeepSeekClient
from core.analyst import AnalystManager, AnalystManagerStream
from core.image_analyzer import ImageAnalyzer
from data.stock_data import StockDataProvider
from storage.mongodb import MongoDBStorage

# 创建 FastAPI 应用
app = FastAPI(
    title="TradingMiniAgents API",
    description="简单股票分析智能体 API",
    version="1.0.0"
)

# 配置 CORS
# 注意：当 allow_origins=["*"] 时，不能使用 allow_credentials=True
# 开发环境允许所有来源，生产环境应该限制具体域名
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名，如 ["http://localhost:8080"]
    allow_credentials=False,  # 使用 "*" 时必须是 False
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# 全局变量存储初始化后的组件
llm_client = None
data_provider = None
analyst_manager = None
analyst_manager_stream = None
mongodb_storage = None
image_analyzer = None


# 请求模型
class AnalysisRequest(BaseModel):
    """分析请求模型"""
    ticker: str
    date: str
    market: str = "A股"
    analysts: List[str] = ["market", "fundamentals"]
    research_depth: int = 3
    image_path: Optional[str] = None


class AnalysisResponse(BaseModel):
    """分析响应模型"""
    success: bool
    message: str
    data: Optional[dict] = None


# 初始化组件
def init_components():
    """初始化所有组件"""
    global llm_client, data_provider, analyst_manager, analyst_manager_stream, mongodb_storage, image_analyzer
    
    try:
        logger.info("📦 初始化组件...")
        
        # LLM 客户端（从环境变量读取所有配置）
        llm_client = DeepSeekClient()
        logger.info("✅ LLM 客户端初始化完成")
        
        # 数据提供者
        data_provider = StockDataProvider()
        logger.info("✅ 数据提供者初始化完成")
        
        # 分析师管理器
        analyst_manager = AnalystManager(llm_client, data_provider)
        logger.info("✅ 分析师管理器初始化完成")
        
        # 流式分析师管理器
        analyst_manager_stream = AnalystManagerStream(llm_client, data_provider)
        logger.info("✅ 流式分析师管理器初始化完成")
        
        # MongoDB 存储
        mongodb_storage = MongoDBStorage()
        if mongodb_storage.connected:
            logger.info("✅ MongoDB 存储初始化完成")
        else:
            logger.warning("⚠️ MongoDB 未连接")
        
        # 图片分析器
        image_analyzer = ImageAnalyzer(llm_client)
        logger.info("✅ 图片分析器初始化完成")
        
    except Exception as e:
        logger.error(f"❌ 组件初始化失败: {e}")
        raise


# 启动时初始化
@app.on_event("startup")
async def startup_event():
    """应用启动时初始化"""
    init_components()


# 获取前端目录路径
frontend_dir = Path(__file__).parent / "front"

# API 路由（必须在静态文件之前定义）
@app.get("/api")
async def api_info():
    """API 信息"""
    return {
        "message": "TradingMiniAgents API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "mongodb_connected": mongodb_storage.connected if mongodb_storage else False,
        "llm_ready": llm_client is not None
    }


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_stock(request: AnalysisRequest):
    """
    执行股票分析
    
    Args:
        request: 分析请求
        
    Returns:
        分析结果
    """
    try:
        logger.info("=" * 60)
        logger.info("🚀 收到分析请求")
        logger.info(f"股票代码: {request.ticker}")
        logger.info(f"分析日期: {request.date}")
        logger.info(f"市场类型: {request.market}")
        logger.info(f"分析师: {', '.join(request.analysts)}")
        logger.info(f"研究深度: {request.research_depth}")
        logger.info("=" * 60)
        
        # 验证请求
        if not request.ticker:
            raise HTTPException(status_code=400, detail="股票代码不能为空")
        
        if not request.date:
            raise HTTPException(status_code=400, detail="分析日期不能为空")
        
        # 图片分析（如果提供）
        image_analysis = None
        if request.image_path:
            logger.info(f"🖼️ 开始分析图片: {request.image_path}")
            image_path = Path(request.image_path)
            if image_path.exists():
                image_analysis = image_analyzer.analyze_image(
                    str(image_path),
                    f"请分析这张与股票 {request.ticker} 相关的图片，提取关键信息用于股票分析。"
                )
                logger.info("✅ 图片分析完成")
            else:
                logger.warning(f"⚠️ 图片文件不存在: {request.image_path}")
        
        # 执行分析
        logger.info("📊 开始执行股票分析...")
        reports = analyst_manager.analyze(
            ticker=request.ticker,
            date=request.date,
            market=request.market,
            analysts=request.analysts
        )
        
        # 保存到 MongoDB
        if mongodb_storage and mongodb_storage.connected:
            logger.info("💾 保存分析结果到 MongoDB...")
            mongodb_storage.save_analysis_report(
                stock_symbol=request.ticker,
                analysis_date=request.date,
                market=request.market,
                analysts=list(reports.keys()),
                reports=reports,
                research_depth=request.research_depth,
                image_analysis=image_analysis
            )
            logger.info("✅ 分析结果已保存到 MongoDB")
        
        # 构建响应
        response_data = {
            "ticker": request.ticker,
            "date": request.date,
            "market": request.market,
            "research_depth": request.research_depth,
            "analysts": list(reports.keys()),
            "reports": reports,
            "image_analysis": image_analysis,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info("✅ 分析完成")
        
        return AnalysisResponse(
            success=True,
            message="分析完成",
            data=response_data
        )
        
    except ValueError as e:
        logger.error(f"❌ 参数错误: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"❌ 分析失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")


@app.post("/api/analyze-stream")
async def analyze_stock_stream(request: AnalysisRequest):
    """
    执行股票分析（流式版本）
    
    Args:
        request: 分析请求
        
    Returns:
        流式分析结果
    """
    try:
        logger.info("=" * 60)
        logger.info("🚀 收到流式分析请求")
        logger.info(f"股票代码: {request.ticker}")
        logger.info(f"分析日期: {request.date}")
        logger.info(f"市场类型: {request.market}")
        logger.info(f"分析师: {', '.join(request.analysts)}")
        logger.info(f"研究深度: {request.research_depth}")
        logger.info("=" * 60)
        
        # 验证请求
        if not request.ticker:
            raise HTTPException(status_code=400, detail="股票代码不能为空")
        
        if not request.date:
            raise HTTPException(status_code=400, detail="分析日期不能为空")
        
        # 创建流式生成器
        async def event_generator():
            """生成 SSE 格式的流式数据"""
            try:
                import json
                
                # 发送开始信号
                yield f"data: {json.dumps({'event': 'start', 'message': '分析开始'})}\n\n"
                
                # 获取分析流
                full_content = {}  # 存储完整的分析内容
                current_analyst = None
                
                async for chunk in analyst_manager_stream.analyze_stream(
                    ticker=request.ticker,
                    date=request.date,
                    market=request.market,
                    analysts=request.analysts
                ):
                    # 处理分析师标记
                    if chunk.startswith("[ANALYST_START]"):
                        current_analyst = chunk.replace("[ANALYST_START]", "").strip()
                        full_content[current_analyst] = ""
                        yield f"data: {json.dumps({'event': 'analyst_start', 'analyst': current_analyst})}\n\n"
                    elif chunk.startswith("[ANALYST_END]"):
                        current_analyst = chunk.replace("[ANALYST_END]", "").strip()
                        yield f"data: {json.dumps({'event': 'analyst_end', 'analyst': current_analyst})}\n\n"
                    else:
                        # 普通内容块
                        if current_analyst:
                            full_content[current_analyst] += chunk
                        
                        # 发送内容块（使用 json.dumps 确保有效的 JSON）
                        yield f"data: {json.dumps({'event': 'content', 'chunk': chunk})}\n\n"
                
                # 发送完成信号并准备保存
                yield f"data: {json.dumps({'event': 'complete', 'message': '分析完成'})}\n\n"
                
                # 保存到 MongoDB（在流式完成后）
                if mongodb_storage and mongodb_storage.connected:
                    logger.info("💾 保存流式分析结果到 MongoDB...")
                    mongodb_storage.save_analysis_report(
                        stock_symbol=request.ticker,
                        analysis_date=request.date,
                        market=request.market,
                        analysts=list(full_content.keys()),
                        reports=full_content,
                        research_depth=request.research_depth,
                        image_analysis=None
                    )
                    logger.info("✅ 流式分析结果已保存到 MongoDB")
                
            except Exception as e:
                logger.error(f"❌ 流式分析失败: {e}", exc_info=True)
                import json
                error_msg = json.dumps(str(e))
                yield f"data: {{'event': 'error', 'message': {error_msg}}}\n\n"
        
        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ 流式分析请求处理失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"流式分析失败: {str(e)}")


@app.get("/api/history")
async def get_analysis_history(ticker: Optional[str] = None, limit: int = 10):
    """
    获取分析历史记录
    
    Args:
        ticker: 股票代码（可选）
        limit: 返回数量限制
        
    Returns:
        历史记录列表
    """
    try:
        if not mongodb_storage or not mongodb_storage.connected:
            return {
                "success": False,
                "message": "MongoDB 未连接",
                "data": []
            }
        
        reports = mongodb_storage.get_analysis_reports(
            stock_symbol=ticker,
            limit=limit
        )
        
        return {
            "success": True,
            "message": "获取成功",
            "data": reports
        }
        
    except Exception as e:
        logger.error(f"❌ 获取历史记录失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取历史记录失败: {str(e)}")


@app.get("/api/stock-info")
async def get_stock_info(ticker: str, market: str = "A股"):
    """
    获取股票基本信息
    
    Args:
        ticker: 股票代码
        market: 市场类型
        
    Returns:
        股票信息
    """
    try:
        if not data_provider:
            raise HTTPException(status_code=500, detail="数据提供者未初始化")
        
        stock_info = data_provider.get_stock_info(ticker, market)
        market_info = data_provider.get_market_info(ticker, market)
        
        return {
            "success": True,
            "message": "获取成功",
            "data": {
                "ticker": ticker,
                "market": market,
                "info": stock_info,
                "market_info": market_info
            }
        }
        
    except Exception as e:
        logger.error(f"❌ 获取股票信息失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取股票信息失败: {str(e)}")


# 根路径 - 返回前端页面（必须在最后，作为后备路由）
@app.get("/")
async def root():
    """根路径 - 返回前端页面"""
    index_file = frontend_dir / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {
        "message": "TradingMiniAgents API",
        "version": "1.0.0",
        "status": "running",
        "frontend": "Frontend not found"
    }

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory=frontend_dir / "static"), name="static")

# 挂载图片目录
app.mount('/images', StaticFiles(directory=frontend_dir / "images"), name="images")

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("API_PORT", 8001))
    host = os.getenv("API_HOST", "0.0.0.0")
    
    logger.info(f"🚀 启动 API 服务器: http://{host}:{port}")
    
    uvicorn.run(
        "api_server:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )


