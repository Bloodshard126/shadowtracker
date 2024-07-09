import requests
import os
from dotenv import find_dotenv, load_dotenv
import playerScoreWeights
import visualizations as viz
from typing import Any

dotenvPath = find_dotenv()
load_dotenv(dotenvPath)
key = os.getenv('shadowtrackerApiKey') # key as env variable

from challenges import jsonData # imports challenges information (challenge Titles)
from championIds import all_champion_id # imports champion Names to replace champion IDs

class Player:
    def __init__(self, puuid: str, summonerID: str, summonerTag: str, region: str):
        self.puuid: str = puuid
        self.summonerID: str = summonerID
        self.summonerTag: str = summonerTag
        self.region:str = region

class Game:
    def __init__(self, gameId: int, teams: list[dict], duration: int, participants: list[dict]):
        self.gameId: int = gameId
        self.teams: list[dict] = teams
        self.redTeam: str = 'red team'
        self.blueTeam: str = 'blue team' 
        self.duration: float = round(duration/60, 2) # duration is returned in seconds, divided by 60 to get duration in minutes
        self.participants: list[dict] = participants
        for team in self.teams:
            if team['win']:
                self.winner: str = self.blueTeam if team['teamId'] == 200 else self.redTeam # team ID = 100 specifies the red team while team ID = 200 specifies the blue team
                break

    def getGameParticipantInfo(self, puuid: str, role: str): # returns players's game, role, name, teamID, win, kills deaths and assists and stores them in class GameParticipant
        for player in self.participants:
            if player['puuid'] == puuid:
                return GameParticipant(
                    self,
                    player,
                    role,
                    player['riotIdGameName'],
                    player['teamId'],
                    player['win'],
                    player['kills'], 
                    player['deaths'], 
                    player['assists'])
        
    def printGameInfo(self): #prints gameID, winner and game duration
        print('Game ID:', self.gameId, 'Winner:',self.winner, 'Duration:', self.duration, 'minutes')
    
    def printGameParticipantInfo(self, puuid: str): #prints player's name, team, kills, deaths, assists, KDA and damage dealt to champions
        gameInfo = self.getGameParticipantInfo(puuid, 'Jungle') # role is a placeholder here
        if gameInfo:
            print("Name:", gameInfo.riotIdGameName)
            print("Team:", gameInfo.team)
            print("Kills:", gameInfo.kills)
            print("Deaths:", gameInfo.deaths)
            print("Assists:", gameInfo.assists)
            print("KDA:", round(gameInfo.getKDA(), 2))
        else:
            print("Game not found.")        
    
    def printInfo(self): #prints all game participant's gameName, champion, kills, deaths, assists and damage dealt for the game
        for participant in self.participants:
            print(str(participant['riotIdGameName']) + ' played ' + str(participant['championName']), ', had ' + str(participant['kills']) + ' kills, ' + str(participant['deaths']) + ' deaths ' +  str(participant['assists']) + ' assists and dealt ' + str(participant['totalDamageDealtToChampions']) + ' damage')

    def createDamageChart(self): #creates chart showing damage for each team with the corresponding team colors
        viz.createDamageChart(self.participants)

