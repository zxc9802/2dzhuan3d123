"""
Prompt Templates for 3D Generation
根据不同的视角和风格构建AI提示词 - 专业工程图纸版本
"""

# 视角描述映射 - 更专业和精确的描述
VIEW_ANGLES = {
    "top": {
        "name": "正交俯视图",
        "camera": "Camera positioned directly above the structure at 90° perpendicular angle (0° elevation, 90° to horizontal plane)",
        "requirement": "STRICT top-down orthographic view with camera pointing straight down. No perspective distortion, no angled views. Show the structure as if looking from directly above using parallel projection."
    },
    "front": {
        "name": "正交正视图",
        "camera": "Camera positioned directly in front at 0° horizontal angle (eye-level, perpendicular to front face)",
        "requirement": "STRICT front orthographic view with camera facing the front elevation. No rotation, no perspective. Show the primary facade as seen from straight ahead using parallel projection."
    },
    "side": {
        "name": "正交侧视图",
        "camera": "Camera positioned at 90° to the front face (side elevation view)",
        "requirement": "STRICT side orthographic view showing the lateral elevation. Camera perpendicular to the side face. No perspective distortion."
    },
    "perspective": {
        "name": "透视图",
        "camera": "Camera positioned at 30-45° elevation angle with slight rotation for 3-point perspective",
        "requirement": "3D perspective view showing depth and dimension. Use realistic perspective with vanishing points to show the structure in three dimensions."
    }
}

# 风格描述映射
STYLES = {
    "realistic": {
        "name": "写实渲染",
        "description": "Photorealistic 3D rendering with detailed materials, accurate lighting (sunlight + ambient), realistic shadows and reflections, professional architectural visualization quality"
    },
    "technical": {
        "name": "技术线稿",
        "description": "Technical line drawing style with clean black lines on white background, precise edges, minimal shading, blueprint aesthetic, professional engineering schematic appearance"
    },
    "cartoon": {
        "name": "简约卡通",
        "description": "Simplified 3D illustration with clean geometric shapes, smooth surfaces, soft pastel colors, minimal details, friendly and accessible artistic style"
    }
}

def build_prompt(description: str, view_angle: str, style: str) -> str:
    """
    构建完整的AI生成提示词 - 强调一致性和准确性
    
    Args:
        description: 用户输入的图纸描述
        view_angle: 视角选择 (front/side/top/perspective)
        style: 风格选择 (realistic/technical/cartoon)
    
    Returns:
        完整的提示词字符串
    """
    view_config = VIEW_ANGLES.get(view_angle, VIEW_ANGLES["perspective"])
    style_config = STYLES.get(style, STYLES["realistic"])
    
    # 基础结构描述（确保一致性）
    base_context = f"""
TASK: Generate a 3D architectural/engineering visualization from the provided technical drawing.

SUBJECT DESCRIPTION: {description if description.strip() else "engineering structure or building from the technical blueprint"}

CRITICAL CONSISTENCY REQUIREMENT:
- The 3D model MUST represent the EXACT SAME structure shown in the reference image
- Maintain the same architectural elements, proportions, and design features across all views
- Do NOT change the building type, structure, or overall design
- Only the camera angle should change, the subject remains identical
"""

    # 视角要求
    view_requirement = f"""
VIEW ANGLE: {view_config['name']}
Camera Setup: {view_config['camera']}
Strict Requirement: {view_config['requirement']}
"""

    # 渲染风格
    style_requirement = f"""
RENDERING STYLE: {style_config['name']}
Style Description: {style_config['description']}
"""

    # 技术要求
    technical_requirements = """
TECHNICAL SPECIFICATIONS:
1. Accuracy: Convert 2D blueprint to 3D while preserving exact proportions and dimensions
2. Detail Level: Include all structural elements visible in the source drawing
3. Spatial Relationships: Maintain correct relative positions and alignments
4. Clean Output: White or neutral background, focus on the structure
5. Professional Quality: High resolution suitable for engineering presentation
6. Material Consistency: Use appropriate materials based on the building type (concrete, steel, glass, etc.)
"""

    # 特殊约束（针对不同视角）
    if view_angle == "top":
        special_constraint = """
SPECIAL CONSTRAINT FOR TOP VIEW:
- Camera must be EXACTLY perpendicular to the ground plane
- Zero tilt, zero rotation from vertical axis
- Show roof plan or ceiling layout as primary element
- Use orthographic projection (NO perspective distortion)
- Do NOT show any side walls or front facade
"""
    elif view_angle in ["front", "side"]:
        special_constraint = """
SPECIAL CONSTRAINT FOR ORTHOGRAPHIC VIEW:
- Use parallel projection (NO vanishing points)
- All vertical lines remain vertical
- All horizontal lines remain horizontal
- No perspective distortion or depth compression
- Show elevation drawing style
"""
    else:
        special_constraint = """
SPECIAL CONSTRAINT FOR PERSPECTIVE VIEW:
- Use 3-point perspective for realistic depth
- Position camera to show primary facade plus one or two additional sides
- Include realistic depth cues with appropriate foreshortening
"""

    # 组合完整提示词
    full_prompt = f"""{base_context}
{view_requirement}
{style_requirement}
{technical_requirements}
{special_constraint}

OUTPUT: Generate ONE clear, professional-quality 3D visualization following ALL requirements above.
"""

    return full_prompt.strip()
