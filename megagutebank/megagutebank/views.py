from django.contrib.auth import login, authenticate

from django.shortcuts import render, redirect

from home.models import Bank, Account, TagesgeldAccount, Employee, Person, User

# fix: Person und Employee wird beim Login des Superusers erstellt

def index(request):
    kontostand = 0
    # sum up all accounts of the user
    if request.user.is_authenticated:
        if request.user.is_staff == True or request.user.is_superuser:
            # create employee instance, if not exists

            if not Person.objects.filter(user_ptr_id=request.user.id):
                p = Person(user_ptr_id=request.user.id, password=request.user.password,
                           last_login=request.user.last_login, is_superuser=request.user.is_superuser,
                           username=request.user.username, first_name=request.user.first_name,
                           last_name=request.user.last_name, email=request.user.email,
                           is_staff=request.user.is_staff, is_active=request.user.is_active,
                           date_joined=request.user.date_joined, birthday="2000-05-10")
                p.__dict__.update(request.user.__dict__)
                p.save()

            if not Employee.objects.filter(person_id=request.user.id).exists():
                e = Employee.objects.create(person_id=request.user.id)
                e.save()

            if not Bank.objects.filter(blz=10010050).exists():
                b = Bank.objects.create(balance=0, profit=0, blz=10010050, name='MGB')
                b.save()


            bankdaten = Bank.objects.get(blz=10010050)

            return render(request, 'employee.html', {'user': request.user, 'bankdaten': bankdaten})
        else:
            for account in request.user.account_set.all():
                kontostand += account.amount
            return render(request, 'index.html', {'user': request.user, 'kontostand': kontostand})
    else:
        return render(request, 'index.html')
