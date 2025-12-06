"""
Doubao SeeDream Service
使用火山引擎豆包 SeeDream 模型生成3D效果图
"""
import os
import base64
import uuid
import httpx
from typing import Optional
from PIL import Image
import io

class DoubaoService:
    """火山引擎豆包 SeeDream 图像生成服务"""
    
    def __init__(self):
        api_key = os.getenv("ARK_API_KEY")
        if not api_key:
            raise ValueError("ARK_API_KEY environment variable is required")
        
        self.api_key = api_key
        self.api_url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
        self.model = "doubao-seedream-4-5-251128"
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
            reference_image: 参考图片的bytes数据
        
        Returns:
            包含图片URL和处理时间的字典
        """
        import time
        start_time = time.time()
        
        try:
            # 将参考图片转为base64
            image_base64 = None
            if reference_image:
                image_base64 = base64.b64encode(reference_image).decode('utf-8')
                # 豆包API需要data URI格式
                image_base64 = f"data:image/png;base64,{image_base64}"
            
            # 构建请求
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": self.model,
                "prompt": prompt,
                "size": "2K",
                "watermark": False
            }
            
            # 如果有参考图片,添加到请求中
            if image_base64:
                payload["image"] = image_base64
            
            # 发送请求
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=payload
                )
                
                if response.status_code != 200:
                    raise Exception(f"API request failed: {response.status_code} {response.text}")
                
                result = response.json()
                
                # 豆包API返回格式: {"data": [{"url": "...", "b64_image": "..."}]}
                if "data" not in result or len(result["data"]) == 0:
                    raise Exception("No image generated in response")
                
                image_data = result["data"][0]
                
                # 优先使用base64图片
                if "b64_image" in image_data and image_data["b64_image"]:
                    # 保存base64图片
                    img_bytes = base64.b64decode(image_data["b64_image"])
                    filename = f"{uuid.uuid4().hex}.png"
                    filepath = os.path.join(self.temp_dir, filename)
                    
                    with open(filepath, "wb") as f:
                        f.write(img_bytes)
                    
                    processing_time = time.time() - start_time
                    
                    return {
                        "success": True,
                        "imageUrl": f"/temp/{filename}",
                        "processingTime": round(processing_time, 2)
                    }
                elif "url" in image_data and image_data["url"]:
                    # 如果只有URL,下载图片
                    async with httpx.AsyncClient() as client:
                        img_response = await client.get(image_data["url"])
                        img_bytes = img_response.content
                    
                    filename = f"{uuid.uuid4().hex}.png"
                    filepath = os.path.join(self.temp_dir, filename)
                    
                    with open(filepath, "wb") as f:
                        f.write(img_bytes)
                    
                    processing_time = time.time() - start_time
                    
                    return {
                        "success": True,
                        "imageUrl": f"/temp/{filename}",
                        "processingTime": round(processing_time, 2)
                    }
                else:
                    raise Exception("No image data in response")
            
        except Exception as e:
            processing_time = time.time() - start_time
            return {
                "success": False,
                "error": str(e),
                "processingTime": round(processing_time, 2)
            }


# 创建全局服务实例
_doubao_service: Optional[DoubaoService] = None

def get_doubao_service() -> DoubaoService:
    """获取豆包服务实例（单例模式）"""
    global _doubao_service
    if _doubao_service is None:
        _doubao_service = DoubaoService()
    return _doubao_service
