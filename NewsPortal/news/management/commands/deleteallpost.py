from django.core.management.base import BaseCommand
from news.models import Post


class Command(BaseCommand):

	def handle(self, *args, **options):
		self.stdout.readable()
		self.stdout.write('Вы действительно хотите удалить все статьи? yes/no?')

		answer = input()

		if answer == 'yes':
			Post.objects.all().delete()
			self.stdout.write(self.style.SUCCESS('Все статьи удалены'))

			return

		self.stdout.write(self.style.WARNING('Удаление отменено'))
