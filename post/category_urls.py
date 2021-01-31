from django.urls import path
from . import views

app_name = 'category'

urlpatterns = [
    path('view/<int:pk>/', views.view_category, name='view'),
    path('view/<int:pk>/page/<int:page>/', views.view_category, name='view_paginated'),
    path('<str:slug>/', views.view_category_by_slug, name='view_by_slug'),
]
