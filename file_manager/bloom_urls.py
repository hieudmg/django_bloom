from django.urls import path
from . import views

app_name = 'file_manager'

urlpatterns = [
    path('', views.index, name='index'),
    path('list_dir/', views.list_dir, name='list_dir'),
    path('create_dir/', views.create_dir, name='create_dir'),
    path('rest/', views.FileManager.as_view(), name='rest'),
    path('rest/<str:absolute_path>/', views.FileManager.as_view(), name='rest'),
]
