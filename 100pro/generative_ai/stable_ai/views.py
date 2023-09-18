'''
画像をリサイズして補完する必要あり
くそめんどくせえ
https://murasan-net.com/index.php/2023/03/07/automatic1111-img2img/
'''

import requests
import base64
import os
from .forms import ImageForm
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from PIL import Image
import io
import random
from .forms import SnsForm, GenerateImageForm, GenerateImageToImageForm, ImageUploadForm
from .models import SnsModel, UploadedImage
import glob
from PIL import Image
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

engine_id = "stable-diffusion-xl-1024-v1-0"
api_host = os.getenv('API_HOST', 'https://api.stability.ai')
# api_key = os.getenv("STABILITY_API_KEY")
api_key = "sk-WSGCH3VWaCUlfTFVVjSijUJUJg4fVqWhuf8zUD34ylRQSwoQ"

if api_key is None:
    raise Exception("Missing Stability API key.")

def add_margin(pil_img):
    width, height = pil_img.size
    new_width = 1024
    new_height = 1024
    result = Image.new(pil_img.mode, (new_width, new_height), 'white')
    result.paste(pil_img, (512-int((width/2)), 512-int((height/2))))
    # result.paste(pil_img, (10, 10))
    return result

def index(request):
    form = GenerateImageForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        text_prompt = form.cleaned_data['text_prompt']
        cfg_scale = form.cleaned_data['cfg_scale']
        height = form.cleaned_data['height']
        width = form.cleaned_data['width']
        samples = form.cleaned_data['samples']
        steps = form.cleaned_data['steps']        
        
        print(text_prompt)
        
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
            with open(f"./media/im2im_generated.png", "wb") as f:
                f.write(base64.b64decode(image["base64"]))        

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
    images =UploadedImage.objects.all()
    return render(request, 'stable_ai/image_list.html', {'images': images})


def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        print(form)
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

def txtotx(request):
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
        os.remove('../generative_ai/media/uploaded_images/createimage.png')
        

        for i, image in enumerate(data["artifacts"]):
            image_data = base64.b64decode(image["base64"])
            image_name = "createimage.png"
            image_file = BytesIO(image_data)
            file = InMemoryUploadedFile(image_file, None, image_name, 'image/png', len(image_data), None)

            # モデルインスタンスを作成し、データベースに保存
            uploaded_image = UploadedImage(image=file)
            uploaded_image.save()
            
            print("パージを遷移")
            
            return redirect('txtoim') 

    return render(request, 'stable_ai/txtotx.html', {'form': form})

def txtoim(request):
    print(request.method)
    new_form = GenerateImageToImageForm(request.POST or None)
    form = SnsForm(request.POST, request.FILES)
    
    print(new_form.is_valid())
    if request.method == "POST":
        print(new_form.errors)
        if new_form.is_valid():
            image_prompt = new_form.cleaned_data['image_prompt']
            negative_prompt = new_form.cleaned_data['negative_prompt']
            image_strength = float(new_form.cleaned_data['image_strength'] / 100)
            weight = new_form.cleaned_data['weight'] / 10
            negative_weight = new_form.cleaned_data['negative_weight'] / 10
            cfg_scale = new_form.cleaned_data['cfg_scale']
            samples = new_form.cleaned_data['samples']
            seeds = new_form.cleaned_data['seeds']
            steps = new_form.cleaned_data['steps']     
            print(image_strength)   
        else:
            pass

        print("ok")
        if form.is_valid():
            # comment = form.save(commit=False)
            # # comment.image = request.FILES["image"]
            # comment.image = request.FILES
            # comment.save()
            form.save()
            context = {}
            # images = SnsModel.objects.latest("image")
            dates = SnsModel.objects.latest("posted_date")
            # SnsModelの中身を使う
            context["dates"] = dates
            # print(context)
            print(dates.content)
            
        response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/image-to-image",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        # ここでデータベースから取得しデータベースに入れる
        files={
            # "init_image": open("./media/"+stable_ai.models.file_name, "rb")
            "init_image": open("./media/uploaded_images/createimage.png", "rb")
        },
        data={           
            "init_image_mode": "IMAGE_STRENGTH",
            "init_image": "<image binary>",
            "clip_guidance_preset": "FAST_BLUE",
            "sampler": "K_DPM_2_ANCESTRAL",
            "image_strength": image_strength,
            "text_prompts[0][text]": image_prompt,
            "text_prompts[0][weight]": weight,
            "text_prompts[1][text]": negative_prompt,
            "text_prompts[1][weight]": negative_weight,
            "cfg_scale": cfg_scale,
            "samples": samples,
            "seed": seeds,
            "steps": steps
        }
    )        
    
        if response.status_code != 200:
            print(response.status_code)
            raise Exception("Non-200 response: " + str(response.text))

        data = response.json()

        for i, image in enumerate(data["artifacts"]):
            with open(f"./media/uploaded_images/createimage.png", "wb") as f:
                f.write(base64.b64decode(image["base64"]))

        # return render('generated', context)
        return render(request, 'stable_ai/onepro_generated.html',context)
        # return redirect('../generated/',context)
    else:
        return render(request, 'stable_ai/txtoim.html', {'new_form': new_form})


