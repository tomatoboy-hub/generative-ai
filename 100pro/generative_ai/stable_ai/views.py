from django.shortcuts import render, redirect,get_object_or_404
import requests
import base64
import os
from .forms import ImageForm
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from PIL import Image
import io
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
def masking_upload(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            img = Image.open('media/masking/Inpainting-C1.png')

            mask = Image.open('media/masking/Inpainting-C3.png')


            # Set up our connection to the API.
            stability_api = client.StabilityInference(
                key=api_key, # API Key reference.
                verbose=True, # Print debug messages.
                engine="stable-diffusion-xl-1024-v1-0", # Set the engine to use for generation.
                # Check out the following link for a list of available engines: https://platform.stability.ai/docs/features/api-parameters#engine
            )

            answers = stability_api.generate(
                prompt="crayon drawing of rocket ship launching from forest",
                init_image=img,
                mask_image=mask,
                start_schedule=1,
                seed=1234, # If attempting to transform an image that was previously generated with our API,
                            # initial images benefit from having their own distinct seed rather than using the seed of the original image generation.
                steps=50, # Amount of inference steps performed on image generation. Defaults to 30.
                cfg_scale=8.0, # Influences how strongly your generation is guided to match your prompt.
                            # Setting this value higher increases the strength in which it tries to match your prompt.
                            # Defaults to 7.0 if not specified.
                width=1024, # Generation width, if not included defaults to 512 or 1024 depending on the engine.
                height=1024, # Generation height, if not included defaults to 512 or 1024 depending on the engine.
                sampler=generation.SAMPLER_K_DPMPP_2M # Choose which sampler we want to denoise our generation with.
                                                            # Defaults to k_lms if not specified. Clip Guidance only supports ancestral samplers.
                                                            # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m, k_dpmpp_sde)
            )

            # Set up our warning to print to the console if the adult content classifier is tripped. If adult content classifier is not tripped, display generated image.
            for resp in answers:
                for artifact in resp.artifacts:
                    if artifact.finish_reason == generation.FILTER:
                        warnings.warn(
                            "Your request activated the API's safety filters and could not be processed."
                            "Please modify the prompt and try again.")
                    if artifact.type == generation.ARTIFACT_IMAGE:
                        img2 = Image.open(io.BytesIO(artifact.binary))
            img2.save('media/masking/image2.png')






            return redirect('masking_result')
        else:
            print(form.errors)
    return render(request, 'stable_ai/masking_upload.html')

def masking_result(request):
    return render(request, 'stable_ai/masking_result.html')


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
