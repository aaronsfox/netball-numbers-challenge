# -*- coding: utf-8 -*-
"""

@author: 
    Aaron Fox
    Centre for Sport Research
    Deakin University
    aaron.f@deakin.edu.au
    
    Extracts player data from Champion Data match centre files.
    
"""

# %% Import packages

import pandas as pd
import os
import glob
import json
import numpy as np
import re

# %% Define functions

#Sort file list alpha-numerically so that round 1 remains first
def sortedNicely(l):
    """ Sorts the given iterable in the way that is expected.
    Required arguments:
    l -- The iterable to be sorted. """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key = alphanum_key)

# %% Set-up

#Navigate to folder with match data
os.chdir('..\\datasets\\vol6\\raw')

#Identify the file list to work through
fileList = []
#Get all match files
for file in glob.glob("*.json"):
    fileList.append(file)
    
#Sort list nicely
fileList = sortedNicely(fileList)
    
#Set up lists to store data
matchIdData = []
roundData = []
matchTypeData = []
yearData = []
compData = []
playerIdData = []
displayNameData = []
firstNameData = []
surnameData = []
minutesPlayedData = []
squadNameData = []

#Set up dictionary to refer to match type
matchTypeLookUp = {'H': 'Regular', 'F': 'Final'}

# %% Extract player data

