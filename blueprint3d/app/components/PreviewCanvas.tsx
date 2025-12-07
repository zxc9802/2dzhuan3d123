'use client'

interface PreviewCanvasProps {
  imageUrl?: string
  isGenerating: boolean
  processingTime?: number
}

export default function PreviewCanvas({ imageUrl, isGenerating, processingTime }: PreviewCanvasProps) {
  return (
    <div className="preview-canvas">
      {isGenerating && (
        <div style={{ textAlign: 'center' }}>
          <div className="loading-spinner" style={{ margin: '0 auto 20px' }} />
          <div style={{ color: '#666' }}>
            AI正在生成3D效果图中...
            {processingTime && <div style={{ fontSize: '0.85rem', marginTop: '5px' }}>已用时 {processingTime}s</div>}
          </div>
        </div>
      )}

      {!isGenerating && !imageUrl && (
        <div className="preview-placeholder">
          <div style={{ fontSize: '4rem', marginBottom: '15px' }}>🎨</div>
          <div style={{ fontSize: '1.1rem', color: '#666' }}>
            上传图片并点击生成按钮
          </div>
          <div style={{ fontSize: '0.9rem', color: '#999', marginTop: '8px' }}>
            即可查看3D可视化效果
          </div>
        </div>
      )}

      {!isGenerating && imageUrl && (
        <img
          src={imageUrl}
          alt="Generated 3D visualization"
          className="preview-image"
          style={{ maxHeight: '500px' }}
        />
      )}
    </div>
  )
}
