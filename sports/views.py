from django.urls import reverse
from nba_api.live.nba.endpoints import scoreboard
from easydict import EasyDict as edict
from django.shortcuts import redirect, render
import requests
from datetime import datetime
from collections import OrderedDict
from .models import *
from .forms import SignUpForm
from django.contrib.auth import login
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)

            return(redirect('home'))
    else:
        form = SignUpForm()

    return render(request,"signup.html",{'form' : form})

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

    news(home_team_name,away_team_name)

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

    # code for chat functionality:
    room,created = Room.objects.get_or_create(name=current_game.gameCode,slug=game_id)
    messages = Message.objects.filter(room = room)[0:25]

    context = {
        "homeTeamName": home_team_name,
        "awayTeamName": away_team_name,
        "homeTeamId" : home_team_id,
        "awayTeamId" : away_team_id,
        "gameId" : game_id,
        "homeW" : home_wins,
        "awayW" : away_wins,
        "series" : series,
        "messages" : messages,
    }

    if(current_game.gameStatus == 1):
        all_news = news(home_team_name,away_team_name)
        context = {
            "homeTeamName": home_team_name,
            "awayTeamName": away_team_name,
            "homeTeamId" : home_team_id,
            "awayTeamId" : away_team_id,
            "gameId" : game_id,
            "homeW" : home_wins,
            "awayW" : away_wins,
            "series" : series,
            "messages" : messages,
            "news" : all_news
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

def rooms(request):
    rooms = Room.objects.all()

    all_news = list()

    test = [{'title': "Meet the Lakers' full coaching staff", 'url': 'https://www.sportingnews.com/ca/nba/news/lakers-head-coaching-staff-darvin-ham-assistant/o972oesaxkcdkgiwuxuro34s', 'source': 'nba_canada'}, {'title': 'More impressive rings: LeBron or Steph?', 'url': 'https://www.sportingnews.com/ca/nba/news/lebron-james-stephen-curry-rings-nba-lakers-warriors/jo3zcdnty3fciqazji9pvda1', 'source': 'nba_canada'}, {'title': 'What channel is Lakers vs. Warriors on tonight?', 'url': 'https://www.sportingnews.com/ca/nba/news/lakers-warriors-channel-nba-playoffs-schedule/gfn1ckvafhlybj3ebm4otknz', 'source': 'nba_canada'}, {'title': 'What time is Lakers vs. Warriors tonight?', 'url': 'https://www.sportingnews.com/ca/nba/news/lakers-warriors-time-channel-nba-playoff-schedule/vzmra2rbpqknubbtcnql4vxh', 'source': 'nba_canada'}, {'title': 'Series preview: What to expect in Warriors-Lakers', 'url': 'https://www.nba.com/news/series-preview-golden-state-warriors-6-los-angeles-lakers-7', 'source': 'nba'}, {'title': 'Lakers vs. Warriors Game 1 odds, picks, predictions, props', 'url': 'https://www.sportingnews.com/ca/nba/news/lakers-vs-warriors-game-1-odds-picks-predictions-props/df8m2hhruczzunnbqetxpqyr', 'source': 'nba_canada'}, {'title': 'How D’Angelo Russell for Andrew Wiggins trade set up Lakers vs. Warriors', 'url': 'https://www.sportingnews.com/ca/nba/news/dangelo-russell-andrew-wiggins-trade-lakers-warriors/nbmdkkplladoy01yu5s9zuux', 'source': 'nba_canada'}, {'title': 'Lakers-Warriors X-Factors ❌', 'url': 'https://bleacherreport.com/articles/10074619-biggest-x-factors-that-will-decide-lakers-vs-warriors-2nd-round-playoff-series', 'source': 'bleacher_report'}, {'title': 'Best Steph Curry & LeBron James prop bets from Warriors-Lakers Game 1', 'url': 'https://www.sportingnews.com/ca/nba/news/best-steph-curry-and-lebron-james-prop-bets-game-1-warriors-vs-lakers/o3hzgnjq9uedzmnn6uvajrmk', 'source': 'nba_canada'}]


    return render(request, 'tests.html', {'rooms' : rooms, 'news' : all_news})

def room(request,slug):
    room = Room.objects.get(slug=slug)
    return render(request, 'room.html', {'room' : room})

def news(homeTeam,awayTeam):
    url1 = "https://nba-latest-news.p.rapidapi.com/articles?team=" + homeTeam
    url2 = "https://nba-latest-news.p.rapidapi.com/articles?team=" + awayTeam


    headers = {
        "X-RapidAPI-Key": "f4594308abmsha49e2ddf1ff1ab6p1d9ec9jsne51411921670",
        "X-RapidAPI-Host": "nba-latest-news.p.rapidapi.com"
    }

    response = requests.get(url1, headers=headers)
    dict1 = response.json()

    response = requests.get(url2, headers=headers)
    dict2 = response.json()

    list1 = list()
    list2 = list()

    for news in dict1:
        title = news['title']
        url_news = news['url']
        source = news['source']

        list1.append((title,url_news,source))

    for news in dict2:
        title = news['title']
        url_news = news['url']
        source = news['source']

        list2.append((title,url_news,source))


    all_news = list(set(list1 + list2))

    return all_news