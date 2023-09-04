from django import forms

class GenerateImageForm(forms.Form):
    text_prompt = forms.CharField(label='Text Prompt', max_length=300, widget=forms.Textarea)
