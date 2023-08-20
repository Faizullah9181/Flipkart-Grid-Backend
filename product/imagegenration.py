import requests
import io
import base64
from PIL import Image
import cloudinary
import cloudinary.uploader


def upload_image(image):
    upload_result = cloudinary.uploader.upload(image, folder="product")
    return upload_result["secure_url"]


def get_image(prompt):
    url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
    payload = {
        "prompt": prompt,
        "steps": 20,
        "negative_prompt": "",
        "sampler_name": "Euler a",
        "cfg_scale": 7,
        "seed": -1,
        "width": 512,
        "height": 512
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        image_data = response.json()["images"]
        image_data = image_data[0]
        img = io.BytesIO(base64.decodebytes(bytes(image_data, "utf-8")))
        data = upload_image(img)
        return data
    else:
        return f"Request failed with status code: {response.status_code}"


def get_image_from_image(prompt, image_url):
    
    response = requests.get(image_url)
    
    if response.status_code == 200:
        image_content = response.content
        base64_image = base64.b64encode(image_content).decode('utf-8')
        
        url = "http://127.0.0.1:7860/sdapi/v1/img2img"
        payload = {
            "init_images": [base64_image],
            "prompt": prompt,
            "steps": 100,
            "negative_prompt": "",
            "sampler_name": "Euler a",
            "cfg_scale": 7,
            "seed": -1,
            "width": 512,
            "height": 512
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            image_data = response.json()["images"]
            image_data = image_data[0]
            img = io.BytesIO(base64.decodebytes(bytes(image_data, "utf-8")))
            data = upload_image(img)
            return data

        else:
            return f"Request failed with status code: {response.status_code}"

    else:
        return f"Failed to download the image. Status code: {response.status_code}"
