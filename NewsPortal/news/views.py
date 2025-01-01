from django.urls import reverse_lazy
from django.views.generic import (
ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm
from .models import Post, BaseRegisterForm, Author
from .filters import PostFilter
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


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


class PostCreate(CreateView):
	form_class = PostForm
	model = Post
	template_name = 'post_edit.html'

	def form_valid(self, form):
		news = form.save(commit=False)
		news.author = self.request.user.author
		news.author.full_name = f"{news.author.user.first_name} {news.author.user.last_name}"
		news.author.save()
		news.post_type = 'NW' if self.request.path.startswith('/news/') else 'AR'
		# form.instance.author = self.request.user.author после аутентификации автора
		return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
	form_class = PostForm
	model = Post
	template_name = 'post_edit.html'
	login_url = '/login/'


class PostDelete(DeleteView):
	model = Post
	template_name = 'post_delete.html'
	success_url = reverse_lazy('posts_list')


class BaseRegisterView(CreateView):
	model = User
	form_class = BaseRegisterForm
	success_url = '/news'

