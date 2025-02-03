from datetime import timedelta
import logging


from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from NewsPortal.settings import BASE_URL
from news.models import Post, Category

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
	today = timezone.now()
	last_week = today - timedelta(weeks=1)
	posts = Post.objects.filter(time__gte=last_week)
	categories_names = set(posts.values_list('category__name', flat=True))
	subscribers_emails = set(Category.objects.filter(name__in=categories_names).values_list('subscribers__email', flat=True))

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
			my_job,
			trigger=CronTrigger(second="*/10"),
			# То же, что и интервал, но задача тригера таким образом более понятна django
			id="my_job",  # уникальный айди
			max_instances=1,
			replace_existing=True,
		)
		logger.info("Added job 'my_job'.")

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