"use client";

interface PreviewCanvasProps {
    resultUrl: string | null;
    isGenerating: boolean;
    onDownload: () => void;
}

export default function PreviewCanvas({
    resultUrl,
    isGenerating,
    onDownload
}: PreviewCanvasProps) {
    return (
        <div style={{ height: '100%', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div className="header" style={{ marginBottom: 0, paddingBottom: 0, border: 'none' }}>
                <h2 className="label" style={{ fontSize: '1.2rem' }}>3D 效果预览</h2>
                {resultUrl && (
                    <button
                        className="button secondary"
                        style={{ width: 'auto', padding: '0.5rem 1rem' }}
                        onClick={onDownload}
                    >
                        下载图片
                    </button>
                )}
            </div>

            <div className="canvas-area">
                {isGenerating && (
                    <div className="loading-overlay">
                        <div className="spinner"></div>
                        <p>正在努力生成中，请稍候...</p>
                        <p className="text-secondary" style={{ fontSize: '0.8rem', marginTop: '0.5rem' }}>通常需要 10-15 秒</p>
                    </div>
                )}

                {resultUrl ? (
                    <img
                        src={resultUrl}
                        alt="3D Result"
                        className="result-image"
                    />
                ) : (
                    !isGenerating && (
                        <div className="empty-state">
                            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" style={{ margin: '0 auto 1rem', color: '#cbd5e1' }}>
                                <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                                <circle cx="8.5" cy="8.5" r="1.5" />
                                <polyline points="21 15 16 10 5 21" />
                            </svg>
                            <p>生成的 3D 效果图将显示在这里</p>
                        </div>
                    )
                )}
            </div>
        </div>
    );
}
