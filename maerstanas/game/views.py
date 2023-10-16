from django.db import models
from django.shortcuts import render, redirect
from .game_logic.game import Game
from .game_logic.game_logic import valid_move, assign_move
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
    if "player2" not in request.session:
        request.session["player2"] = "computer"
    if "data" not in request.session:
        my_game = Game()
        request.session["data"] = {
            "move_list": my_game.move_list,
            "moves_left": my_game.moves_left,
            "score_p1": my_game.score_p1,
            "score_p2": my_game.score_p2,
            "result": my_game.result,
            "active_player": my_game.active_player,
            "board": my_game.board.data,
            "game_over": False,
            "player2": request.session["player2"],
        }
    reversed_list = request.session["data"]["move_list"]
    reversed_list.reverse()
    board_dict = {}
    for row in range(1, 8):
        col_dict = {}
        for col in range(1, 8):
            col_dict[col] = request.session["data"]["board"][row][col]
            board_dict[row] = col_dict
    context = {
        "reversed_list": reversed_list,
        "board_dict": board_dict
    }
    return render(request, "game.html", context=context)


def session_game(request, game_name):
    if "userid" not in request.session:
        return redirect("/")
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


def new_game(request, players):
    request.session.clear()
    if players == 1:
        request.session["player2"] = "computer"
    if players == 2:
        request.session["player2"] = "human"
    return redirect("guest game")


def process(request, row, col):
    if valid_move(request.session["data"], row, col):
        request.session["data"] = assign_move(request.session["data"], row, col)
    if (request.session["data"]["active_player"] == 2) and (
            request.session["data"]["player2"] == "computer"):
        if len(request.session["data"]["moves_left"]):
            best_row, best_col = get_best_move(request.session["data"],
                                               sim_num=100,
                                               depth=49)
            request.session["data"] = assign_move(request.session["data"],
                                                  best_row,
                                                  best_col)
    request.session["data"]["game_over"] = (
            request.session["data"]["moves_left"] == []
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
