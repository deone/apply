from django.shortcuts import render, redirect
from django.conf import settings

import json
import requests

def index(request):
    return render(request, 'payments/index.html', {})

def pay(request):
    headers = {
        'Content-Type': 'application/json',
        'MP-Master-Key': settings.PAYMENT_MASTER_KEY,
        'MP-Private-Key': settings.PAYMENT_TEST_PRIVATE_KEY,
        'MP-Token': '84ca940ca8ad14a592d4',
    }

    data = '{"invoice": {"total_amount": "' + settings.APPLICATION_FEE + '", "description": "' + settings.PAYMENT_DESCRIPTION + '"}, "store": {"name": "' + settings.STORE_NAME + '"}}'

    response = requests.post(settings.PAYMENT_TEST_URL, headers=headers, data=data)
    obj = json.loads(response.content)
    return redirect(obj['response_text'])