class GameParticipant:
    def __init__(self, game: Game, player: dict[str, Any], role: str, riotIdGameName: str, teamid: int, win: bool, kills: int, deaths: int, assists: int):
        self.game: Game = game
        self.player: dict[str, Any] = player
        self.riotIdGameName: str = riotIdGameName
        self.team: str = game.redTeam if teamid == 100 else game.blueTeam
        self.win: bool = win
        self.kills: int = kills
        self.deaths: int = deaths
        self.assists: int = assists
        self.roleWeights: list[int] = playerScoreWeights.weights[role] # returns variable weights depending on the player's role as responsibilities differ
        self.weightedValuesList: list = self.calculateWeightedValues()
        self.playerScore: float = self.calculatePlayerScore()

    def getKDA(self) -> float:
        if self.deaths == 0: 
            return (self.kills + self.assists) # if player doesn't die during the game, his KDA is perfect and equals sum of kills and assists
        return (self.kills + self.assists) / self.deaths

    def getDPM(self) -> float: # DPM means Damage per Minute
        return self.player['totalDamageDealtToChampions'] / self.game.duration

    def calculateWeightedValues(self) -> list[float]: # to calculate the weighted variable, normal variable is divided by the max value * the weight
        roleWeights: list = self.roleWeights
        maxValues: dict = playerScoreWeights.getMaxValues(self.game.duration)
        weightedWin: int = self.win * roleWeights[0]
        weightedKDA: float = min(self.getKDA() / maxValues['KDA'] * roleWeights[1], roleWeights[1])
        weightedDDTT: float = min(self.player['damageDealtToTurrets'] / maxValues['DDTT'] * roleWeights[2], roleWeights[2]) # DDTT means Damage Dealt to Turrets 
        weightedDPM: float = min(self.getDPM() / maxValues['DPM'] * roleWeights[3], roleWeights[3]) 
        weightedCC: float = min((self.player['timeCCingOthers'] / (self.game.duration * maxValues['ccPerMinute'])) * roleWeights[4], roleWeights[4]) # CC means Crowd Control, counted in seconds
        weightedHeals: float = min((self.player['totalHealsOnTeammates'] / (self.game.duration * maxValues['healsPerMinute'])) * roleWeights[5], roleWeights[5]) 
        weightedShields: float = min((self.player['totalDamageShieldedOnTeammates'] / (self.game.duration * maxValues['shieldsPerMinute'])) * roleWeights[6], roleWeights[6]) 
        weightedMinions: float = min((self.player['neutralMinionsKilled'] / (self.game.duration * maxValues['minionsPerMinute'])) * roleWeights[7], roleWeights[7]) 
        weightedVision: float = min((self.player['visionScore'] / (self.game.duration * maxValues['visionPerMinute'])) * roleWeights[8], roleWeights[8])
        weightedObjectiveKills: float = min((self.player['baronKills'] + self.player['dragonKills'] / (maxValues['baronKills'] + maxValues['dragonKills'])) * roleWeights[9], roleWeights[9]) 
        weightedMitigatedDamage: float = min((self.player['damageSelfMitigated'] / (self.game.duration * maxValues['mitigatedDamagePerMinute'])) * roleWeights[10], roleWeights[10])
        return [weightedWin, weightedKDA, weightedDDTT, weightedDPM, weightedCC, weightedHeals, weightedShields, weightedMinions, weightedVision, weightedObjectiveKills, weightedMitigatedDamage]

    def calculatePlayerScore(self) -> float: # returns player's score, a number with 2 decimals capped to 100.
        score = sum(self.weightedValuesList) * 100
        return round(score,2)
        
    def createStatsChart(self):   
        roleWeights: list[int] = self.roleWeights
        viz.createStatsChart(self.weightedValuesList, roleWeights)

class Champions:
    def __init__(self, championId, championName):
        self.championId = championId
        self.championName = championName

