from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib import messages
import bcrypt

# Create your views here.


def index(request):
    return HttpResponse('route test')


def login(request):
    return render(request, 'login.html')


def login_process(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect("/")
    else:
        user = User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(),
                              logged_user.password.encode()):
                request.session['userid'] = logged_user.id
                return redirect('/users/dashboard/')
            else:
                errors["password"] = "Invalid password"
            for key, value in errors.items():
                messages.error(request, value)
                return redirect("/users/login")


def registration(request):
    return render(request, 'register.html')


def registration_process(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect("/registration/")
    else:
        password = request.POST["password"]
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            username=request.POST["username"],
            email=request.POST["email"],
            password=pw_hash)
        user.save()
        request.session['userid'] = user.id
        return redirect("/users/dashboard/")


def dashboard(request):
    if "userid" not in request.session:
        return redirect("/")
    else:
        user = User.objects.get(id=request.session["userid"])
        # user_organizations = Organization.objects.filter(creator=user)
        context = {
            # "user_organizations": user_organizations,
            "user": user
            }
        return render(request, "dashboard.html", context)


def logout(request):
    request.session.clear()
    return redirect("/")
