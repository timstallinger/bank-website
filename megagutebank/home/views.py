from django.contrib.auth import login, authenticate

from .forms import SignUpForm, KontoForm, UberweisungForm
from django.shortcuts import render, redirect
from .models import *

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

def profile_data(request):
    u = request.user
    p = u

    if Person.objects.filter(id=u.id).exists():
        p = Person.objects.get(id=u.id)
        if not p.birthday:
            p = u

    a = Account.objects.filter(owner=u.id)

    return render(request, 'profile.html', {'user': u, 'person': p, 'accounts': a})

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

    return render(request, 'konto_uberweisen.html', {'form': form, 'accounts': accounts, 'checked': False})


def transactions(request):
    trans = []
    # get all of users accounts
    accounts = Account.objects.filter(owner=request.user)
    # get all transactions of user
    for account in accounts:
        for t in Transaction.objects.filter(sending_account=account):
            t.amount = -t.amount
            trans.append(t)
        for t in Transaction.objects.filter(receiving_account=account.iban):
            trans.append(t)
    trans.sort(key=lambda x: x.time_of_transaction, reverse=True)

    return render(request, 'standing_transactions.html', {'gesendet': trans})