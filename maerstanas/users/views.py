from django.shortcuts import render, HttpResponse

# Create your views here.


def index(request):
    return HttpResponse('route test')


def login(request):
    return HttpResponse('route test')


def login_process(request):
    return HttpResponse('route test')


def registration(request):
    return HttpResponse('route test')


def registration_process(request):
    return HttpResponse('route test')


def dashboard(request):
    return HttpResponse('route test')


def logout(request):
    return HttpResponse('route test')
