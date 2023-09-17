'''
フォームを作成するためだけのpythonファイル
'''

from django import forms
from django.views.generic.edit import CreateView
from .models import SnsModel, UploadedImage

class SnsForm(forms.ModelForm):
    class Meta:
        model = SnsModel
        # fields = ["title", "content", "image","readtext"]
        fields = ["image"]

class GenerateImageForm(forms.Form):
    text_prompt = forms.CharField(label='Text Prompt', max_length=300, widget=forms.Textarea)
    cfg_scale = forms.FloatField(label='Config Scale',initial=7, widget=forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 10, 'step': 0.1}))
    height = forms.IntegerField(label='Height',initial=1024, widget=forms.NumberInput(attrs={'type': 'range', 'min': 100, 'max': 2000, 'step': 1}))
    width = forms.IntegerField(label='Width',initial=1024, widget=forms.NumberInput(attrs={'type': 'range', 'min': 100, 'max': 2000, 'step': 1}))
    samples = forms.IntegerField(label='Samples',initial=1, widget=forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 10, 'step': 1}))
    steps = forms.IntegerField(label='Steps',initial = 30, widget=forms.NumberInput(attrs={'type': 'range', 'min': 10, 'max': 50, 'step': 1}))

class GenerateImageToImageForm(forms.Form):
    # プロンプト
    image_prompt = forms.CharField(label='image Prompt', max_length=100, widget=forms.Textarea)
    negative_prompt = forms.CharField(label='negative Prompt',initial="no attribute", max_length=100, widget=forms.Textarea)
    # 入力画像の影響具合　後で/100して調整
    image_strength = forms.FloatField(label='image strength',initial=35, widget=forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 100, 'step': 1}))
    # プロンプトの影響具合　後で/10して調整
    weight = forms.IntegerField(label='weight',initial=5, widget=forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 10, 'step': 1}))
    negative_weight = forms.IntegerField(label='negative weight',initial=5, widget=forms.NumberInput(attrs={'type': 'range', 'min': -10, 'max': 0, 'step': 1}))
    # 拡散プロセスがプロンプトテキストにどの程度厳密に準拠しているか(値が大きいほど、画像がプロンプトに近づきます)
    cfg_scale = forms.FloatField(label='Config Scale',initial=7, widget=forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 35, 'step': 1}))
    # 生成する画像の数
    samples = forms.IntegerField(label='samples',initial = 1, widget=forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 10, 'step': 1}))
    # 元画像の要素をどれだけ残すか（プロンプトと併用）
    seeds = forms.IntegerField(label='seeds',initial=0, widget=forms.NumberInput(attrs={'type': 'range', 'min': -1, 'max': 4294967295, 'step': 1}))
    # 何回画像生成プロセスを繰り返すか　多いほど綺麗になり時間がかかる
    steps = forms.IntegerField(label='Steps',initial = 50, widget=forms.NumberInput(attrs={'type': 'range', 'min': 10, 'max': 150, 'step': 1}))

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']
