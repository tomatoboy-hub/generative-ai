from django.test import TestCase

# Create your tests here.
from PIL import Image
new_name = Image.open('../generative_ai/media/changed.jpg')

def add_margin(pil_img):
    width, height = pil_img.size
    new_width = 1024
    new_height = 1024
    result = Image.new(pil_img.mode, (new_width, new_height), 'white')
    # result.paste(pil_img, (512-(width/2), 512-(height/2)))
    result.paste(pil_img, (10, 10))
    return result

new_image = add_margin(im)
new_image.save('../generative_ai/media/changed.png', quality=80)