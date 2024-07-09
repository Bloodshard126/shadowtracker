import shadowtracker

account = shadowtracker.getPlayerInfo('europe', 'Baxari', '1806')
matchIds = shadowtracker.getMatchIds(account.region, account.puuid)

challenges = shadowtracker.getChallenges(account.puuid)
challenges.printChallengeInfo(101100)
challenges.createAramChallengeChart()

game = shadowtracker.getGame(account.region, matchIds[2])
game.printGameParticipantInfo(account.puuid)
game.printInfo()
game.printGameInfo()
game.createDamageChart()

points = shadowtracker.getMasteryPoints(account.puuid)
points.printTopChampions(5)
points.createMasteryChart(10)

gameParticipant = game.getGameParticipantInfo(account.puuid, 'Jungle')
print(gameParticipant.calculatePlayerScore())

playerStats = shadowtracker.PlayerStats(account.puuid)
for matchId in reversed(matchIds):
    game = shadowtracker.getGame(account.region, matchId)
    gameParticipant = game.getGameParticipantInfo(account.puuid, 'Jungle')
    playerStats.addGameIfParticipant(game, gameParticipant)
playerStats.printMatchHistory()
#playerStats.plotStats()

print(gameParticipant.calculatePlayerScore())
gameParticipant.createStatsChart()

