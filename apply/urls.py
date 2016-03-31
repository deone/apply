from django.conf.urls import url, include
from django.contrib import admin

from accounts.views import ApplyRegistrationView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/register/$', ApplyRegistrationView.as_view(), name='register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^payments/', include('payments.urls', namespace='payments')),
    url(r'^app/', include('app.urls', namespace='app')),
]
