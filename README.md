# Blueprint3D - 2D转3D图纸生成器

基于AI的工程图纸转3D效果图生成服务。

## 功能特点

- 上传2D工程图纸（PNG、JPG等格式）
- 使用AI生成对应的3D效果图
- 实时预览生成结果
- 支持下载生成的3D效果图

## 技术栈

- **前端**: Next.js 16, React 19, Tailwind CSS
- **后端**: FastAPI, Python
- **AI服务**: ARK API

## 部署说明

### Vercel部署

1. 将项目推送到GitHub
2. 在Vercel中导入项目
3. 配置环境变量：
   - `ARK_API_KEY`: 你的ARK API密钥
   - `HOST`: 0.0.0.0
   - `PORT`: 8000
   - `DEBUG`: false
   - `CORS_ORIGINS`: https://your-domain.vercel.app

### 本地开发

#### 前端
```bash
cd blueprint3d
npm install
npm run dev
```

#### 后端
```bash
cd backend
pip install -r requirements.txt
# 复制环境变量文件并配置
cp .env.example .env
# 编辑 .env 文件，填入你的API密钥
python -m uvicorn main:app --reload
```

## 环境变量配置

在后端部署时需要配置以下环境变量：

- `ARK_API_KEY`: ARK API的密钥（必需）
- `HOST`: 服务器地址（默认: 0.0.0.0）
- `PORT`: 服务器端口（默认: 8000）
- `DEBUG`: 调试模式（默认: false）
- `CORS_ORIGINS`: 允许的跨域来源（用逗号分隔）

## API文档

部署后访问 `/docs` 查看交互式API文档。

## 许可证

MIT
