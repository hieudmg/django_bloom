from django.forms import ModelForm
from django import forms
from .models import Post, Category
from django.utils.translation import ugettext_lazy as _


class PostForm(ModelForm):
    title = forms.CharField(label=_('Title'), required=True)
    content = forms.CharField(label=_('Content'), widget=forms.Textarea)
    category = forms.ModelMultipleChoiceField(label=_('Category'), queryset=Category.objects.all().order_by('string'),
                                              required=False)
    slug = forms.CharField(label=_('Url key'), help_text=_('Url key for this post.'))

    class Meta:
        model = Post
        fields = ('title', 'content', 'category', 'slug')


class CategoryForm(ModelForm):
    name = forms.CharField(label=_('Name'), required=True)
    description = forms.CharField(label=_('Description'), max_length=150, widget=forms.Textarea)
    parent_category = forms.ModelChoiceField(label=_('Parent Category'), queryset=Category.objects.all(),
                                             required=False)
    slug = forms.CharField(label=_('Url key'), help_text=_('Url key for this category.'))

    class Meta:
        model = Category
        fields = ('name', 'description', 'parent_category', 'slug')
