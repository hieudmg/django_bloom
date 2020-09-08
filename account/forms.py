from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from account.models import SchoolClass
from django.utils.translation import ugettext_lazy as _


class SignUpForm(UserCreationForm):
    school_class = forms.ModelChoiceField(label=_('School class'), queryset=SchoolClass.objects.all(), required=False)
    first_name = forms.CharField(label=_('First name'), max_length=150)
    last_name = forms.CharField(label=_('Last name'), max_length=150)
    email = forms.EmailField(label=_('Email'), help_text=_('Required. Inform a valid email address.'))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'school_class', 'email', 'password1', 'password2',)
