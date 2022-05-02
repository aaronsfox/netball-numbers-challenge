# -*- coding: utf-8 -*-
"""

@author: 
    Aaron Fox
    Centre for Sport Research
    Deakin University
    aaron.f@deakin.edu.au
    
    Extracts shooting zone data from Champion Data match centre files.
    
    Notes for position and distance code combinations. This is for an inverted
    shooting circle to what is shown on the match centre with the baseline along 
    the bottom and circle projecting upwards:
    
"""

# %% Import packages

import pandas as pd
import os

# %% Set-up

#Set home directory
homeDir = os.getcwd()

#Get helper functions for loadings
os.chdir('..\\..\\netball-analysis\\code\\matchCentre')
import collatestats

#Get back to original directory
os.chdir(homeDir)

#Create dictionary to map squad names to ID's
squadDict = {804: 'Vixens',
             806: 'Swifts',
             807: 'Firebirds',
             8117: 'Lightning',
             810: 'Fever',
             8119: 'Magpies',
             801: 'Thunderbirds',
             8118: 'GIANTS'}

#Set base directory for processed data
baseDir = '..\\..\\netball-analysis\\data\\matchCentre\\processed'

# %% Extract scoring data

#Grab the scoreflow dataframes from SSN years with matched scoring data
scoreFlowData = collatestats.getSeasonStats(baseDir = baseDir,
                                            years = [2018, 2019, 2020, 2021, 2022],
                                            fileStem = 'scoreFlow',
                                            matchOptions = ['regular', 'final'])

#Grab player lists across same year for coding names
playerListData = collatestats.getSeasonStats(baseDir = baseDir,
                                             years = [2018, 2019, 2020, 2021, 2022],
                                             fileStem = 'playerList',
                                             matchOptions = ['regular', 'final'])

#Loop through years and add details
for year in list(scoreFlowData.keys()):
    
    #Add year column
    scoreFlowData[year]['year'] = [year]*len(scoreFlowData[year])
    
    #Collate player display names
    playerName = []
    for playerId in scoreFlowData[year]['playerId']:
        
        #Get current data points display name and append to list
        playerName.append(playerListData[year].loc[playerListData[year]['playerId'] == playerId,
                                                   ]['displayName'].unique()[0])
        
    #Append to dataframe
    scoreFlowData[year]['playerName'] = playerName

#Concatenate the yearly dataframes together
scoringData = pd.concat([scoreFlowData[year] for year in scoreFlowData.keys()])

#Replace the squad Id with names
scoringData['squadId'].replace(squadDict, inplace = True)

#Rename certain columns
scoringData.rename(columns = {'squadId': 'squadName', 'scorePoints': 'scoreValue'},
                   inplace = True)

#Reset indices
scoringData.reset_index(drop = True, inplace = True)

#Create the descriptors for shot location

#Create a new combined id variable
scoringData['shotLocation'] = [str(scoringData['positionCode'][ii])+str(scoringData['distanceCode'][ii]) for ii in range(len(scoringData))]

#Create dictionary to map shot location values against
shotLocationDict = {
    '00': 'left-short',
    '01': 'left-long',
    '03': 'left-baseline-long',
    '10': 'middle-short',
    '11': 'middle-long',
    '13': 'left-baseline-short',
    '20': 'right-short',
    '21': 'right-long',
    '23': 'right-baseline-long',
    '33': 'right-baseline-short',
    }

#Replace values in column
scoringData['shotLocation'].replace(shotLocationDict, inplace = True)

#Reset datafraframe to desired ordering and columns
scoringData = scoringData[['matchId', 'year', 'matchType',
                           'squadName', 'playerId', 'playerName',
                           'shotLocation',
                           'roundNo', 'gameNo',
                           'period', 'periodSeconds',
                           'scoreName', 'scoreValue',
                           ]]

#Add a generic success variable
shotResult = []
for scoreName in scoringData['scoreName']:
    if scoreName == 'goal' or scoreName == '2pt Goal':
        shotResult.append('successful')
    else:
        shotResult.append('unsuccessful')
scoringData['shotResult'] = shotResult

# %% Export data

#Write to CSV & Excel
scoringData.to_csv('..\\datasets\\vol7\\inTheZone.csv', index = False)
scoringData.to_excel('..\\datasets\\vol7\\inTheZone.xlsx', index = False)

# %%% ----- End of inTheZone_compileDataset.py -----