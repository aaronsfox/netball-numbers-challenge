# -*- coding: utf-8 -*-
"""

@author: 
    Aaron Fox
    Centre for Sport Research
    Deakin University
    aaron.f@deakin.edu.au
    
    Cleans up compiled player and team stats for dataset.
    
"""

# %% Import packages

import pandas as pd
import os
from itertools import compress
import numpy as np

# %% Set-up

#Navigate to folder with match data
os.chdir('..\\datasets\\vol8\\raw\\compiled')

#Load in player data
playerData = pd.read_csv('compiledPlayerStats.csv')

# %% Clean up player data

#Do some checks of unique values for categorical descriptors
playerData['team'].unique()
playerData['opponent'].unique()
playerData['matchType'].unique()

#Replace nan's in court positions with an I for interchange
courtPositionCols = [col for col in playerData.columns if 'courtPosition' in col]
for col in courtPositionCols:
    playerData[col].fillna(value = 'I', inplace = True)

#Set columns to fill with zeros
zeroFillCols = ['minutesPlayed', 'goalsScored', 'goalsAttempted', 'shootingPer', 'goalAssists',
                'feeds',  'centrePassReceives', 'gains', 'intercepts', 'deflections',
                'attackingRebounds', 'defensiveRebounds', 'pickups', 'contactPenalties', 
                'obstructionPenalties', 'offsides','badHands', 'footwork', 'otherError']

#Fil columns with zeros
for col in zeroFillCols:
    playerData[col].fillna(value = 0, inplace = True)
    
#Calculate a more accurate shooting percentage
playerData['shootingPer'] = playerData['goalsScored'] / playerData['goalsAttempted'] * 100
playerData['shootingPer'].fillna(value = 0, inplace = True)

#Create some new variables
#Goals missed
playerData['goalsMissed'] = playerData['goalsAttempted'] - playerData['goalsScored']
#Total rebounds
playerData['totalRebounds'] = playerData['defensiveRebounds'] + playerData['attackingRebounds']
#Total penalties
playerData['totalPenalties'] = playerData['contactPenalties'] + playerData['obstructionPenalties']
#Total errors
playerData['totalErrors'] = playerData['offsides'] + playerData['badHands'] + \
    playerData['footwork'] + playerData['otherError']
    
#Create player surname and given name columns
surname = []
givenNames = []

#Loop through names
for name in playerData['name']:
    
    #Split name by space
    nameSplit = name.split(' ')
    
    #Identify capitalised names
    upperNames = [n.isupper() for n in nameSplit]
    
    #Get surname based on upper
    surname.append(' '.join(list(compress(nameSplit, upperNames))))
    
    #Get given names with what is left
    givenNames.append(' '.join(list(compress(nameSplit, [not ii for ii in upperNames]))))
    
#Append to dataframe
playerData['surname'] = surname
playerData['givenNames'] = givenNames
    
#Order columns appropriately
playerData = playerData[['matchNo', 'team', 'opponent', 'matchType', 'surname', 'givenNames',
                         'courtPosition_Q1', 'courtPosition_Q2', 'courtPosition_Q3', 'courtPosition_Q4', 'minutesPlayed',
                         'goalsScored', 'goalsAttempted', 'goalsMissed', 'shootingPer',
                         'goalAssists', 'feeds',  'centrePassReceives', 'gains', 'intercepts', 'deflections',
                         'attackingRebounds', 'defensiveRebounds', 'totalRebounds', 'pickups',
                         'contactPenalties',  'obstructionPenalties', 'totalPenalties',
                         'offsides','badHands', 'footwork', 'otherError', 'totalErrors']]    

# %% Clean up team data

#Load in the basic team data
basicTeamData = pd.read_csv('compiledBasicTeamStats.csv')

#Get the unique variable names
teamVars = list(basicTeamData['variable'].unique())

#Get the match numbers from the player data
allMatchNo = playerData['matchNo'].unique()

#Create a dictionary to store the compiled team data in
teamDataDict = {'matchNo': [], 'team': [], 'opponent': [], 'matchType': [], 'quarter': [],
                'Goals': [], 'Interceptions': [], 'Deflections': [],
                'Match Play Errors': [], 'Contact Penalties': [], 'Obstruction Penalties': [],
                'Time in Possession': []}

#Loop through match numbers and extract data
for matchNo in allMatchNo:
    
    #Get the teams in the match
    teams = tuple(playerData.loc[playerData['matchNo'] == matchNo,]['team'].unique())
    
    #Get match type
    matchType = list(playerData.loc[playerData['matchNo'] == matchNo,]['matchType'].unique())[0]
    
    #Append basic data to dictionary
    #Team 1
    for quarter in ['Q1', 'Q2', 'Q3', 'Q4']:
        teamDataDict['matchNo'].append(matchNo)
        teamDataDict['team'].append(teams[0])
        teamDataDict['opponent'].append(teams[1])
        teamDataDict['matchType'].append(matchType)
        teamDataDict['quarter'].append(quarter)
    #Team 2
    for quarter in ['Q1', 'Q2', 'Q3', 'Q4']:
        teamDataDict['matchNo'].append(matchNo)
        teamDataDict['team'].append(teams[1])
        teamDataDict['opponent'].append(teams[0])
        teamDataDict['matchType'].append(matchType)
        teamDataDict['quarter'].append(quarter)
    
    #Loop through team variables to extract
    for var in teamVars:
        
        #Extract the current variable from the team data
        currVarData = basicTeamData.loc[basicTeamData['variable'] == var, ].reset_index(drop = True)
        
        #Extract the relevant data based on index
        dataTeam1 = currVarData.iloc[(matchNo-1)*2]
        dataTeam2 = currVarData.iloc[(matchNo-1)*2+1]
        
        #Append data to dictionary
        #Team 1
        for quarter in ['Q1', 'Q2', 'Q3', 'Q4']:
            teamDataDict[var].append(dataTeam1[quarter])
        #Team 2
        for quarter in ['Q1', 'Q2', 'Q3', 'Q4']:
            teamDataDict[var].append(dataTeam2[quarter])
        
