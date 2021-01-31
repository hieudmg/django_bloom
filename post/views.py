from django.contrib.redirects.models import Redirect
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Post, Category
from .forms import PostForm, CategoryForm
from django.views.generic import CreateView, UpdateView


def all_post(request):
    return render(request, 'bloom/post/index.html')


class NewPost(CreateView):
    model = Post
    template_name = 'bloom/post/new.html'
    form_class = PostForm

    def get_success_url(self):
        return reverse('bloom:post:all')


class EditPost(UpdateView):
    model = Post
    template_name = 'bloom/post/edit.html'
    form_class = PostForm

    def get_success_url(self):
        return reverse('bloom:post:all')


def view_post(request, pk=None):
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        raise Http404
    post.views += 1
    post.save()
    return render(request, 'frontend/post/view.html', {'post': post})


def view_post_by_slug(request, slug=None):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        raise Http404
    return view_post(request, pk=post.id)


def view_category(request, pk=None, page=1):
    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist:
        raise Http404
    page_size = 20
    max_pages = int((category.post_set.count() - 1) / page_size) + 1
    if page < 1:
        return redirect("category:view_paginated", pk=pk, page=1)
    elif page > max_pages:
        return redirect("category:view_paginated", pk=pk, page=max_pages)

    paginator = Paginator(category.get_post_set(), page_size)
    posts = paginator.page(page)

    return render(request, 'frontend/category/view.html',
                  {'category': category, 'posts': posts, 'page': page, 'max_pages': max_pages})


def view_category_by_slug(request, slug=None):
    try:
        category = Category.objects.get(slug=slug)
    except Post.DoesNotExist:
        raise Http404
    return view_post(request, pk=category.id)


def all_categories(request):
    return render(request, 'bloom/category/index.html')


class NewCategory(CreateView):
    model = Category
    template_name = 'bloom/category/new.html'
    form_class = CategoryForm

    def get_success_url(self):
        return reverse('bloom:category:all')


class EditCategory(UpdateView):
    model = Category
    template_name = 'bloom/category/edit.html'
    form_class = CategoryForm

    def get_success_url(self):
        return reverse('bloom:category:edit', kwargs={'pk': self.object.id})
