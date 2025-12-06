"use client";

interface OptionsPanelProps {
    viewAngle: string;
    setViewAngle: (val: string) => void;
    style: string;
    setStyle: (val: string) => void;
    description: string;
    setDescription: (val: string) => void;
    onGenerate: () => void;
    isGenerating: boolean;
    canGenerate: boolean;
}

export default function OptionsPanel({
    viewAngle,
    setViewAngle,
    style,
    setStyle,
    description,
    setDescription,
    onGenerate,
    isGenerating,
    canGenerate
}: OptionsPanelProps) {
    return (
        <>
            <div className="form-group">
                <label className="label">2. 补充描述 (可选)</label>
                <textarea
                    className="textarea"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    placeholder="例如：这是一张钢结构厂房的平面图，屋顶有天窗..."
                />
            </div>

            <div className="form-group">
                <label className="label">3. 视角选择</label>
                <select
                    className="select"
                    value={viewAngle}
                    onChange={(e) => setViewAngle(e.target.value)}
                >
                    <option value="perspective">透视图 (Perspective)</option>
                    <option value="top">俯视图 (Top View)</option>
                    <option value="front">正视图 (Front View)</option>
                    <option value="side">侧视图 (Side View)</option>
                </select>
            </div>

            <div className="form-group">
                <label className="label">4. 风格选择</label>
                <select
                    className="select"
                    value={style}
                    onChange={(e) => setStyle(e.target.value)}
                >
                    <option value="realistic">写实渲染 (Realistic)</option>
                    <option value="technical">技术线稿 (Technical)</option>
                    <option value="cartoon">简约卡通 (Cartoon)</option>
                </select>
            </div>

            <div style={{ marginTop: 'auto' }}>
                <button
                    className="button"
                    onClick={onGenerate}
                    disabled={!canGenerate || isGenerating}
                >
                    {isGenerating ? "正在生成..." : "生成 3D 效果图"}
                </button>
            </div>
        </>
    );
}
