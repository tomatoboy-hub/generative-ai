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
        fields = ["content", "image"]

class GenerateImageForm(forms.Form):
    text_prompt = forms.CharField(label='Text Prompt', max_length=300, widget=forms.Textarea)
    cfg_scale = forms.FloatField(label='Config Scale',initial=7, widget=forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 10, 'step': 0.1}))
    height = forms.IntegerField(label='Height',initial=1024, widget=forms.NumberInput(attrs={'type': 'range', 'min': 100, 'max': 2000, 'step': 1}))
    width = forms.IntegerField(label='Width',initial=1024, widget=forms.NumberInput(attrs={'type': 'range', 'min': 100, 'max': 2000, 'step': 1}))
    samples = forms.IntegerField(label='Samples',initial=1, widget=forms.NumberInput(attrs={'type': 'range', 'min': 1, 'max': 10, 'step': 1}))
    steps = forms.IntegerField(label='Steps',initial = 30, widget=forms.NumberInput(attrs={'type': 'range', 'min': 10, 'max': 50, 'step': 1}))

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']