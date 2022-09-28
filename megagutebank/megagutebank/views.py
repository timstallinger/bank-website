from django.contrib.auth import login, authenticate

from django.shortcuts import render, redirect

from home.models import Bank

def index(request):
    kontostand = 0
    # sum up all accounts of the user
    if request.user.is_authenticated:
        if request.user.is_staff == True:
            bankdaten = Bank.objects.get(bic='MALADE51KRE')
            return render(request, 'employee.html', {'user': request.user, 'bankdaten': bankdaten})
        else:
            for account in request.user.account_set.all():
                kontostand += account.amount
            return render(request, 'index.html', {'user': request.user, 'kontostand': kontostand})
    else:
        return render(request, 'index.html')