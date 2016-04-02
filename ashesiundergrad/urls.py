from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<form_slug>[-.\w]+)/$', views.application_form),
]
