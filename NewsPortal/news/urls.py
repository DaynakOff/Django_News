from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
	PostList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete, IndexView, BaseRegisterView, category_detail
)
from .views import upgrade_me, toggle_subscription


urlpatterns = [
	path('news/', PostList.as_view(), name='posts_list'),
	path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
	path('news/search/', PostSearch.as_view(), name='post_search'),
	path('news/create/', PostCreate.as_view(), name='news_create'),
	path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),
	path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
	path('articles/create/', PostCreate.as_view(), name='news_create'),
	path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),
	path('articles/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
	path('login/', LoginView.as_view(template_name='login.html'), name='login'),
	path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
	path('index/', IndexView.as_view(), name='index'),
	path('signup/', BaseRegisterView.as_view(template_name='signup.html'), name='signup'),
	path('upgrade/', upgrade_me, name='upgrade'),
	path('category/<int:category_id>/', category_detail, name='category_detail'),
	path('category/<int:category_id>/toggle_subscription/<int:user_id>/', toggle_subscription, name='toggle_subscription'),

]
