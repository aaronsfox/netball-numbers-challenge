# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 13:44:37 2021

@author:
    Aaron Fox
    Centre for Sport Research
    Deakin University
    aaron.f@deakin.edu.au
    
    This script provides some example code for analysing the volume 2 dataset 
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
from matplotlib.patches import Circle
from matplotlib.colors import LinearSegmentedColormap

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
              'Magpies': '#494b4a',
              'Swifts': '#0082cd',
              'Thunderbirds': '#e54078',
              'Vixens': '#00a68e'}

#Set court height and width
courtHeight = 200
courtWidth = 100
courtHeight_m = 30.5
courtWidth_m = 15.25

#Load the dataset
data = pd.read_csv('..\\..\\datasets\\vol2\\askAndYouShallReceive.csv')

# %% Map proportions of where 2nd phase ends up for each team

#Extract the 2nd phase data from the full dataset
dataSecondPhase = data[~data['secondPhaseRec'].isnull()]

#Create team list to work through
teamList = list(colourDict.keys())

#Create figure to map data to
fig, ax = plt.subplots(figsize = (11,9), nrows = 2, ncols = 4)

#Set vertical and horizontal spacing
plt.subplots_adjust(left = 0.05, right = 0.95, bottom = 0.01, top = 0.80,
                    wspace = 0.30, hspace = 0.35)

#Loop through teams
for team in teamList:   
    
    #Extract teams dataset
    dataTeam = dataSecondPhase.loc[dataSecondPhase['teamName'] == team,]
    
    #Create colourmap for team
    teamCmap = LinearSegmentedColormap.from_list('teamCmap', ['white', colourDict[team]])
    
    #Plot court on teams axes
    
    #Set current axes
    currAx = ax.flat[teamList.index(team)]
    
    #Turn off axis
    currAx.axis('off')
        
    #Set bounds to same as court coordinates
    currAx.set_xlim([0,100])
    currAx.set_ylim([0,200])
    
    #Plot court
    #Baselines
    currAx.plot([0,courtWidth], [0,0],
                linestyle = '-', linewidth = 1.5, color = 'k',
                zorder = 10, clip_on = False)
    currAx.plot([0,courtWidth], [courtHeight,courtHeight],
                linestyle = '-', linewidth = 1.5, color = 'k',
                zorder = 10, clip_on = False)
    #Third lines
    currAx.plot([0,courtWidth], [courtHeight/3,courtHeight/3],
                linestyle = '-', linewidth = 1.5, color = 'k',
                zorder = 10, clip_on = False)
    currAx.plot([0,courtWidth], [courtHeight/3*2,courtHeight/3*2],
                linestyle = '-', linewidth = 1.5, color = 'k',
                zorder = 10, clip_on = False)
    #Draw centre circle
    currAx.add_patch(Circle((courtWidth/2,courtHeight/2), (0.9/courtWidth_m)*courtWidth,
                            linestyle = '-', linewidth = 1.5, edgecolor = 'k', facecolor = 'none',
                            zorder = 10))    
    #Add shooting circles
    currAx.add_patch(Circle((courtWidth/2,0), (4.9/courtWidth_m)*courtWidth,
                            linestyle = '-', linewidth = 1.5,
                            edgecolor = 'k', facecolor = 'none',
                            zorder = 10, clip_on = True))
    currAx.add_patch(Circle((courtWidth/2,courtHeight), (4.9/courtWidth_m)*courtWidth,
                            linestyle = '-', linewidth = 1.5,
                            edgecolor = 'k', facecolor = 'none',
                            zorder = 10, clip_on = True))
    
    #Add hexagonal binning histogram over the top of court based on XY coordinates
    #of second phase data
    hb = currAx.hexbin(dataTeam['secondPhaseX'], dataTeam['secondPhaseY'],
                       gridsize = (5,4), vmin = 0, mincnt = 1, extent = (0,100,0,200),
                       cmap = teamCmap, alpha = 1, zorder = 8,
                       clip_on = False)
    
    #Set edge colour and width for spacing between hexes
    hb.set_linewidth(1)
    hb.set_edgecolors('#fffaf0')
    
    #Get counts for each bin
    binCounts = hb.get_array()
    
    #Find top 5 bin counts and relevant percentage of total
    topInd = np.argpartition(binCounts, -5)[-5:]
    topPer = binCounts[topInd] / len(dataTeam) * 100
    # #Option to just get max
    # maxCount = np.max(binCounts)
    # maxPer = maxCount / len(dataTeam) * 100
    # maxInd = np.where(binCounts == maxCount)[0][0]
    
    #Loop through top counts and display text
    for ii in range(len(topInd)):
        #Get x,y coordinate of current hex
        topXY = hb.get_offsets()[topInd[ii]]        
        #Add text at current bin
        currAx.text(topXY[0], topXY[1], f'{np.round(topPer[ii],1)}%',
                    zorder = 11, color = 'white', ha = 'center', va = 'center',
                    fontsize = 9, fontweight = 'bold')
    
    #Add team logo for title
    #Load image
    teamLogo = plt.imread(f'images\\{team}_small.png')
    #Figure out zoom factor
    #Target height of 40
    zoomFac = 50 / teamLogo.shape[1]
    #Create offset image
    imOffset = OffsetImage(teamLogo, zoom = zoomFac)
    #Create annotation box
    annBox = AnnotationBbox(imOffset, (courtWidth/2,courtHeight),
                            xybox = (0, 35), frameon = False,
                            xycoords = 'data', boxcoords = 'offset points',
                            pad = 0)
    #Add the image
    currAx.add_artist(annBox)
        
    #Set axes face colour
    currAx.set_facecolor('#fffaf0')
    
#Set figure colouring
fig.patch.set_facecolor('#fffaf0')

#Add figure title using text
fig.text(0.05, 0.97, 'Distribution of second phase court locations during Super Netball 2018',
         fontsize = 14, fontweight = 'bold', ha = 'left', va = 'top')
fig.text(0.05, 0.94, 'Denser colours represent more frequently used court locations',
         fontsize = 10, fontweight = 'normal', ha = 'left', va = 'top')
fig.text(0.05, 0.92, 'The percentage use for the top 5 court locations are shown for each team',
         fontsize = 10, fontweight = 'normal', ha = 'left', va = 'top')

#Save figure
plt.savefig('vol2_example.png', format = 'png', 
            facecolor = fig.get_facecolor(), edgecolor = 'none',
            dpi = 300)

#Close figure
# plt.close()

# %% ---- End of vol2_example.py -----