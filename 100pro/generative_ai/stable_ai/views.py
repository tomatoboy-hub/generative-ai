from django.shortcuts import render, redirect
import requests
import base64
import os
from .forms import ImageForm
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from PIL import Image
import io

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
