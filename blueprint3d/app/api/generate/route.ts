import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()

    // 在 Render 中，前后端在同一项目，可使用相对路径
    // 开发环境使用 localhost，生产环境使用内部服务名
    const isDevelopment = process.env.NODE_ENV === 'development'
    const apiUrl = isDevelopment
      ? (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000')
      : `http://blueprint3d-backend:${process.env.PORT || 10000}`

    const response = await fetch(`${apiUrl}/api/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    })

    const data = await response.json()
    return NextResponse.json(data, { status: response.status })
  } catch (error) {
    console.error('API proxy error:', error)
    return NextResponse.json(
      { success: false, detail: 'Failed to connect to backend service' },
      { status: 500 }
    )
  }
}
