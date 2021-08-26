# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 11:59:23 2021

@author:
    Aaron Fox
    Centre for Sport Research
    Deakin University
    aaron.f@deakin.edu.au
    
    This script provides some example code for analysing the volume 1 dataset 
    from the Netball Numbers Challenge.
    
    Python (v3.7.6) is the language used for this analysis, and includes a series
    of dependencies that can be viewed in the below import packages code chunk.
    
    See associated README.MD in folder for description.
    
"""

# %% Import packages

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# %% Set-up

#Set plot parameters
from matplotlib import rcParams
# rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = 'Arial'
rcParams['font.weight'] = 'bold'
rcParams['axes.labelsize'] = 12
rcParams['axes.titlesize'] = 16
rcParams['axes.linewidth'] = 1.5
rcParams['hatch.linewidth'] = 1.5
rcParams['axes.labelweight'] = 'bold'
rcParams['legend.fontsize'] = 10
rcParams['xtick.major.width'] = 1.5
rcParams['ytick.major.width'] = 1.5
rcParams['legend.framealpha'] = 0.0
rcParams['savefig.dpi'] = 300
rcParams['savefig.format'] = 'pdf'

#Set team colour palettes
colourDict = {'Fever': '#00953b',
              'Firebirds': '#4b2c69',
              'Giants': '#f57921',
              'Lightning': '#fdb61c',
              'Magic': '#000000',
              'Magpies': '#494b4a',
              'Mystics': '#0000cd',
              'Pulse': '#ffd500',
              'Steel': '#00b7eb',
              'Swifts': '#0082cd',
              'Tactix': '#ee161f',
              'Thunderbirds': '#e54078',
              'Vixens': '#00a68e'}

#Load the dataset
data = pd.read_csv('..\\..\\datasets\\vol1\\resultsFromTheTimeMachine.csv')

# %% Calculate average goal difference for teams across each year

#Add variable to dataframe for average goal difference
data['GdiffAvg'] = data['Gdiff'] / data['played']

#Create a grouped database that collates min, mean and max average goal difference
#Sort values by the mean values
groupedGoalDiff = data.groupby(['team']).describe()['GdiffAvg'].sort_values('mean', ascending = True)

#Extract the values into a dictionary for plotting
plotDict = {'team': list(groupedGoalDiff.index),
            'minGdiff': groupedGoalDiff['min'].values,
            'meanGdiff': groupedGoalDiff['mean'].values,
            'maxGdiff': groupedGoalDiff['max'].values}

# %% Create figure

#Set-up figure and axes
fig, ax = plt.subplots(figsize = (7,9))

#Set general marker size
mSize = 75

#Plot mean data
ax.scatter(plotDict['meanGdiff'], np.linspace(1,len(colourDict),len(colourDict)),
           c = [colourDict[plotDict['team'][ii]] for ii in range(len(plotDict['team']))],
           s = mSize, zorder = 4)

#Plot min data
ax.scatter(plotDict['minGdiff'], np.linspace(1,len(colourDict),len(colourDict)),
           c = [colourDict[plotDict['team'][ii]] for ii in range(len(plotDict['team']))],
           marker = 'v', s = mSize/2, zorder = 4)

#Plot max data
ax.scatter(plotDict['maxGdiff'], np.linspace(1,len(colourDict),len(colourDict)),
           c = [colourDict[plotDict['team'][ii]] for ii in range(len(plotDict['team']))],
           marker = '^', s = mSize/2, zorder = 4)

#Plot mean-max range line for each team
for tt in range(len(colourDict)):
    #Plot range line
    ax.plot([plotDict['minGdiff'][tt],plotDict['maxGdiff'][tt]],
            [tt+1,tt+1],
            ls = '--', lw = 1.5, color = 'darkgrey',
            zorder = 1)

#Set axes labels
ax.set_ylabel('')
ax.set_xlabel('Season Average Goal Difference', labelpad = 15)

#Set x-limits for smooth edges
ax.set_xlim([-25,15])

#Set ticks and labels
ax.set_yticks(np.linspace(1,len(colourDict),len(colourDict)))
ax.set_yticklabels(plotDict['team'], ha = 'right')
ax.tick_params(axis = 'y', length = 0)

#Replace y-axis ticks with images
for team in ax.get_yticklabels():
    #Get position
    pos = team.get_position()
    #Load image
    teamLogo = plt.imread(f'images\\{team.get_text()}_small.png')
    #Figure out zoom factor
    #Target height of 40
    zoomFac = 40 / teamLogo.shape[1]
    #Create offset image
    imOffset = OffsetImage(teamLogo, zoom = zoomFac)
    #Create annotation box
    annBox = AnnotationBbox(imOffset, (ax.get_xlim()[0],pos[1]),
                            xybox = (-25, 0), frameon = False,
                            xycoords = 'data', boxcoords = 'offset points',
                            pad = 0)
    #Add the image
    ax.add_artist(annBox)

#Clear out the y-ticks now
ax.set_yticks([])

#Add vertical zero line
ax.axvline(x = 0, ls = ':', lw = 1.0, color = 'lightgrey')

#Remove unwanted axes borders
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)

#Add figure title using text
fig.text(0.05, 0.97, 'Average, best and worst per game goal difference.',
         fontsize = 14, fontweight = 'bold', ha = 'left', va = 'top')
fig.text(0.05, 0.94, 'Circles represent average across all seasons.',
         fontsize = 10, fontweight = 'normal', ha = 'left', va = 'top')
fig.text(0.05, 0.92, 'Arrows represent best and worst season averages.',
         fontsize = 10, fontweight = 'normal', ha = 'left', va = 'top')

#Add annotations for best and worst season averages

#Loop through teams
for tt in range(len(plotDict['team'])):
    
    #Get current teams best and worst goal difference
    bestGdiff = plotDict['maxGdiff'][tt]
    worstGdiff = plotDict['minGdiff'][tt]
    
    #Set yCoord for current teams data points
    yCoord = tt + 1
    
    #Identify the year and win loss record for best/worst data points
    bestWin, bestLoss, bestYear = data.loc[(data['GdiffAvg'] == bestGdiff) &
                                           (data['team'] == plotDict['team'][tt]),
                                           ['win', 'loss','year']].values[0][:]
    worstWin, worstLoss, worstYear = data.loc[(data['GdiffAvg'] == worstGdiff) &
                                              (data['team'] == plotDict['team'][tt]),
                                              ['win', 'loss','year']].values[0][:]
    
    #Convert data coordinates to axes coordinates
    bestAxCoords = ax.transAxes.inverted().transform(ax.transData.transform((bestGdiff,yCoord)))
    worstAxCoords = ax.transAxes.inverted().transform(ax.transData.transform((worstGdiff,yCoord)))
    
    #Set strings for wins and losses based on number
    if bestWin == 1:
        bestWinString = 'win'
    else:
        bestWinString = 'wins'
    if worstWin == 1:
        worstWinString = 'win'
    else:
        worstWinString = 'wins'
    if bestLoss == 1:
        bestLossString = 'loss'
    else:
        bestLossString = 'losses'
    if worstLoss == 1:
        worstLossString = 'loss'
    else:
        worstLossString = 'losses'

    #Add text
    ax.text(bestAxCoords[0]+0.005, bestAxCoords[1]+0.005, f'{bestYear}\n{bestWin} {bestWinString} / {bestLoss} {bestLossString}',
            va = 'bottom', ha = 'left', fontsize = 6, fontweight = 'normal', style = 'italic',
            transform = ax.transAxes)
    ax.text(worstAxCoords[0]-0.005, worstAxCoords[1]-0.005, f'{worstYear}\n{worstWin} {worstWinString} / {worstLoss} {worstLossString}',
            va = 'top', ha = 'right', fontsize = 6, fontweight = 'normal', style = 'italic',
            transform = ax.transAxes)

#Set axes face colour here too
ax.set_facecolor('#fffaf0')

#Set figure colouring
fig.patch.set_facecolor('#fffaf0')

#Save figure
plt.savefig('vol1_example.png', format = 'png', 
            facecolor = fig.get_facecolor(), edgecolor = 'none',
            dpi = 300)

#Close figure
# plt.close()

# %% ---- End of vol1_example.py -----