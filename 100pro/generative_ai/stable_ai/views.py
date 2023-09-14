from django.shortcuts import render, redirect,get_object_or_404
import requests
import base64
import os
from .forms import GenerateImageForm
from .models import UploadedImage
from .forms import ImageUploadForm
from django.http import HttpResponseRedirect
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

engine_id = "stable-diffusion-xl-1024-v1-0"
api_host = os.getenv('API_HOST', 'https://api.stability.ai')
api_key = os.getenv("STABILITY_API_KEY")

if api_key is None:
    raise Exception("Missing Stability API key.")

def index(request):
    form = GenerateImageForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        text_prompt = form.cleaned_data['text_prompt']
        cfg_scale = form.cleaned_data['cfg_scale']
        height = form.cleaned_data['height']
        width = form.cleaned_data['width']
        samples = form.cleaned_data['samples']
        steps = form.cleaned_data['steps']

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
                        "text": text_prompt
                    }
                ],
                "cfg_scale": cfg_scale,
                "height": height,
                "width": width,
                "samples": samples,
                "steps": steps,
            },
        )

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        data = response.json()

        for i, image in enumerate(data["artifacts"]):
            image_data = base64.b64decode(image["base64"])
            image_name = f"v1_txt2img_{i}.png"
            image_file = BytesIO(image_data)
            file = InMemoryUploadedFile(image_file, None, image_name, 'image/png', len(image_data), None)

            # モデルインスタンスを作成し、データベースに保存
            uploaded_image = UploadedImage(image=file)
            uploaded_image.save()

    return render(request, 'stable_ai/index.html', {'form': form})

def image_list(request):
    images = UploadedImage.objects.all()
    return render(request, 'stable_ai/image_list.html', {'images': images})


def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/images/')  # 画像のリストページにリダイレクトする
    else:
        form = ImageUploadForm()

    return render(request, 'stable_ai/upload.html', {'form': form})
def delete_image(request, image_id):
    if request.method == "POST":
        image = get_object_or_404(UploadedImage, id=image_id)
        image.delete()
        return redirect('image_list')