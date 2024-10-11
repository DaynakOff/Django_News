from django.urls import reverse_lazy
from django.views.generic import (
ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .forms import PostForm
from .models import Post
from .filters import PostFilter

# Create your views here.


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


class NewsCreate(CreateView):
	form_class = PostForm
	model = Post
	template_name = 'post_edit.html'

	def form_valid(self, form):
		news = form.save(commit=False)
		form.instance.post_type = 'NW'
		return super().form_valid(form)


class NewsUpdate(UpdateView):
	form_class = PostForm
	model = Post
	template_name = 'post_edit.html'


class NewsDelete(DeleteView):
	model = Post
	template_name = 'post_delete.html'
	success_url = reverse_lazy('posts_list')


class ArticlesCreate(CreateView):
	form_class = PostForm
	model = Post
	template_name = 'post_edit.html'

	def form_valid(self, form):
		news = form.save(commit=False)
		form.instance.post_type = 'AR'
		return super().form_valid(form)


class ArticlesUpdate(UpdateView):
	form_class = PostForm
	model = Post
	template_name = 'post_edit.html'


class ArticlesDelete(DeleteView):
	model = Post
	template_name = 'post_delete.html'
	success_url = reverse_lazy('posts_list')
