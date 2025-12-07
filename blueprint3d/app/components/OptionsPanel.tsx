'use client'

import { GenerationSettings } from '../page'

interface OptionsPanelProps {
  settings: GenerationSettings
  onSettingsChange: (settings: Partial<GenerationSettings>) => void
}

export default function OptionsPanel({ settings, onSettingsChange }: OptionsPanelProps) {
  const viewAngles = [
    { value: 'perspective', label: '透视图', icon: '🔭' },
    { value: 'front', label: '正视图', icon: '📐' },
    { value: 'side', label: '侧视图', icon: '📏' },
    { value: 'top', label: '俯视图', icon: '📊' },
  ]

  const styles = [
    { value: 'realistic', label: '写实风格', icon: '🎨', desc: '高质量渲染，专业建筑效果' },
    { value: 'technical', label: '技术线稿', icon: '✏️', desc: '黑白线条，工程图纸风格' },
    { value: 'cartoon', label: '简约卡通', icon: '🌈', desc: '明亮色彩，扁平化设计' },
  ]

  return (
    <div>
      <div className="form-group">
        <label>视角选择</label>
        <div className="options-group">
          {viewAngles.map((angle) => (
            <label
              key={angle.value}
              className={`option-item ${settings.viewAngle === angle.value ? 'selected' : ''}`}
            >
              <input
                type="radio"
                name="viewAngle"
                value={angle.value}
                checked={settings.viewAngle === angle.value}
                onChange={(e) => onSettingsChange({ viewAngle: e.target.value })}
              />
              <span style={{ marginRight: '8px' }}>{angle.icon}</span>
              <span>{angle.label}</span>
            </label>
          ))}
        </div>
      </div>

      <div className="form-group">
        <label>风格选择</label>
        <div className="options-group">
          {styles.map((style) => (
            <label
              key={style.value}
              className={`option-item ${settings.style === style.value ? 'selected' : ''}`}
              style={{ flexDirection: 'column', alignItems: 'flex-start' }}
            >
              <div style={{ display: 'flex', alignItems: 'center', width: '100%' }}>
                <input
                  type="radio"
                  name="style"
                  value={style.value}
                  checked={settings.style === style.value}
                  onChange={(e) => onSettingsChange({ style: e.target.value })}
                />
                <span style={{ marginRight: '8px', marginLeft: '8px' }}>{style.icon}</span>
                <span style={{ fontWeight: 500 }}>{style.label}</span>
              </div>
              <span style={{ fontSize: '0.85rem', color: '#666', marginLeft: '28px', marginTop: '4px' }}>
                {style.desc}
              </span>
            </label>
          ))}
        </div>
      </div>

      <div style={{ marginTop: '30px', padding: '15px', background: '#f8f9ff', borderRadius: '8px', fontSize: '0.9rem', color: '#666' }}>
        <strong>💡 提示：</strong>
        <ul style={{ marginTop: '8px', marginLeft: '20px', lineHeight: '1.6' }}>
          <li>写实风格：适合展示最终效果</li>
          <li>技术线稿：适合工程分析</li>
          <li>简约卡通：适合快速预览</li>
        </ul>
      </div>
    </div>
  )
}
