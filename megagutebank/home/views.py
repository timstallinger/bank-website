from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

template = loader.get_template('index.html')

context ={
    'home': '',
}

def index(request):
    return HttpResponse(template.render(context, request))
    # return HttpResponse("Willkommen bei der Megagutebank Bank!")