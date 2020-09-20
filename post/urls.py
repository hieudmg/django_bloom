from django.contrib.auth.decorators import user_passes_test
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'post'

login_forbidden = user_passes_test(lambda u: u.is_anonymous(), '/')

urlpatterns = [
    path('all/', views.all_post, name='all'),
    path('new/', views.NewPost.as_view(), name='new'),
    path('edit/<int:pk>/', views.EditPost.as_view(), name='edit'),
]
