"""
测试脚本：验证 Doubao API 连接和生成功能
"""

import base64
import os
import sys

# 添加 backend 目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from services.doubao_service import DoubaoService

def encode_image_to_base64(image_path):
    """将图片文件编码为 base64"""
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:image/png;base64,{encoded_string}"

def test_doubao_api():
    """测试 Doubao API"""
    print("🚀 开始测试 Doubao API...")
    print("=" * 50)

    # 初始化服务
    service = DoubaoService()
    print(f"✓ API URL: {service.api_url}")
    print(f"✓ 模型: {service.model}")
    print(f"✓ API Key: {service.api_key[:10]}...")
    print()

    # 测试用例
    test_cases = [
        {
            "name": "钢结构厂房",
            "prompt": "将这个工程图纸转换为透视的3D效果图，写实风格，高质量渲染，专业建筑可视化效果。钢结构厂房平面图，包含主结构、支撑系统、屋面和墙体结构。",
            "viewAngle": "perspective",
            "style": "realistic"
        },
        {
            "name": "技术线稿风格",
            "prompt": "将这个工程图纸转换为侧视图的3D效果图，技术线稿风格，黑白线条图，工程图纸风格。",
            "viewAngle": "side",
            "style": "technical"
        },
        {
            "name": "简约卡通风格",
            "prompt": "将这个工程图纸转换为俯视图的3D效果图，简约卡通风格，明亮色彩，扁平化设计。",
            "viewAngle": "top",
            "style": "cartoon"
        }
    ]

    # 模拟测试（实际测试需要真实图片）
    for i, test_case in enumerate(test_cases, 1):
        print(f"测试用例 {i}: {test_case['name']}")
        print(f"  视角: {test_case['viewAngle']}")
        print(f"  风格: {test_case['style']}")
        print(f"  提示词: {test_case['prompt'][:50]}...")
        print(f"  状态: ⏳ 待测试")
        print()

    print("=" * 50)
    print("💡 使用说明:")
    print("  1. 确保已配置正确的 API Key")
    print("  2. 准备测试图片（建议 1024x1024 或更高分辨率）")
    print("  3. 修改代码中的 image_data 参数")
    print("  4. 运行服务测试完整流程")
    print()

if __name__ == "__main__":
    test_doubao_api()
