"""
图片分析模块
"""

import base64
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class ImageAnalyzer:
    """图片分析器"""
    
    def __init__(self, llm_client):
        """
        初始化图片分析器
        
        Args:
            llm_client: LLM 客户端实例
        """
        self.llm_client = llm_client
    
    def analyze_image(self, image_path: str, prompt: str) -> str:
        """
        分析图片
        
        Args:
            image_path: 图片路径
            prompt: 分析提示
            
        Returns:
            分析结果
        """
        try:
            # 读取图片并转换为 base64
            image_base64 = self._image_to_base64(image_path)
            
            # 使用 LLM 分析图片
            # 注意：这里需要 LLM 支持图片输入
            # 简化版本：先读取图片信息，然后结合文本分析
            analysis_prompt = f"""
请分析以下图片内容，并结合股票分析需求进行解读：

{prompt}

图片路径: {image_path}
"""
            
            # 如果 LLM 支持图片输入，可以在这里添加图片数据
            # 当前简化版本仅使用文本描述
            result = self.llm_client.analyze(
                prompt=analysis_prompt,
                system_prompt="你是一位专业的股票分析师，擅长分析股票相关的图表和数据。"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"图片分析失败: {e}")
            return f"图片分析失败: {str(e)}"
    
    def _image_to_base64(self, image_path: str) -> str:
        """
        将图片转换为 base64 编码
        
        Args:
            image_path: 图片路径
            
        Returns:
            base64 编码的图片数据
        """
        try:
            from PIL import Image
            import io
            
            with open(image_path, 'rb') as f:
                image_data = f.read()
                return base64.b64encode(image_data).decode('utf-8')
        except Exception as e:
            logger.warning(f"图片编码失败: {e}")
            return ""
    
    def get_image_info(self, image_path: str) -> dict:
        """
        获取图片基本信息
        
        Args:
            image_path: 图片路径
            
        Returns:
            图片信息字典
        """
        try:
            from PIL import Image
            
            img = Image.open(image_path)
            return {
                'format': img.format,
                'size': img.size,
                'mode': img.mode,
                'path': image_path
            }
        except Exception as e:
            logger.error(f"获取图片信息失败: {e}")
            return {'error': str(e)}

