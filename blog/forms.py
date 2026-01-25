from django.forms import ModelForm
from .models import Post
from django import forms

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок статьи'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Введите текст статьи'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'id': 'image-input'}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['title'].label = 'Заголовок статьи'
            self.fields['body'].label = 'Текст статьи'
            self.fields['category'].label = 'Категория'
            self.fields['image'].label = 'Изображение'



