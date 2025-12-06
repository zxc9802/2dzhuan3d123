import requests
import base64
import os
import json

def test_api():
    url = "http://localhost:8000/api/generate"
    image_path = "test_input.png"
    
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found")
        return

    print("Sending request to backend...")
    
    files = {
        'image': ('test_input.png', open(image_path, 'rb'), 'image/png')
    }
    data = {
        'description': 'Modern office building test',
        'viewAngle': 'perspective',
        'style': 'realistic'
    }
    
    try:
        response = requests.post(url, files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("SUCCESS! Image generated.")
                print(f"Image URL: {result.get('imageUrl')}")
                print(f"Processing Time: {result.get('processingTime')}s")
            else:
                print("FAILED in logic.")
                print(result)
        else:
            print(f"FAILED with status {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Exception: {str(e)}")

if __name__ == "__main__":
    test_api()
