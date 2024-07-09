weights: dict[str, list] = {
'Tank Top':    [0.15, 0.10, 0.5, 0.5, 0.15, 0, 0, 0.20, 0.10, 0, 0.20],
'Bruiser':   [0.15, 0.15, 0.20, 0.10, 0, 0,  0, 0.20, 0.10, 0, 0.10],
'Jungle':      [0.15, 0.20, 0.05, 0.05, 0.05, 0, 0, 0.10, 0.20, 0.10, 0.10],
'Mid':         [0.15, 0.25, 0.15, 0.20, 0, 0, 0, 0.15, 0.10, 0, 0],
'ADC':         [0.15, 0.15, 0.15, 0.25, 0, 0, 0, 0.20, 0.10,  0, 0],
'Heal Supp':   [0.15, 0.25, 0,  0.5,  0,  0.25, 0, 0, 0.30, 0, 0],
'Tank Supp':   [0.15, 0.20, 0,  0, 0.15, 0, 0, 0, 0.30, 0, 0.20]
}

def getMaxValues(duration: float) -> dict:
    gameDuration: float = duration
    BaronSpawnTime: int = 20
    DragonSpawnTime: int = 4
    BaronRespawnInterval: int = 5
    DragonRespawnInterval: int = 5
    maxvalues: dict = {
    'KDA': 4,
    'DDTT': 15000,
    'DPM': 1800,
    'ccPerMinute': 2,
    'healsPerMinute': 200,
    'shieldsPerMinute': 200,
    'minionsPerMinute': 10,
    'visionPerMinute': 2,
    'baronKills' : (gameDuration - BaronSpawnTime) % BaronRespawnInterval,
    'dragonKills' : (gameDuration - DragonSpawnTime) % DragonRespawnInterval,
    'mitigatedDamagePerMinute' : 2000
}
    return maxvalues