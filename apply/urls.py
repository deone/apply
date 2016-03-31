from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from accounts.views import ApplyRegistrationView
from accounts.forms import LoginForm

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/create/$', ApplyRegistrationView.as_view(), name='create_account'),
    url(r'^accounts/login/$', auth_views.login,
      {'authentication_form': LoginForm, 'template_name': 'registration/login.html'}, name='login'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^payments/', include('payments.urls', namespace='payments')),
    url(r'^apply/', include('app.urls', namespace='app')),
]
