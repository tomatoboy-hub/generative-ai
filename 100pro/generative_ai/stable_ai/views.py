'''
画像をリサイズして補完する必要あり
くそめんどくせえ
https://murasan-net.com/index.php/2023/03/07/automatic1111-img2img/
'''

import requests
import base64
import os
from .forms import SnsForm, GenerateImageForm, ImageUploadForm
from .models import SnsModel, UploadedImage
import glob
from PIL import Image
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

engine_id = "stable-diffusion-xl-1024-v1-0"
api_host = os.getenv('API_HOST', 'https://api.stability.ai')
api_key = "API"

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

def im2im(request):
    print(request.method)
    if request.method == "POST":
        form = SnsForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            print("OK")
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
            
            print(new_name)
            os.replace('../generative_ai/media/'+str(dates.image), new_name)
            
            # JPEGの場合はPINGに変更する
            if ext=='jpg':
                new_name = Image.open('../generative_ai/media/changed.jpg')
                new_name.save('../generative_ai/media/changed.png')
                os.remove('../generative_ai/media/changed.jpg')
            else:
                pass
            
            # os.replace('../generative_ai/media/'+str(dates.image), new_name)
            
            print('../generative_ai/media/'+str(dates.image))
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
        img_resized.save('changed.png', quality=90)
        
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
            "image_strength": 0.35,
            "init_image_mode": "IMAGE_STRENGTH",
            "text_prompts[0][text]": dates.content,
            # "text_prompts[0][text]": "more colorful",
            "cfg_scale": 7,
            "samples": 1,
            "steps": 30,
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
        return render(request, 'stable_ai/im2im.html')

def generated(request,context):
        return render(request, 'stable_ai/generated.html',context)
