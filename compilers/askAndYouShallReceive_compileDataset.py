# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 20:37:24 2021

@author:
    Aaron Fox
    Centre for Sport Research
    Deakin University
    aaron.f@deakin.edu.au
    
    Script to compile centre pass receives and 2nd phase data
    from the 2018 SSN coding dataset.
    
"""

# %% Import packages

import os
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np

# %% Set-up

#Navigate to directory
os.chdir('C:\\Users\\aafox\\Syncplicity\\RDS26531-csv files')

#Identify regular season filelist
fileList = []
for fname in os.listdir():
   # Apply file type filter   
   if fname.startswith('Round'):
        #Append to list
        fileList.append(fname)
        
#Set team list for searching
teamList = ['Fever', 'Firebirds', 'Giants', 'Lightning',
            'Magpies', 'Swifts', 'Thunderbirds', 'Vixens']

#Set up dictionary to fill with data
fillDict = {'roundNo': [], 'matchNo': [],
            'quarterNo': [], 'teamName': [],
            'centrePassRec': [], 'centrePassX': [], 'centrePassY': [],
            'secondPhaseRec': [], 'secondPhaseX': [], 'secondPhaseY': []}
        
# %% Get data
        
#Loop through rounds
for rr in range(1,15):
    
    #Get files in current round
    roundFiles = []
    for fname in fileList:
        #Apply file type filter   
        if fname.startswith(f'Round {rr} '):
            #Append to list
            roundFiles.append(fname)
            
    #Loop through games
    for gg in range(len(roundFiles)):
        
        #Load the match data
        data = pd.read_csv(roundFiles[gg])
        
        #Identify the two team names
        #team0
        ii = 0
        keepSearch = True
        while keepSearch:
            if teamList[ii] in roundFiles[gg].split('vs')[0]:
                team0 = teamList[ii]
                keepSearch = False
            else:
                ii += 1
        #team1
        ii = 0
        keepSearch = True
        while keepSearch:
            if teamList[ii] in roundFiles[gg].split('vs')[1]:
                team1 = teamList[ii]
                keepSearch = False
            else:
                ii += 1
                
        #Loop through teams
        teamSet = [team0, team1]
        for tt in range(len(teamSet)):
            
            #Extract data for current team
            teamData = data.loc[data['Team'] == tt,]
            
            #Loop through quarters
            for qq in range(1,5):
                
                #Extract data for current quarter
                quarterData = teamData.loc[(teamData['Period'] == qq) &
                                           (teamData['Event'].isin(['Assist - Centre Pass Rec',
                                                                    'Assist - 2nd Phase'])),].reset_index(drop = True)
                
                #Check coordinate data are in integer format
                quarterData['YCoord'] = quarterData['YCoord'].astype(int)
                quarterData['XCoord'] = quarterData['XCoord'].astype(int)
                
                #Identify whether this quarter needs the XY coordinates inverted
                #If the shots being taken are down the south end (i.e. near 0),
                #then we convert them to the north end. Subsequently the X coordinates
                #of these also need to be flipped over the other side of 50 to be on the
                #appropriate side
                
                #Check whether to invert data
                if np.mean(teamData.loc[(teamData['Period'] == qq) &
                                        (teamData['Event'].isin(['Goal - Score','Goal - Miss'])),
                                        ['YCoord']]['YCoord']) < 33:
                    invert = True
                else:
                    invert = False
                    
                #Invert data if necessary
                if invert:
                    #Y-coordinates
                    quarterData['YCoord'] = 200 - quarterData['YCoord']
                    #X-coordinates
                    quarterData['XCoord'] = 100 - quarterData['XCoord']
                
                #Extract centre pass receptions
                cprData = quarterData.loc[quarterData['Event'] == 'Assist - Centre Pass Rec',]
                
                #Loop through centre passes and extract data
                for cc in list(cprData.index):
                    
                    #Set general data
                    fillDict['roundNo'].append(rr)
                    fillDict['matchNo'].append(gg+1 + ((rr-1)*4))
                    fillDict['teamName'].append(teamSet[tt])
                    fillDict['quarterNo'].append(qq)
                    
                    #Get centre pass data
                    fillDict['centrePassRec'].append(cprData['Role'][cc])
                    fillDict['centrePassX'].append(cprData['XCoord'][cc])
                    fillDict['centrePassY'].append(cprData['YCoord'][cc])
                    
                    #Check for subsequent 2nd phase event
                    if cc != cprData.index[-1]: #check for final entry
                        if quarterData['Event'][cc+1] == 'Assist - 2nd Phase':
                            #Extract data
                            fillDict['secondPhaseRec'].append(quarterData['Role'][cc+1])
                            fillDict['secondPhaseX'].append(quarterData['XCoord'][cc+1])
                            fillDict['secondPhaseY'].append(quarterData['YCoord'][cc+1])
                        else:
                            #Fill with nans
                            fillDict['secondPhaseRec'].append(np.nan)
                            fillDict['secondPhaseX'].append(np.nan)
                            fillDict['secondPhaseY'].append(np.nan)
                    else:
                        #Fill with nans
                        fillDict['secondPhaseRec'].append(np.nan)
                        fillDict['secondPhaseX'].append(np.nan)
                        fillDict['secondPhaseY'].append(np.nan)
                        
# %% Finish up
                        
#Convert dictionary to dataframe
finalData = pd.DataFrame.from_dict(fillDict)
            
#Export data
os.chdir('C:\\+GitRepos+\\netball-numbers-challenge\\datasets\\futureVols')
finalData.to_csv('askAndYouShallReceive.csv', index = False)

# %% ----- End of askAndYouShallReceive_compileDataset.py -----