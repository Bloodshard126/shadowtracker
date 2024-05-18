import shadowtracker

""" for game in matchIds:
    gameInfo = getGame(account.region, game)
    gameInfo.printInfo()
    break  """

account = shadowtracker.getPlayerInfo('europe', 'Krokonut', '5578')
matchIds = shadowtracker.getMatchIds(account.region, account.puuid)

challenges = shadowtracker.getChallenges(account.puuid)
challenges.printChallengeInfo(101000)
challenges.printChallenges()

game = shadowtracker.getGame(account.region, matchIds[0])
game.printGameParticipantInfo(account.puuid)
game.printInfo()