import re

from django import template

from ..models import Category

register = template.Library()


BAD_WORDS = ['редиска', 'шухер', 'скачок', 'шухере', 'скачке']


@register.filter(name='censor')
def censor(value):
	if not isinstance(value, str):
		raise ValueError("Фильтр 'censor' применяется только к строкам.")

	regex_pattern = r'\b('+'|'.join(re.escape(word) for word in BAD_WORDS) + r')\b'

	def censor_match(match):
		word = match.group(0)
		return word[0] + '*' * (len(word) - 1)

	censured_text = re.sub(regex_pattern, censor_match, value, flags=re.IGNORECASE)
	return censured_text


@register.filter
def get_category_name(category):
	return dict(Category.CATEGORY_CHOICES)[category.name]
