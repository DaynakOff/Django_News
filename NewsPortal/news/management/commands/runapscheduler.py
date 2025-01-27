import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from .models import Post
from .signal import send_new_post_notification
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


def get_new_posts():
	last_week = datetime.now() - timedelta(days=7)
	new_posts = Post.objects.filter(time__gte=last_week)
	return new_posts


def send_weekly_newsletter():
	new_posts = get_new_posts()
	for post in new_posts:
		send_new_post_notification(post)


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
	"""This job deletes all apscheduler job executions older than `max_age` from the database."""
	DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
	help = "Runs apscheduler."

	def handle(self, *args, **options):
		scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
		scheduler.add_jobstore(DjangoJobStore(), "default")

		# добавляем работу нашему задачнику
		scheduler.add_job(
			send_weekly_newsletter,
			trigger=CronTrigger(day_of_week='mon', hour='08', minute='00'),
			# То же, что и интервал, но задача тригера таким образом более понятна django
			id="send_weekly_newsletter",  # уникальный айди
			max_instances=1,
			replace_existing=True,
		)
		logger.info("Added weekly job: 'send_weekly_newsletter'.")

		scheduler.add_job(
			delete_old_job_executions,
			trigger=CronTrigger(
				day_of_week="mon", hour="00", minute="00"
			),
			# Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
			id="delete_old_job_executions",
			max_instances=1,
			replace_existing=True,
		)
		logger.info(
			"Added weekly job: 'delete_old_job_executions'."
		)

		try:
			logger.info("Starting scheduler...")
			scheduler.start()
		except KeyboardInterrupt:
			logger.info("Stopping scheduler...")
			scheduler.shutdown()
			logger.info("Scheduler shut down successfully!")