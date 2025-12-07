'use client'

import { useState } from 'react'
import ImageUpload from './components/ImageUpload'
import PreviewCanvas from './components/PreviewCanvas'
import OptionsPanel from './components/OptionsPanel'

export interface GenerationSettings {
  viewAngle: string
  style: string
  description: string
}

export interface GeneratedImage {
  url: string
  processingTime: number
}

export default function Home() {
  const [uploadedImage, setUploadedImage] = useState<string>('')
  const [generatedImage, setGeneratedImage] = useState<GeneratedImage | null>(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const [error, setError] = useState('')
  const [settings, setSettings] = useState<GenerationSettings>({
    viewAngle: 'perspective',
    style: 'realistic',
    description: ''
  })

  const handleImageUpload = (imageData: string) => {
    setUploadedImage(imageData)
    setGeneratedImage(null)
    setError('')
  }

  const handleSettingsChange = (newSettings: Partial<GenerationSettings>) => {
    setSettings(prev => ({ ...prev, ...newSettings }))
  }

  const handleGenerate = async () => {
    if (!uploadedImage) {
      setError('请先上传图片')
      return
    }

    setIsGenerating(true)
    setError('')

    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image: uploadedImage,
          description: settings.description,
          viewAngle: settings.viewAngle,
          style: settings.style
        }),
      })

      const data = await response.json()

      if (!response.ok || !data.success) {
        throw new Error(data.detail || '生成失败')
      }

      setGeneratedImage({
        url: data.imageUrl,
        processingTime: data.processingTime
      })
    } catch (err) {
      setError(err instanceof Error ? err.message : '生成失败，请重试')
    } finally {
      setIsGenerating(false)
    }
  }

  const handleRegenerate = () => {
    handleGenerate()
  }

  const handleDownload = async () => {
    if (!generatedImage) return

    try {
      const response = await fetch(generatedImage.url)
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `blueprint3d-${Date.now()}.png`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err) {
      setError('下载失败')
    }
  }

  return (
    <div className="container">
      <header className="header">
        <h1>Blueprint3D</h1>
        <p>一键将工程图纸转化为3D可视化效果图</p>
      </header>

      <div className="main-layout">
        <div className="panel">
          <h2>上传图纸</h2>
          <ImageUpload onImageUpload={handleImageUpload} />

          {uploadedImage && (
            <div className="uploaded-image-preview" style={{ marginTop: '20px' }}>
              <h3>已上传的图片</h3>
              <img
                src={uploadedImage}
                alt="Uploaded blueprint"
                style={{
                  maxWidth: '100%',
                  maxHeight: '300px',
                  borderRadius: '8px',
                  marginTop: '10px',
                  objectFit: 'contain'
                }}
              />
            </div>
          )}

          <div className="form-group" style={{ marginTop: '20px' }}>
            <label>补充描述（可选）</label>
            <textarea
              placeholder="请描述图纸的关键信息，例如：钢结构厂房平面图、尺寸标注等..."
              value={settings.description}
              onChange={(e) => handleSettingsChange({ description: e.target.value })}
            />
          </div>

          <button
            className="button"
            onClick={handleGenerate}
            disabled={!uploadedImage || isGenerating}
          >
            {isGenerating ? '生成中...' : '生成3D效果图'}
          </button>
        </div>

        <div className="panel">
          <h2>预览效果</h2>
          <PreviewCanvas
            imageUrl={generatedImage?.url}
            isGenerating={isGenerating}
            processingTime={generatedImage?.processingTime}
          />

          {generatedImage && (
            <div className="preview-actions">
              <button className="button" onClick={handleRegenerate}>
                重新生成
              </button>
              <button className="button" onClick={handleDownload}>
                下载图片
              </button>
            </div>
          )}
        </div>

        <div className="panel">
          <h2>生成设置</h2>
          <OptionsPanel
            settings={settings}
            onSettingsChange={handleSettingsChange}
          />
        </div>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {generatedImage && (
        <div className="success-message">
          生成成功！用时 {generatedImage.processingTime} 秒
        </div>
      )}
    </div>
  )
}
