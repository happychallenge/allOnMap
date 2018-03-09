from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.views import serve
from django.shortcuts import redirect
from django.conf.urls import (
        handler400, handler403, handler404, handler500
)

from accounts import views as login_views

urlpatterns = [
    url('^$', lambda r: redirect('/onmap/'), name='home'),
    url(r'^xmlyoon/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^login/$', login_views.login, name='login'),
    url(r'^logout/$', login_views.logout, name='logout'),
    url(r'^myprofile/$', login_views.myprofile, name='myprofile'),
    url(r'^onmap/', include('onmap.urls', namespace="onmap")),
    # url(r'^proposal/', include('proposal.urls', namespace="proposal")),
]

handler404 = 'allOnMap.https.handler404'
handler500 = 'allOnMap.https.handler500'

if settings.DEBUG and settings.AWSS3 is False:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    
    from django.conf.urls.static import static
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
