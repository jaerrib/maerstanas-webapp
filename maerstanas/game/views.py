from django.db import models
from django.shortcuts import render, redirect
from .game_logic.game import Game
from .game_logic.game_logic import valid_move, assign_move, assign_guest_move
from .game_logic.ai_player import get_best_move
from game.models import SessionGame
from users.models import User
import bcrypt


# Create your views here.
def index(request):
    if "userid" not in request.session:
        return render(request, "index.html")
    else:
        return redirect("dashboard")


def guest_game(request):
    if "player_two" not in request.session:
        request.session["player_two"] = "computer"
    if "guest_game" not in request.session:
        game = Game()
        request.session["guest_game"] = {
            "move_list": game.move_list,
            "moves_left": game.moves_left,
            "score_p1": game.score_p1,
            "score_p2": game.score_p2,
            "result": game.result,
            "active_player": game.active_player,
            "board": game.board.data,
            "player_one": "guest",
            "player_two": request.session["player_two"],
            "game_over": False,
        }

    reversed_list = request.session["guest_game"]["move_list"]
    reversed_list.reverse()
    board_dict = {}
    for row in range(1, 8):
        col_dict = {}
        for col in range(1, 8):
            col_dict[col] = request.session["guest_game"]["board"][row][col]
        board_dict[row] = col_dict
    context = {
        "reversed_list": reversed_list,
        "board_dict": board_dict
    }
    return render(request, "game.html", context=context)


def session_game(request, game_name):
    if "userid" not in request.session:
        return redirect("registration")
    else:
        user = User.objects.get(id=request.session["userid"])
        session_game = SessionGame.objects.get(game_name=game_name)
        reversed_list = session_game.game.move_list
        reversed_list.reverse()
        board_dict = {}
        for row in range(1, 8):
            col_dict = {}
            for col in range(1, 8):
                col_dict[col] = session_game.game.board.data[row][col]
                board_dict[row] = col_dict
        context = {
            "board_dict": board_dict,
            "reversed_list": reversed_list,
            "session_game": session_game,
            "user": user,
            }
    return render(request, "session_game.html", context=context)


def session_game_process(request, game_name, row, col):
    if "userid" not in request.session:
        return redirect("registration")
    else:
        user = User.objects.get(id=request.session["userid"])
        session_game = SessionGame.objects.get(game_name=game_name)
        if ((user.username == session_game.player_one.username
            and session_game.game.active_player == 1)
                or (user.username == session_game.player_two.username
                    and session_game.game.active_player == 2)):
            if valid_move(data=session_game.game.board.data, row=row, col=col):
                session_game.game = (
                    assign_move(game=session_game.game, row=row, col=col))
                session_game.game.game_over = (session_game.game.moves_left == [])
                session_game.save()
        return redirect("session game", game_name)


def new_game(request, players):
    request.session.clear()
    if players == 1:
        request.session["player2"] = "computer"
    if players == 2:
        request.session["player2"] = "human"
    return redirect("guest game")


def process(request, row, col):
    if valid_move(request.session["guest_game"]["board"], row, col):
        request.session["guest_game"] = assign_guest_move(request.session["guest_game"], row, col)
    if (request.session["guest_game"]["active_player"] == 2) and (
            request.session["guest_game"]["player_two"] == "computer"):
        if len(request.session["guest_game"]["moves_left"]):
            best_row, best_col = get_best_move(request.session["guest_game"],
                                               sim_num=100,
                                               depth=49)
            request.session["guest_game"] = assign_guest_move(request.session["guest_game"],
                                                  best_row,
                                                  best_col)
    request.session["guest_game"]["game_over"] = (
            request.session["guest_game"]["moves_left"] == []
    )
    return redirect("guest game")


def reset(request):
    request.session.pop("data")
    return redirect("guest game")


def new_session(request):
    # create the session and save it to the db
    user = User.objects.get(id=request.session["userid"])
    password = request.POST["password"]
    protected = False
    if password != "":
        protected = True
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
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
