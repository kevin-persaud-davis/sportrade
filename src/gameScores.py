import os
import csv

import requests

from readData import getKey

class BetOutcome():

    def __init__(self, game, spread, total, odds, betSize):
        self.game = game
        self.spread = spread
        self.total = total
        self.odds = odds
        self.betSize = betSize
        self.mlWinner = None
        self.spreadWinner = None
        self.ouWinner = None

class Game():

    def __init__(self, id, completed, hTeam, aTeam):
        self.id = id
        self.completed = completed
        self.hTeam = hTeam
        self.aTeam = aTeam
        self.hScore = None
        self.aScore = None

    def setHomScore(self, homeScore):
        self.hScore = int(homeScore)

    def setAwayScore(self, awayScore):
        self.aScore = int(awayScore)

    def getFinalScore(self):
        return (self.hScore, self.aScore)

    def getTotalScore(self):
        return self.hScore + self.aScore
    


def getGameOutcomes(games):
    
    finishedGames = []

    for game in games:
        gameCompleted = game["completed"]
        if gameCompleted:
            gameID = game["id"]
            hTeam = game["home_team"]
            aTeam = game["away_team"]

            gameScores = game["scores"]

            fGame = Game(gameID, gameCompleted, hTeam, aTeam)

            for i, score in enumerate(gameScores):
                if i == 0:
                    # print("HOME TEAM:", score["name"], score["score"])
                    fGame.setHomScore(score["score"])
                else:
                    # print("AWAY TEAM: ", score["name"], score["score"])
                    fGame.setAwayScore(score["score"])

            finishedGames.append(fGame)


    return finishedGames

def winner(game, hscore, ascore):
    if hscore > ascore:
        return game.hTeam
    elif ascore > hscore:
        return game.aTeam
    else:
        print(f"No winner of {game.hTeam} vs {game.aTeam}")
        return None

def spreadWinner(game, hSpread):
    hSpreadScore = game.hScore + hSpread
    aSpreadScore = game.aScore
    return winner(game, hSpreadScore, aSpreadScore)

def writeData(gamesData, fname):

    mainDirPath = os.path.dirname(os.path.dirname(__file__))
    fpath = os.path.join(mainDirPath, fname)
    with open(fpath, "a", encoding="UTF8", newline="") as f:
        writer = csv.writer(f, delimiter=",")

        for gData in gamesData:
            writer.writerow(gData)

def writeScores(gameScores, fname):
    """Write completed game scores to disk."""

    gsData = [
            (gs.id,
            gs.hTeam,
            gs.aTeam,
            gs.hScore,
            gs.aScore) 
            for gs in gameScores]
    

    writeData(gsData, fname)


def fetchScores(apiKey, sports, daysFrom, dateFormat):
    
    url = f" https://api.the-odds-api.com/v4/sports/{sports}/scores"

    with requests.Session() as s:
        r = s.get(url,
            params={
                "api_key": apiKey,
                "daysFrom": daysFrom,
                "dateFormat": dateFormat
            })
        
        if r.status_code == 200:
            games = r.json()
            print(f"Number of events: {len(games)}")
            print(games)
            finishedGames = []

            for game in games:
                gameCompleted = game["completed"]
                if gameCompleted:
                    gameID = game["id"]
                    hTeam = game["home_team"]
                    aTeam = game["away_team"]

                    gameScores = game["scores"]

                    fGame = Game(gameID, gameCompleted, hTeam, aTeam)

                    for i, score in enumerate(gameScores):
                        if i == 0:
                            # print("HOME TEAM:", score["name"], score["score"])
                            fGame.setHomScore(score["score"])
                        else:
                            # print("AWAY TEAM: ", score["name"], score["score"])
                            fGame.setAwayScore(score["score"])

                    finishedGames.append(fGame)

            # check usage quota
            print(f"Remaining requests {r.headers['x-requests-remaining']}")
            return finishedGames
        else:
            print(f"Failed to get odds: status_code {r.status_code}, response body {r.text}")

