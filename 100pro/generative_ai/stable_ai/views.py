from django.shortcuts import render, redirect
import requests
import base64
import os
from .forms import ImageForm

engine_id = "stable-diffusion-xl-1024-v1-0"
api_host = os.getenv('API_HOST', 'https://api.stability.ai')
api_key = os.getenv("STABILITY_API_KEY")

if api_key is None:
    raise Exception("Missing Stability API key.")

def index(request):
    if request.method == "POST":
        response = requests.post(
            f"{api_host}/v1/generation/{engine_id}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "text_prompts": [
                    {
                        "text": "Girls With boyfriend"
                    }
                ],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30,
            },
        )

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        data = response.json()

        for i, image in enumerate(data["artifacts"]):
            with open(f"./media/v1_txt2img_{i}.png", "wb") as f:
                f.write(base64.b64decode(image["base64"]))

        return redirect('index')
    
    return render(request, 'stable_ai/index.html')

def masking_upload(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('masking_result')
        else:
            print(form.errors)
    return render(request, 'stable_ai/masking_upload.html')

def masking_result(request):
    return render(request, 'stable_ai/masking_result.html')
