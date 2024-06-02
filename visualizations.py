import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from typing import Any
import numpy as np

def createDamageChart(participants: list[dict]):
    players: list[str] = []
    damage: list[int] = []
    teamColors: list[str] = []
    for player in participants:
        players += [player['riotIdGameName']]
        damage += [player['totalDamageDealtToChampions']]
        teamColor = 'blue' if player['teamId'] == 200 else 'red'
        teamColors += [teamColor]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    ax1.barh(players[:5], damage[:5], color=teamColors[5])
    ax2.barh(players[5:], damage[5:], color=teamColors[0])
    plt.xlabel('Damage Dealt to Champions')
    plt.tight_layout()
    plt.show()

def createAramChallengeChart(aramChallenges: list[str], normalizedChallenges: list[str], aramLevel: list[str]):
    colors: dict = {
        "IRON": "#6A4E42",  # Brownish color for iron
        "BRONZE": "#CD7F32",  # Bronze
        "SILVER": "#C0C0C0",  # Silver
        "GOLD": "#FFD700",  # Gold
        "PLATINUM": "#1FF497",  # Platinum
        "DIAMOND": "#00BFFF",  # Blue for diamond
        "MASTER": "#FF00FF",  # Magenta for master
        "GRANDMASTER": "#FF4500",  # Orange red for grandmaster
        "CHALLENGER": "#FF0000"  # Red for challenger
    }
    bars = plt.barh(aramChallenges, normalizedChallenges, color=[colors[level] for level in aramLevel])
    legend_handles = [Patch(color=color, label=rank) for rank, color in colors.items()]
    plt.legend(handles=legend_handles, title="Ranks", loc='center left', bbox_to_anchor=(1, 0.5))
    plt.xlabel('Percentage (%)')
    plt.ylabel('Challenge')
    plt.title('Normalized Challenge Progress Compared to Max Amount')
    plt.show()

def createMasteryChart(championName: list[str], masteryPoints: list[int], numberOfChampions: int):
    plt.barh(championName[:numberOfChampions], masteryPoints[:numberOfChampions])
    plt.xlabel('Mastery Points')
    plt.ylabel('Champions')
    plt.title('Mastery Points per Champion')
    plt.gca().invert_yaxis()
    plt.show()

def plotStats(numberOfGames: int, gameDurations: list[float], kills: list[int], deaths: list[int], damageDealt: list[int]):
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    ticks = range(0, numberOfGames + 2, 2)

    # Game durations
    axs[0, 0].plot(range(len(gameDurations)), gameDurations, marker='o', color='blue')
    axs[0, 0].set_title('Game Duration')
    axs[0, 0].set_xlabel('Game Number')
    axs[0, 0].set_ylabel('Duration (minutes)')
    axs[0, 0].set_xticks(ticks)

    # Kills
    axs[0, 1].plot(range(len(kills)), kills, marker='o', color='green')
    axs[0, 1].set_title('Kills per Game')
    axs[0, 1].set_xlabel('Game Number')
    axs[0, 1].set_ylabel('Kills')
    axs[0, 1].set_xticks(ticks)

    # Deaths
    axs[1, 0].plot(range(len(deaths)), deaths, marker='o', color='red')
    axs[1, 0].set_title('Deaths per Game')
    axs[1, 0].set_xlabel('Game Number')
    axs[1, 0].set_ylabel('Deaths')
    axs[1, 0].set_xticks(ticks)

    # Damage Dealt
    axs[1, 1].plot(range(len(damageDealt)), damageDealt, marker='o', color='purple')
    axs[1, 1].set_title('Damage Dealt per Game')
    axs[1, 1].set_xlabel('Game Number')
    axs[1, 1].set_ylabel('Damage Dealt')
    axs[1, 1].set_xticks(ticks)

    plt.tight_layout()
    plt.show()

def createStatsChart(valuesList: list[float], roleWeights: list[int]):
    valueslistArray = np.arange(len(valuesList))
    labels: list[str] = [ 'Win','KDA', 'DDTT','DPM','ccPerMinute','healsPerMinute','shieldsPerMinute','minionsPerMinute','visionPerMinute','Objectives','mitigatedDamagePerMinute']
    valuesArray = np.array(valuesList)
    roleWeightsArray = np.array(roleWeights)
    normalizedValues = []
    for i in range(len(valuesArray)):
        if roleWeightsArray[i] != 0:
            normalizedValues.append(valuesArray[i]/roleWeightsArray[i])
        else:
            normalizedValues.append(0)
    normalizedValuesArray = np.array(normalizedValues)
    normalizedValuesArray *= 100

    plt.barh(valueslistArray, normalizedValuesArray)
    plt.yticks(valueslistArray, labels)
    plt.xlabel('Max Values')
    plt.ylabel('Variables')
    plt.title('Weighted Variables Score')
    plt.show()

