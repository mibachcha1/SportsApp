from nba_api.live.nba.endpoints import scoreboard
from easydict import EasyDict as edict
from django.shortcuts import render
import requests

# Create your views here.

def index(request):
    return render(request, 'index.html')

def test(request):
    games = scoreboard.ScoreBoard()
    all_games = edict(games.get_dict())
    game_Ids = []
    toReturn = {}
    for game in all_games.scoreboard.games:
        game_Ids.append(game.gameId)
        toReturn[game.gameId] = {"home" : game.homeTeam, "away" : game.awayTeam}

    context = {'ids' : game_Ids, 'games' : toReturn}
    return render(request, 'test.html', context)