def main():

    exampleJson = [
    {
        "id": "572d984e132eddaac3da93e5db332e7e",
        "sport_key": "basketball_nba",
        "sport_title": "NBA",
        "commence_time": "2022-02-06T03:10:38Z",
        "completed": True,
        "home_team": "Sacramento Kings",
        "away_team": "Oklahoma City Thunder",
        "scores": [
            {
                "name": "Sacramento Kings",
                "score": "113"
            },
            {
                "name": "Oklahoma City Thunder",
                "score": "103"
            }
        ],
        "last_update": "2022-02-06T05:18:19Z"
    },
    {
        "id": "e2296d6d1206f8d185466876e2b444ea",
        "sport_key": "basketball_nba",
        "sport_title": "NBA",
        "commence_time": "2022-02-06T03:11:26Z",
        "completed": True,
        "home_team": "Portland Trail Blazers",
        "away_team": "Milwaukee Bucks",
        "scores": [
            {
                "name": "Portland Trail Blazers",
                "score": "108"
            },
            {
                "name": "Milwaukee Bucks",
                "score": "137"
            }
        ],
        "last_update": "2022-02-06T05:21:01Z"
    },
    {
        "id": "8d8affc2e29bcafd3cdec8b414256cda",
        "sport_key": "basketball_nba",
        "sport_title": "NBA",
        "commence_time": "2022-02-06T20:41:04Z",
        "completed": True,
        "home_team": "Denver Nuggets",
        "away_team": "Brooklyn Nets",
        "scores": [
            {
                "name": "Denver Nuggets",
                "score": "124"
            },
            {
                "name": "Brooklyn Nets",
                "score": "104"
            }
        ],
        "last_update": "2022-02-06T22:50:22Z"
    },
    {
        "id": "aae8b3294ab2de36e63c614e44e94d80",
        "sport_key": "basketball_nba",
        "sport_title": "NBA",
        "commence_time": "2022-02-06T20:41:47Z",
        "completed": True,
        "home_team": "Minnesota Timberwolves",
        "away_team": "Detroit Pistons",
        "scores": [
            {
                "name": "Minnesota Timberwolves",
                "score": "118"
            },
            {
                "name": "Detroit Pistons",
                "score": "105"
            }
        ],
        "last_update": "2022-02-06T22:52:29Z"
    },
    {
        "id": "07767ff2952c6b025aa5584626db2910",
        "sport_key": "basketball_nba",
        "sport_title": "NBA",
        "commence_time": "2022-02-06T20:42:13Z",
        "completed": True,
        "home_team": "Chicago Bulls",
        "away_team": "Philadelphia 76ers",
        "scores": [
            {
                "name": "Chicago Bulls",
                "score": "108"
            },
            {
                "name": "Philadelphia 76ers",
                "score": "119"
            }
        ],
        "last_update": "2022-02-06T22:58:23Z"
    },
    {
        "id": "3f63cadf65ad249c5bc6b1aac8ba426d",
        "sport_key": "basketball_nba",
        "sport_title": "NBA",
        "commence_time": "2022-02-06T23:10:53Z",
        "completed": True,
        "home_team": "Orlando Magic",
        "away_team": "Boston Celtics",
        "scores": [
            {
                "name": "Orlando Magic",
                "score": "83"
            },
            {
                "name": "Boston Celtics",
                "score": "116"
            }
        ],
        "last_update": "2022-02-07T01:18:57Z"
    },
    {
        "id": "4843de62e910869ee34065ffe4c20137",
        "sport_key": "basketball_nba",
        "sport_title": "NBA",
        "commence_time": "2022-02-06T23:11:42Z",
        "completed": True,
        "home_team": "Dallas Mavericks",
        "away_team": "Atlanta Hawks",
        "scores": [
            {
                "name": "Dallas Mavericks",
                "score": "103"
            },
            {
                "name": "Atlanta Hawks",
                "score": "94"
            }
        ],
        "last_update": "2022-02-07T01:26:29Z"
    },
    {
        "id": "e0f6669de3ae5af63162c3d9459184bf",
        "sport_key": "basketball_nba",
        "sport_title": "NBA",
        "commence_time": "2022-02-06T23:12:42Z",
        "completed": True,
        "home_team": "Cleveland Cavaliers",
        "away_team": "Indiana Pacers",
        "scores": [
            {
                "name": "Cleveland Cavaliers",
                "score": "98"
            },
            {
                "name": "Indiana Pacers",
                "score": "85"
            }
        ],
        "last_update": "2022-02-07T01:36:15Z"
    },
    {
        "id": "a306576b1789dd1c884cc1aa61fda4bf",
        "sport_key": "basketball_nba",
        "sport_title": "NBA",
        "commence_time": "2022-02-07T00:11:03Z",
        "completed": True,
        "home_team": "Houston Rockets",
        "away_team": "New Orleans Pelicans",
        "scores": [
            {
                "name": "Houston Rockets",
                "score": "107"
            },
            {
                "name": "New Orleans Pelicans",
                "score": "120"
            }
        ],
        "last_update": "2022-02-07T02:25:17Z"
    },
    {
        "id": "4b25562aa9e87b57aa16f970abaec8cc",
        "sport_key": "basketball_nba",
        "sport_title": "NBA",
        "commence_time": "2022-02-07T02:11:01Z",
        "completed": False,
        "home_team": "Los Angeles Clippers",
        "away_team": "Milwaukee Bucks",
        "scores": [
            {
                "name": "Los Angeles Clippers",
                "score": "40"
            },
            {
                "name": "Milwaukee Bucks",
                "score": "37"
            }
        ],
        "last_update": "2022-02-07T02:47:23Z"
    },
    {
        "id": "19434a586e3723c55cd3d028b90eb112",
        "sport_key": "basketball_nba",
        "sport_title": "NBA",
        "commence_time": "2022-02-08T00:10:00Z",
        "completed": False,
        "home_team": "Charlotte Hornets",
        "away_team": "Toronto Raptors",
        "scores": "null",
        "last_update": "null"
    },
    {
        "id": "444e56cbf5a6d534741bb8d1298e2d50",
        "sport_key": "basketball_nba",
        "sport_title": "NBA",
        "commence_time": "2022-02-08T01:10:00Z",
        "completed": False,
        "home_team": "Oklahoma City Thunder",
        "away_team": "Golden State Warriors",
        "scores": "null",
        "last_update": "null"
    },
    {
        "id": "16d461b95e9d643d7f2469f72c098a20",
        "sport_key": "basketball_nba",
        "sport_title": "NBA",
        "commence_time": "2022-02-08T02:10:00Z",
        "completed": False,
        "home_team": "Utah Jazz",
        "away_team": "New York Knicks",
        "scores": "null",
        "last_update": "null"
    }
]
    
    testJson = [{'id': '8c74bc0adb5686f680448c8e502feb77', 'sport_key': 'basketball_ncaab', 'sport_title': 'NCAAB', 'commence_time': 1647821380, 'completed': True, 'home_team': 'Auburn Tigers', 'away_team': 'Miami Hurricanes', 'scores': [{'name': 'Auburn Tigers', 'score': '61'}, {'name': 'Miami Hurricanes', 'score': '79'}], 'last_update': 1647829143}, 
    {'id': '09ef48bc375a44591895f70cfb3bfb89', 'sport_key': 'basketball_ncaab', 'sport_title': 'NCAAB', 'commence_time': 1647824821, 'completed': True, 'home_team': 'Purdue Boilermakers', 'away_team': 'Texas Longhorns', 'scores': [{'name': 'Purdue Boilermakers', 'score': '81'}, {'name': 'Texas Longhorns', 'score': '71'}], 'last_update': 1647833623}, 
    {'id': '1849b460e9c100bde647113e9add689e', 'sport_key': 'basketball_ncaab', 'sport_title': 'NCAAB', 'commence_time': 1647827714, 'completed': True, 'home_team': 'Arizona Wildcats', 'away_team': 'TCU Horned Frogs', 'scores': [{'name': 'Arizona Wildcats', 'score': '85'}, {'name': 'TCU Horned Frogs', 'score': '80'}], 'last_update': 1647837531}, 
    {'id': 'df974047ae0d101c3d3c12e247ed2061', 'sport_key': 'basketball_ncaab', 'sport_title': 'NCAAB', 'commence_time': 1647882000, 'completed': True, 'home_team': 'UNC Wilmington Seahawks', 'away_team': 'Drake Bulldogs', 'scores': [{'name': 'UNC Wilmington Seahawks', 'score': '76'}, {'name': 'Drake Bulldogs', 'score': '75'}], 'last_update': 1647888679}, 
    {'id': 'ba9d2e844b1cc75d8b535b2626a1f640', 'sport_key': 'basketball_ncaab', 'sport_title': 'NCAAB', 'commence_time': 1647891000, 'completed': True, 'home_team': 'UNC Asheville Bulldogs', 'away_team': 'N Colorado Bears', 'scores': [{'name': 'UNC Asheville Bulldogs', 'score': '84'}, {'name': 'N Colorado Bears', 'score': '87'}], 'last_update': 1647897636}, 
    {'id': 'ecad3e3b17d507d1f97ec250ef9e0e37', 'sport_key': 'basketball_ncaab', 'sport_title': 'NCAAB', 'commence_time': 1647900000, 'completed': True, 'home_team': 'Boston Univ. Terriers', 'away_team': 'Middle Tennessee Blue Raiders', 'scores': [{'name': 'Boston Univ. Terriers', 'score': '46'}, {'name': 'Middle Tennessee Blue Raiders', 'score': '76'}], 'last_update': 1647906484}, 
    {'id': '99c94fc7cde2566b126dcfd0f2eea87a', 'sport_key': 'basketball_ncaab', 'sport_title': 'NCAAB', 'commence_time': 1647903600, 'completed': True, 'home_team': 'Coastal Carolina Chanticleers', 'away_team': 'Florida Gulf Coast Eagles', 'scores': [{'name': 'Coastal Carolina Chanticleers', 'score': '84'}, {'name': 'Florida Gulf Coast Eagles', 'score': '68'}], 'last_update': 1647910588},
    {'id': 'c294036bc8c41db6f2ecade461e54921', 'sport_key': 'basketball_ncaab', 'sport_title': 'NCAAB', 'commence_time': 1647907200, 'completed': True, 'home_team': 'South Alabama Jaguars', 'away_team': 'South Carolina Upstate Spartans', 'scores': [{'name': 'South Alabama Jaguars', 'score': '83'}, {'name': 'South Carolina Upstate Spartans', 'score': '79'}], 'last_update': 1647914768},
    {'id': 'a0f886561516b82bb5119ef57e169d39', 'sport_key': 'basketball_ncaab', 'sport_title': 'NCAAB', 'commence_time': 1647909000, 'completed': True, 'home_team': 'Abilene Christian Wildcats', 'away_team': 'Ohio Bobcats', 'scores': [{'name': 'Abilene Christian Wildcats', 'score': '91'}, {'name': 'Ohio Bobcats', 'score': '86'}], 'last_update': 1647916966}, 
    {'id': '289175f5741ea89599c3ef4d2a72354d', 'sport_key': 'basketball_ncaab', 'sport_title': 'NCAAB', 'commence_time': 1647990000, 'completed': False, 'home_team': 'N Colorado Bears', 'away_team': 'UNC Wilmington Seahawks', 'scores': [{'name': 'N Colorado Bears', 'score': '23'}, {'name': 'UNC Wilmington Seahawks', 'score': '36'}], 'last_update': 1647993654},
    {'id': '441bf2b1547021568ca225e4315b9eee', 'sport_key': 'basketball_ncaab', 'sport_title': 'NCAAB', 'commence_time': 1647997200, 'completed': False, 'home_team': 'UTEP Miners', 'away_team': 'Southern Utah Thunderbirds', 'scores': None, 'last_update': None}, 
    {'id': 'acf73418bf348ccebbf56300605f6256', 'sport_key': 'basketball_ncaab', 'sport_title': 'NCAAB', 'commence_time': 1647999000, 'completed': False, 'home_team': 'Abilene Christian Wildcats', 'away_team': 'Middle Tennessee Blue Raiders', 'scores': None, 'last_update': None}, 
    {'id': '14c3d37898391d2454ef7ab6acbf35e2', 'sport_key': 'basketball_ncaab', 'sport_title': 'NCAAB', 'commence_time': 1648087200, 'completed': False, 'home_team': 'Fresno St Bulldogs', 'away_team': 'Youngstown St Penguins', 'scores': None, 'last_update': None}, 
    {'id': '05b0c5500e87feae25d31c67595adb9b', 'sport_key': 'basketball_ncaab', 'sport_title': 'NCAAB', 'commence_time': 1648163340, 'completed': False, 'home_team': 'Gonzaga Bulldogs', 'away_team': 'Arkansas Razorbacks', 'scores': None, 'last_update': None}, 
    {'id': 'fe01e717bdbcd295a3cbdd4f279a771a', 'sport_key': 'basketball_ncaab', 'sport_title': 'NCAAB', 'commence_time': 1648164540, 'completed': False, 'home_team': 'Villanova Wildcats', 'away_team': 'Michigan Wolverines', 'scores': None, 'last_update': None},
    {'id': '55b6fb57e5eed466ef4bfa9e45f9bcb1', 'sport_key': 'basketball_ncaab', 'sport_title': 'NCAAB', 'commence_time': 1648172340, 'completed': False, 'home_team': 'Duke Blue Devils', 'away_team': 'Texas Tech Red Raiders', 'scores': None, 'last_update': None}, 
    {'id': '632bfb1428dc4475a87fdc2f6ae0662a', 'sport_key': 'basketball_ncaab', 'sport_title': 'NCAAB', 'commence_time': 1648173600, 'completed': False, 'home_team': 'Arizona Wildcats', 'away_team': 'Houston Cougars', 'scores': None, 'last_update': None},
    {'id': 'fb61147c9061e18ea4b3bde586db6099', 'sport_key': 'basketball_ncaab', 'sport_title': 'NCAAB', 'commence_time': 1648249740, 'completed': False, 'home_team': 'Purdue Boilermakers', 'away_team': "Saint Peter's Peacocks", 'scores': None, 'last_update': None}, 
    {'id': 'dffe350d38177bd36b537ae97162b8a5', 'sport_key': 'basketball_ncaab', 'sport_title': 'NCAAB', 'commence_time': 1648250940, 'completed': False, 'home_team': 'Kansas Jayhawks', 'away_team': 'Providence Friars', 'scores': None, 'last_update': None}, 
    {'id': '12d3a3d23d21a98b908ec77a3e7ec7d3', 'sport_key': 'basketball_ncaab', 'sport_title': 'NCAAB', 'commence_time': 1648258740, 'completed': False, 'home_team': 'UCLA Bruins', 'away_team': 'North Carolina Tar Heels', 'scores': None, 'last_update': None}, 
    {'id': '223238654875fa092dcf47bbd8e09052', 'sport_key': 'basketball_ncaab', 'sport_title': 'NCAAB', 'commence_time': 1648260000, 'completed': False, 'home_team': 'Miami Hurricanes', 'away_team': 'Iowa State Cyclones', 'scores': None, 'last_update': None}]
    
    # fGames = getGameOutcomes(exampleJson)
    API_KEY = getKey("private\\api.text")

    SPORTS = "basketball_ncaab"

    DAYS_FROM = 3

    DATE_FORMAT = "unix"

    fGames = fetchScores(API_KEY, SPORTS, DAYS_FROM, DATE_FORMAT)

    fname = "data\\gameScores.csv"
    writeScores(fGames, fname)

    # game1 = fGames[0]
    
    # sWinner = spreadWinner(game1, -11)
    # print(sWinner)

if __name__ == "__main__":
    main()