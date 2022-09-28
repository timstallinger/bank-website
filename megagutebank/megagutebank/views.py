from django.contrib.auth import login, authenticate

from django.shortcuts import render, redirect

from home.models import Bank, Account, TagesgeldAccount

def index(request):
    kontostand = 0
    # sum up all accounts of the user
    if request.user.is_authenticated:
        if request.user.is_staff == True:
            bankdaten = Bank.objects.get(bic='MALADE51KRE')
            accounts = Account.objects.all()
            balance = 0
            revenue = 0
            cost = 0
            for a in accounts:
                if a.type == 0:
                    cost += a.amount * a.interest
                elif a.type == 1:
                    if a.amount < 0:
                        revenue += a.amount * a.negative_interest * -1
                else:
                    cost += a.amount * a.interest
            balance = revenue + cost
            bankdaten.balance = balance
            bankdaten.profit = revenue
            bankdaten.save()
            return render(request, 'employee.html', {'user': request.user, 'bankdaten': bankdaten})
        else:
            for account in request.user.account_set.all():
                kontostand += account.amount
            return render(request, 'index.html', {'user': request.user, 'kontostand': kontostand})
    else:
        return render(request, 'index.html')