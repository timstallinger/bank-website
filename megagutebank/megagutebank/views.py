from django.contrib.auth import login, authenticate

from django.shortcuts import render, redirect

from home.models import Bank, Account, TagesgeldAccount, Employee, Person

def index(request):
    kontostand = 0
    # sum up all accounts of the user
    if request.user.is_authenticated:
        if request.user.is_staff == True or request.user.is_superuser:
            # create employee instance, if not exists

            if not Employee.objects.filter(person_id=request.user.id).exists():
                if not Person.objects.filter(id=request.user.id).exists():
                    p = Person.objects.create(user_ptr_id=request.user.id, birthday="2000-05-10" ,confirmed=True)
                    p.save()
                e = Employee.objects.create(person_id=request.user.id)
                e.save()

            if not Bank.objects.filter(blz=10010050).exists():
                b = Bank.objects.create(balance=0, profit=0, blz=10010050, name='MGB')
                b.save()


            bankdaten = Bank.objects.get(blz=10010050)
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