# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: 
    Aaron Fox
    Centre for Sport Research
    Deakin University
    aaron.f@deakin.edu.au
    
"""

# %% Import packages

import os
import pandas as pd
import json
import glob
import re

# %% Define functions

#Sort json file list alpha-numerically so that round 1 remains first
def sortedNicely(l):
    """ Sorts the given iterable in the way that is expected.
    Required arguments:
    l -- The iterable to be sorted. """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key = alphanum_key)

# %% Set-up

#Navigate to existing folder with match data
os.chdir('..\\..\\super-netball-analysis\\Projects\\winProbability\\MatchData')

#Identify SSN regular season match data
fileList = []
#Get all SSN files
for file in glob.glob("SSN_*.json"):
    fileList.append(file)
#Extract only up to round 14
jsonFileList = []
for file in fileList:
    #Extract round
    rd = int(file.split('_')[2].split('r')[1])
    #Append if round 14 or less
    if rd <= 14:
        jsonFileList.append(file)
        
#Sort the file list nicely
jsonFileList = sortedNicely(jsonFileList)

#Set player stats to extract
#2017
playerStats2017 = ['startingPositionCode', 'minutesPlayed', 'squadId', 'playerId',
                   'centrePassReceives', 'feeds',
                   'deflections', 'gain', 
                   'goalAssists', 'goalAttempts', 'goalMisses', 'goals',
                   'turnovers', 'intercepts',
                   'obstructionPenalties', 'offsides', 'contactPenalties', 'penalties',
                   'rebounds']
#2018+
playerStats2018 = ['startingPositionCode', 'minutesPlayed', 'squadId', 'playerId',
                   'centrePassReceives', 'feeds', 'feedWithAttempt',
                   'deflectionWithGain', 'deflectionWithNoGain', 'gain', 
                   'goalAssists', 'goalAttempts', 'goalMisses', 'goals',
                   'intercepts', 'generalPlayTurnovers',
                   'obstructionPenalties', 'offsides', 'contactPenalties', 'penalties',
                   'netPoints', 'rebounds']

#Set dictionary to store data in
dataDict = {'playerName': [], 'squadName': [], 'year': [], 'round': [],
            'startingPositionCode': [], 'minutesPlayed': [], 'squadId': [], 'playerId': [],
            'centrePassReceives': [], 'feeds': [], 'feedWithAttempt': [],
            'deflections': [], 'deflectionWithGain': [], 'deflectionWithNoGain': [],
            'gain': [], 
            'goalAssists': [], 'goalAttempts': [], 'goalMisses': [], 'goals': [],
            'turnovers': [], 'generalPlayTurnovers': [], 'intercepts': [],
            'obstructionPenalties': [], 'offsides': [], 'contactPenalties': [], 'penalties': [],
            'netPoints': [], 'rebounds': []}

# %% Extract match data

#Loop through files
for file in jsonFileList:
    
    #Load the .json data
    with open(file) as json_file:
        data = json.load(json_file)
        
    #Get number of players to loop through in game
    nPlayers = len(data['playerStats']['player'])
    
    #Get current round
    rNo = data['matchInfo']['roundNumber'][0]
    
    #Get current year
    yNo = int(file.split('_')[1])
    
    #Loop through players for the match
    for playerNo in range(nPlayers):
        
        #Loop through and extract the players stats
        if yNo == 2017:
            for stat in playerStats2017:
                dataDict[stat].append(data['playerStats']['player'][playerNo][stat][0])
            #Add in empty stats for different year
            dataDict['deflectionWithGain'].append('n/a')
            dataDict['deflectionWithNoGain'].append('n/a')
            dataDict['generalPlayTurnovers'].append('n/a')
            dataDict['feedWithAttempt'].append('n/a')
            dataDict['netPoints'].append('n/a')
        else:
            for stat in playerStats2018:
                dataDict[stat].append(data['playerStats']['player'][playerNo][stat][0])
            #Add in empty stats for different year
            dataDict['deflections'].append('n/a')
            dataDict['turnovers'].append('n/a')
            
            
        #Append round and year
        dataDict['year'].append(yNo)
        dataDict['round'].append(rNo)
        
        #Find squad and player name
        squadId = data['playerStats']['player'][playerNo]['squadId'][0]
        playerId = data['playerStats']['player'][playerNo]['playerId'][0]
        
        #Append to dictionary
        #Team name
        for teamNo in range(len(data['teamInfo']['team'])):
            #Check first team
            if data['teamInfo']['team'][teamNo]['squadId'][0] == squadId:
                dataDict['squadName'].append(data['teamInfo']['team'][teamNo]['squadNickname'][0])
            #Check second team
            elif data['teamInfo']['team'][teamNo]['squadId'][0] == squadId:
                dataDict['squadName'].append(data['teamInfo']['team'][teamNo]['squadNickname'][0])
        #Player name
        checkPlayer = True
        playerNo = 0
        while checkPlayer:
            #Check current player id
            if playerId == data['playerInfo']['player'][playerNo]['playerId'][0]:
                #Append to dictionary
                dataDict['playerName'].append(data['playerInfo']['player'][playerNo]['displayName'][0])
                #Stop looking for player
                checkPlayer = False
            else:
                #Move on to next player
                playerNo += 1

#Convert to dataframe
playerData = pd.DataFrame.from_dict(dataDict)

#Export to file
os.chdir('..\\..\\..\\..\\netball-numbers-challenge\\datasets\\vol5')
playerData.to_csv('superNetballersOfChristmas.csv', index = False)
playerData.to_excel('superNetballersOfChristmas.xlsx', index = False)
    
# %%% ----- End of superNetballersOfChristmas_compileDataset.py -----