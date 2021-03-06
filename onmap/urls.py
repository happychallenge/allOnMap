from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name="index"),
    url(r'^add/$', views.add, name="add"),
    url(r'^detail/(?P<slug>[-\w]+)/$', views.detail, name="detail"),
    url(r'^call_detail/$', views.call_detail, name="call_detail"),
    url(r'^edit/(?P<slug>[-\w]+)/$', views.edit, name="edit"),
    url(r'^delete/$', views.delete, name="delete"),
    url(r'^privacy/$', views.privacy, name="privacy"),
    url(r'^manual/$', views.manual, name="manual"),
    url(r'^mylist/$', views.mylist, name="mylist"),
    url(r'^popularlist/$', views.popularlist, name="popularlist"),
    url(r'^like/$', views.userlike, name="userlike"),
    url(r'^(?P<slug>[-_@\w]+)/$', views.apicall, name="apicall"),
    # url(r'^test/(?P<slug>[-\w]+)/$', views.testcall, name="testcall"),
]
