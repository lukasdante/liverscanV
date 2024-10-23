from django.shortcuts import render,    redirect
from liverscan.models import (Diagnosis)
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import logout

# Create your views here.
def logout_view(request):
    if request.method == "POST":
        if 'logout' in request.POST:
            logout(request)
            return redirect('login')
        
def doctor_required(user):
    return user.role == 'doctor'

def home_view(request):
    logout_view(request)

    context = {}
    context['curr_page'] = 'home'
    return render(request, 'index.html', context=context)

@login_required
def results_view(request):
    logout_view(request)

    context = {}
    context['curr_page'] = 'results'
    return render(request, 'results.html', context=context)

@user_passes_test(doctor_required)
def doctor_results_view(request):
    logout_view(request)

    context = {}
    context['curr_page'] = 'doctor-results'
    return render(request, 'doctor_results.html', context=context)

@user_passes_test(doctor_required)
def patient_history_view(request):
    logout_view(request)

    context = {}
    context['curr_page'] = 'patient-history'
    return render(request, 'patient_history.html', context=context)

@user_passes_test(doctor_required)
def upload_view(request):
    logout_view(request)
    
    context = {}
    context['curr_page'] = 'upload'
    return render(request, 'upload.html', context=context)