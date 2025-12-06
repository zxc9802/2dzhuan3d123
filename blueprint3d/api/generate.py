"""
Vercel Serverless Function for /api/generate
"""
import os
import httpx
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json
import uuid
import tempfile
from PIL import Image
import io
import base64

# Request models
class Point(BaseModel):
    x: int
    y: int

class GenerateRequest(BaseModel):
    points: List[Point]
    prompt: str
    negative_prompt: str = "low quality, blurry, distortion"

app = FastAPI()

@app.post("/generate")
async def generate_image(request: GenerateRequest):
    """
    Generate 3D image from 2D blueprint points
    """
    try:
        # Get API key from environment variables
        api_key = os.getenv("ARK_API_KEY")
        if not api_key:
            raise Exception("ARK_API_KEY not configured")

        # Convert points to a simple string representation
        points_str = ",".join([f"({p.x},{p.y})" for p in request.points])

        # Create the ARK API request
        url = "https://ark.cn-beijing.volces.com/api/v3/image/synthesis"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Create a simple text prompt based on points
        enhanced_prompt = f"{request.prompt}. 2D blueprint points: {points_str}. Convert to 3D visualization."

        data = {
            "model": "ep-20241203143501-q4lqv",
            "prompt": enhanced_prompt,
            "negative_prompt": request.negative_prompt,
            "size": "512x512",
            "n": 1
        }

        # Call ARK API
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()

            result = response.json()

            # Extract image URL
            image_url = result.get("data", [{}])[0].get("url", "")

            if not image_url:
                raise Exception("No image URL in response")

            # Download and save the image temporarily
            img_response = await client.get(image_url)
            img_response.raise_for_status()

            # Convert image to Base64
            img = Image.open(io.BytesIO(img_response.content))
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            
            return {
                "status": "success",
                "image_url": f"data:image/png;base64,{img_str}",
                "filename": "generated.png"
            }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# For non-FastAPI deployment
async def handler(request):
    """
    Vercel serverless function handler
    """
    try:
        # Parse request body
        body = await request.json()

        # Create request object
        generate_request = GenerateRequest(**body)

        # Process request
        result = await generate_image(generate_request)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization"
            },
            "body": json.dumps(result)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "status": "error",
                "message": str(e)
            })
        }