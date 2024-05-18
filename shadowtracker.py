import requests
import os
from dotenv import find_dotenv, load_dotenv

dotenvPath = find_dotenv()
load_dotenv(dotenvPath)
key = os.getenv('shadowtrackerApiKey') #key as env variable

from challenges import jsonData #imports challenges information (challenge Titles) from JSON file

championsLink = 'https://github.com/Najsr/League-Of-Legends-Champions-ID-List/blob/master/list.php'

class Player:
    def __init__(self, puuid, summonerID, summonerTag, region):
        self.puuid = puuid
        self.summonerID = summonerID
        self.summonerTag = summonerTag
        self.region = region

class Game:
    def __init__(self, gameId, result, duration, participants):
        self.gameId = gameId
        self.result = result
        self.duration = duration / 60 #duration is returned in seconds, divided by 60 to get duration in minutes
        self.participants = participants

    def getGameParticipantInfo(self, puuid): #returns players's puuid, kills, deaths, asstists and totaldamage dealt for game, stores it in class GameParticipant
        for player in self.participants:
            if player['puuid'] == puuid:
                return GameParticipant(
                    player['puuid'],
                    player['kills'], 
                    player['deaths'], 
                    player['assists'],
                    player['totalDamageDealtToChampions'])
    
    def printGameParticipantInfo(self, puuid): #prints player's puuid, kills, deaths, assists and total damage dealt to champions
        gameInfo = self.getGameParticipantInfo(puuid)
        if gameInfo:
            print("Puuid:", gameInfo.puuid)
            print("Kills:", gameInfo.kills)
            print("Deaths:", gameInfo.deaths)
            print("Assists:", gameInfo.assists)
            print('Total Damage Dealt:', gameInfo.totalDamageDealtToChampions)
        else:
            print("Game not found.")        
    
    def printInfo(self): #prints all game participant's gameName, kills, deaths, assists and damage dealt for the game
        for participant in self.participants:
            print(str(participant['riotIdGameName']) + ' had ' + str(participant['kills']) + ' kills, ' + str(participant['deaths']) + ' deaths ' +  str(participant['assists']) + ' assists and dealt ' + str(participant['totalDamageDealtToChampions']) + ' damage')

class GameParticipant:
    def __init__(self, puuid, kills, deaths, assists, totalDamageDealtToChampions):
        self.puuid = puuid
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.totalDamageDealtToChampions = totalDamageDealtToChampions

    def getKDA(self): #calculates and returns the KDA of the selected player for the game
        pass

    def getDamageDealt(self): #returns physical, magical and total damage dealt by the selected player for the game
        pass

class Champions:
    def __init__(self, championId, championName):
        self.championId = championId
        self.championName = championName

class Challenges:
    def __init__(self, challenges, totalpoints):
        self.challenges = challenges
        self.totalpoints = totalpoints

    def getChallengeInfo(self, challengeId): #if challenge ID requested exists, returns challenge Id, percentile, level and value, stores it in class Challengeinfo
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

    def printChallengeInfo(self, challengeId): #if challenge ID requested exists, prints challenge Id, percentile, level and value
        challengeInfo = self.getChallengeInfo(challengeId)
        if challengeInfo:
            print("Challenge Name:", challengeInfo.challengeName)
            print("Percentile:", challengeInfo.challengePercentile)
            print("Level:", challengeInfo.challengeLevel)
            print("Value:", challengeInfo.challengeValue)
        else:
            print("Challenge not found.")
    
    def printChallenges(self): #prints challenge name, level and value for all challenges for selected account
        for challenge in self.challenges:
            print('Challenge: ' + jsonData["challenges"][str(challenge['challengeId'])]["name"] + ', level:', str(challenge['level']) + ' , points: ' + str(challenge['value']))

class ChallengeInfo:
    def __init__(self, challengeId, challengePercentile, challengeLevel, challengeValue):
        self.challengeId = challengeId
        self.challengeName = jsonData["challenges"][str(challengeId)]["name"]
        self.challengePercentile = challengePercentile
        self.challengeLevel = challengeLevel
        self.challengeValue = challengeValue
        
class MasteryPoints:
    pass

def getPlayerInfo(region, gameName, tagline): #returns puuid, summonerID, summonerTag, region for designated player from API and stores it in class Player
    url = f'https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagline}'
    payload = {"api_key": key}
    response = requests.get(url, params = payload)
    response_json = response.json()

    return Player(response_json['puuid'], response_json['gameName'], response_json['tagLine'], region)

def getMatchIds(region, puuid): #returns match Ids for last 20 games for specified puuid
    url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids'
    payload = {"api_key": key}
    response = requests.get(url, params = payload)
    response_json = response.json()
  
    return response_json

def getGame(region, matchId): #gets gameId, result, duration, participants about a designated match from API and stores it in class Game
    url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/{matchId}'
    payload = {"api_key": key}
    response = requests.get(url, params = payload)
    response_json = response.json()
    data = response_json['info']
    
    return Game(data['gameId'], data['endOfGameResult'], data['gameDuration'], data['participants'])

def getChallenges(puuid): #gets challenges for player from API and stores it in class Challenges
    url = f'https://eun1.api.riotgames.com/lol/challenges/v1/player-data/{puuid}'
    payload = {"api_key": key}
    response = requests.get(url, params = payload)
    response_json = response.json()
    data = response_json['challenges']
 
    return Challenges(data, response_json['totalPoints'])

def changeChampionId(championID): #returns champion name for given championID, stores it in class Champions
    pass

def changeChallengeId(challengeId): #returns challenge name for given challengeId, stores it in class Challenges
    pass

def getStats(numberofGames): #returns average game length, win rate, KDA and damage for numberofgames for selected player
    pass