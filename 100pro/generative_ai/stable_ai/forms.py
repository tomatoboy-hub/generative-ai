'''
フォームを作成するためだけのpythonファイル
'''

from django import forms
from django.views.generic.edit import CreateView
from .models import SnsModel

class SnsForm(forms.ModelForm):
    class Meta:
        model = SnsModel
        # fields = ["title", "content", "image","readtext"]
        fields = ["content", "image"]
