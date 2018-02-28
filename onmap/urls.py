from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^my/$', views.myhome, name="myhome"),
    url(r'^add/$', views.add, name="add"),
    url(r'^detail/(?P<id>\d+)/$', views.detail, name="detail"),
    url(r'^apicall/(?P<id>\d+)/$', views.apicall, name="apicall"),
]
