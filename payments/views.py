from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.conf import settings

from setup.models import UserApplication

import json
import requests

def index(request, pk):
    current_site = Site.objects.get_current()
    user_application = get_object_or_404(UserApplication, pk=pk)
    org_name = user_application.application.organization.slug
    application_slug = user_application.application.slug
    headers = {
        'Content-Type': 'application/json',
        'MP-Master-Key': settings.PAYMENT_MASTER_KEY,
        'MP-Private-Key': settings.PAYMENT_TEST_PRIVATE_KEY,
        'MP-Token': '84ca940ca8ad14a592d4',
    }

    return_url = 'http://%s%s' % (current_site.domain,
        reverse('application',
          kwargs={'orgname': org_name, 'slug': application_slug}))
    data = '{"invoice": {"total_amount": "' + str(user_application.application.fee) + '", "description": "' + settings.PAYMENT_DESCRIPTION + '"}, "store": {"name": "' + settings.STORE_NAME + '"}, "actions": {"return_url": "' + return_url + '"}}'

    response = requests.post(settings.PAYMENT_TEST_URL, headers=headers, data=data)
    obj = json.loads(response.content)
    return redirect(obj['response_text'])
