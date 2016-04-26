from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^applications/(?P<pk>\d+)/list/$', views.user_application_list, name='user_application_list'),
]