#Loop through files
for file in fileList:
    
    #Load the .json data
    with open(file) as json_file:
        data = json.load(json_file)
        
    #Check if game was completed
    if data['matchInfo']['matchStatus'][0] == 'complete':
        
        #Loop through players in list
        for playerInd in range(len(data['playerInfo']['player'])):
            
            #Get current player Id
            playerId = data['playerInfo']['player'][playerInd]['playerId'][0]
            
            #Find index of current player Id in stats
            for playerStatsInd in range(len(data['playerStats']['player'])):
                if data['playerStats']['player'][playerStatsInd]['playerId'][0] == playerId:
                    break
            
            #Check if player recorded any minutes
            if data['playerStats']['player'][playerStatsInd]['startingPositionCode'][0] == '-':
                #Check if they recorded a substituion on
                #Get all subbed on player Id's
                if 'player' in data['playerSubs']: #initial check to see if subs made
                    subbedOn = []
                    #Check if single sub dictionary
                    if isinstance(data['playerSubs']['player'], dict):
                        subbedOn.append(data['playerSubs']['player']['playerId'][0])                        
                    else:                    
                        for nSubs in range(len(data['playerSubs']['player'])):
                            subbedOn.append(data['playerSubs']['player'][nSubs]['playerId'][0])
                    #Check if player Id is in list
                    if playerId in subbedOn:
                        playedMins = True
                    else:
                        playedMins = False
                else: #if no subs then obviously didn't play
                    playedMins = False
            else:
                #They started, so obviously played
                playedMins = True
                
            #Extract player info if they played minutes
            if playedMins:
                
                #Get the relevant player data
                displayName = data['playerInfo']['player'][playerInd]['displayName'][0]
                firstName = data['playerInfo']['player'][playerInd]['firstname'][0]
                surname = data['playerInfo']['player'][playerInd]['surname'][0]
                
                #Get players squad Id
                squadId = data['playerStats']['player'][playerStatsInd]['squadId'][0]
                for teamInd in range(len(data['teamInfo']['team'])):
                    if data['teamInfo']['team'][teamInd]['squadId'][0] == squadId:
                        squadName = data['teamInfo']['team'][teamInd]['squadNickname'][0]
                
                #Get match details
                matchId = data['matchInfo']['matchId'][0]
                matchType = matchTypeLookUp[data['matchInfo']['matchType'][0]]
                compType = file.split('_')[1]
                roundNo = int(data['matchInfo']['roundNumber'][0])
                year = int(data['matchInfo']['localStartTime'][0].split('-')[0])
                
                #Calculate the players minutes
                #Set lists to store values in
                startingPos = []
                startingTime = []
                finishPos = []
                finishTime = []
                #Identify positions and timings
                startingPos.append(data['playerStats']['player'][playerStatsInd]['startingPositionCode'][0])
                startingTime.append(0)
                #Loop through and identify any substitutions
                if 'player' in data['playerSubs']:
                    
                    #Check if only one sub, as this has a different structure
                    if isinstance(data['playerSubs']['player'], dict):
                        #Examine the one substitution
                        if data['playerSubs']['player']['playerId'][0] == playerId:
                            #Append info to finishing lists
                            finishPos.append(data['playerSubs']['player']['toPos'][0])
                            finishTime.append(data['playerSubs']['player']['periodSeconds'][0] + \
                                              ((data['playerSubs']['player']['period'][0]-1) * (15*60)))
                            #Append same above info to starting time for next step
                            startingPos.append(data['playerSubs']['player']['toPos'][0])
                            startingTime.append(data['playerSubs']['player']['periodSeconds'][0] + \
                                                ((data['playerSubs']['player']['period'][0]-1) * (15*60)))                        
                    else:
                        #Loop through subs
                        for subNo in range(len(data['playerSubs']['player'])):
                            if data['playerSubs']['player'][subNo]['playerId'][0] == playerId:
                                #Append info to finishing lists
                                finishPos.append(data['playerSubs']['player'][subNo]['toPos'][0])
                                finishTime.append(data['playerSubs']['player'][subNo]['periodSeconds'][0] + \
                                                  ((data['playerSubs']['player'][subNo]['period'][0]-1) * (15*60)))
                                #Append same above info to starting time for next step
                                startingPos.append(data['playerSubs']['player'][subNo]['toPos'][0])
                                startingTime.append(data['playerSubs']['player'][subNo]['periodSeconds'][0] + \
                                                    ((data['playerSubs']['player'][subNo]['period'][0]-1) * (15*60)))
                                
                    #Wrap up finishing pos and finishing time once looping through subs
                    if len(finishPos) == 0:
                        #Player played the whole game
                        finishPos.append(startingPos[0])
                        finishTime.append(np.sum([data['periodInfo']['qtr'][ii]['periodSeconds'][0] for ii in range(len(data['periodInfo']['qtr']))]))                    
                    else:
                        #Player had some substitutions
                        finishPos.append(finishPos[-1])
                        finishTime.append(np.sum([data['periodInfo']['qtr'][ii]['periodSeconds'][0] for ii in range(len(data['periodInfo']['qtr']))]))
                    
                else:
                    #No subs were made
                    #Add finishing pos
                    finishPos.append(startingPos[0])
                    finishTime.append(np.sum([data['periodInfo']['qtr'][ii]['periodSeconds'][0] for ii in range(len(data['periodInfo']['qtr']))]))
                    
                #Convert to dataframe
                minutesData = pd.DataFrame(list(zip(startingPos, startingTime,
                                                    finishPos, finishTime)),
                                           columns = ['startingPos', 'startingTime',
                                                      'finishPos', 'finishTime'])
                
                #Add a duration column
                minutesData['duration'] = minutesData['finishTime'] - minutesData['startingTime']
                
                #Calculate minutes in on-court positions
                minutesPlayed = np.round(np.sum(minutesData.loc[minutesData['startingPos'].isin(['GS','GA','WA','C','WD','GD','GK']),
                                                                ['duration']].to_numpy()) / 60)
                
                #Put check in place for the 61 minute games that seem to occur regularly
                if minutesPlayed == 61:
                    minutesPlayed = 60
                
                #Append to data lists
                matchIdData.append(matchId)
                roundData.append(roundNo)
                matchTypeData.append(matchType)
                yearData.append(year)
                compData.append(compType)
                playerIdData.append(playerId)
                displayNameData.append(displayName)
                firstNameData.append(firstName)
                surnameData.append(surname)
                minutesPlayedData.append(minutesPlayed)
                squadNameData.append(squadName)
        
#Convert to dataframe
playerData = pd.DataFrame(list(zip(matchIdData, roundData, matchTypeData, yearData, compData,
                                   playerIdData, displayNameData, firstNameData, surnameData,
                                   minutesPlayedData, squadNameData)),
                          columns = ['matchId', 'roundNo', 'matchType', 'year', 'competition',
                                     'playerId', 'displayName', 'firstName', 'surname',
                                     'minutesPlayed','squadName'])

#Sort values by round, year and player Id
playerData.sort_values(['year', 'roundNo', 'playerId'],
                       ascending = (True, True, True),
                       inplace = True)

#Replace double-ups on certain team names
playerData['squadName'].replace('WBOP Magic', 'Magic', inplace = True)
playerData['squadName'].replace('Mainland Tactix', 'Tactix', inplace = True)

# %% Export data

#Write to CSV
playerData.to_csv('..\\whoDoYouPlayFor.csv', index = False)
playerData.to_excel('..\\whoDoYouPlayFor.xlsx', index = False)

# %%% ----- End of whoDoYouPlayFor_compileDataset.py -----