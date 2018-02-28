from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.views import serve

from accounts import views as login_views

urlpatterns = [
    url(r'^xmlyoon/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^login', login_views.login, name='login'),
    url(r'^logout', login_views.logout, name='logout'),
    url(r'^', include('onmap.urls', namespace="onmap")),
]

if settings.DEBUG == True:
    from django.conf.urls.static import static
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
