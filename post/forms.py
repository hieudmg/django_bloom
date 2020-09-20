from django.forms import ModelForm
from django import forms
from .models import Posts, Categories
from django.utils.translation import ugettext_lazy as _


class PostForm(ModelForm):
    title = forms.CharField(label=_('Title'), required=True)
    content = forms.CharField(label=_('Content'), max_length=150, widget=forms.Textarea)
    category = forms.ModelChoiceField(label=_('Category'), queryset=Categories.objects.all(), required=False)
    slug = forms.CharField(label=_('Url key'), help_text=_('Url key for this post.'))

    class Meta:
        model = Posts
        fields = ('title', 'content', 'category', 'slug')
