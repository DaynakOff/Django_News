from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Category


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = [
			'name',
			'post',
			'category',
		]
		labels = {
			'name': 'Название',
			'post': 'Содержание',
			'category': 'Категория',
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['category'].queryset = Category.objects.all()

	def clean(self):
		cleaned_data = super().clean()
		return cleaned_data
