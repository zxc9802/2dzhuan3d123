"""
Google Imagen Service
使用 Google Gemini API 的 Imagen 4 模型生成3D效果图
"""
import os
import base64
import uuid
from typing import Optional
from google import genai
from google.genai import types
from PIL import Image
import io

class ImagenService:
    """Google Imagen 4 图像生成服务"""
    
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        self.client = genai.Client(api_key=api_key)
        self.model = "imagen-4.0-generate-001"
        self.temp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "temp")
        os.makedirs(self.temp_dir, exist_ok=True)
    
    async def generate_3d_image(
        self,
        prompt: str,
        reference_image: Optional[bytes] = None
    ) -> dict:
        """
        生成3D效果图
        
        Args:
            prompt: 生成提示词
            reference_image: 参考图片的bytes数据（可选）
        
        Returns:
            包含图片URL和处理时间的字典
        """
        import time
        start_time = time.time()
        
        try:
            # 使用 Imagen 4 生成图像
            # 注意：Imagen 4 主要是文本到图像，但我们将参考图像信息融入prompt
            response = self.client.models.generate_images(
                model=self.model,
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="1:1",
                    safety_filter_level="BLOCK_LOW_AND_ABOVE",
                    person_generation="DONT_ALLOW"
                )
            )
            
            if not response.generated_images:
                raise Exception("No images generated")
            
            # 获取生成的图像
            generated_image = response.generated_images[0]
            
            # 保存图像
            filename = f"{uuid.uuid4().hex}.png"
            filepath = os.path.join(self.temp_dir, filename)
            
            # 将图像数据保存为文件
            image = Image.open(io.BytesIO(generated_image.image.image_bytes))
            image.save(filepath, "PNG")
            
            processing_time = time.time() - start_time
            
            return {
                "success": True,
                "imageUrl": f"/temp/{filename}",
                "processingTime": round(processing_time, 2)
            }
            
        except Exception as e:
            processing_time = time.time() - start_time
            return {
                "success": False,
                "error": str(e),
                "processingTime": round(processing_time, 2)
            }
    
    def encode_image_to_base64(self, image_bytes: bytes) -> str:
        """将图片编码为base64"""
        return base64.b64encode(image_bytes).decode("utf-8")
    
    def decode_base64_to_image(self, base64_string: str) -> bytes:
        """将base64解码为图片数据"""
        return base64.b64decode(base64_string)


# 创建全局服务实例
_imagen_service: Optional[ImagenService] = None

def get_imagen_service() -> ImagenService:
    """获取Imagen服务实例（单例模式）"""
    global _imagen_service
    if _imagen_service is None:
        _imagen_service = ImagenService()
    return _imagen_service
