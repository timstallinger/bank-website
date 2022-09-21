from django.contrib.auth import login, authenticate
from .forms import SignUpForm, KontoForm
from django.shortcuts import render, redirect

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def konto_create(request):
    if request.method == 'POST':
        form = KontoForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
        else:
            form = KontoForm(request.user)
    else:
        form = KontoForm(request.user)
    return render(request, 'konto_create.html', {'form': form})