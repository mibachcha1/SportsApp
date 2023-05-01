from django.urls import reverse
from nba_api.live.nba.endpoints import scoreboard
from easydict import EasyDict as edict
from django.shortcuts import redirect, render
import requests
import urllib3
from datetime import datetime
from collections import OrderedDict

# Create your views here.

def index(request):
    games = scoreboard.ScoreBoard()
    all_games = edict(games.get_dict())
    game_Ids = []
    toReturn = {}
    for game in all_games.scoreboard.games:
        game_Ids.append(game.gameId)
        toReturn[game.gameId] = {"home" : game.homeTeam, "away" : game.awayTeam}

    context = {'ids' : game_Ids, 'games' : toReturn}
    return render(request, 'index.html', context)

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

def boxscore(request):
    game_id = request.GET.get('id')
    url = 'https://cdn.nba.com/static/json/liveData/boxscore/boxscore_' + game_id + '.json'
    r = requests.get(url)
    scores = edict(r.json())

    home = scores.game.homeTeam
    away = scores.game.awayTeam

    context = {"home" : home, "away" : away}
    return render(request, 'boxscore.html', context)


def schedule(request):
    url = 'https://cdn.nba.com/static/json/staticData/scheduleLeagueV2.json'
    r = requests.get(url)
    games = edict(r.json())

    today = datetime.today().date()

    available = []
    ongoing_games = {}
    past_games = {}

    for g in games.leagueSchedule.gameDates:
        gameDate = datetime.strptime(g.gameDate, '%m/%d/%Y %H:%M:%S').date()
        strDate = gameDate.strftime("%m/%d/%Y")
        if  gameDate >= today:
            ongoing_games[strDate] = g.games
        else:
            past_games[strDate] = g.games

    for k, v in ongoing_games.items():
        past_games_array = []
        for g in v[:]:  # iterate over a copy of the list
            if g.gameStatus == 3:
                past_games_array.append(g)
                v.remove(g)
        past_games[k] = past_games_array

    past = OrderedDict(reversed(list(past_games.items())))

    context = {"all_data" : ongoing_games, "past" : past}

    return render(request, 'schedule.html',context)

def search(request):
    search_prompt = request.GET.get("prompt")
    print(search_prompt)

    return redirect(reverse('home'))