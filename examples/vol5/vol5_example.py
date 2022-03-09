# -*- coding: utf-8 -*-
"""

@author: 
    Aaron Fox
    Centre for Sport Research
    Deakin University
    aaron.f@deakin.edu.au
    
    This script dives into the 12 Super Netballers of Christmas dataset to pick
    my group and generates iterative visuals to progressively reveal the selected
    players.
    
    NOTE: earlier years total minutes potentially off --- impacts per 15 measures...
    
"""

# %% Import packages

import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.patches import Ellipse
from matplotlib.transforms import Bbox, TransformedBbox
import numpy as np

# %% Set-up

#Set matplotlib parameters
from matplotlib import rcParams
# rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = 'Arial'
rcParams['font.weight'] = 'bold'
rcParams['axes.labelsize'] = 12
rcParams['axes.titlesize'] = 16
rcParams['axes.linewidth'] = 1.5
rcParams['axes.labelweight'] = 'bold'
rcParams['legend.fontsize'] = 10
rcParams['xtick.major.width'] = 1.5
rcParams['ytick.major.width'] = 1.5
rcParams['legend.framealpha'] = 0.0
rcParams['savefig.dpi'] = 300
rcParams['savefig.format'] = 'pdf'

#Colour settings for teams
colourDict = {'Fever': '#00953b',
              'Firebirds': '#4b2c69',
              'GIANTS': '#f57921',
              'Lightning': '#fdb61c',
              'Magpies': '#494b4a',
              'Swifts': '#0082cd',
              'Thunderbirds': '#e54078',
              'Vixens': '#00a68e'}

#Set red/green christmas colours to alternate through
xmasColRed = '#a11313'
xmasColGreen = '#165b33'

#Import the dataset
playerData = pd.read_csv('..\\..\\datasets\\vol5\\superNetballersOfChristmas.csv')

# %% Define functions

#Create figure base
def figureBase(titleLabels):
    
    #Set red/green christmas colours to alternate through
    #Set to start on red
    xmasColRed = '#a11313'
    xmasColGreen = '#165b33' 
    setXmasCol = xmasColRed

    #Set labels for xmas icons
    xmasIcons = ['bell', 'holly', 'stocking', 'tree', 'wreath']
    xmasIcons = xmasIcons + xmasIcons + xmasIcons + xmasIcons #extras for iterartions
    iconCounter = 0 #counter to progress through list

    #Create the figure
    fig, ax = plt.subplots(figsize = (15,6), nrows = 2, ncols = 7)

    #Adjust axes window
    plt.subplots_adjust(left = 0.05, right = 0.95, top = 0.85, bottom = 0.05)

    #Set axis counter to monitor when to plot circles
    axisCounter = 0

    #Loop through axes and add visuals
    for axes in ax.flatten():
        
        #Set axes aspect and limits
        axes.set_aspect(1)
        axes.set_xlim([0,1])
        axes.set_ylim([0,1])
        
        #Check if we want to plot on this axis
        if axisCounter != 7 and axisCounter != 13:

            #Add ellipse to axis
            #Add no edge filled ellipse to sit under player
            axes.add_artist(Ellipse((0.5,0.5),
                                    1.0, 1.0,
                                    ec = None, lw = 0,
                                    fc = '#fffaf0',
                                    transform = axes.transAxes,
                                    zorder = 3,
                                    clip_on = False))
            #Add no fill edge to sit above player
            axes.add_artist(Ellipse((0.5,0.5),
                                    1.0,1.0,
                                    ec = setXmasCol, lw = 2,
                                    fc = 'none',
                                    transform = axes.transAxes,
                                    zorder = 6,
                                    clip_on = False))
            
            #Add appropriate christmas image
            if setXmasCol == xmasColRed:
                #Use a green image
                #Load image, using counter
                xmasImg = plt.imread(f'images\\{xmasIcons[iconCounter]}_green.png')
                #Figure out zoom factor
                #Target height took a bit of experimentation
                zoomFac =  0.4
                #Create offset image
                imOffset = OffsetImage(xmasImg, zoom = zoomFac)
                #Create annotation box
                annBox = AnnotationBbox(imOffset, (0.5,0.55),
                                        #xybox = (0, 0),
                                        frameon = False,
                                        box_alignment = (0.5,0.5),
                                        xycoords = axes.transAxes,
                                        #boxcoords = 'offset points',
                                        pad = 0)
                annBox.zorder = 4
                #Add the image
                axes.add_artist(annBox)
            elif setXmasCol == xmasColGreen:
                #Use a red image
                #Load image, using counter
                xmasImg = plt.imread(f'images\\{xmasIcons[iconCounter]}_red.png')
                #Figure out zoom factor
                #Target height took a bit of experimentation
                zoomFac =  0.4
                #Create offset image
                imOffset = OffsetImage(xmasImg, zoom = zoomFac)
                #Create annotation box
                annBox = AnnotationBbox(imOffset, (0.5,0.55),
                                        #xybox = (0, 0),
                                        frameon = False,
                                        box_alignment = (0.5,0.5),
                                        xycoords = axes.transAxes,
                                        #boxcoords = 'offset points',
                                        pad = 0)
                annBox.zorder = 4
                #Add the image
                axes.add_artist(annBox)
            
            #Add to icon counter
            iconCounter += 1
            
            #Add axis title
            axes.text(0.5, 1.1, titleLabels[axisCounter], color = setXmasCol,
                      ha = 'center', va = 'center',
                      fontsize = 14, fontweight = 'bold', clip_on = False)
            
        #Turn axis off
        axes.axis('off')
        
        #Reset xmas colouring
        if setXmasCol == xmasColRed:
            setXmasCol = xmasColGreen
        else:
            setXmasCol = xmasColRed
            
        #Add to axis counter
        axisCounter += 1

    #Add figure title using text
    fig.text(0.05, 0.98, 'The 12 Super Netballers of Christmas',
             fontsize = 14, fontweight = 'bold', ha = 'left', va = 'top')
    fig.text(0.05, 0.94, 'Based on data from regular season Super Netball matches from 2017 - 2021',
             fontsize = 8, fontweight = 'normal', ha = 'left', va = 'top')
    fig.text(0.05, 0.92, 'Statistical rankings are ''in-season'' (i.e. compared to players from the same year)',
             fontsize = 8, fontweight = 'normal', ha = 'left', va = 'top')
    fig.text(0.05, 0.90, 'Positional rankings are made against those who started in the same position for at least 7 matches',
             fontsize = 8, fontweight = 'normal', ha = 'left', va = 'top')

    #Set figure colouring
    fig.patch.set_facecolor('#fffaf0')
    
    return fig, ax

# %% General data

#Create a total stats dataframe
totalStats = playerData.groupby(['year','playerName', 'playerId']).sum().reset_index(drop = False)

#Drop round and squad ID from total stats
totalStats.drop(['round', 'squadId'], axis = 1, inplace = True)

#Create per 15 minute data in total stats dataframe

#Get the variables to extract
calcPer15Vars = list(totalStats.columns)
calcPer15Vars.remove('year')
calcPer15Vars.remove('playerName')
calcPer15Vars.remove('playerId')
calcPer15Vars.remove('minutesPlayed')

#Loop through and calculate per 15 values & team proportions
for dataVar in calcPer15Vars:
    
    #Create new variable name
    newVarName1 = dataVar+'_per15'
    newVarName2 = dataVar+'_teamProp'
    
    #Calculate based on total minutes
    #Append to dataframe
    totalStats[newVarName1] = (totalStats[dataVar] / totalStats['minutesPlayed']) * 15
    
    #Loop through dataframe of players and calculate team proportion
    tempStatList = []
    for playerNo in range(len(totalStats)):
        #Get the squad ID for the player and year
        currSquadId = playerData.loc[(playerData['playerId'] == totalStats['playerId'][playerNo]) &
                                     (playerData['year'] == totalStats['year'][playerNo]),
                                     ['squadId']]['squadId'].unique()[0]
        #Calculate the team total for the current stat & year
        totalStatNo = playerData.loc[(playerData['year'] == totalStats['year'][playerNo]) &
                                     (playerData['squadId'] == currSquadId),
                                     [dataVar]][dataVar].sum()
        #Calculate the current players proportion and append to list
        tempStatList.append(totalStats[dataVar][playerNo] / totalStatNo)
    
    #Add the new column to the total stats dataframe
    totalStats[newVarName2] = tempStatList

#Create lists of players who started at certain positions for at least 7 games
#within a year as the 'main' players to review
yearList = list(playerData['year'].unique())

#Set positions
posList = ['GS', 'GA', 'WA', 'C', 'WD', 'GD', 'GK']

#Create dictionary to store data in
starterDict = {'year': [], 'pos': [], 'playerId': [], 'playerName': []}

#Loop through years
for year in yearList:
    
    #Loop through positions
    for pos in posList:
        
        #Get years and position worth of data
        yearPosData = playerData.loc[(playerData['year'] == year) &
                                     (playerData['startingPositionCode'] == pos),
                                     ['playerId', 'playerName', 'startingPositionCode']].reset_index(drop = True)
        
        #Get sum of WA starting counts for current year
        startCounts = yearPosData.groupby(['playerId', 'playerName']).count().reset_index()
    
        #Get the list of players with greater than 7 starts
        playerList = startCounts.loc[startCounts['startingPositionCode'] >= 7,
                                     ['playerId', 'playerName']].reset_index(drop = True)
        
        #Loop through list and append data
        for playerNo in range(len(playerList)):
            starterDict['year'].append(year)
            starterDict['pos'].append(pos)
            starterDict['playerId'].append(playerList['playerId'][playerNo])
            starterDict['playerName'].append(playerList['playerName'][playerNo])

#Convert to dataframe
startersData = pd.DataFrame.from_dict(starterDict)

# %% Create the initial 'Christmas' framework to reveal players

