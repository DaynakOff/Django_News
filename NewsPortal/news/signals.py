from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=Post, dispatch_uid='send_new_post_notification')
def send_new_post_notification(sender, instance, **kwargs):
	category = instance.category.all().first()
	if category:
		subscribers = category.subscribers.all()
		for subscriber in subscribers:
			subject = instance.name
			message = f'Здравствуй, {subscriber.username}. Новая статья в твоем любимом разделе! Перейди по ссылке, чтобы прочитать: {settings.BASE_URL}{instance.get_absolute_url()}<br><br>{instance.post}'
			html_message = f'<h1>{instance.name}</h1><p>Здравствуй, {subscriber.username}. Новая статья в твоем любимом разделе!</p><p>{instance.post[:50]}</p><p><a href="{settings.BASE_URL}{instance.get_absolute_url()}">Прочитать статью</a></p>'
			send_mail(
				subject,
				message,
				settings.DEFAULT_FROM_EMAIL,
				[subscriber.email],
				html_message=html_message,
				fail_silently=False,
			)