def im2im(request):
    print(request.method)
    screen_form = GenerateImageToImageForm(request.POST or None)
    form = SnsForm(request.POST, request.FILES)

    if request.method == "POST":
        if screen_form.is_valid():
            image_prompt = screen_form.cleaned_data['image_prompt']
            negative_prompt = screen_form.cleaned_data['negative_prompt']
            image_strength = float(screen_form.cleaned_data['image_strength'] / 100)
            weight = screen_form.cleaned_data['weight'] / 10
            negative_weight = screen_form.cleaned_data['negative_weight'] / 10
            cfg_scale = screen_form.cleaned_data['cfg_scale']
            samples = screen_form.cleaned_data['samples']
            seeds = screen_form.cleaned_data['seeds']
            steps = screen_form.cleaned_data['steps']        
        else:
            print(screen_form.errors)

        print("ok")
        if form.is_valid():
            # comment = form.save(commit=False)
            # # comment.image = request.FILES["image"]
            # comment.image = request.FILES
            # comment.save()
            form.save()
            context = {}
            # images = SnsModel.objects.latest("image")
            dates = SnsModel.objects.latest("posted_date")
            # SnsModelの中身を使う
            context["dates"] = dates
            # print(context)
            
            # 取得した画像の名前をmedia/changed.に変更する
            def_name = str(dates.image)
            ext = def_name.split('.')[-1]
            new_name = f'../generative_ai/media/changed.{ext}'
            print(str(dates.image))

            os.replace('../generative_ai/media/'+str(dates.image), new_name)
            
            # JPEGの場合はPINGに変更する
            if ext=='jpg':
                new_name = Image.open('../generative_ai/media/changed.jpg')
                new_name.save('../generative_ai/media/changed.png')
                os.remove('../generative_ai/media/changed.jpg')
            else:
                pass
            
            # os.replace('../generative_ai/media/'+str(dates.image), new_name)
            
            # context = {'images':images, 'dates':dates}
            # print(context[])
            # if not context[]:
            #     print("空です")
            resize_name = Image.open('../generative_ai/media/changed.png')
            new_image = add_margin(resize_name)
            new_image.save('../generative_ai/media/changed.png', quality=80)

        else:
            print(form.errors)
            
        # リサイズ前の画像を読み込み
        img = Image.open(new_name)
        # 読み込んだ画像の幅、高さを取得し半分に
        if img.width >=1024:
            (width, height) = ( 1024 , img.height * 1024 // img.width)            
            # 画像をリサイズする
            img_resized = img.resize((width, height))
        elif img.height >= 1024: 
            (width, height) = (img.width *1024 // img.height,  1024 )        
             # 画像をリサイズする
            img_resized = img.resize((width, height))
        # ファイルを保存
        img_resized.save('../generative_ai/media/changed.png', quality=90)
            
        response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/image-to-image",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        # ここでデータベースから取得しデータベースに入れる
        files={
            # "init_image": open("./media/"+stable_ai.models.file_name, "rb")
            "init_image": open("./media/changed.png", "rb")
        },
        data={           
            "init_image_mode": "IMAGE_STRENGTH",
            "init_image": "<image binary>",
            "clip_guidance_preset": "FAST_BLUE",
            "sampler": "K_DPM_2_ANCESTRAL",
            "image_strength": image_strength,
            "text_prompts[0][text]": image_prompt,
            "text_prompts[0][weight]": weight,
            "text_prompts[1][text]": negative_prompt,
            "text_prompts[1][weight]": negative_weight,
            "cfg_scale": cfg_scale,
            "samples": samples,
            "seed": seeds,
            "steps": steps
        }
    )        
    
        if response.status_code != 200:
            print(response.status_code)
            raise Exception("Non-200 response: " + str(response.text))

        data = response.json()

        for i, image in enumerate(data["artifacts"]):
            with open(f"./media/im2im_generated.png", "wb") as f:
                f.write(base64.b64decode(image["base64"]))

        # return render('generated', context)
        return render(request, 'stable_ai/generated.html',context)
        # return redirect('../generated/',context)
    else:
        return render(request, 'stable_ai/im2im.html', {'screen_form': screen_form})

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
                seed=random.randint(1,100), # If attempting to transform an image that was previously generated with our API,
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
def generated(request,context):
        return render(request, 'stable_ai/generated.html',context)
