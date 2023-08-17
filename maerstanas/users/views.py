from django.shortcuts import render, redirect, HttpResponse

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
                return redirect('/dashboard/')
            else:
                errors["password"] = "Invalid password"
            for key, value in errors.items():
                messages.error(request, value)
                return redirect("/")


def registration(request):
    return render(request, 'register.html')


def registration_process(request):
    return HttpResponse('route test')


def dashboard(request):
    return HttpResponse('route test')


def logout(request):
    return HttpResponse('route test')
