from django.forms import ModelForm
from .models import Post
from django import forms

# Создаём модельную форму
class NewsForm(ModelForm):
# В класс мета, как обычно, надо написать модель, по которой будет строиться форма, и нужные нам поля. Мы уже делали что-то похожее с фильтрами
    class Meta:
        model = Post
        fields = ['author', 'post_type', 'title', 'post_text']
        widgets = {
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author'
            }),
            'post_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter title'
            }),
            'post_text': forms.Textarea(attrs={
                'class': 'form-control',
            }),
        }

