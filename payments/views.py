from django.shortcuts import render
from django.http import JsonResponse

import requests

def index(request):
    return render(request, 'payments/index.html', {})

def pay(request):
    return JsonResponse({'status': 'ok'})
