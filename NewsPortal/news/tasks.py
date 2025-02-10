from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from news.models import Post, Category
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from NewsPortal.settings import BASE_URL


@shared_task
def send_new_post_notification(post_id):
	post = Post.objects.get(id=post_id)
	if post.category.all().exists():
		for category in post.category.all():
			subscribers = category.subscribers.all()
			for subscriber in subscribers:
				subject = post.name
				message = f'Здравствуй, {subscriber.username}. Новая статья в твоем любимом разделе! Перейди по ссылке, чтобы прочитать: {settings.BASE_URL}{post.get_absolute_url()}<br><br>{post.post}'
				html_message = f'<h1>{post.name}</h1><p>Здравствуй, {subscriber.username}. Новая статья в твоем любимом разделе!</p><p>{post.post[:50]}</p><p><a href="{settings.BASE_URL}{post.get_absolute_url()}">Прочитать статью</a></p>'
				send_mail(
					subject,
					message,
					settings.DEFAULT_FROM_EMAIL,
					[subscriber.email],
					html_message=html_message,
					fail_silently=False,
				)


def send_weekly_news_notification():
	today = timezone.now()
	last_week = today - timedelta(weeks=1)
	posts = Post.objects.filter(time__gte=last_week)
	categories_names = set(posts.values_list('category__name', flat=True))
	subscribers_emails = set(
		Category.objects.filter(name__in=categories_names).values_list('subscribers__email', flat=True))

	html_content = render_to_string(
		'send_weekly_posts.html',
		{
			'posts': posts,
			'BASE_URL': BASE_URL,
		},

	)

	msg = EmailMultiAlternatives(
		subject='Список последних публикаций на сайте за неделю',
		body='',
		from_email=settings.DEFAULT_FROM_EMAIL,
		to=list(subscribers_emails),
	)

	msg.attach_alternative(html_content, "text/html")
	msg.send()
