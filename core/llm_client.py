"""
DeepSeek LLM 客户端
基于 HTTP 的 OpenAI Chat Completions 兼容接口
"""

import os
import logging
from typing import Optional, List
import httpx
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

logger = logging.getLogger(__name__)


class DeepSeekClient:
    """
    DeepSeek LLM 客户端
    使用 HTTP 直接调用 DeepSeek API（兼容 OpenAI Chat Completions 格式）
    """
    
    def __init__(self) -> None:
        """初始化客户端，从 .env 文件读取配置"""
        # 从环境变量读取配置
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        base_url = os.getenv("DEEPSEEK_BASE_URL")
        self.model = os.getenv("DEEPSEEK_MODEL")
        
        # 读取温度参数
        temp_str = os.getenv("DEEPSEEK_TEMPERATURE", "0.1")
        try:
            self.temperature = float(temp_str)
        except ValueError:
            self.temperature = 0.1
        
        # 读取 max_tokens
        max_tokens_str = os.getenv("DEEPSEEK_MAX_TOKENS")
        if max_tokens_str and max_tokens_str.strip():
            try:
                self.max_tokens = int(max_tokens_str)
            except ValueError:
                self.max_tokens = None
        else:
            self.max_tokens = None
        
        # 验证必需配置
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY 未设置，请在 .env 文件中配置")
        
        if not base_url:
            raise ValueError("DEEPSEEK_BASE_URL 未设置，请在 .env 文件中配置")
        
        if not self.model:
            raise ValueError("DEEPSEEK_MODEL 未设置，请在 .env 文件中配置")
        
        
        
        self.base_url = base_url
        self.model_name = self.model
        
        # 创建同步 HTTP 客户端
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=60.0,
        )
        
        logger.info(f"✅ DeepSeek 客户端初始化完成: model={self.model}, base_url={self.base_url}")
    
    def _chat(self, messages: List[dict]) -> str:
        """
        内部方法：调用 Chat Completions API
        
        Args:
            messages: 消息列表，格式为 [{"role": "system", "content": "..."}, ...]
            
        Returns:
            模型响应文本
        """
        if not self.api_key:
            return "LLM 未配置（缺少 DEEPSEEK_API_KEY 环境变量），当前为占位回复。"
        print(f"api_key: {self.api_key}")
        print(f"model: {self.model}")
        print(f"temperature: {self.temperature}")
        print(f"max_tokens: {self.max_tokens}")
        print(f"messages: {messages}")
        print(f"base_url: {self.base_url}")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }


        payload = {
            "model": self.model,
            "messages": messages,
            # "messages": messages,
            "temperature": self.temperature,
            "max_tokens": 4096,
        }
        print(f"payload: {payload},headers: {headers}")
        # 如果设置了 max_tokens，添加到 payload
        if self.max_tokens is not None:
            payload["max_tokens"] = self.max_tokens

        try:
            # 调用 /v1/chat/completions 端点
            response = self._client.post("/chat/completions", headers=headers, json=payload)
            
            # 检查 HTTP 状态码
            if response.status_code != 200:
                error_detail = response.text
                logger.error(
                    f"LLM API 调用失败: status={response.status_code}, "
                    f"model={self.model}, "
                    f"error={error_detail}"
                )
                print(f"error_detail: {error_detail}")
                # 检查是否是模型不存在的错误
                if response.status_code == 404 or "model" in error_detail.lower() or "not found" in error_detail.lower():
                    raise ValueError(
                        f"模型 '{self.model}' 不存在或没有访问权限。\n"
                        f"请检查：\n"
                        f"1. 模型名称是否正确（可用模型：deepseek-chat, deepseek-coder, deepseek-reasoner）\n"
                        f"2. 你的 API Key 是否有权限访问该模型\n"
                        f"3. 在 .env 文件中设置 DEEPSEEK_MODEL=deepseek-chat 使用通用模型\n"
                        f"原始错误: {error_detail[:500]}"
                    )
                
                raise ValueError(
                    f"LLM API 调用失败（状态码: {response.status_code}）。"
                    f"请检查 API Key 和模型名称是否正确。错误详情: {error_detail[:200]}"
                )
            
            data = response.json()
            
            # 检查返回数据格式
            if "choices" not in data or not data["choices"]:
                logger.error(f"LLM API 返回格式异常: {data}")
                raise ValueError("LLM API 返回数据格式异常，请检查 API 响应。")
            
            # 按照官方返回格式，从 choices[0].message.content 中读取回复
            content = data["choices"][0]["message"]["content"]
            return content
            
        except httpx.TimeoutException:
            logger.error("LLM API 调用超时")
            raise ValueError("LLM API 调用超时，请稍后重试。")
        except httpx.RequestError as e:
            logger.error(f"LLM API 网络请求错误: {e}")
            raise ValueError(f"LLM API 网络请求失败: {str(e)}。请检查网络连接和 API 地址。")
        except KeyError as e:
            logger.error(f"LLM API 返回数据缺少必要字段: {e}, data={data if 'data' in locals() else 'N/A'}")
            raise ValueError("LLM API 返回数据格式不正确，缺少必要字段。")
        except ValueError:
            # 重新抛出 ValueError（模型不存在等错误）
            raise
        except Exception as e:
            logger.error(f"LLM API 调用发生未知错误: {e}", exc_info=True)
            raise ValueError(f"LLM API 调用发生错误: {str(e)}。请查看日志获取详细信息。")
    
    def invoke(self, messages: List[dict]) -> str:
        """
        调用模型生成响应（兼容旧接口）
        
        Args:
            messages: 消息列表，格式为 [{"role": "system", "content": "..."}, ...]
            
        Returns:
            模型响应文本
        """
        return self._chat(messages)
    
    def analyze(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        分析文本
        
        Args:
            prompt: 用户提示
            system_prompt: 系统提示（可选）
            
        Returns:
            分析结果
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        return self._chat(messages)
    
    def close(self) -> None:
        """关闭 HTTP 客户端"""
        if hasattr(self, '_client'):
            self._client.close()
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()

