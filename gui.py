from tkinter import *
from tkinter import ttk
import shadowtracker

account = None
challenges = None
matchIds = None
game = None

def findPlayer():
    global account
    account = shadowtracker.getPlayerInfo(regionEntry.get(), nameEntry.get(), puuidEntry.get())
    global matchIds
    matchIds = shadowtracker.getMatchIds(account.region, account.puuid)
    global challenges
    challenges = shadowtracker.getChallenges(account.puuid)
    openOptionsWindow()

def openOptionsWindow():
    optionsWindow = Toplevel(root)
    optionsWindow.title('ShadowTracker - Options')
    optionsWindow.geometry('300x250')
    optionsWindow.resizable(False, False)

    Button(optionsWindow, text='Challenges', command=openChallengesWindow).pack(pady=10)
    Button(optionsWindow, text='Top Champions', command=findTopChampions).pack(pady=10)
    Button(optionsWindow, text='Match History', command=openGamesWindow).pack(pady=10)
    Button(optionsWindow, text='Player Stats', command=openStatsWindow).pack(pady=10)
    Button(optionsWindow, text='Back', command=optionsWindow.destroy).pack(pady=10)

def showAramChallengeChart():  
    challenges.createAramChallengeChart()

def findChallengeByName(name):
    id = challenges.challengeNames[name]
    challenges.printChallengeInfo(id)

def openChallengesWindow():
    challengesWindow = Toplevel(root)
    challengesWindow.title('Challenges - Options')
    challengesWindow.geometry('300x250')
    challengesWindow.resizable(False, False)
    Label(challengesWindow, text='Challenge ID:').pack(pady=10)
    challengeNames = list(challenges.challengeNames.keys())
    challengeEntry = ttk.Combobox(challengesWindow, values=challengeNames)
    challengeEntry.pack(pady=10)
    Button(challengesWindow, text='Find Challenge', command=lambda: findChallengeByName(challengeEntry.get())).pack(pady=10)
    Button(challengesWindow, text='Aram Challenges Chart', command=showAramChallengeChart).pack(pady=10)
    Button(challengesWindow, text='Back', command=challengesWindow.destroy).pack(pady=10)

def findTopChampions():
    points = shadowtracker.getMasteryPoints(account.puuid)
    points.createMasteryChart(10)

def getDataForGames(role):
    playerStats = shadowtracker.PlayerStats(account.puuid)
    for matchId in reversed(matchIds):
        game = shadowtracker.getGame(account.region, matchId)
        gameParticipant = game.getGameParticipantInfo(account.puuid, role)
        playerStats.addGameIfParticipant(game, gameParticipant)
    return playerStats

def printMatchHistory():
    matches = getDataForGames('Jungle') # 'Jungle' is just a placeholder here
    matches.printMatchHistory()

def findPlayerStats(role):
    matches = getDataForGames(role)
    matches.printAllStats()

def showPlayerCharts(role):
    matches = getDataForGames(role)
    matches.plotStats()

def findGameStats():
    game.printGameInfo()
    game.printInfo()

def showDamageGraph():
    game.createDamageChart()

def getGameScore(role):
    gameParticipant = game.getGameParticipantInfo(account.puuid, role)
    print(f"Player's Score was: {gameParticipant.playerScore} / 100")

def getScoreChart(role):
    gameParticipant = game.getGameParticipantInfo(account.puuid, role)
    gameParticipant.createStatsChart()

def openGamesWindow():
    def on_game_selected(event):
        global game
        game = shadowtracker.getGame(account.region, gameEntry.get())

    gamesWindow = Toplevel(root)
    gamesWindow.title('Challenges - Games Stats')
    gamesWindow.geometry('300x450')
    gamesWindow.resizable(False, False)
    Button(gamesWindow, text='Match History', command= printMatchHistory).pack(pady=10)

    Label(gamesWindow, text='Game:').pack(pady=10)
    gameEntry = ttk.Combobox(gamesWindow, values=matchIds)
    gameEntry.pack(pady=10)
    gameEntry.bind("<<ComboboxSelected>>", on_game_selected)

    Label(gamesWindow, text='Role:').pack(pady=10)
    roles =['Tank Top', 'Bruiser', 'Jungle', 'Mid', 'ADC', 'Heal Supp', 'Tank Supp']
    roleEntry = ttk.Combobox(gamesWindow, values=roles)
    roleEntry.pack(pady=10)
    
    Button(gamesWindow, text='Show Game Info', command=findGameStats).pack(pady=10)
    Button(gamesWindow, text='Show Damage Graph', command=showDamageGraph).pack(pady=10)
    Button(gamesWindow, text='Show Player Score', command= lambda: getGameScore(roleEntry.get())).pack(pady=10)
    Button(gamesWindow, text='Show Score Chart', command= lambda: getScoreChart(roleEntry.get())).pack(pady=10)
    Button(gamesWindow, text='Back', command=gamesWindow.destroy).pack(pady=10)

def openStatsWindow():
    playerWindow = Toplevel(root)
    playerWindow.title('Challenges - Games Stats')
    playerWindow.geometry('300x200')
    playerWindow.resizable(False, False)
    
    Button(playerWindow, text='Show Player Stats', command=lambda: findPlayerStats('Jungle')).pack(pady=10)
    Button(playerWindow, text='Show Stats Chart', command=lambda: showPlayerCharts('Jungle')).pack(pady=10)
    Button(playerWindow, text='Back', command=playerWindow.destroy).pack(pady=10)

# Main window
root = Tk()
root.title('ShadowTracker')
root.geometry('300x200')
root.resizable(False, False)

Label(root, text='Region:').grid(row=0)
Label(root, text='Name:').grid(row=1)
Label(root, text='Tag:').grid(row=2)

options = ['americas', 'asia', 'europe']
regionEntry = ttk.Combobox(values=options)
nameEntry = Entry(root)
puuidEntry = Entry(root)

regionEntry.grid(row=0, column=1)
nameEntry.grid(row=1, column=1)
puuidEntry.grid(row=2, column=1)

Button(root, text='Find Player', command=findPlayer).grid(row=3, column=1)

root.mainloop()
