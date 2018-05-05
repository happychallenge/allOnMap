from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import views as django_login


from accounts import views as user_login

urlpatterns = [
    url('^$', lambda r: redirect('/onmap/'), name='home'),
    url(r'^xmlyoon/', admin.site.urls),
    
    url(r'^accounts/', include('allauth.urls')),
    url(r'^signup/$', user_login.signup, name='signup'),
    url(r'^login/$', user_login.login, name='login'),
    url(r'^logout/$', user_login.logout, name='logout'),
    url(r'^myprofile/$', user_login.myprofile, name='myprofile'),
    url(r'^friend/(?P<username>[-_@\.\w]+)/$', user_login.otherprofile, name='otherprofile'),
    url(r'^login_email', django_login.login, 
        {'template_name': 'accounts/login_email.html'}, name='login_email'),
    
    url(r'^onmap/', include('onmap.urls', namespace="onmap")),
    
    # url(r'^proposal/', include('proposal.urls', namespace="proposal")),
]

handler404 = 'allOnMap.https.handler404'
handler500 = 'allOnMap.https.handler500'

if settings.DEBUG and settings.AWSS3 is False:
    # import debug_toolbar
    # urlpatterns = [
    #     url(r'^__debug__/', include(debug_toolbar.urls)),
    # ] + urlpatterns
    
    from django.conf.urls.static import static
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
