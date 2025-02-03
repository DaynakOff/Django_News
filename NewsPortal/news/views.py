from django.urls import reverse_lazy
from django.views.generic import (
ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import PostForm
from .models import Post, BaseRegisterForm, Author, Category, User
from .filters import PostFilter
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.utils import timezone

# Create your views here.

@login_required
def upgrade_me(request):
	user = request.user
	authors_group = Group.objects.get(name='Authors')
	if not request.user.groups.filter(name='Authors').exists():
		authors_group.user_set.add(user)
		Author.objects.get_or_create(user=user)
	return redirect('/news')


class IndexView(LoginRequiredMixin, TemplateView):
	template_name = 'index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['is_not_author'] = not self.request.user.groups.filter(name='Authors').exists()
		return context


class PostList(ListView):
	model = Post
	ordering = '-time'
	template_name = 'posts.html'
	context_object_name = 'posts'
	paginate_by = 10


class PostDetail(DetailView):
	model = Post
	template_name = 'post.html'
	context_object_name = 'post'


class PostSearch(ListView):
	model = Post
	template_name = 'post_search.html'
	context_object_name = 'posts'
	paginate_by = 10

	def get_queryset(self):
		queryset = super().get_queryset()
		self.filterset = PostFilter(self.request.GET, queryset)
		return self.filterset.qs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['filterset'] = self.filterset
		return context


class PostCreate(LoginRequiredMixin,UserPassesTestMixin, CreateView):
	form_class = PostForm
	model = Post
	template_name = 'post_edit.html'

	def form_valid(self, form):
		news = form.save(commit=False)
		news.author = self.request.user.author
		news.author.full_name = f"{news.author.user.first_name} {news.author.user.last_name}"
		news.author.save()
		news.post_type = 'NW' if self.request.path.startswith('/news/') else 'AR'
		news.save()
		category_ids = self.request.POST.getlist('category')
		news.category.set(Category.objects.filter(id__in=category_ids))
		return super().form_valid(form)


	def test_func(self):
		today = timezone.now().date()
		yesterday = today - timezone.timedelta(days=1)
		user_posts_today = Post.objects.filter(author=self.request.user.author, time__date=today).count()
		user_posts_yesterday = Post.objects.filter(author=self.request.user.author, time__date=yesterday).count()

		if user_posts_today + user_posts_yesterday >= 3:
			return False

		return self.request.user.groups.filter(name='Authors').exists()


class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	form_class = PostForm
	model = Post
	template_name = 'post_edit.html'
	login_url = '/login/'

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author.user or self.request.user.is_superuser


class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	template_name = 'post_delete.html'
	success_url = reverse_lazy('posts_list')

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author.user or self.request.user.is_superuser


class BaseRegisterView(CreateView):
	model = User
	form_class = BaseRegisterForm
	success_url = '/news'

	def form_valid(self, form):
		user = form.save()
		Author.objects.create(user=user)
		return super().form_valid(form)


def category_detail(request, category_id):
	category = get_object_or_404( Category, id=category_id)
	posts = Post.objects.filter(category=category).order_by('-time')
	user = request.user

	is_subscribed = user in category.subscribers.all()

	context = {
		'category': category,
		'posts': posts,
		'is_subscribed': is_subscribed,
	}

	return render(request, 'category_detail.html', context)


def toggle_subscription(request, category_id, user_id):
	category = get_object_or_404(Category, id=category_id)
	user = get_object_or_404(User, id=user_id)

	if user in category.subscribers.all():
		category.subscribers.remove(user)
	else:
		category.subscribers.add(user)

	return redirect('category_detail', category_id=category_id)


def create_authors_for_authors_group(request):
	authors_group = Group.objects.get(name='Authors')
	users_without_author = User.objects.filter(groups=authors_group).exclude(author__isnull=False)

	for user in users_without_author:
		Author.objects.create(user=user)

	return redirect('your_redirect_url')
