from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm


# Create your views here.
def signup_view(request):
    context = {}

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
        context['form'] = form
    
    return render(request, 'signup.html', context=context)

def role_based_redirect(user):
    if user.role == 'doctor':
        return 'doctor-results'
    if user.role == 'patient':
        return 'results'

def login_view(request):
    context = {}

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(role_based_redirect(user))
        else:
            context['error'] = 'Invalid login credentials.'
            return render(request, 'login.html', context=context)
    return render(request, 'login.html', context=context)

def doctor_login_view(request):
    context = {}

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(role_based_redirect(user))
        else:
            context['error'] = 'Invalid login credentials.'
            return render(request, 'doctor_login.html', context=context)
    return render(request, 'doctor_login.html', context=context)