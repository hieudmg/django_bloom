from django.contrib.auth.decorators import user_passes_test
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'

login_forbidden = user_passes_test(lambda u: u.is_anonymous(), '/')

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('settings/', views.user_settings, name='settings'),
    path('profile/', views.profile, name='profile'),
    path('register/', auth_views.LoginView.as_view(), name='register'),
    path('activation_sent/', views.activation_sent, name='activation_sent'),
    path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
]
