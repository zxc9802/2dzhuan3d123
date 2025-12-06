"""
Blueprint3D Backend - FastAPI Application
将工程图纸转化为3D效果图的AI服务
"""
import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import time

from api.generate import router as generate_router

# 加载环境变量
load_dotenv()

# 创建FastAPI应用
app = FastAPI(
    title="Blueprint3D API",
    description="将工程平面图纸转化为3D可视化效果图",
    version="1.0.0"
)

# CORS配置
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建临时文件目录
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

# 挂载静态文件目录
app.mount("/temp", StaticFiles(directory=TEMP_DIR), name="temp")

# 注册路由
app.include_router(generate_router, prefix="/api", tags=["generate"])

@app.get("/")
async def root():
    return {
        "message": "Blueprint3D API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": time.time()}

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    uvicorn.run("main:app", host=host, port=port, reload=debug)
