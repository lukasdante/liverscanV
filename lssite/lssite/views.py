from django.shortcuts import render
from liverscan.models import (Diagnosis)

# Create your views here.
def home_view(request):
    context = {}
    return render(request, 'index.html', context=context)

def results_view(request):
    context = {}
    return render(request, 'results.html', context=context)

def signup_view(request):
    context = {}
    return render(request, 'signup.html', context=context)

def login_view(request):
    context = {}
    return render(request, 'login.html', context=context)