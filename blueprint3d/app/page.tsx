"use client";

import { useState } from "react";
import ImageUpload from "./components/ImageUpload";
import PreviewCanvas from "./components/PreviewCanvas";

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [description, setDescription] = useState("");
  const [viewAngle, setViewAngle] = useState("perspective");
  const [style, setStyle] = useState("realistic");
  const [isGenerating, setIsGenerating] = useState(false);
  const [resultUrl, setResultUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async () => {
    if (!selectedFile) return;

    setIsGenerating(true);
    setError(null);
    setResultUrl(null);

    const formData = new FormData();
    formData.append("image", selectedFile);
    formData.append("description", description);
    formData.append("viewAngle", viewAngle);
    formData.append("style", style);

    try {
      const response = await fetch("http://localhost:8000/api/generate", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "生成失败");
      }

      if (data.success && data.imageUrl) {
        setResultUrl(`http://localhost:8000${data.imageUrl}`);
      } else {
        throw new Error("API未返回图片链接");
      }
    } catch (err: any) {
      console.error(err);
      setError(err.message || "请求发生错误，请重试");
    } finally {
      setIsGenerating(false);
    }
  };

  const handleDownload = () => {
    if (resultUrl) {
      const link = document.createElement('a');
      link.href = resultUrl;
      link.download = `blueprint3d-${Date.now()}.png`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  return (
    <div className="container">
      <header className="header">
        <div className="logo">Blueprint3D</div>
        <div className="text-secondary">v1.0</div>
      </header>

      <main className="main-layout">
        {/* Left Column: Upload + Description + Generate */}
        <aside className="panel">
          <ImageUpload
            onImageSelect={setSelectedFile}
            selectedImage={selectedFile}
          />

          <div className="form-group">
            <label className="label">2. 补充描述 (可选)</label>
            <textarea
              className="textarea"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="例如：这是一张钢结构厂房的平面图，屋顶有天窗..."
            />
          </div>

          <div style={{ marginTop: 'auto' }}>
            {error && <div className="error-message" style={{ marginBottom: '1rem' }}>{error}</div>}

            <button
              className="button"
              onClick={handleGenerate}
              disabled={!selectedFile || isGenerating}
            >
              {isGenerating ? "正在生成..." : "生成 3D 效果图"}
            </button>
          </div>
        </aside>

        {/* Center Column: Preview */}
        <section className="panel" style={{ background: 'white', flex: 1, padding: '1rem', overflow: 'hidden' }}>
          <PreviewCanvas
            resultUrl={resultUrl}
            isGenerating={isGenerating}
            onDownload={handleDownload}
          />
        </section>

        {/* Right Column: Settings */}
        <aside className="panel">
          <h3 className="label" style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>生成设置</h3>

          <div className="form-group">
            <label className="label">3. 视角选择</label>
            <div className="text-xs text-secondary mb-2">选择生成图像的相机视角</div>
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
            <div className="text-xs text-secondary mb-2">选择渲染的艺术风格</div>
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

          <div className="mt-auto p-4 bg-blue-50 rounded-lg text-sm text-blue-800" style={{ background: '#eff6ff', color: '#1e40af' }}>
            <strong>💡 提示:</strong>
            <p className="mt-1">上传清晰的平面图，并在描述中补充材质或颜色信息，效果会更好。</p>
          </div>
        </aside>
      </main>
    </div>
  );
}