class Challenges:
    def __init__(self, challenges: list[dict], totalpoints: int):
        self.challenges: list[dict] = challenges
        self.challengeNames: dict[str, int] = self.getChallengeNames()
        self.totalpoints: int = totalpoints
        self.aramChallenges: list[str] = []
        self.aramPoints: list[float] = []
        self.aramLevel: list[str] = []
        self.challengeCaps: list[float] = []
        self.aramParentIds: list[str] = ['101000','101100','101200','101300'] #where 101000, 101100, 101200 and 101300 are the iDs for the ARAM parent challenges respectivelly.
        for challenge in self.challenges:
            file = jsonData['challenges'][str(challenge['challengeId'])]
            if 'tags' in file and 'parent' in file['tags']:
                if file['tags']['parent'] in self.aramParentIds: 
                    self.aramChallenges += [file['name']]
                    self.aramLevel += [challenge['level']]
                    self.aramPoints += [int(challenge['value'])]
                    if file['name'] == 'Pop Goes the Poro':
                        self.challengeCaps += [file['thresholds']['BRONZE']['value']]
                    if 'thresholds' in file and 'MASTER' in file['thresholds']:
                        self.challengeCaps += [file['thresholds']['MASTER']['value']]
    
    def getChallengeNames(self) -> dict[str, int]: # creates a dictionary with challenge names as the keys and challenge ids as the values
        challengeNames = {}
        for challenge in self.challenges:
            challengeInfo = ChallengeInfo(challenge['challengeId'],
                    challenge['percentile'],
                    challenge['level'],
                    challenge['value']
                )
            challengeNames[challengeInfo.challengeName] = challengeInfo.challengeId
        return challengeNames

    def getChallengeInfo(self, challengeId: int): #if challenge ID requested exists, returns challenge Id, percentile, level and value, stores it in class Challengeinfo
        for challenge in self.challenges:
            if challenge['challengeId'] == challengeId:
                return ChallengeInfo(
                    challenge['challengeId'],
                    challenge['percentile'],
                    challenge['level'],
                    challenge['value']
                )
        print("Challenge with ID", challengeId, "not found.")
        return None

    def printChallengeInfo(self, challengeId: int): #if challenge ID requested exists, prints challenge Id, percentile, level and value
        challengeInfo = self.getChallengeInfo(challengeId)
        if challengeInfo:
            print('Challenge Name:', challengeInfo.challengeName)
            print('Challenge ID:', challengeId)
            print("Percentile:", challengeInfo.challengePercentile * 100, '%')
            print("Level:", challengeInfo.challengeLevel)
            print("Value:", challengeInfo.challengeValue)
        else:
            print("Challenge not found.")

    def normalizeAramChallenges(self) -> list[float]: # returns normalized challenges in a scale of 0 to 100
        normalizedChallenges: list[float] = []
        for challenge in range(len(self.aramChallenges)):
            normalizedChallenges += [min((self.aramPoints[challenge] / self.challengeCaps[challenge]) * 100, 100)]
        return normalizedChallenges
    
    def createAramChallengeChart(self):
        normalizedChallenges: list[float] = self.normalizeAramChallenges()
        viz.createAramChallengeChart(self.aramChallenges, normalizedChallenges, self.aramLevel)

    def printChallenges(self):
        for challenge in self.challenges:
            print('Challenge: ' + jsonData['challenges'][str(challenge['challengeId'])]["name"] + ', level:', str(challenge['level']) + ' , points: ' + str(challenge['value']))

class ChallengeInfo:
    def __init__(self, challengeId: int, challengePercentile: float, challengeLevel: str, challengeValue: float):
        self.challengeId: int = challengeId
        self.challengeName: str = jsonData["challenges"][str(challengeId)]["name"] # utilizes challenges.py to find the name of each challenge based on challenge id
        self.challengePercentile: float = challengePercentile
        self.challengeLevel: str = challengeLevel
        self.challengeValue: float = challengeValue
        
class MasteryPoints:
    def __init__(self, championName: list[str], points: list[int]):
        self.championName: list[str] = championName
        self.masteryPoints: list[int] = points

    def printTopChampions(self, numberOfChampions: int):
        print(self.championName[:numberOfChampions], self.masteryPoints[:numberOfChampions])

    def createMasteryChart(self, numberOfChampions: int): #creates chart of top x champions with most mastery points of selected player
        viz.createMasteryChart(self.championName, self.masteryPoints, numberOfChampions)