#Convert to dataframe
teamData = pd.DataFrame.from_dict(teamDataDict)

#Convert time in possession to seconds
teamData['timeInPossessionSecs'] = [(int(timeInPos.split(':')[0])*60)+int(timeInPos.split(':')[1]) for timeInPos in teamData['Time in Possession']]

#Drop the original time in possession column
teamData.drop(['Time in Possession'], axis = 1, inplace = True)

#Rename columns
teamData.rename(columns = {'Goals': 'goalsScored',
                           'Interceptions': 'intercepts',
                           'Deflections': 'deflections',
                           'Match Play Errors': 'totalErrors',
                           'Contact Penalties': 'contactPenalties',
                           'Obstruction Penalties': 'obstructionPenalties'},
                inplace = True)

#Set columns to fill with zeros
zeroFillCols = ['goalsScored', 'intercepts', 'deflections', 'totalErrors',
                'contactPenalties', 'obstructionPenalties',  'timeInPossessionSecs']

#Fil columns with zeros & also change data to numeric type
for col in zeroFillCols:
    teamData[col].fillna(value = 0, inplace = True)
    teamData[col] = pd.to_numeric(teamData[col])

#Create new variables
#Total penalties
teamData['totalPenalties'] = teamData['contactPenalties'] + teamData['obstructionPenalties']
#Goal differential
goalDifferential = []
for ind in teamData.index:
    #Find goals scored for current index
    goalsFor = teamData.iloc[ind]['goalsScored']
    #Find team, opponent, match type and quarter to id goals against
    currTeam = teamData.iloc[ind]['team']
    currOpp = teamData.iloc[ind]['opponent']
    currType = teamData.iloc[ind]['matchType']
    currQuarter = teamData.iloc[ind]['quarter']
    #Find goals against using conditionals
    goalsAgainst = teamData.loc[(teamData['team'] == currOpp) &
                                (teamData['opponent'] == currTeam) &
                                (teamData['matchType'] == currType) &
                                (teamData['quarter'] == currQuarter),
                                ]['goalsScored'].values[0]
    #Calculate and append differential
    goalDifferential.append(goalsFor - goalsAgainst)
#Append to dataframe
teamData['goalDifferential'] = goalDifferential

#Order columns appropriately
teamData = teamData[['matchNo', 'team', 'opponent', 'matchType', 'quarter', 
                     'goalsScored', 'goalDifferential', 'intercepts', 'deflections',
                     'contactPenalties', 'obstructionPenalties', 'totalPenalties',
                     'totalErrors', 'timeInPossessionSecs']]          

# %% Create a cumulative team stats dataset

#Set dictionary to store values in
teamDataCumulativeDict = {'team': [], 'quartersPlayed': [],
                          'goalsScored': [], 'goalDifferential': [],
                          'intercepts': [], 'deflections': [],
                          'contactPenalties': [], 'obstructionPenalties': [],
                          'totalPenalties': [], 'totalErrors': [], 
                          'timeInPossessionSecs': []}

#Set variables to collect
cumulativeVars = ['goalsScored', 'goalDifferential', 'intercepts', 'deflections',
                  'contactPenalties', 'obstructionPenalties', 'totalPenalties',
                  'totalErrors', 'timeInPossessionSecs']

#Loop through teams
for team in list(teamData['team'].unique()):
    
    #Get the current teams data
    currTeamData = teamData.loc[teamData['team'] == team, ].sort_values(by = 'matchNo')
    
    #Append team and quarters played data to dictionary
    
    #Set zero values for stats to collect
    [teamDataCumulativeDict['team'].append(team) for nQuarters in range(len(currTeamData))]
    [teamDataCumulativeDict['quartersPlayed'].append(qPlayed+1) for qPlayed in range(len(currTeamData))]
    
    #Loop through stat variables
    for var in cumulativeVars:
        [teamDataCumulativeDict[var].append(val) for val in list(np.cumsum(currTeamData[var]))]

#Convert to dataframe
teamDataCumulative = pd.DataFrame.from_dict(teamDataCumulativeDict)

# %% Export data

#Write to CSV
playerData.to_csv('..\\..\\theGames_playerData.csv', index = False)
teamData.to_csv('..\\..\\theGames_teamData.csv', index = False)
teamDataCumulative.to_csv('..\\..\\theGames_teamDataCumulative.csv', index = False)

# %%% ----- End of theGames_compileDataset.py -----