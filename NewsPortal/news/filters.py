import django_filters
from django_filters import FilterSet
from .models import Post
from django.forms import DateInput


class PostFilter(FilterSet):
	name = django_filters.CharFilter(lookup_expr='icontains', label='Название')
	author__full_name = django_filters.CharFilter(lookup_expr='icontains', label='Автор')
	time = django_filters.DateFilter(field_name='time', lookup_expr='gte', label='Опубликовано после',
	                                 widget=DateInput(attrs={'type': 'date'}))

	class Meta:
		model = Post
		fields = ['name', 'author__full_name', 'time']