class PlayerStats:
    def __init__(self, puuid: str):
        self.puuid: str = puuid
        self.numberOfGames: int = 0
        self.gameIds: list[int] = []
        self.gameDurations: list[float] = []
        self.kills: list[int] = []
        self.deaths: list[int] = []
        self.assists: list[int] = []
        self.damageDealt: list[float] = []
        self.matchHistory: list[str] = []

    def addGameIfParticipant(self, game, gameParticipant): #adds game statistics to class PlayerStats if the participant is part of the game and the game ID is not already present
        for participant in game.participants:
            if participant['puuid'] == self.puuid and game.gameId not in self.gameIds:
                gameFound = True
                self.numberOfGames += 1
                self.gameIds += [game.gameId]
                self.gameDurations += [game.duration]
                self.kills += [participant['kills']]
                self.deaths += [participant['deaths']]
                self.assists += [participant['assists']]
                self.damageDealt += [participant['totalDamageDealtToChampions']]
                self.matchHistory += [f" game id: {game.gameId}, game duration: {game.duration} minutes, result: {'win!' if gameParticipant.win else 'loss'}"]
                break
        if not gameFound:
            raise ValueError('Puuid or game not found')
        
    def printMatchHistory(self):
        for match in self.matchHistory:
            print(match)

    def returnAvgGameTime(self) -> float:
        return round(sum(self.gameDurations) / len(self.gameDurations), 2)
    
    def returnAvgKills(self) -> float:
        return sum(self.kills) / len(self.kills)
    
    def returnAvgDeaths(self) -> float:
        return sum(self.deaths) / len(self.deaths) 
      
    def returnAvgAssists(self) -> float:
        return sum(self.assists) / len(self.assists)
    
    def returnAvgDamageDealt(self) -> float:
        return sum(self.damageDealt) / len(self.damageDealt)
    
    def printAllStats(self):
        print(f"average game time: {self.returnAvgGameTime()}, " +
      f"average kills: {self.returnAvgKills()}, " +
      f"average deaths: {self.returnAvgDeaths()}, " +
      f"average assists: {self.returnAvgAssists()}, " +
      f"average damage dealt: {self.returnAvgDamageDealt()}")

    def plotStats(self): #creates 4 plots depicting game duration, kills, deaths and damage dealt for all games for selected player
        viz.plotStats(self.numberOfGames, self.gameDurations, self.kills, self.deaths, self.damageDealt)

def apiRequests(url: str, params: dict)-> Any:
    try:
        response = requests.get(url, params = params)
        response_json = response.json()
        response.raise_for_status()
        return response_json 
    except requests.exceptions.HTTPError as errh: 
        print('HTTP Error') 
        print(errh.args[0])
        if response.status_code == 403:
            print('wrong or expired key')
        elif response.status_code == 404:
            print('Player not found')
    except requests.exceptions.ReadTimeout as errrt: 
        print('Time out') 
    except requests.exceptions.ConnectionError as conerr: 
        print('Connection error')
        print('wrong region, try again')
        return
    except requests.exceptions.RequestException as errex: 
        print('Exception request')

def getPlayerInfo(region: str, gameName: str, tagline: str): #returns puuid, summonerID, summonerTag, region for designated player from API and stores it in class Player
    url: str = f'https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagline}'
    payload: dict = {"api_key": key}
    response_json: dict[Any, Any] = apiRequests(url, payload)
    if response_json:
        return Player(response_json['puuid'], response_json['gameName'], response_json['tagLine'], region)
    return None

def getMatchIds(region: str, puuid: str) -> list[int]: #returns match Ids for last 20 games for specified puuid
    url: str = f'https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids'
    payload: dict = {"api_key": key}
    response_json: list[int] = apiRequests(url, payload)
    if response_json:
        return response_json
    return []

def getGame(region: str, matchId: int): #gets gameId, result, duration, participants about a designated match from API and stores it in class Game
    url: str = f'https://{region}.api.riotgames.com/lol/match/v5/matches/{matchId}'
    payload: dict = {"api_key": key}
    response_json: dict[Any, Any] = apiRequests(url, payload)
    if response_json:
        data = response_json['info']
        return Game(data['gameId'], data['teams'], data['gameDuration'], data['participants'])
    return None

def getChallenges(puuid: str): #gets challenges for player from API and stores it in class Challenges
    url: str = f'https://eun1.api.riotgames.com/lol/challenges/v1/player-data/{puuid}'
    payload: dict = {"api_key": key}
    response_json: dict[Any, Any] = apiRequests(url, payload)
    if response_json:
        data = response_json['challenges']
        return Challenges(data, response_json['totalPoints'])
    return None

def getMasteryPoints(puuid: str): #gets Champion names and Mastery points from API and stores them in class MasteryPoints
    url: str = f'https://eun1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}'
    payload: dict = {"api_key": key}
    response_json: list = apiRequests(url, payload)
    if response_json:
        names: list[str] = []
        points: list[int] = []
        for champion in response_json:
            names += [all_champion_id[champion['championId']]]
            points += [champion['championPoints']]
        return MasteryPoints(names, points)
    return None