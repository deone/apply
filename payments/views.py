from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.sites.models import Site

import json
import requests

def index(request):
    return render(request, 'payments/index.html', {})

def pay(request):
    current_site = Site.objects.get_current()
    headers = {
        'Content-Type': 'application/json',
        'MP-Master-Key': settings.PAYMENT_MASTER_KEY,
        'MP-Private-Key': settings.PAYMENT_TEST_PRIVATE_KEY,
        'MP-Token': '84ca940ca8ad14a592d4',
    }

    return_url = 'http://%s%s' % (current_site.domain, reverse('application', kwargs={'orgname': 'ashesi', 'slug': 'undergraduate-application-2016'}))
    data = '{"invoice": {"total_amount": "' + settings.APPLICATION_FEE + '", "description": "' + settings.PAYMENT_DESCRIPTION + '"}, "store": {"name": "' + settings.STORE_NAME + '"}, "actions": {"return_url": "' + return_url + '"}}'

    response = requests.post(settings.PAYMENT_TEST_URL, headers=headers, data=data)
    obj = json.loads(response.content)
    return redirect(obj['response_text'])
