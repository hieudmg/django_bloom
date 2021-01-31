from django.contrib.auth.decorators import user_passes_test
from django.urls import path
from . import views

app_name = 'category'

login_forbidden = user_passes_test(lambda u: u.is_anonymous(), '/')

urlpatterns = [
    path('category/all/', views.all_categories, name='all'),
    path('category/new/', views.NewCategory.as_view(), name='new'),
    path('category/edit/<int:pk>/', views.EditCategory.as_view(), name='edit')
]
