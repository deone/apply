from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^pay/(?P<pk>\d+)/$', views.pay, name='pay'),
]
