from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Willkommen bei der Megagutebank Bank!")