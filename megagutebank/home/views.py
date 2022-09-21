from django.contrib.auth import login, authenticate

from .models import Account
from .forms import SignUpForm, KontoForm, UberweisungForm
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

def konto_uberweisen(request):
    if request.method == 'POST':
        form = UberweisungForm(request.user, request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('user_profile')
        else:
            form = UberweisungForm(request.user)
    else:
        form = UberweisungForm(request.user)
    # get all accounts of the user
    accounts = Account.objects.filter(owner=request.user)

    return render(request, 'konto_uberweisen.html', {'form': form, 'accounts': accounts})