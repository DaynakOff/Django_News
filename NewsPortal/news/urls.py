from django.urls import path
from .views import (
	PostList, PostDetail, PostSearch, NewsCreate, NewsUpdate, NewsDelete,
ArticlesCreate, ArticlesDelete, ArticlesUpdate
)


urlpatterns = [
	path('news/', PostList.as_view(), name='posts_list'),
	path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
	path('news/search/', PostSearch.as_view(), name='post_search'),
	path('news/create/', NewsCreate.as_view(), name='news_create'),
	path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
	path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
	path('articles/create/', ArticlesCreate.as_view(), name='news_create'),
	path('articles/<int:pk>/edit/', ArticlesUpdate.as_view(), name='news_edit'),
	path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='news_delete'),

]
