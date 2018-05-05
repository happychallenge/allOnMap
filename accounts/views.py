from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.views import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate

from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers
from django.template.loader import render_to_string

from .forms import ProfileForm, SignUpForm
from onmap.models import Position

NUM_CONTENT = 5

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            password = form.cleaned_data.get('password')

            User.objects.create_user(username=username, first_name=first_name, 
                            password=password, email=email)

            user = authenticate(
                    username=form.cleaned_data.get('email'),
                    password=form.cleaned_data.get('password')
                )

            user.profile.nickname = first_name
            user.profile.save()

            if user is not None and user.is_active:
                auth.login(request, user)

            return redirect('myprofile')
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/signup.html', {'form':form})

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


def _position_list(request, template, position_list, author, form=None):
    data = {}
    paginator = Paginator(position_list, NUM_CONTENT)
    page = request.GET.get('page')
    try:
        position_list = paginator.page(page)
    except PageNotAnInteger:
        position_list = paginator.page(1)
        page = 1
    except EmptyPage:
        position_list = paginator.page(paginator.num_pages)

# For Next Button
    if( int(page) == paginator.num_pages):
        next_page = False
    else:
        next_page = True

    if request.is_ajax():
        context = {'positions': position_list, 'next_page':next_page}
        data["next_page"] = next_page
        if request.user == author:
            data["html"] = render_to_string("onmap/position_mylist_ajax.html", context)
        else:
            data["html"] = render_to_string("onmap/position_popularlist_ajax.html", context)
        return JsonResponse(data, safe=False)
    else:
        return render(request, template, 
            {'positions': position_list, 'form':form, 'next_page':next_page, 'author': author})


@login_required
def myprofile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save()
            
            return redirect('myprofile')
    else:
        form = ProfileForm(instance=profile)
        positions = Position.objects.prefetch_related(
                'pictures', 'plikes').filter(author = request.user, ptype='S')

    return _position_list(request, 'accounts/myprofile.html', positions, request.user, form )


def otherprofile(request, username):
    User = get_user_model()
    author = User.objects.get(username=username)

    positions = Position.objects.prefetch_related(
                'pictures', 'plikes').filter(author = author, ptype='S', public=True)
    return _position_list(request, 'accounts/otherprofile.html', positions, author, )


def logout(request):
    auth.logout(request)
    return redirect('login')

