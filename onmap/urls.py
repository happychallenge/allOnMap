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
    url(r'^mylist_ajax/$', views.mylist_ajax, name="mylist_ajax"),
    url(r'^popularlist/$', views.popularlist, name="popularlist"),
    url(r'^popularlist_ajax/$', views.popularlist_ajax, name="popularlist_ajax"),
    url(r'^detail/(?P<slug>[-\w]+)/$', views.detail, name="detail"),
    url(r'^like/$', views.userlike, name="userlike"),
    url(r'^call/(?P<slug>[-\w]+)/$', views.apicall, name="apicall"),
]
