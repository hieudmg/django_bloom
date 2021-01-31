from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User

from account.forms import SignUpForm
from account.tokens import account_activation_token


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            user.refresh_from_db()
            user.profile.school_class = form.cleaned_data.get('school_class')
            user.profile.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Bloom Account'
            message = render_to_string('frontend/account/email/activation.html', {
                'user': user,
                'domain': request.build_absolute_uri('/'),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account:activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'frontend/account/signup.html', {'form': form})


def activation_sent(request):
    return render(request, 'frontend/account/activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'frontend/account/activation_invalid.html')


def user_settings(request):
    return render(request, 'frontend/account/settings.html', {})


def user_logout(request):
    logout(request)
    return redirect('home')


def profile(request):
    return render(request, 'frontend/account/profile.html', {})


class LoginView(auth_views.LoginView):
    redirect_authenticated_user = True
    template_name = 'frontend/registration/login.html'
    pass
