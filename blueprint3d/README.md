# Blueprint3D - 工程图纸3D可视化平台

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一键将复杂的工程平面图纸，转化为直观易懂的3D可视化效果图。

## ✨ 特性

- 📤 **简单上传**: 支持拖拽或点击上传 JPG、PNG 格式图片
- 🎨 **多种风格**: 写实风格、技术线稿、简约卡通三种视觉风格
- 🔭 **多视角生成**: 透视图、正视图、侧视图、俯视图
- ⚡ **AI驱动**: 基于 Volcengine Doubao API 的高质量图像生成
- 💾 **一键下载**: 生成结果支持直接下载保存
- 📱 **响应式设计**: 适配桌面端和移动端

## 🚀 快速开始

### 环境要求

- Node.js 18+
- Python 3.8+
- Volcengine Doubao API Key

### 安装依赖

#### 前端依赖
```bash
cd blueprint3d
npm install
```

#### 后端依赖
```bash
cd backend
pip install -r requirements.txt
```

### 配置环境变量

复制环境变量示例文件：
```bash
cp backend/.env.example backend/.env
```

编辑 `backend/.env` 文件，配置您的 API Key：
```env
DOBAO_API_KEY=your_api_key_here
DOBAO_API_URL=https://ark.cn-beijing.volces.com/api/v3/images/generations
DOBAO_MODEL=doubao-seedream-4-5-251128
```

### 启动服务

#### 1. 启动后端服务
```bash
cd backend
python main.py
```
后端服务将在 http://localhost:8000 启动

#### 2. 启动前端服务
```bash
cd blueprint3d
npm run dev
```
前端应用将在 http://localhost:3000 启动

### 访问应用

打开浏览器，访问 http://localhost:3000

## 📖 使用指南

### 1. 上传图片
- 点击左侧面板的"上传图纸"区域
- 或直接拖拽图片文件到该区域
- 支持 JPG、PNG 格式，最大 10MB

### 2. 配置参数
- **补充描述**（可选）：描述图纸的关键信息，帮助AI更好理解
- **视角选择**：选择需要的视图类型
- **风格选择**：选择视觉效果风格

### 3. 生成图片
- 点击"生成3D效果图"按钮
- 等待 AI 处理（通常 10-30 秒）
- 查看生成结果

### 4. 下载结果
- 点击"下载图片"按钮保存结果
- 或点击"重新生成"尝试不同效果

## 🛠️ 技术架构

### 前端技术栈
- **Next.js 14** - React 框架
- **TypeScript** - 类型安全
- **Vanilla CSS** - 样式

### 后端技术栈
- **FastAPI** - Python Web 框架
- **Volcengine Doubao API** - AI 图像生成服务
- **Requests** - HTTP 客户端

### 系统架构

```
┌─────────────────┐
│   Next.js 前端   │
│   (Port 3000)   │
└────────┬────────┘
         │
         │ HTTP
         │
┌────────▼────────┐
│   FastAPI 后端   │
│   (Port 8000)   │
└────────┬────────┘
         │
         │ API Call
         │
┌────────▼────────┐
│  Doubao API     │
│ (图像生成服务)    │
└─────────────────┘
```

## 📁 项目结构

```
blueprint3d/
├── app/                      # Next.js 应用
│   ├── api/                  # API 路由
│   │   └── generate/         # 生成接口代理
│   ├── components/           # React 组件
│   │   ├── ImageUpload.tsx   # 图片上传组件
│   │   ├── PreviewCanvas.tsx # 预览画布组件
│   │   └── OptionsPanel.tsx  # 选项面板组件
│   ├── globals.css           # 全局样式
│   ├── layout.tsx            # 根布局
│   └── page.tsx              # 主页面
├── backend/                  # FastAPI 后端
│   ├── api/                  # API 路由
│   ├── services/             # 业务服务
│   │   └── doubao_service.py # Doubao API 服务
│   ├── templates/            # 提示词模板
│   ├── .env.example          # 环境变量示例
│   ├── main.py               # 应用入口
│   └── requirements.txt      # Python 依赖
├── next.config.ts            # Next.js 配置
├── package.json              # 项目配置
└── tsconfig.json             # TypeScript 配置
```

## 🎯 核心功能实现

### 图片上传
- 支持拖拽上传
- 文件格式验证（JPG/PNG）
- 文件大小限制（10MB）
- Base64 编码转换

### 参数配置
- **视角选项**：
  - 透视图 - 3D 立体效果
  - 正视图 - 正面视角
  - 侧视图 - 侧面视角
  - 俯视图 - 顶部视角

- **风格选项**：
  - 写实风格 - 高质量渲染，专业建筑效果
  - 技术线稿 - 黑白线条，工程图纸风格
  - 简约卡通 - 明亮色彩，扁平化设计

### AI 生成
- 智能提示词构建
- API 请求处理
- 错误处理与重试
- 处理时间统计

## 🔧 部署

### Vercel + Railway 部署

#### 1. 部署后端到 Railway
```bash
# 安装 Railway CLI
npm install -g @railway/cli

# 登录并部署
railway login
railway init
railway deploy
```

#### 2. 部署前端到 Vercel
```bash
# 安装 Vercel CLI
npm install -g vercel

# 部署
vercel --prod
```

#### 3. 更新前端 API 代理配置
部署后需要更新 `app/api/generate/route.ts` 中的后端服务 URL

## 🧪 测试

### 本地测试
1. 启动后端服务：`python backend/main.py`
2. 启动前端服务：`npm run dev`
3. 访问 http://localhost:3000
4. 上传测试图片，验证生成流程

### API 测试
```bash
curl -X GET http://localhost:8000/health
```

## 📝 注意事项

1. **API Key 安全**：请勿将 API Key 提交到代码仓库
2. **CORS 配置**：生产环境请配置正确的跨域访问策略
3. **文件大小限制**：前端和后端均限制图片大小为 10MB
4. **超时设置**：API 请求超时时间为 60 秒

## 🐛 常见问题

### Q: 图片上传失败？
A: 检查图片格式是否为 JPG/PNG，且大小不超过 10MB

### Q: 生成失败？
A: 检查后端服务是否启动，API Key 是否配置正确

### Q: 生成速度慢？
A: AI 生成通常需要 10-30 秒，请耐心等待

## 📄 许可证

MIT License

## 👥 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

如有问题，请提交 GitHub Issue

---

Built with ❤️ using Next.js, FastAPI, and Volcengine Doubao API
