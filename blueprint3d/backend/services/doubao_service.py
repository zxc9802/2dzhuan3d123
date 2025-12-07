import os
import requests
from typing import Optional

class DoubaoService:
    """Service for interacting with Volcengine Doubao image generation API"""

    def __init__(self):
        self.api_key = os.getenv("DOBAO_API_KEY", "95d2a060-7ab5-4fdc-92bf-d9da19aa652c")
        self.api_url = os.getenv("DOBAO_API_URL", "https://ark.cn-beijing.volces.com/api/v3/images/generations")
        self.model = os.getenv("DOBAO_MODEL", "doubao-seedream-4-5-251128")

    def generate_image(
        self,
        image_data: str,
        prompt: str,
        size: str = "2K",
        watermark: bool = False
    ) -> Optional[str]:
        """
        Generate image using Doubao API

        Args:
            image_data: Base64 encoded image or image URL
            prompt: Text prompt for generation
            size: Image size (default: 2K)
            watermark: Whether to add watermark (default: False)

        Returns:
            Generated image URL or None if failed
        """
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "image": image_data,
                "size": size,
                "watermark": watermark
            }

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("data", {}).get("url", "")
            else:
                print(f"API request failed with status {response.status_code}: {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None
