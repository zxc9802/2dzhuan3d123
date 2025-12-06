"""
Generate API - 3D效果图生成接口
"""
import base64
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from PIL import Image
import io

from services.doubao_service import get_doubao_service
from templates.prompts import build_prompt

router = APIRouter()

class GenerateRequest(BaseModel):
    """生成请求模型"""
    image: str  # base64编码的图片
    description: str = ""
    viewAngle: str = "perspective"
    style: str = "realistic"

class GenerateResponse(BaseModel):
    """生成响应模型"""
    success: bool
    imageUrl: Optional[str] = None
    error: Optional[str] = None
    processingTime: float

# 支持的图片格式
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def validate_file(filename: str, file_size: int) -> None:
    """验证上传的文件"""
    # 检查文件扩展名
    ext = filename.lower().split(".")[-1] if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式。支持的格式: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # 检查文件大小
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"文件大小超过限制。最大允许: 10MB"
        )

@router.post("/generate", response_model=GenerateResponse)
async def generate_3d_image(
    image: UploadFile = File(..., description="工程图纸图片"),
    description: str = Form("", description="图纸描述"),
    viewAngle: str = Form("perspective", description="视角: front/side/top/perspective"),
    style: str = Form("realistic", description="风格: realistic/technical/cartoon")
):
    """
    生成3D效果图
    
    - **image**: 上传的工程图纸（JPG/PNG/PDF）
    - **description**: 图纸描述（可选，建议填写）
    - **viewAngle**: 视角选择（正视/侧视/俯视/透视）
    - **style**: 风格选择（写实/技术线稿/卡通）
    """
    try:
        # 读取文件内容
        file_content = await image.read()
        file_size = len(file_content)
        
        # 验证文件
        validate_file(image.filename or "unknown.png", file_size)
        
        # 如果是PDF，转换为图片（取第一页）
        if image.filename and image.filename.lower().endswith(".pdf"):
            # 简化处理：对于MVP，我们提示用户上传图片格式
            raise HTTPException(
                status_code=400,
                detail="PDF支持即将推出，请暂时使用JPG或PNG格式"
            )
        
        # 验证图片格式
        try:
            img = Image.open(io.BytesIO(file_content))
            img.verify()
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="无法解析图片文件，请确保上传有效的图片"
            )
        
        # 构建提示词
        desc = description.strip() if description else "engineering blueprint or technical drawing"
        prompt = build_prompt(desc, viewAngle, style)
        
        # 调用AI服务生成图片
        doubao_service = get_doubao_service()
        result = await doubao_service.generate_3d_image(
            prompt=prompt,
            reference_image=file_content
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"生成失败: {result.get('error', '未知错误')}"
            )
        
        return GenerateResponse(
            success=True,
            imageUrl=result["imageUrl"],
            processingTime=result["processingTime"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"服务器错误: {str(e)}"
        )

@router.post("/generate-json", response_model=GenerateResponse)
async def generate_3d_image_json(request: GenerateRequest):
    """
    生成3D效果图（JSON格式请求）
    
    适用于前端已将图片转为base64的场景
    """
    try:
        # 解码base64图片
        try:
            image_data = base64.b64decode(request.image)
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="无效的base64图片数据"
            )
        
        # 验证图片
        try:
            img = Image.open(io.BytesIO(image_data))
            img.verify()
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="无法解析图片数据"
            )
        
        # 构建提示词
        desc = request.description.strip() if request.description else "engineering blueprint or technical drawing"
        prompt = build_prompt(desc, request.viewAngle, request.style)
        
        # 调用AI服务
        doubao_service = get_doubao_service()
        result = await doubao_service.generate_3d_image(
            prompt=prompt,
            reference_image=image_data
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"生成失败: {result.get('error', '未知错误')}"
            )
        
        return GenerateResponse(
            success=True,
            imageUrl=result["imageUrl"],
            processingTime=result["processingTime"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"服务器错误: {str(e)}"
        )
