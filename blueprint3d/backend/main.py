from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import base64
import requests
import time
from typing import Optional
from pydantic import BaseModel

app = FastAPI(title="Blueprint3D API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    image: str
    description: Optional[str] = ""
    viewAngle: Optional[str] = "perspective"
    style: Optional[str] = "realistic"

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/generate")
async def generate_image(request: GenerateRequest):
    """
    Generate 3D visualization from engineering blueprint
    """
    start_time = time.time()

    try:
        # API configuration
        api_url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
        api_key = "95d2a060-7ab5-4fdc-92bf-d9da19aa652c"

        # Build prompt based on style and view angle
        style_prompts = {
            "realistic": "写实风格，高质量渲染，专业建筑可视化效果",
            "technical": "技术线稿风格，黑白线条图，工程图纸风格",
            "cartoon": "简约卡通风格，明亮色彩，扁平化设计"
        }

        angle_prompts = {
            "perspective": "透视图",
            "front": "正视图",
            "side": "侧视图",
            "top": "俯视图"
        }

        base_prompt = f"将这个工程图纸转换为{angle_prompts.get(request.viewAngle, '透视')}的3D效果图，{style_prompts.get(request.style, style_prompts['realistic'])}"

        if request.description:
            base_prompt += f"，补充描述：{request.description}"

        # Prepare API request payload
        payload = {
            "model": "doubao-seedream-4-5-251128",
            "prompt": base_prompt,
            "image": request.image,
            "size": "2K",
            "watermark": False
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # Call Doubao API
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail=f"API request failed: {response.text}"
            )

        result = response.json()

        # Safely extract image URL from response
        image_url = ""
        if isinstance(result, dict):
            data = result.get("data", {})
            if isinstance(data, dict):
                image_url = data.get("url", "")
            elif isinstance(data, list) and len(data) > 0:
                # Handle case where data is a list
                first_item = data[0]
                if isinstance(first_item, dict):
                    image_url = first_item.get("url", "")

        processing_time = round(time.time() - start_time, 2)

        return JSONResponse({
            "success": True,
            "imageUrl": image_url,
            "processingTime": processing_time
        })

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="API request timed out")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API request error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
