from django.urls import path

from . import views

app_name = 'bloom'
urlpatterns = [
    path('', views.admin, name='admin'),
]
