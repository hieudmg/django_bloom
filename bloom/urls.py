from django.urls import path, include

from . import views

app_name = 'bloom'
urlpatterns = [
    path('', views.index, name='index'),
    path('post/', include("post.bloom_urls"), name='post'),
    path('category/', include("post.bloom_category_urls"), name='category'),
    path('file_manager/', include("file_manager.bloom_urls"), name='file_manager'),
]
