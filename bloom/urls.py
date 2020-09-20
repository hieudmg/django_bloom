from django.urls import path, include

from . import views

app_name = 'bloom'
urlpatterns = [
    path('', views.index, name='index'),
    path('post/', include("post.urls"), name='post'),
]
