@echo off
echo 🚀 启动 Blueprint3D 服务
echo ==================================
echo.

REM 检查 Node.js
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 错误: 未找到 Node.js，请先安装 Node.js 18+
    pause
    exit /b 1
)

REM 检查 Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 错误: 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo ✅ 环境检查通过
echo.

REM 安装前端依赖
echo 📦 安装前端依赖...
npm install
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 前端依赖安装失败
    pause
    exit /b 1
)
echo.

REM 安装后端依赖
echo 📦 安装后端依赖...
cd backend
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 后端依赖安装失败
    pause
    exit /b 1
)
cd ..
echo.

REM 检查环境变量
if not exist "backend\.env" (
    echo ⚠️  警告: 未找到 backend\.env 文件
    echo 请复制 backend\.env.example 到 backend\.env 并配置您的 API Key
    echo.
)

echo ✅ 安装完成！
echo.
echo 🚀 启动服务...
echo.
echo 请在新终端窗口中分别运行以下命令：
echo.
echo 终端 1 ^(后端^):
echo   cd backend && python main.py
echo.
echo 终端 2 ^(前端^):
echo   cd blueprint3d && npm run dev
echo.
echo 然后访问: http://localhost:3000
echo.
pause
