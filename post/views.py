from django.shortcuts import render
from django.urls import reverse

from .models import Posts
from .forms import PostForm
from django.views.generic import CreateView, UpdateView


def all_post(request):
    return render(request, 'bloom/post/index.html')


class NewPost(CreateView):
    model = Posts
    template_name = 'bloom/post/new.html'
    form_class = PostForm

    def get_success_url(self):
        return reverse('bloom:post:all')


class EditPost(UpdateView):
    model = Posts
    template_name = 'bloom/post/edit.html'
    form_class = PostForm

    def get_success_url(self):
        return reverse('bloom:post:all')
