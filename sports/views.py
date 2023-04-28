from nba_api.live.nba.endpoints import scoreboard
from easydict import EasyDict as edict
from django.shortcuts import render
import requests
import urllib3

# Create your views here.

def index(request):
    return render(request, 'index.html')    

def play_by_play(request):
    game_id = request.GET.get('id')
    games = scoreboard.ScoreBoard()
    all_games = edict(games.get_dict())
    current_game = {}
    for game in all_games.scoreboard.games:
        if game.gameId == game_id:
            current_game = game
    
    home_team_name = current_game.homeTeam.teamName
    away_team_name = current_game.awayTeam.teamName
    home_team_id =  current_game.homeTeam.teamId
    away_team_id =  current_game.awayTeam.teamId
    
    home_wins = str(current_game.homeTeam.wins) + "-" + str(current_game.homeTeam.losses)
    away_wins = str(current_game.awayTeam.wins) + "-" + str(current_game.awayTeam.losses)
    series = current_game.seriesText
    context = {
        "homeTeamName": home_team_name,
        "awayTeamName": away_team_name,
        "homeTeamId" : home_team_id,
        "awayTeamId" : away_team_id,
        "gameId" : game_id,
        "homeW" : home_wins,
        "awayW" : away_wins,
        "series" : series,
    }
    
    return render(request, 'playbyplay.html', context)

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
