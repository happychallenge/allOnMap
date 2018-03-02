from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name="index"),
    url(r'^add/$', views.add, name="add"),
    url(r'^edit/(?P<slug>[-\w]+)/$', views.edit, name="edit"),
    url(r'^delete/(?P<slug>[-\w]+)/$', views.delete, name="delete"),
    url(r'^privacy/$', views.privacy, name="privacy"),
    url(r'^manual/$', views.manual, name="manual"),
    url(r'^mylist/$', views.mylist, name="mylist"),
    url(r'^detail/(?P<slug>[-\w]+)/$', views.detail, name="detail"),
    url(r'^(?P<slug>[-\w]+)/$', views.apicall, name="apicall"),
]