#Set title labels for this iteration
titleLabels = ['GS', 'GA', 'WA', 'C', 'WD', 'GD', 'GK',
               '', 'Bench', 'Bench', 'Bench', 'Bench', 'Bench', ''] #extras for axes structure

#Use function to create base figure
fig, ax = figureBase(titleLabels)

#Export blank starting figure
plt.savefig('outputs\\vol5_example_0.png', format = 'png', 
            facecolor = fig.get_facecolor(), edgecolor = 'none',
            dpi = 300)

#Close figure
plt.close()

# %% Goal Shooter

#Obviously Fowler is the go to here, we just need to pick the year that Fowler
#played 'better' than other years.
#
#Base our GS selection on:
    #Ranking for goals in year
    #Accounting for % of team score
    #Shooting percentage
    
#Set dictionary to store data in
fowlerDict = {'year': [], 'goalsScored': [], 'goalRank': [], 'teamProp': [], 'shootingPer': [], 'goalDiff': []}
    
#Find Fowler's player ID to just confirm there aren't any issues
fowlerId = list(playerData.loc[playerData['playerName'] == 'J.Fowler',
                               ['playerId']]['playerId'].unique())
if len(fowlerId) > 1:
    raise ValueError('Multiple J.Fowler ID found')
else:
    fowlerId = fowlerId[0]
    
#Extract the years that Fowler has played
fowlerYears = list(playerData.loc[playerData['playerId'] == fowlerId,
                                  ['year']]['year'].unique())

#Loop through years and calculate the aforementioned statistics
for year in fowlerYears:
    
    #Extract current year
    yearData = playerData.loc[playerData['year'] == year, ].reset_index(drop= True)
    
    #Create a count of the goals grouped by players to get a ranking
    #Use the sort and reset_index functions in here to get a sorted output
    yearlyGoals = yearData.groupby('playerName').sum()['goals'].reset_index().sort_values(
        'goals', ascending = False).reset_index(drop = True)
    
    #Calculate Fowlers rank for the year
    #Add 1 to get appropriate ranking
    yearGoalRank = yearlyGoals.index[yearlyGoals['playerName'] == 'J.Fowler'].tolist()[0] + 1
    
    #Extract how far from number two or the top Fowler was
    if yearGoalRank == 1:
        goalDiff = yearlyGoals['goals'][0] - yearlyGoals['goals'][1]
    else:
        goalDiff = yearlyGoals['goals'][yearGoalRank-1] - yearlyGoals['goals'][0]
    
    #Get number of goals
    goalsScored = yearlyGoals['goals'][yearGoalRank-1]
    
    #Calculate % team score accounted for
    
    #Get the squad id for Fowler that year
    squadId = list(yearData.loc[yearData['playerName'] == 'J.Fowler',
                                ['squadId']]['squadId'].unique())[0]
    
    #Extract the total goals scored across the year by the team
    teamGoals = yearData.loc[yearData['squadId'] == squadId, ['playerId','goals']].reset_index(drop = True)
    totalTeamGoals = teamGoals['goals'].sum()
    
    #Get Fowlers goals from the year
    fowlerGoals = teamGoals.loc[teamGoals['playerId'] == fowlerId, ]['goals'].sum()
    
    #Calculate the proportion of total team goals
    teamGoalProp = (fowlerGoals / totalTeamGoals) * 100
    
    #Extract shooting percentage for the year
    
    #Extract the makes and misses by Fowler across the year
    attempts = yearData.loc[yearData['playerId'] == fowlerId, ['goalAttempts']]['goalAttempts'].sum()
    misses = yearData.loc[yearData['playerId'] == fowlerId, ['goalMisses']]['goalMisses'].sum()
    
    #Calculate shooting percentage
    yearShootingPer = ((attempts - misses) / attempts) * 100
    
    #Append to dictionary to examine
    fowlerDict['year'].append(year)
    fowlerDict['goalsScored'].append(goalsScored)
    fowlerDict['goalRank'].append(yearGoalRank)
    fowlerDict['teamProp'].append(teamGoalProp)
    fowlerDict['shootingPer'].append(yearShootingPer)
    fowlerDict['goalDiff'].append(goalDiff)
    
#Fowler was number 1 for goals each year - so no distinction there
#There's only a slight bit of variation with respect to proportion of team goals
#and shooting percentage across years. 2020 had the highest contribution to team
#scoring proportion and also has the greatest difference for goals relative to
#the rest of the competition.
#
#End result: 2020 Fowler - GS position

#Set title labels for this iteration
titleLabels = ['J.Fowler (2020)', 'GA', 'WA', 'C', 'WD', 'GD', 'GK',
               '', 'Bench', 'Bench', 'Bench', 'Bench', 'Bench', ''] #extras for axes structure

#Use function to create base figure
fig, ax = figureBase(titleLabels)

#Set axes to use
axes = ax.flatten()[0]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Fowler image
#Image placement took a bit of experimentation - still some stray pixels outside
#Use a green image
#Load image, using counter
playerImg = plt.imread('images\\J.Fowler_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.51
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.506,0.545),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0)
annBox.zorder = 5
#Add image
axes.add_artist(annBox)

