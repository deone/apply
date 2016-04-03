from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from accounts.views import ApplyRegistrationView
from accounts.forms import LoginForm
from setup import views as setup_views

urlpatterns = [
    url(r'^$', setup_views.ApplicationList.as_view(), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^logout/$', auth_views.logout, {'next_page': '/accounts/login/'}, name='logout'),
    url(r'^accounts/create/$', ApplyRegistrationView.as_view(), name='create_account'),
    url(r'^accounts/login/$', auth_views.login,
      {'authentication_form': LoginForm, 'template_name': 'registration/login.html'}, name='login'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^payments/', include('payments.urls', namespace='payments')),
    url(r'^apply/', include('app.urls', namespace='app')),
    url(r'^(?P<orgname>[-.\w]+)/(?P<slug>[-.\w]+)/(?P<form_slug>[-.\w]+)/$', setup_views.application_form, name='application_form'),
    url(r'^(?P<orgname>[-.\w]+)/(?P<slug>[-.\w]+)/$', setup_views.ApplicationDetail.as_view(), name='application'),
]
