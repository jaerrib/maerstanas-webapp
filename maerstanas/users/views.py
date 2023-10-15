from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib import messages
from game.models import SessionGame
import bcrypt

# Create your views here.


def index(request):
    if "userid" not in request.session:
        return redirect("homepage")
    else:
        return redirect("dashboard")


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
                return redirect('dashboard')
            else:
                errors["password"] = "Invalid password"
            for key, value in errors.items():
                messages.error(request, value)
                return redirect("login")


def registration(request):
    return render(request, 'register.html')


def registration_process(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect("registration")
    else:
        password = request.POST["password"]
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            username=request.POST["username"],
            email=request.POST["email"],
            password=pw_hash,
            # wins=0,
            # losses=0,
            # ties=0
        )
        user.save()
        request.session['userid'] = user.id
        return redirect("dashboard")


def dashboard(request):
    if "userid" not in request.session:
        return redirect("/")
    else:
        user = User.objects.get(id=request.session["userid"])
        hosted_games = SessionGame.objects.filter(player_one=user.id)
        joined_games = SessionGame.objects.filter(player_two=user)
        context = {
            "hosted_games": hosted_games,
            "joined_games": joined_games,
            "user": user
            }
        return render(request, "dashboard.html", context)


def profile(request, username):
    if "userid" not in request.session:
        return redirect("/")
    else:
        user = User.objects.filter(username=username)
        context = {
            "user": user
            }
    return render(request, 'profile.html', context)


def host_new(request):
    if "userid" not in request.session:
        return redirect("/")
    else:
        user = User.objects.get(id=request.session["userid"])
        context = {
            "user": user
            }
    return render(request, 'host_new.html', context)


def host_new_process(request):
    if "userid" not in request.session:
        return redirect("homepage")
    else:
        user = User.objects.get(id=request.session["userid"])
        password = request.POST["password"]
        protected = False
        if password != "":
            protected = True
            pw_hash = bcrypt.hashpw(password.encode(),
                                    bcrypt.gensalt()).decode()
        else:
            pw_hash = ""
        session_game = SessionGame(
            game_name=request.POST["game_name"],
            player_one=user,
            player_two=None,
            protected=protected,
            password=pw_hash,
            status="open",
        )
        session_game.save()
        return redirect("dashboard")


def open_games(request):
    if "userid" not in request.session:
        return redirect("homepage")
    else:
        user = User.objects.get(id=request.session["userid"])
        open_games = SessionGame.objects.filter(player_two=None, status="open")
        context = {
            "open_games": open_games,
            "user": user,
        }
        return render(request, "open_games.html", context)


def join_game(request, game_name):
    if "userid" not in request.session:
        return redirect("homepage")
    else:
        open_game = SessionGame.objects.get(game_name=game_name)
        user = User.objects.get(id=request.session["userid"])
        if open_game.protected and user.id != open_game.player_one.id:
            context = {
                "open_game": open_game,
                "user": user,
            }
            return render(request, "join_game.html", context)
        elif user.id != open_game.player_one.id:
            open_game.player_two = user
            open_game.status = "active"
            open_game.save()
            return redirect("dashboard")
        else:
            return redirect("open games")


def private_game_process(request):
    if "userid" not in request.session:
        return redirect("homepage")
    else:
        open_game = SessionGame.objects.get(game_name=request.POST["game_name"])
        user = User.objects.get(id=request.session["userid"])
        if bcrypt.checkpw(request.POST['password'].encode(),
                          open_game.password.encode()):
            if user.id != open_game.player_one.id:
                open_game.player_two = user
                open_game.status = "active"
                open_game.save()
                return redirect("dashboard")
        else:
            context = {
                "open_game": open_game,
                "user": user,
            }
            return render(request, "join_game.html", context)


def logout(request):
    request.session.clear()
    return redirect("homepage")