#Add annotations below image
#+212 more goals than the second ranked scorer for the year
axes.text(0.5, -0.1, '#1 Goals Scored (795 goals)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
#Second highest seasons shooting percentage over super netball career
#96.55% in 2021 season
axes.text(0.5, -0.2, '93.64% Shooting Percentage', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
#Highest proportion of teams scoring across Super Netball career
axes.text(0.5, -0.3, '87.36% of Teams Scoring', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Save as next figure reveal
plt.savefig('outputs\\vol5_example_1.png', format = 'png', 
            facecolor = fig.get_facecolor(), edgecolor = 'none',
            dpi = 300)

#Close
plt.close()

#Create some figures to support Fowler statistics to demonstrate gap in 2020
year = 2020
yearData = playerData.loc[playerData['year'] == year, ].reset_index(drop= True)

#Create a figure plotting goals scored against the rest of the top 10

#Get the sum of players goals
yearlyGoals = yearData.groupby(['playerName','squadName']).sum()['goals'].reset_index().sort_values(
    'goals', ascending = False).reset_index(drop = True)

#Create figure for top 10 goal scorers for the year
figTopGoals, axTopGoals = plt.subplots(figsize = (7,5))

#Adjust subplot
plt.subplots_adjust(bottom = 0.2)

#Plot the bars for the top 10
axTopGoals.bar(np.linspace(1,10,10), yearlyGoals['goals'][0:10].to_numpy(),
               width = 0.15, zorder = 2)

#Loop through bars, change colour, add lollipop point
barWidth = 0.15
for barNo in range(len(axTopGoals.patches)):   
    #Set colour of patch to match team colour
    newCol = colourDict[yearlyGoals['squadName'][barNo]]
    axTopGoals.patches[barNo].set_fc(newCol)    
    #Add lollipop point
    #Get the x,y coordinate to plot
    xPt,yPt = axTopGoals.patches[barNo].get_x(),axTopGoals.patches[barNo].get_height()
    #Plot the point
    axTopGoals.scatter(xPt + (barWidth/2), yPt,
                       color = newCol, s = 300, zorder = 4)
    #Add goal number
    axTopGoals.text(xPt + (barWidth/2), yPt,
                    str(yearlyGoals['goals'][barNo]),
                    color = 'white',
                    ha = 'center', va = 'center',
                    zorder = 5,
                    fontsize = 8, fontweight = 'bold', clip_on = False)
    
#Add y-label
axTopGoals.set_ylabel('Total Goals Scored', labelpad = 10)

#Set x-ticks
axTopGoals.set_xticks(np.linspace(1,10,10))
axTopGoals.set_xticklabels(list(yearlyGoals['playerName'][0:10]),
                           rotation = 45, ha = 'right')

#Set and get rid of y-ticks
axTopGoals.tick_params(axis = 'y', length = 0)
axTopGoals.set_yticks(np.linspace(0,800,9))

#Add horizontal lines
for lineLevel in axTopGoals.get_yticks():
    axTopGoals.axhline(y = lineLevel, c = 'lightgrey',
               lw = 0.5, ls = '--', zorder = 1)
    
#Turn off axes lines we don't want
axTopGoals.spines['top'].set_visible(False)
axTopGoals.spines['left'].set_visible(False)
axTopGoals.spines['right'].set_visible(False)

#Add figure title using text
figTopGoals.text(0.05, 0.98, 'Top 10 Goal Scorers from Super Netball 2020',
         fontsize = 14, fontweight = 'bold', ha = 'left', va = 'top')

#Set figure colouring
figTopGoals.patch.set_facecolor('#fffaf0')
axTopGoals.set_facecolor('#fffaf0')

#Save figure
plt.savefig('outputs\\vol5_example_GS_0.png', format = 'png', 
            facecolor = fig.get_facecolor(), edgecolor = 'none',
            dpi = 300)

#Close figure
plt.close()

#Create a figure plotting team score proportion against the rest of the top 10

#Create figure for top 10 goal scorers for the year
figGoalProp, axGoalProp = plt.subplots(figsize = (7,5))

#Adjust subplot
plt.subplots_adjust(bottom = 0.2)

#Calculate the proportion of each player in the top 10 goals scored
playerProps = [] #place to store proportions
for shooter in list(yearlyGoals['playerName'][0:10]):
    #Get the players team name
    squadName = yearlyGoals.loc[yearlyGoals['playerName'] == shooter,
                                ['squadName']]['squadName'].to_numpy()[0]
    #Get the total goals scored by that team during the current year
    totalGoals = playerData.loc[(playerData['year'] == year) &
                                (playerData['squadName'] == squadName),
                                ['goals']].sum()['goals']
    #Get player goals
    playerGoals = yearlyGoals.loc[yearlyGoals['playerName'] == shooter,
                                  ['goals']]['goals'].to_numpy()[0]
    #Calculate proportion and append to list
    playerProps.append(playerGoals/totalGoals*100)

#Plot the bars for the top 10
axGoalProp.bar(np.linspace(1,10,10), playerProps,
               width = 0.15, zorder = 2)

#Loop through bars, change colour, add lollipop point
barWidth = 0.15
for barNo in range(len(axGoalProp.patches)):   
    #Set colour of patch to match team colour
    newCol = colourDict[yearlyGoals['squadName'][barNo]]
    axGoalProp.patches[barNo].set_fc(newCol)    
    #Add lollipop point
    #Get the x,y coordinate to plot
    xPt,yPt = axGoalProp.patches[barNo].get_x(),axGoalProp.patches[barNo].get_height()
    #Plot the point
    axGoalProp.scatter(xPt + (barWidth/2), yPt,
                       color = newCol, s = 300, zorder = 4)
    #Add goal number
    axGoalProp.text(xPt + (barWidth/2), yPt,
                    str(int(np.round(playerProps[barNo],0)))+'%',
                    color = 'white',
                    ha = 'center', va = 'center',
                    zorder = 5,
                    fontsize = 8, fontweight = 'bold', clip_on = False)
    
#Add y-label
axGoalProp.set_ylabel('Proportion of Team Total Goals', labelpad = 10)

#Set x-ticks
axGoalProp.set_xticks(np.linspace(1,10,10))
axGoalProp.set_xticklabels(list(yearlyGoals['playerName'][0:10]),
                           rotation = 45, ha = 'right')

#Set and get rid of y-ticks
axGoalProp.tick_params(axis = 'y', length = 0)
axGoalProp.set_yticks(np.linspace(0,100,11))

#Turn off axes lines we don't want
axGoalProp.spines['top'].set_visible(False)
axGoalProp.spines['left'].set_visible(False)
axGoalProp.spines['right'].set_visible(False)

#Add horizontal lines
for lineLevel in axGoalProp.get_yticks():
    axGoalProp.axhline(y = lineLevel, c = 'lightgrey',
               lw = 0.5, ls = '--', zorder = 1)
    
#Add figure title using text
figGoalProp.text(0.05, 0.98, 'Top 10 Goal Scorers from Super Netball 2020',
         fontsize = 14, fontweight = 'bold', ha = 'left', va = 'top')
figGoalProp.text(0.05, 0.94, 'Data indicates the proportion of teams total goals accounted for by player',
         fontsize = 8, fontweight = 'normal', ha = 'left', va = 'top')

#Set figure colouring
figGoalProp.patch.set_facecolor('#fffaf0')
axGoalProp.set_facecolor('#fffaf0')

#Save figure
plt.savefig('outputs\\vol5_example_GS_1.png', format = 'png', 
            facecolor = fig.get_facecolor(), edgecolor = 'none',
            dpi = 300)

#Close figure
plt.close()

# %% Wing Attack

#Base our WA selection on:
    #CPR rankings and team % accounted for (per 15 too)
    #Feeds rankings and team % accounted for (per 15 too)
    #Turnover rankings per 15

#Here we'll cast a bit of a wider net and view the statistics of players who
#started at least 7 games at WA within a year (i.e. 50% of matches)

#Set the years to search through
yearList = list(playerData['year'].unique())

#Set data dictionary to store data in
waDataDict = {'playerId': [], 'playerName': [], 'squadName': [], 'year': [],
              'totalCPR': [], 'teamPropCPR': [], 'per15CPR': [], 
              'totalFeeds': [], 'teamPropFeeds': [], 'per15Feeds': [], 
              'totalTurnovers': [], 'per15Turnovers': []}

#Loop through years
for year in yearList:
    
    #Get years worth of data
    yearPosData = playerData.loc[(playerData['year'] == year) &
                                 (playerData['startingPositionCode'] == 'WA'),
                                 ['playerId', 'startingPositionCode']].reset_index(drop = True)
    
    #Get sum of WA starting counts for current year
    startCounts = yearPosData.groupby(['playerId']).count().reset_index()
    
    #Get the list of players with greater than 10 starts at WA
    playerList = list(startCounts.loc[startCounts['startingPositionCode'] >= 7,]['playerId'])
    
    #Loop through players and calculate statistics
    for player in playerList:
        
        #Extract players data from the year
        waPlayerData = playerData.loc[(playerData['year'] == year) &
                                      (playerData['playerId'] == player),].reset_index(drop = True)
        
        #Calculate statistics
        
        #Centre pass receives
        #Total centre pass receives
        totalCPR = waPlayerData['centrePassReceives'].sum()
        #Team proportion centre pass receives
        teamTotalCPR = playerData.loc[(playerData['year'] == year) &
                                      (playerData['squadId'] == waPlayerData['squadId'].unique()[0]),
                                      ['centrePassReceives']].sum()['centrePassReceives']
        teamPropCPR = totalCPR / teamTotalCPR * 100
        #Per 15 centre pass receives
        totalMinsPlayed = waPlayerData['minutesPlayed'].sum()
        per15CPR = totalCPR / (totalMinsPlayed / 15)
        
        #Feeds
        #Total feeds
        totalFeeds = waPlayerData['feeds'].sum()
        #Team proportion feeds
        teamTotalFeeds = playerData.loc[(playerData['year'] == year) &
                                      (playerData['squadId'] == waPlayerData['squadId'].unique()[0]),
                                      ['feeds']].sum()['feeds']
        teamPropFeeds = totalFeeds / teamTotalFeeds * 100
        #Per 15 feeds
        per15Feeds = totalFeeds / (totalMinsPlayed / 15)
        
        #Turnovers
        #Total turnovers
        if year == 2017:
            totalTurnovers = waPlayerData['turnovers'].sum()
        else:
            totalTurnovers = waPlayerData['generalPlayTurnovers'].sum()        
        #Per 15 turnovers
        per15Turnovers = totalTurnovers / (totalMinsPlayed / 15)
        
        #Append data to dictionary
        waDataDict['playerId'].append(player)
        waDataDict['playerName'].append(waPlayerData['playerName'].unique()[0])
        waDataDict['squadName'].append(waPlayerData['squadName'].unique()[0])
        waDataDict['year'].append(year)
        waDataDict['totalCPR'].append(totalCPR)
        waDataDict['teamPropCPR'].append(teamPropCPR)
        waDataDict['per15CPR'].append(per15CPR)
        waDataDict['totalFeeds'].append(totalFeeds)
        waDataDict['teamPropFeeds'].append(teamPropFeeds)
        waDataDict['per15Feeds'].append(per15Feeds)
        waDataDict['totalTurnovers'].append(totalTurnovers)
        waDataDict['per15Turnovers'].append(per15Turnovers)
        
#Convert to dataframe
waData = pd.DataFrame.from_dict(waDataDict)

#Create new ranking variables for each of the calculated statistics so it's
#easier to view a summary across years and players

#Set variables to inspect
waVars = ['totalCPR', 'teamPropCPR', 'per15CPR', 'totalFeeds', 'teamPropFeeds',
          'per15Feeds', 'totalTurnovers', 'per15Turnovers']

#Loop through variables
for var in waVars:
    
    #Sort the dataframe by the current variable
    if 'Turnovers' in var:
        waDataSorted = waData.sort_values(var)
    else:
        waDataSorted = waData.sort_values(var, ascending = False)
        
    #Create an order rankings variable based on numer of players
    rankList = np.linspace(1, len(waData), len(waData), dtype = int)
    
    #Create an ordered rank list to slot back into original dataframe based on index
    orderedRanks = [x for _, x in sorted(zip(list(waDataSorted.index),rankList))]
    
    #Create new variable name for adding back to dataframe
    rankVarName = var+'_rank'
    
    #Add back in to original dataframe
    waData[rankVarName] = orderedRanks
    
#Create an average ranked variable for each player
avgRank = []
for playerNo in range(len(waData['playerName'])):
    #Set list to put ranks in
    ranks = []
    #Get the rank variables
    for var in waVars:
        #Variable name
        rankVarName = var+'_rank'
        #Get the data point and append to list
        ranks.append(waData[rankVarName][playerNo])
    #Average ranks and append to list
    avgRank.append(np.mean(ranks))
#Append to dataframe
waData['avgRank'] = avgRank

#Liz Watson is perhaps the most consistent high performing player in WA, and has
#consistently been the starting WA in the team of the year - much like with Fowler
#the difficulty is perhaps picking the year to take

#Grab Watson's data over the years
waWatsonData = waData.loc[waData['playerName'] == 'L.Watson',].reset_index(drop = True)

#2019 Liz Watson is probably the one to go with. Career hight for total CPR and
#team proportion of CPRs. No. 1 ranked WA for 2019 in both total CPR and total
#feeds

#Set title labels for this iteration
titleLabels = ['J.Fowler (2020)', 'GA', 'L.Watson (2019)', 'C', 'WD', 'GD', 'GK',
               '', 'Bench', 'Bench', 'Bench', 'Bench', 'Bench', ''] #extras for axes structure

#Use function to create base figure
fig, ax = figureBase(titleLabels)

#Re-add Fowler details

#Set axes to use
axes = ax.flatten()[0]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Fowler image
#Image placement took a bit of experimentation - still some stray pixels outside
#Use a green image
#Load image, using counter
playerImg = plt.imread('images\\J.Fowler_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.51
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.506,0.545),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0)
annBox.zorder = 5
#Add image
axes.add_artist(annBox)

#Add annotations below image
#+212 more goals than the second ranked scorer for the year
axes.text(0.5, -0.1, '#1 Goals Scored (795 goals)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
#Second highest seasons shooting percentage over super netball career
#96.55% in 2021 season
axes.text(0.5, -0.2, '93.64% Shooting Percentage', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
#Highest proportion of teams scoring across Super Netball career
axes.text(0.5, -0.3, '87.36% of Teams Scoring', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Add Watson details

#Set axes to use
axes = ax.flatten()[2]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Watson image
#Image placement took a bit of experimentation - still some stray pixels outside
#Use a green image
#Load image, using counter
playerImg = plt.imread('images\\L.Watson_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.51
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.506,0.545),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0)
annBox.zorder = 5
#Add image
axes.add_artist(annBox)

#Add annotations below image
axes.text(0.5, -0.1, '#1 Total Feeds (553)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.2, '#1 Total Feeds w/ Attempts (436)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.3, '#2 Total CPRs for WAs (331)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Save as next figure reveal
plt.savefig('outputs\\vol5_example_2.png', format = 'png', 
            facecolor = fig.get_facecolor(), edgecolor = 'none',
            dpi = 300)

#Close figure
plt.close()

#Create some figures comparing Watson to other WAs in 2019
year = 2019

#Get the 2019 data
waData2019 = waData.loc[waData['year'] == 2019,]

#Create figure for WA total CPRs
figCPR, axCPR = plt.subplots(figsize = (7,5))

#Adjust subplot
plt.subplots_adjust(bottom = 0.2)

#Sort values by total CPR
waData2019_CPR = waData2019.sort_values('totalCPR', ascending = False).reset_index(drop = True)

#Plot the bars for the WAs for CPRs
axCPR.bar(np.linspace(1,len(waData2019_CPR),len(waData2019_CPR)),
          waData2019_CPR['totalCPR'],
          width = 0.15, zorder = 2)

#Loop through bars, change colour, add lollipop point
barWidth = 0.15
for barNo in range(len(axCPR.patches)):   
    #Set colour of patch to match team colour
    newCol = colourDict[waData2019_CPR['squadName'][barNo]]
    axCPR.patches[barNo].set_fc(newCol)    
    #Add lollipop point
    #Get the x,y coordinate to plot
    xPt,yPt = axCPR.patches[barNo].get_x(),axCPR.patches[barNo].get_height()
    #Plot the point
    axCPR.scatter(xPt + (barWidth/2), yPt,
                  color = newCol, s = 300, zorder = 4)
    #Add CPR number
    axCPR.text(xPt + (barWidth/2), yPt,
               str(waData2019_CPR['totalCPR'][barNo]),
               color = 'white',
               ha = 'center', va = 'center',
               zorder = 5,
               fontsize = 8, fontweight = 'bold', clip_on = False)
    
#Add y-label
axCPR.set_ylabel('Total Centre Passes Received', labelpad = 10)

#Set x-ticks
axCPR.set_xticks(np.linspace(1,len(waData2019_CPR),len(waData2019_CPR)))
axCPR.set_xticklabels(list(waData2019_CPR['playerName'][0:len(waData2019_CPR)]),
                           rotation = 45, ha = 'right')

#Set and get rid of y-ticks
axCPR.tick_params(axis = 'y', length = 0)
axCPR.set_yticks(np.linspace(0,350,8))

#Turn off axes lines we don't want
axCPR.spines['top'].set_visible(False)
axCPR.spines['left'].set_visible(False)
axCPR.spines['right'].set_visible(False)

#Add horizontal lines
for lineLevel in axCPR.get_yticks():
    axCPR.axhline(y = lineLevel, c = 'lightgrey',
                  lw = 0.5, ls = '--', zorder = 1)
    
#Add figure title using text
figCPR.text(0.05, 0.98, 'Total Centre Passes Received by Wing Attacks in Super Netball 2019',
            fontsize = 14, fontweight = 'bold', ha = 'left', va = 'top')
figCPR.text(0.05, 0.94, 'Minimum 7 matches started at WA to be included',
            fontsize = 8, fontweight = 'normal', ha = 'left', va = 'top')

#Set figure colouring
figCPR.patch.set_facecolor('#fffaf0')
axCPR.set_facecolor('#fffaf0')

#Save figure
plt.savefig('outputs\\vol5_example_WA_0.png', format = 'png', 
            facecolor = fig.get_facecolor(), edgecolor = 'none',
            dpi = 300)

#Close figure
plt.close()

#Create figure for WA total feeds
figFeeds, axFeeds = plt.subplots(figsize = (7,5))

#Adjust subplot
plt.subplots_adjust(bottom = 0.2)

#Sort values by total CPR
waData2019_Feeds = waData2019.sort_values('totalFeeds', ascending = False).reset_index(drop = True)

#Plot the bars for the WAs for CPRs
axFeeds.bar(np.linspace(1,len(waData2019_Feeds),len(waData2019_Feeds)),
            waData2019_Feeds['totalFeeds'],
            width = 0.15, zorder = 2)

#Loop through bars, change colour, add lollipop point
barWidth = 0.15
for barNo in range(len(axFeeds.patches)):   
    #Set colour of patch to match team colour
    newCol = colourDict[waData2019_Feeds['squadName'][barNo]]
    axFeeds.patches[barNo].set_fc(newCol)    
    #Add lollipop point
    #Get the x,y coordinate to plot
    xPt,yPt = axFeeds.patches[barNo].get_x(),axFeeds.patches[barNo].get_height()
    #Plot the point
    axFeeds.scatter(xPt + (barWidth/2), yPt,
                  color = newCol, s = 300, zorder = 4)
    #Add CPR number
    axFeeds.text(xPt + (barWidth/2), yPt,
               str(waData2019_Feeds['totalFeeds'][barNo]),
               color = 'white',
               ha = 'center', va = 'center',
               zorder = 5,
               fontsize = 8, fontweight = 'bold', clip_on = False)
    
#Add y-label
axFeeds.set_ylabel('Total Feeds', labelpad = 10)

#Set x-ticks
axFeeds.set_xticks(np.linspace(1,len(waData2019_Feeds),len(waData2019_Feeds)))
axFeeds.set_xticklabels(list(waData2019_Feeds['playerName'][0:len(waData2019_Feeds)]),
                           rotation = 45, ha = 'right')

#Set and get rid of y-ticks
axFeeds.tick_params(axis = 'y', length = 0)
axFeeds.set_yticks(np.linspace(0,500,6))

#Turn off axes lines we don't want
axFeeds.spines['top'].set_visible(False)
axFeeds.spines['left'].set_visible(False)
axFeeds.spines['right'].set_visible(False)

#Add horizontal lines
for lineLevel in axFeeds.get_yticks():
    axFeeds.axhline(y = lineLevel, c = 'lightgrey',
                  lw = 0.5, ls = '--', zorder = 1)
    
#Add figure title using text
figFeeds.text(0.05, 0.98, 'Total Feeds by Wing Attacks in Super Netball 2019',
            fontsize = 14, fontweight = 'bold', ha = 'left', va = 'top')
figFeeds.text(0.05, 0.94, 'Minimum 7 matches started at WA to be included',
            fontsize = 8, fontweight = 'normal', ha = 'left', va = 'top')

#Set figure colouring
figFeeds.patch.set_facecolor('#fffaf0')
axFeeds.set_facecolor('#fffaf0')

#Save figure
plt.savefig('outputs\\vol5_example_WA_1.png', format = 'png', 
            facecolor = fig.get_facecolor(), edgecolor = 'none',
            dpi = 300)

#Close figure
plt.close()

# %% Goal Keeper

#Extract data from 'starting' GKs

#Get the list of starters by year
eligibleStarters = startersData.loc[startersData['pos'] == 'GK',
                                    ].reset_index(drop = True)

#Loop through eligible starters to create mask
extractInd = []
for starterNo in range(len(eligibleStarters)):
    
    #Create current mask
    starterMask = (totalStats['year'] == eligibleStarters['year'][starterNo]) & \
        (totalStats['playerId'] == eligibleStarters['playerId'][starterNo])
        
    #Find where current mask is True and append
    extractInd.append(np.where(starterMask == True)[0][0])
    
#Extract data, keeping a focused set of variables
posStats = totalStats.iloc[extractInd][['year', 'playerName','playerId',
                                        'deflections', 'deflectionWithGain', 'deflectionWithNoGain',
                                        'gain', 'turnovers', 'generalPlayTurnovers',
                                        'intercepts', 'obstructionPenalties',
                                        'contactPenalties', 'penalties',
                                        'netPoints', 'rebounds',
                                        'deflections_per15', 'deflectionWithGain_per15', 'deflectionWithNoGain_per15',
                                        'gain_per15', 'turnovers_per15', 'generalPlayTurnovers_per15',
                                        'intercepts_per15', 'obstructionPenalties_per15',
                                        'contactPenalties_per15', 'penalties_per15',
                                        'netPoints_per15', 'rebounds_per15',]].reset_index(drop = True)

#Sterling from 2019 can take starting GK
#No. 1 for league and GK's within year for gains, deflections and intercepts
#No. 1 across these total categories of any player within a season in this 2019

#Mentor or Layton from 2017 close behind and one of these should be backup

# %% Goal Defence

#Extract data from 'starting' GDs

#Get the list of starters by year
eligibleStarters = startersData.loc[startersData['pos'] == 'GD',
                                    ].reset_index(drop = True)

#Loop through eligible starters to create mask
extractInd = []
for starterNo in range(len(eligibleStarters)):
    
    #Create current mask
    starterMask = (totalStats['year'] == eligibleStarters['year'][starterNo]) & \
        (totalStats['playerId'] == eligibleStarters['playerId'][starterNo])
        
    #Find where current mask is True and append
    extractInd.append(np.where(starterMask == True)[0][0])
    
#Extract data, keeping a focused set of variables
posStats = totalStats.iloc[extractInd][['year', 'playerName','playerId',
                                        'deflections', 'deflectionWithGain', 'deflectionWithNoGain',
                                        'gain', 'turnovers', 'generalPlayTurnovers',
                                        'intercepts', 'obstructionPenalties',
                                        'contactPenalties', 'penalties',
                                        'netPoints', 'rebounds', 'centrePassReceives',
                                        'deflections_per15', 'deflectionWithGain_per15', 'deflectionWithNoGain_per15',
                                        'gain_per15', 'turnovers_per15', 'generalPlayTurnovers_per15',
                                        'intercepts_per15', 'obstructionPenalties_per15',
                                        'contactPenalties_per15', 'penalties_per15',
                                        'netPoints_per15', 'rebounds_per15', 'centrePassReceives_per15',]].reset_index(drop = True)

#Pretorius from 2019 gets the nod for GD's
#No. 1 amount GD's for gains and intercepts within year
#No. 2 in league for intercepts within year
#No. 1 for GD's across this category within any year

# %% Wing Defence

#Extract data from 'starting' WDs

#Get the list of starters by year
eligibleStarters = startersData.loc[startersData['pos'] == 'WD',
                                    ].reset_index(drop = True)

#Loop through eligible starters to create mask
extractInd = []
for starterNo in range(len(eligibleStarters)):
    
    #Create current mask
    starterMask = (totalStats['year'] == eligibleStarters['year'][starterNo]) & \
        (totalStats['playerId'] == eligibleStarters['playerId'][starterNo])
        
    #Find where current mask is True and append
    extractInd.append(np.where(starterMask == True)[0][0])
    
#Extract data, keeping a focused set of variables
posStats = totalStats.iloc[extractInd][['year', 'playerName','playerId',
                                        'deflections', 'deflectionWithGain', 'deflectionWithNoGain',
                                        'gain', 'turnovers', 'generalPlayTurnovers',
                                        'intercepts', 'obstructionPenalties',
                                        'contactPenalties', 'penalties',
                                        'netPoints', 'rebounds', 'centrePassReceives',
                                        'deflections_per15', 'deflectionWithGain_per15', 'deflectionWithNoGain_per15',
                                        'gain_per15', 'turnovers_per15', 'generalPlayTurnovers_per15',
                                        'intercepts_per15', 'obstructionPenalties_per15',
                                        'contactPenalties_per15', 'penalties_per15',
                                        'netPoints_per15', 'rebounds_per15', 'centrePassReceives_per15',]].reset_index(drop = True)

#Brazill in 2018 no. 1 across WDs for gains, intercepts and CPRs
#No. 1 in all of these categories across WDs for any year

# %% Defensive Crew Reveal

#Do a 3-player reveal for the defensive crew

#Set title labels for this iteration
titleLabels = ['J.Fowler (2020)', 'GA', 'L.Watson (2019)', 'C', 'A.Brazill (2018)', 'K.Pretorius (2019)', 'S.Sterling (2019)',
               '', 'Bench', 'Bench', 'Bench', 'Bench', 'Bench', ''] #extras for axes structure

#Use function to create base figure
fig, ax = figureBase(titleLabels)

#Re-add Fowler details

#Set axes to use
axes = ax.flatten()[0]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Fowler image
#Image placement took a bit of experimentation - still some stray pixels outside
#Use a green image
#Load image, using counter
playerImg = plt.imread('images\\J.Fowler_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.51
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.506,0.545),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0)
annBox.zorder = 5
#Add image
axes.add_artist(annBox)

#Add annotations below image
#+212 more goals than the second ranked scorer for the year
axes.text(0.5, -0.1, '#1 Goals Scored (795 goals)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
#Second highest seasons shooting percentage over super netball career
#96.55% in 2021 season
axes.text(0.5, -0.2, '93.64% Shooting Percentage', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
#Highest proportion of teams scoring across Super Netball career
axes.text(0.5, -0.3, '87.36% of Teams Scoring', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Add Watson details

#Set axes to use
axes = ax.flatten()[2]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Watson image
#Image placement took a bit of experimentation - still some stray pixels outside
#Use a green image
#Load image, using counter
playerImg = plt.imread('images\\L.Watson_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.51
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.506,0.545),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0)
annBox.zorder = 5
#Add image
axes.add_artist(annBox)

#Add annotations below image
axes.text(0.5, -0.1, '#1 Total Feeds (553)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.2, '#1 Total Feeds w/ Attempts (436)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.3, '#2 Total CPRs for WAs (331)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Add Brazill details

#Set axes to use
axes = ax.flatten()[4]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Brazill image
#Load image, using counter
playerImg = plt.imread('images\\A.Brazill_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.51
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.50,0.545),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0)
annBox.zorder = 5
#Add image
axes.add_artist(annBox)

#Add annotations below image
axes.text(0.5, -0.1, '#1 Total Gains for WDs (45)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.2, '#1 Total Intercepts for WDs (33)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.3, '#1 Total CPRs for WDs (147)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Add Pretorius details

#Set axes to use
axes = ax.flatten()[5]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Pretorius image
#Load image, using counter
playerImg = plt.imread('images\\K.Pretorius_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.51
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.50,0.545),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0)
annBox.zorder = 5
#Add image
axes.add_artist(annBox)

#Add annotations below image
axes.text(0.5, -0.1, '#1 Total Gains for GDs (92)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.2, '#2 Total Gains (92)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.3, '#1 Total Intercepts for GDs (63)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Add Sterling details

#Set axes to use
axes = ax.flatten()[6]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Sterling image
#Load image, using counter
playerImg = plt.imread('images\\S.Sterling_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.51
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.50,0.545),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0)
annBox.zorder = 5
#Add image
axes.add_artist(annBox)

#Add annotations below image
axes.text(0.5, -0.1, '#1 Total Gains (126)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.2, '#1 Total Deflections (120)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.3, '#1 Total Intercepts (68)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Save as next figure reveal
plt.savefig('outputs\\vol5_example_3.png', format = 'png', 
            facecolor = fig.get_facecolor(), edgecolor = 'none',
            dpi = 300)

#Close figure
plt.close()

#Create a subplot of gains and intercepts across all seasons for visual

#Create figure for total gains and intercepts
figDef, axDef = plt.subplots(figsize = (14,6), nrows = 1, ncols = 2)

#Adjust subplot
plt.subplots_adjust(bottom = 0.2)

#Get the top 10 for gains & intercepts

#Get the dataframes sorted
gainsTotal = totalStats.sort_values('gain', ascending = False).reset_index(drop = True)
interceptsTotal = totalStats.sort_values('intercepts', ascending = False).reset_index(drop = True)

#Get the top 10 values, player name & year, and squad
valsGains = []
xLabelsGains = []
squadNameGains = []
valsIntercepts = []
xLabelsIntercepts = []
squadNameIntercepts = []
for indNo in range(10):
    #Gains
    #Get the current value
    valsGains.append(gainsTotal['gain'][indNo])
    #Get the label for player and year
    xLabelsGains.append(gainsTotal['playerName'][indNo]+' ('+str(gainsTotal['year'][indNo])+')')
    #Get the squad name
    squadNameGains.append(playerData.loc[(playerData['playerName'] == gainsTotal['playerName'][indNo]) &
                                         (playerData['year'] == gainsTotal['year'][indNo]),
                                         ['squadName']]['squadName'].unique()[0])
    #Intercepts
    #Get the current value
    valsIntercepts.append(interceptsTotal['intercepts'][indNo])
    #Get the label for player and year
    xLabelsIntercepts.append(interceptsTotal['playerName'][indNo]+' ('+str(interceptsTotal['year'][indNo])+')')
    #Get the squad name
    squadNameIntercepts.append(playerData.loc[(playerData['playerName'] == interceptsTotal['playerName'][indNo]) &
                                              (playerData['year'] == interceptsTotal['year'][indNo]),
                                              ['squadName']]['squadName'].unique()[0])

#Plot the bars for gains
axDef[0].bar(np.linspace(1,len(valsGains),len(valsGains)),
             valsGains, width = 0.15, zorder = 2)

#Loop through bars, change colour, add lollipop point
barWidth = 0.15
for barNo in range(len(axDef[0].patches)):   
    #Set colour of patch to match team colour
    newCol = colourDict[squadNameGains[barNo]]
    axDef[0].patches[barNo].set_fc(newCol)    
    #Add lollipop point
    #Get the x,y coordinate to plot
    xPt,yPt = axDef[0].patches[barNo].get_x(),axDef[0].patches[barNo].get_height()
    #Plot the point
    axDef[0].scatter(xPt + (barWidth/2), yPt,
                     color = newCol, s = 300, zorder = 4)
    #Add number
    axDef[0].text(xPt + (barWidth/2), yPt,
                  str(valsGains[barNo]),
                  color = 'white',
                  ha = 'center', va = 'center',
                  zorder = 5,
                  fontsize = 8, fontweight = 'bold', clip_on = False)
    
#Add y-label
axDef[0].set_ylabel('Total Gains', labelpad = 10)

#Set x-ticks
axDef[0].set_xticks(np.linspace(1,len(valsGains),len(valsGains)))
axDef[0].set_xticklabels(xLabelsGains, rotation = 45, ha = 'right')

#Set and get rid of y-ticks
axDef[0].tick_params(axis = 'y', length = 0)
axDef[0].set_yticks(np.linspace(0,120,7))

#Turn off axes lines we don't want
axDef[0].spines['top'].set_visible(False)
axDef[0].spines['left'].set_visible(False)
axDef[0].spines['right'].set_visible(False)

#Add horizontal lines
for lineLevel in axDef[0].get_yticks():
    axDef[0].axhline(y = lineLevel, c = 'lightgrey',
                     lw = 0.5, ls = '--', zorder = 1)
    
#Plot the bars for intercepts
axDef[1].bar(np.linspace(1,len(valsIntercepts),len(valsIntercepts)),
             valsIntercepts, width = 0.15, zorder = 2)

#Loop through bars, change colour, add lollipop point
barWidth = 0.15
for barNo in range(len(axDef[1].patches)):   
    #Set colour of patch to match team colour
    newCol = colourDict[squadNameIntercepts[barNo]]
    axDef[1].patches[barNo].set_fc(newCol)    
    #Add lollipop point
    #Get the x,y coordinate to plot
    xPt,yPt = axDef[1].patches[barNo].get_x(),axDef[1].patches[barNo].get_height()
    #Plot the point
    axDef[1].scatter(xPt + (barWidth/2), yPt,
                     color = newCol, s = 300, zorder = 4)
    #Add number
    axDef[1].text(xPt + (barWidth/2), yPt,
                  str(valsIntercepts[barNo]),
                  color = 'white',
                  ha = 'center', va = 'center',
                  zorder = 5,
                  fontsize = 8, fontweight = 'bold', clip_on = False)
    
#Add y-label
axDef[1].set_ylabel('Total Intercepts', labelpad = 10)

#Set x-ticks
axDef[1].set_xticks(np.linspace(1,len(valsIntercepts),len(valsIntercepts)))
axDef[1].set_xticklabels(xLabelsIntercepts, rotation = 45, ha = 'right')

#Set and get rid of y-ticks
axDef[1].tick_params(axis = 'y', length = 0)
axDef[1].set_yticks(np.linspace(0,70,8))

#Turn off axes lines we don't want
axDef[1].spines['top'].set_visible(False)
axDef[1].spines['left'].set_visible(False)
axDef[1].spines['right'].set_visible(False)

#Add horizontal lines
for lineLevel in axDef[1].get_yticks():
    axDef[1].axhline(y = lineLevel, c = 'lightgrey',
                     lw = 0.5, ls = '--', zorder = 1)
    
#Add figure title using text
figDef.text(0.05, 0.98, 'Total gains and intercepts by players across all years of Super Netball',
            fontsize = 14, fontweight = 'bold', ha = 'left', va = 'top')
figDef.text(0.05, 0.94, 'Player and year highlighted in axis labels',
            fontsize = 8, fontweight = 'normal', ha = 'left', va = 'top')

#Set figure colouring
figDef.patch.set_facecolor('#fffaf0')
axDef[0].set_facecolor('#fffaf0')
axDef[1].set_facecolor('#fffaf0')

#Save figure
plt.savefig('outputs\\vol5_example_GK_0.png', format = 'png', 
            facecolor = figDef.get_facecolor(), edgecolor = 'none',
            dpi = 300)

#Close figure
plt.close()

# %% Goal Attack

#Extract data from 'starting' GAs

#Get the list of starters by year
eligibleStarters = startersData.loc[startersData['pos'] == 'GA',
                                    ].reset_index(drop = True)

#Loop through eligible starters to create mask
extractInd = []
for starterNo in range(len(eligibleStarters)):
    
    #Create current mask
    starterMask = (totalStats['year'] == eligibleStarters['year'][starterNo]) & \
        (totalStats['playerId'] == eligibleStarters['playerId'][starterNo])
        
    #Find where current mask is True and append
    extractInd.append(np.where(starterMask == True)[0][0])
    
#Extract data, keeping a focused set of variables
posStatsTotal = totalStats.iloc[extractInd][['year', 'playerName','playerId',
                                             'feeds', 'feedWithAttempt',
                                             'turnovers', 'generalPlayTurnovers',
                                             'netPoints', 'rebounds', 'centrePassReceives',
                                             'goalAssists', 'goalAttempts', 'goalMisses', 'goals',
                                             ]].reset_index(drop = True)

posStatsProp = totalStats.iloc[extractInd][['year', 'playerName','playerId',
                                            'feeds_teamProp', 'feedWithAttempt_teamProp',
                                            'turnovers_teamProp', 'generalPlayTurnovers_teamProp',
                                            'netPoints_teamProp', 'rebounds_teamProp', 'centrePassReceives_teamProp',
                                            'goalAssists_teamProp', 'goalAttempts_teamProp', 'goalMisses_teamProp', 'goals_teamProp',
                                            ]].reset_index(drop = True)

posStatsPer = totalStats.iloc[extractInd][['year', 'playerName','playerId',
                                           'feeds_per15', 'feedWithAttempt_per15',
                                           'turnovers_per15', 'generalPlayTurnovers_per15',
                                           'netPoints_per15', 'rebounds_per15', 'centrePassReceives_per15',
                                           'goalAssists_per15', 'goalAttempts_per15', 'goalMisses_per15', 'goals_per15',
                                           ]].reset_index(drop = True)

#Tippett from 2019 for GA - #1 for total goals for GAs in year and overall, #1
#for team proportion of goals among GAs in year and overall, #1 for CPRs among
#GAs for the year and #2 overall

#Medhurst a relevant back-up GA for different reasons (i.e. feeds, assists)
#Philip another potential option

#Set title labels for this iteration
titleLabels = ['J.Fowler (2020)', 'G.Tippett (2019)', 'L.Watson (2019)', 'C', 'A.Brazill (2018)', 'K.Pretorius (2019)', 'S.Sterling (2019)',
               '', 'Bench', 'Bench', 'Bench', 'Bench', 'Bench', ''] #extras for axes structure

#Use function to create base figure
fig, ax = figureBase(titleLabels)

#Re-add Fowler details

#Set axes to use
axes = ax.flatten()[0]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Fowler image
#Image placement took a bit of experimentation - still some stray pixels outside
#Use a green image
#Load image, using counter
playerImg = plt.imread('images\\J.Fowler_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.51
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.506,0.545),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0)
annBox.zorder = 5
#Add image
axes.add_artist(annBox)

#Add annotations below image
#+212 more goals than the second ranked scorer for the year
axes.text(0.5, -0.1, '#1 Goals Scored (795 goals)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
#Second highest seasons shooting percentage over super netball career
#96.55% in 2021 season
axes.text(0.5, -0.2, '93.64% Shooting Percentage', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
#Highest proportion of teams scoring across Super Netball career
axes.text(0.5, -0.3, '87.36% of Teams Scoring', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Add Watson details

#Set axes to use
axes = ax.flatten()[2]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Watson image
#Image placement took a bit of experimentation - still some stray pixels outside
#Use a green image
#Load image, using counter
playerImg = plt.imread('images\\L.Watson_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.51
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.506,0.545),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0)
annBox.zorder = 5
#Add image
axes.add_artist(annBox)

#Add annotations below image
axes.text(0.5, -0.1, '#1 Total Feeds (553)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.2, '#1 Total Feeds w/ Attempts (436)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.3, '#2 Total CPRs for WAs (331)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Add Brazill details

#Set axes to use
axes = ax.flatten()[4]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Brazill image
#Load image, using counter
playerImg = plt.imread('images\\A.Brazill_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.51
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.50,0.545),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0)
annBox.zorder = 5
#Add image
axes.add_artist(annBox)

#Add annotations below image
axes.text(0.5, -0.1, '#1 Total Gains for WDs (45)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.2, '#1 Total Intercepts for WDs (33)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.3, '#1 Total CPRs for WDs (147)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Add Pretorius details

#Set axes to use
axes = ax.flatten()[5]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Pretorius image
#Load image, using counter
playerImg = plt.imread('images\\K.Pretorius_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.51
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.50,0.545),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0)
annBox.zorder = 5
#Add image
axes.add_artist(annBox)

#Add annotations below image
axes.text(0.5, -0.1, '#1 Total Gains for GDs (92)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.2, '#2 Total Gains (92)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.3, '#1 Total Intercepts for GDs (63)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Add Sterling details

#Set axes to use
axes = ax.flatten()[6]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Sterling image
#Load image, using counter
playerImg = plt.imread('images\\S.Sterling_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.51
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.50,0.545),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0)
annBox.zorder = 5
#Add image
axes.add_artist(annBox)

#Add annotations below image
axes.text(0.5, -0.1, '#1 Total Gains (126)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.2, '#1 Total Deflections (120)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.3, '#1 Total Intercepts (68)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Add Tippett details

#Set axes to use
axes = ax.flatten()[1]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Tippett image
#Load image, using counter
playerImg = plt.imread('images\\G.Tippett_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.49
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.50,0.515),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0,
                        clip_on = True)
annBox.zorder = 5

#Add image
axes.add_artist(annBox)

#Add annotations below image
axes.text(0.5, -0.1, '#1 Total Goals for GAs (394)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.2, '#1 Total CPRs for GAs (325)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.3, '48.34% of Teams Scoring', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Save as next figure reveal
plt.savefig('outputs\\vol5_example_4.png', format = 'png', 
            facecolor = fig.get_facecolor(), edgecolor = 'none',
            dpi = 300)

#Close figure
plt.close()

#Create a subplot of GAs total CPRs and scoring proportion across all seasons for visual

#Create figure for total gains and intercepts
figGa, axGa = plt.subplots(figsize = (14,6), nrows = 1, ncols = 2)

#Adjust subplot
plt.subplots_adjust(bottom = 0.2)

#Get the top 10 for total CPRs & team goal proportions

#Get the dataframes sorted
cprTotal = posStatsTotal.sort_values('centrePassReceives', ascending = False).reset_index(drop = True)
goalsProp = posStatsProp.sort_values('goals_teamProp', ascending = False).reset_index(drop = True)

#Get the top 10 values, player name & year, and squad
valsGoals = []
xLabelsGoals = []
squadNameGoals = []
valsCPRs = []
xLabelsCPRs = []
squadNameCPRs = []
for indNo in range(10):
    #Gains
    #Get the current value
    valsGoals.append(goalsProp['goals_teamProp'][indNo])
    #Get the label for player and year
    xLabelsGoals.append(goalsProp['playerName'][indNo]+' ('+str(goalsProp['year'][indNo])+')')
    #Get the squad name
    squadNameGoals.append(playerData.loc[(playerData['playerName'] == goalsProp['playerName'][indNo]) &
                                         (playerData['year'] == goalsProp['year'][indNo]),
                                         ['squadName']]['squadName'].unique()[0])
    #Intercepts
    #Get the current value
    valsCPRs.append(cprTotal['centrePassReceives'][indNo])
    #Get the label for player and year
    xLabelsCPRs.append(cprTotal['playerName'][indNo]+' ('+str(cprTotal['year'][indNo])+')')
    #Get the squad name
    squadNameCPRs.append(playerData.loc[(playerData['playerName'] == cprTotal['playerName'][indNo]) &
                                              (playerData['year'] == cprTotal['year'][indNo]),
                                              ['squadName']]['squadName'].unique()[0])

#Plot the bars for goals
axGa[0].bar(np.linspace(1,len(valsGoals),len(valsGoals)),
             valsGoals, width = 0.15, zorder = 2)

#Loop through bars, change colour, add lollipop point
barWidth = 0.15
for barNo in range(len(axGa[0].patches)):   
    #Set colour of patch to match team colour
    newCol = colourDict[squadNameGoals[barNo]]
    axGa[0].patches[barNo].set_fc(newCol)    
    #Add lollipop point
    #Get the x,y coordinate to plot
    xPt,yPt = axGa[0].patches[barNo].get_x(),axGa[0].patches[barNo].get_height()
    #Plot the point
    axGa[0].scatter(xPt + (barWidth/2), yPt,
                     color = newCol, s = 300, zorder = 4)
    #Add number
    axGa[0].text(xPt + (barWidth/2), yPt,
                  str(int(np.round(valsGoals[barNo]*100)))+'%',
                  color = 'white',
                  ha = 'center', va = 'center',
                  zorder = 5,
                  fontsize = 8, fontweight = 'bold', clip_on = False)
    
#Add y-label
axGa[0].set_ylabel('Proportion of Teams Total Scoring', labelpad = 10)

#Set x-ticks
axGa[0].set_xticks(np.linspace(1,len(valsGoals),len(valsGoals)))
axGa[0].set_xticklabels(xLabelsGoals, rotation = 45, ha = 'right')

#Set and get rid of y-ticks
axGa[0].tick_params(axis = 'y', length = 0)
axGa[0].set_yticks(np.linspace(0,0.5,6))

#Turn off axes lines we don't want
axGa[0].spines['top'].set_visible(False)
axGa[0].spines['left'].set_visible(False)
axGa[0].spines['right'].set_visible(False)

#Add horizontal lines
for lineLevel in axGa[0].get_yticks():
    axGa[0].axhline(y = lineLevel, c = 'lightgrey',
                     lw = 0.5, ls = '--', zorder = 1)
    
#Plot the bars for centre pass receives
axGa[1].bar(np.linspace(1,len(valsCPRs),len(valsCPRs)),
             valsCPRs, width = 0.15, zorder = 2)

#Loop through bars, change colour, add lollipop point
barWidth = 0.15
for barNo in range(len(axGa[1].patches)):   
    #Set colour of patch to match team colour
    newCol = colourDict[squadNameCPRs[barNo]]
    axGa[1].patches[barNo].set_fc(newCol)    
    #Add lollipop point
    #Get the x,y coordinate to plot
    xPt,yPt = axGa[1].patches[barNo].get_x(),axGa[1].patches[barNo].get_height()
    #Plot the point
    axGa[1].scatter(xPt + (barWidth/2), yPt,
                     color = newCol, s = 300, zorder = 4)
    #Add number
    axGa[1].text(xPt + (barWidth/2), yPt,
                  str(valsCPRs[barNo]),
                  color = 'white',
                  ha = 'center', va = 'center',
                  zorder = 5,
                  fontsize = 8, fontweight = 'bold', clip_on = False)
    
#Add y-label
axGa[1].set_ylabel('Total Centre Pass Receives', labelpad = 10)

#Set x-ticks
axGa[1].set_xticks(np.linspace(1,len(valsCPRs),len(valsCPRs)))
axGa[1].set_xticklabels(xLabelsCPRs, rotation = 45, ha = 'right')

#Set and get rid of y-ticks
axGa[1].tick_params(axis = 'y', length = 0)
axGa[1].set_yticks(np.linspace(0,350,8))

#Turn off axes lines we don't want
axGa[1].spines['top'].set_visible(False)
axGa[1].spines['left'].set_visible(False)
axGa[1].spines['right'].set_visible(False)

#Add horizontal lines
for lineLevel in axGa[1].get_yticks():
    axGa[1].axhline(y = lineLevel, c = 'lightgrey',
                     lw = 0.5, ls = '--', zorder = 1)
    
#Add figure title using text
figGa.text(0.05, 0.98, 'Proportion of teams total scoring and total CPRs by GAs across all years of Super Netball',
            fontsize = 14, fontweight = 'bold', ha = 'left', va = 'top')
figGa.text(0.05, 0.94, 'Player and year highlighted in axis labels',
            fontsize = 8, fontweight = 'normal', ha = 'left', va = 'top')

#Set figure colouring
figGa.patch.set_facecolor('#fffaf0')
axGa[0].set_facecolor('#fffaf0')
axGa[1].set_facecolor('#fffaf0')

#Save figure
plt.savefig('outputs\\vol5_example_GA_0.png', format = 'png', 
            facecolor = figGa.get_facecolor(), edgecolor = 'none',
            dpi = 300)

#Close figure
plt.close()

# %% Centre

#Extract data from 'starting' Cs

#Get the list of starters by year
eligibleStarters = startersData.loc[startersData['pos'] == 'C',
                                    ].reset_index(drop = True)

#Loop through eligible starters to create mask
extractInd = []
for starterNo in range(len(eligibleStarters)):
    
    #Create current mask
    starterMask = (totalStats['year'] == eligibleStarters['year'][starterNo]) & \
        (totalStats['playerId'] == eligibleStarters['playerId'][starterNo])
        
    #Find where current mask is True and append
    extractInd.append(np.where(starterMask == True)[0][0])
    
#Extract data, keeping a focused set of variables
posStatsTotal = totalStats.iloc[extractInd][['year', 'playerName','playerId',
                                             'feeds', 'feedWithAttempt',
                                             'turnovers', 'generalPlayTurnovers',
                                             'netPoints', 'goalAssists',
                                             'deflections', 'deflectionWithGain',
                                             'gain', 'intercepts',
                                        ]].reset_index(drop = True)

posStatsProp = totalStats.iloc[extractInd][['year', 'playerName','playerId',
                                            'feeds_teamProp', 'feedWithAttempt_teamProp',
                                            'turnovers_teamProp', 'generalPlayTurnovers_teamProp',
                                            'netPoints_teamProp', 'goalAssists_teamProp',
                                            'deflections_teamProp', 'deflectionWithGain_teamProp',
                                            'gain_teamProp', 'intercepts_teamProp',
                                            ]].reset_index(drop = True)

posStatsPer = totalStats.iloc[extractInd][['year', 'playerName','playerId',
                                           'feeds_per15', 'feedWithAttempt_per15',
                                           'turnovers_per15', 'generalPlayTurnovers_per15',
                                           'netPoints_per15',  'goalAssists_per15',
                                           'deflections_per15', 'deflectionWithGain_per15',
                                           'gain_per15', 'intercepts_per15',
                                           ]].reset_index(drop = True)

#Moloney from 2019 for C
#No. 1 NetPoints for C in 2019 and all years, No. 9 all positions
#No. 1 feeds with attempt for C in 2019, No. 3 all years for C, 
#No. 1 goal assists for C in 2019, No. 3 all years

#Create reveal figure for centre

#Set title labels for this iteration
titleLabels = ['J.Fowler (2020)', 'G.Tippett (2019)', 'L.Watson (2019)', 'K.Moloney (2019)', 'A.Brazill (2018)', 'K.Pretorius (2019)', 'S.Sterling (2019)',
               '', 'Bench', 'Bench', 'Bench', 'Bench', 'Bench', ''] #extras for axes structure

#Use function to create base figure
fig, ax = figureBase(titleLabels)

#Re-add Fowler details

#Set axes to use
axes = ax.flatten()[0]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Fowler image
#Image placement took a bit of experimentation - still some stray pixels outside
#Use a green image
#Load image, using counter
playerImg = plt.imread('images\\J.Fowler_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.51
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.506,0.545),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0)
annBox.zorder = 5
#Add image
axes.add_artist(annBox)

#Add annotations below image
#+212 more goals than the second ranked scorer for the year
axes.text(0.5, -0.1, '#1 Goals Scored (795 goals)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
#Second highest seasons shooting percentage over super netball career
#96.55% in 2021 season
axes.text(0.5, -0.2, '93.64% Shooting Percentage', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
#Highest proportion of teams scoring across Super Netball career
axes.text(0.5, -0.3, '87.36% of Teams Scoring', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Add Watson details

#Set axes to use
axes = ax.flatten()[2]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Watson image
#Image placement took a bit of experimentation - still some stray pixels outside
#Use a green image
#Load image, using counter
playerImg = plt.imread('images\\L.Watson_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.51
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.506,0.545),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0)
annBox.zorder = 5
#Add image
axes.add_artist(annBox)

#Add annotations below image
axes.text(0.5, -0.1, '#1 Total Feeds (553)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.2, '#1 Total Feeds w/ Attempts (436)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.3, '#2 Total CPRs for WAs (331)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Add Brazill details

#Set axes to use
axes = ax.flatten()[4]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Brazill image
#Load image, using counter
playerImg = plt.imread('images\\A.Brazill_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.51
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.50,0.545),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0)
annBox.zorder = 5
#Add image
axes.add_artist(annBox)

#Add annotations below image
axes.text(0.5, -0.1, '#1 Total Gains for WDs (45)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.2, '#1 Total Intercepts for WDs (33)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.3, '#1 Total CPRs for WDs (147)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Add Pretorius details

#Set axes to use
axes = ax.flatten()[5]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Pretorius image
#Load image, using counter
playerImg = plt.imread('images\\K.Pretorius_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.51
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.50,0.545),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0)
annBox.zorder = 5
#Add image
axes.add_artist(annBox)

#Add annotations below image
axes.text(0.5, -0.1, '#1 Total Gains for GDs (92)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.2, '#2 Total Gains (92)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.3, '#1 Total Intercepts for GDs (63)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Add Sterling details

#Set axes to use
axes = ax.flatten()[6]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Sterling image
#Load image, using counter
playerImg = plt.imread('images\\S.Sterling_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.51
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.50,0.545),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0)
annBox.zorder = 5
#Add image
axes.add_artist(annBox)

#Add annotations below image
axes.text(0.5, -0.1, '#1 Total Gains (126)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.2, '#1 Total Deflections (120)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.3, '#1 Total Intercepts (68)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Add Tippett details

#Set axes to use
axes = ax.flatten()[1]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Tippett image
#Load image, using counter
playerImg = plt.imread('images\\G.Tippett_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.49
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.50,0.515),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0,
                        clip_on = True)
annBox.zorder = 5

#Add image
axes.add_artist(annBox)

#Add annotations below image
axes.text(0.5, -0.1, '#1 Total Goals for GAs (394)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.2, '#1 Total CPRs for GAs (325)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.3, '48.34% of Teams Scoring', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Add Moloney details

#Set axes to use
axes = ax.flatten()[3]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Moloney image
#Load image, using counter
playerImg = plt.imread('images\\K.Moloney_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.49
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.50,0.515),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0,
                        clip_on = True)
annBox.zorder = 5

#Add image
axes.add_artist(annBox)

#Add annotations below image
axes.text(0.5, -0.1, '#1 NetPoints for Cs (1043.5)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.2, '#1 Total Assists for Cs (258)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.3, '#1 Feeds w/ Attempts for Cs (297)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Save as next figure reveal
plt.savefig('outputs\\vol5_example_5.png', format = 'png', 
            facecolor = fig.get_facecolor(), edgecolor = 'none',
            dpi = 300)

#Close figure
plt.close()

# %% Bench

#Create reveal figure for bench

#Set title labels for this iteration
titleLabels = ['J.Fowler (2020)', 'G.Tippett (2019)', 'L.Watson (2019)', 'K.Moloney (2019)', 'A.Brazill (2018)', 'K.Pretorius (2019)', 'S.Sterling (2019)',
               '', 'G.Mentor (2017)', 'N.Medhurst (2018)', 'M.Browne (2018)', 'A.Parmenter (2020)', 'M.Cassidy (2020)', ''] #extras for axes structure

#Use function to create base figure
fig, ax = figureBase(titleLabels)

#Re-add Fowler details

#Set axes to use
axes = ax.flatten()[0]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Fowler image
#Image placement took a bit of experimentation - still some stray pixels outside
#Use a green image
#Load image, using counter
playerImg = plt.imread('images\\J.Fowler_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.51
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.506,0.545),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0)
annBox.zorder = 5
#Add image
axes.add_artist(annBox)

#Add annotations below image
#+212 more goals than the second ranked scorer for the year
axes.text(0.5, -0.1, '#1 Goals Scored (795 goals)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
#Second highest seasons shooting percentage over super netball career
#96.55% in 2021 season
axes.text(0.5, -0.2, '93.64% Shooting Percentage', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
#Highest proportion of teams scoring across Super Netball career
axes.text(0.5, -0.3, '87.36% of Teams Scoring', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Add Watson details

#Set axes to use
axes = ax.flatten()[2]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Watson image
#Image placement took a bit of experimentation - still some stray pixels outside
#Use a green image
#Load image, using counter
playerImg = plt.imread('images\\L.Watson_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.51
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.506,0.545),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0)
annBox.zorder = 5
#Add image
axes.add_artist(annBox)

#Add annotations below image
axes.text(0.5, -0.1, '#1 Total Feeds (553)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.2, '#1 Total Feeds w/ Attempts (436)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.3, '#2 Total CPRs for WAs (331)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Add Brazill details

#Set axes to use
axes = ax.flatten()[4]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Brazill image
#Load image, using counter
playerImg = plt.imread('images\\A.Brazill_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.51
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.50,0.545),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0)
annBox.zorder = 5
#Add image
axes.add_artist(annBox)

#Add annotations below image
axes.text(0.5, -0.1, '#1 Total Gains for WDs (45)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.2, '#1 Total Intercepts for WDs (33)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.3, '#1 Total CPRs for WDs (147)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Add Pretorius details

#Set axes to use
axes = ax.flatten()[5]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Pretorius image
#Load image, using counter
playerImg = plt.imread('images\\K.Pretorius_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.51
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.50,0.545),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0)
annBox.zorder = 5
#Add image
axes.add_artist(annBox)

#Add annotations below image
axes.text(0.5, -0.1, '#1 Total Gains for GDs (92)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.2, '#2 Total Gains (92)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.3, '#1 Total Intercepts for GDs (63)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Add Sterling details

#Set axes to use
axes = ax.flatten()[6]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Sterling image
#Load image, using counter
playerImg = plt.imread('images\\S.Sterling_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.51
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.50,0.545),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0)
annBox.zorder = 5
#Add image
axes.add_artist(annBox)

#Add annotations below image
axes.text(0.5, -0.1, '#1 Total Gains (126)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.2, '#1 Total Deflections (120)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.3, '#1 Total Intercepts (68)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Add Tippett details

#Set axes to use
axes = ax.flatten()[1]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Tippett image
#Load image, using counter
playerImg = plt.imread('images\\G.Tippett_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.49
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.50,0.515),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0,
                        clip_on = True)
annBox.zorder = 5

#Add image
axes.add_artist(annBox)

#Add annotations below image
axes.text(0.5, -0.1, '#1 Total Goals for GAs (394)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.2, '#1 Total CPRs for GAs (325)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.3, '48.34% of Teams Scoring', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Add Moloney details

#Set axes to use
axes = ax.flatten()[3]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add Moloney image
#Load image, using counter
playerImg = plt.imread('images\\K.Moloney_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.49
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.50,0.515),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0,
                        clip_on = True)
annBox.zorder = 5

#Add image
axes.add_artist(annBox)

#Add annotations below image
axes.text(0.5, -0.1, '#1 NetPoints for Cs (1043.5)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.2, '#1 Total Assists for Cs (258)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.3, '#1 Feeds w/ Attempts for Cs (297)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Add Mentor details

#Set axes to use
axes = ax.flatten()[8]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add image
#Load image, using counter
playerImg = plt.imread('images\\G.Mentor_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.49
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.50,0.515),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0,
                        clip_on = True)
annBox.zorder = 5

#Add image
axes.add_artist(annBox)

#Add annotations below image
axes.text(0.5, -0.1, '#1 Total Gains (106)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.2, '#1 Total Deflections (90)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.3, '#2 Total Intercepts (41)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Mentor's numbers were #1/2 for any players irrespective across positions for the year
#She was also SSN player of the year

#Add Medhurst details

#Set axes to use
axes = ax.flatten()[9]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add image
#Load image, using counter
playerImg = plt.imread('images\\N.Medhurst_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.485
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.50,0.515),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0,
                        clip_on = True)
annBox.zorder = 5

#Add image
axes.add_artist(annBox)

#Add annotations below image
axes.text(0.5, -0.1, '#1 Total Feeds for GAs (527)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.2, '#1 Total Assists for GAs (394)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.3, '47.19% of Teams Assists', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Medhurst's rankings are the highest for GAs across any years

#Add Browne details

#Set axes to use
axes = ax.flatten()[10]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add image
#Load image, using counter
playerImg = plt.imread('images\\M.Browne_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.49
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.50,0.515),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0,
                        clip_on = True)
annBox.zorder = 5

#Add image
axes.add_artist(annBox)

#Add annotations below image
axes.text(0.5, -0.1, '#1 Total CPRs (357)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.2, '#2 Total Assists for WAs (316)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.3, '#3 Total Feeds w/ Attempts (383)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Browne high in a range of relevant offensive statistics within season and overall

#Add Parmenter details

#Set axes to use
axes = ax.flatten()[11]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add image
#Load image, using counter
playerImg = plt.imread('images\\A.Parmenter_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.49
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.50,0.515),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0,
                        clip_on = True)
annBox.zorder = 5

#Add image
axes.add_artist(annBox)

#Add annotations below image
axes.text(0.5, -0.1, '#1 Total Deflections for WDs (62)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.2, '#1 Total Intercepts for WDs (26)', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.3, '0.76 Intercepts per 15 mins', color = xmasColGreen,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Parmenter no. 1 for deflections in year WDs, no. 2 all-time for WDs
#Also no. 1 for intercepts in year for WDs, no. 3 all time for WDs
#Intercepts per 15 minutes highest of any WD all-time

#Add Cassidy details

#Set axes to use
axes = ax.flatten()[12]

#Add a blank ellipse over xmas image
axes.add_artist(Ellipse((0.5,0.5),
                        1.0, 1.0,
                        ec = None, lw = 0,
                        fc = '#fffaf0',
                        transform = axes.transAxes,
                        zorder = 4,
                        clip_on = False))

#Add image
#Load image, using counter
playerImg = plt.imread('images\\M.Cassidy_cropped.png')
#Figure out zoom factor
#Target height took a bit of experimentation
zoomFac =  0.49
#Create offset image
imOffset = OffsetImage(playerImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.50,0.515),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (0.5,0.5),
                        xycoords = axes.transAxes,
                        #boxcoords = 'offset points',
                        pad = 0,
                        clip_on = True)
annBox.zorder = 5

#Add image
axes.add_artist(annBox)

#Add annotations below image
axes.text(0.5, -0.1, '#1 Total Feeds for Cs (495)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.2, '#1 Total Assists for Cs (266)', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)
axes.text(0.5, -0.3, '39.58% of Teams Assists', color = xmasColRed,
          ha = 'center', va = 'center',
          fontsize = 9, fontweight = 'bold', clip_on = False)

#Cassidy no. 1 for total feeds & goal assists for year and all-time for Cs
#Proportion of team assists highest for any C all-time

#Save as next figure reveal
plt.savefig('outputs\\vol5_example_6.png', format = 'png', 
            facecolor = fig.get_facecolor(), edgecolor = 'none',
            dpi = 300)

#Close figure
plt.close()

# %%% ----- End of vol5_example.py -----