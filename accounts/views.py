from django.conf import settings
from django.contrib import auth
from django.shortcuts import redirect, render
from django.contrib.auth.views import login as auth_login
from django.contrib.auth.decorators import login_required

from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers

from .forms import ProfileForm

def login(request):
    providers = []

    for provider in get_providers():
        try:
            provider.social_app = SocialApp.objects.get(provider=provider.id, sites=settings.SITE_ID)
        except SocialApp.DoesNotExist:
            provider.social_app = None

        providers.append(provider)

    return auth_login(request, template_name="accounts/login.html", 
        extra_context={'providers': providers})


def logout(request):
    auth.logout(request)
    return redirect('home')


@login_required
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save()
            
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
        context = {'form':form}
    return render(request, 'accounts/profile.html', context)


def logout(request):
    auth.logout(request)
    return redirect('login')