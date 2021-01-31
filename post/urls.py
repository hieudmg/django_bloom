from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('view/<int:pk>/', views.view_post, name='view'),
    path('<str:slug>/', views.view_post_by_slug, name='view_by_slug'),
]
