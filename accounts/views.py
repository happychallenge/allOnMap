from django.conf import settings
from django.contrib.auth.views import login as auth_login
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers

# from .forms import LoginForm

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
    return redirect('login')
