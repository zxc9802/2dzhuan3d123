"""
测试不同视角的提示词生成
"""
import sys
sys.path.append('backend')

from backend.templates.prompts import build_prompt

# 测试描述
test_description = "现代办公大楼，玻璃幕墙，矩形结构"

print("=" * 80)
print("提示词优化测试 - 不同视角对比")
print("=" * 80)

views = ["top", "front", "side", "perspective"]

for view in views:
    print(f"\n\n{'='*80}")
    print(f"视角: {view.upper()}")
    print('='*80)
    prompt = build_prompt(test_description, view, "realistic")
    print(prompt)
    print("\n")
