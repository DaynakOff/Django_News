from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class Author(models.Model):
	full_name = models.CharField(max_length=255)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	age = models.IntegerField(blank=True, null=True)
	email = models.EmailField(blank=True, null=True)
	rating = models.FloatField(default=0.0)


	def update_rating(self):
		post_rating = self.post_set.aggregate(total=models.Sum('rating'))['total'] or 0
		post_rating *= 3

		author_comments_rating = self.user.comment_set.aggregate(total=models.Sum('rating'))['total'] or 0

		post_comments_rating = Comment.objects.filter(post__author=self).aggregate(total=models.Sum('rating'))['total'] or 0

		self.rating = post_rating + author_comments_rating + post_comments_rating
		self.save()
	pass


class Category(models.Model):
	politics = 'PO'
	kulture = 'KU'
	showbiz = 'SH'
	economy = 'EC'
	science = 'SC'
	sport = 'SP'
	trevel = 'TR'

	CATEGORY_CHOICES = [
		(politics, 'Политика'),
		(kulture, 'Культура'),
		(showbiz, 'Шоу-Бизнес'),
		(economy, 'Экономика'),
		(science, 'Наука и Техника'),
		(sport, 'Спорт'),
		(trevel, 'Путешествия')
	]
	name = models.CharField(max_length=2, choices=CATEGORY_CHOICES, unique=True)

	pass


class Post(models.Model):
	article = "AR"
	news = "NW"
	POST_TYPE = [
		(article, "Статья"),
		(news, "Новость")
	]
	author = models.ForeignKey(Author, on_delete=models.CASCADE)
	post_type = models.CharField(max_length=2, choices=POST_TYPE)
	name = models.CharField(max_length=255)
	post = models.TextField()
	time = models.DateTimeField(auto_now_add=True)
	rating = models.IntegerField(default=0)
	category = models.ManyToManyField(Category, through='PostCategory')

	def like(self):
		self.rating += 1
		self.save()

	def dislike(self):
		self.rating -= 1
		self.save()

	def preview(self):
		return self.post[:124] + '...' if len(self.post) > 124 else self.post


	pass


class PostCategory(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	pass


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.TextField()
	time = models.DateTimeField(auto_now_add=True)
	rating = models.IntegerField(default=0)


	def like(self):
		self.rating += 1
		self.save()


	def dislike(self):
		self.rating -= 1
		self.save()

	pass
