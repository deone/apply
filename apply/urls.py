from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from accounts.views import ApplyRegistrationView
from accounts.forms import LoginForm
from setup import views as setup_views

urlpatterns = [
    url(r'^$', setup_views.applicant_home, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^logout/$', auth_views.logout, {'next_page': '/accounts/login/'}, name='logout'),
    url(r'^accounts/create/$', ApplyRegistrationView.as_view(), name='create_account'),
    url(r'^accounts/login/$', auth_views.login,
      {'authentication_form': LoginForm, 'template_name': 'registration/login.html'}, name='login'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^payments/', include('payments.urls', namespace='payments')),
    url(r'^(?P<orgname>[-.\w]+)/admin/', include('staffadmin.urls', namespace='staffadmin')),
    url(r'^(?P<orgname>[-.\w]+)/(?P<slug>[-.\w]+)/success/$', setup_views.success, name='success'),
    url(r'^(?P<orgname>[-.\w]+)/(?P<slug>[-.\w]+)/(?P<form_slug>[-.\w]+)/$', setup_views.application_form, name='application_form'),
    url(r'^(?P<orgname>[-.\w]+)/(?P<slug>[-.\w]+)/$', setup_views.application_index, name='application'),
    url(r'^(?P<slug>[-.\w]+)/$', setup_views.OrganizationDetail.as_view(), name='organization'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
