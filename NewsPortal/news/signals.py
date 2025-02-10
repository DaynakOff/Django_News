from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from .tasks import send_new_post_notification



@receiver(post_save, sender=Post, dispatch_uid='send_new_post_notification')
def send_new_post_notification_task(sender, instance, created, **kwargs):
	if created:
		send_new_post_notification.delay(instance.id)
