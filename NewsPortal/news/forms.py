from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Category, Author
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


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


class BasicSignupForm(SignupForm):

	def save(self, request):
		user = super(BasicSignupForm, self).save(request)
		users_group = Group.objects.get(name='Users')
		users_group.user_set.add(user)
		return user
