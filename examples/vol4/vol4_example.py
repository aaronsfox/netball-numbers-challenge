# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 11:28:30 2021

@author:
    Aaron Fox
    Centre for Sport Research
    Deakin University
    aaron.f@deakin.edu.au
    
    This code looks at average Colin sightings across each round of the season.
    
"""

# %% Import packages

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

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

# %% Load dataset

#Read csv file
colinSightings = pd.read_csv('..\\..\\datasets\\vol4\\haveYouSeenColin.csv')

# %% Create a plot of average Colin sightings per round

# This is actually pretty easy with the built in functions of Seaborn. Here we
# can create the base visual and edit the specific parameters from there

#Create the figure
fig, ax = plt.subplots(figsize = (10,6), nrows = 1, ncols = 1)

#Adjust axes window
plt.subplots_adjust(left = 0.075, right = 0.925, top = 0.9, bottom = 0.2)

#Set y-axes limits
ax.set_ylim([0,8.25])

#Set y-axis ticks
ax.set_yticks(np.linspace(0,8,9, dtype = int))

#Get rid of ticks
ax.tick_params(axis = 'y', length = 0)

#Add horizontal lines
for lineLevel in ax.get_yticks():
    ax.axhline(y = lineLevel, c = 'lightgrey',
               lw = 0.5, ls = '--')
    
#Add the point plot
sns.pointplot(data = colinSightings, x = 'round', y = 'colinSightings',
              join = False, ci = 'sd', color = '#b6004a', #use of HCF red logo colour
              scale = 2, ax = ax)

#Set zorder to overlay points
plt.setp(ax.collections, zorder = 100)

#Add average sighting number to points
for xVal in ax.get_xticks():
    #Get the average value for the current round
    avgVal = np.mean(colinSightings.loc[colinSightings['round'] == xVal+1, ['colinSightings']].to_numpy())
    #Add text at central point
    ax.text(xVal, avgVal, '{0:3.1f}'.format(avgVal),
            fontsize = 8, fontweight = 'bold', color = 'white',
            ha = 'center', va = 'center', zorder = 150)

#Turn off axes lines we don't want
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)

#Set axes labels
ax.set_ylabel('Avg. Colin Sightings per Match', labelpad = 15)
ax.set_xlabel('Round No.', labelpad = 15)

#Set x tick labels
roundLabels = []
for xLabel in ax.get_xticks():
    roundLabels.append('Round '+str(xLabel+1))
ax.set_xticklabels(roundLabels, rotation = 45, va = 'top', ha = 'right')
    
#Set figure colouring
fig.patch.set_facecolor('#fffaf0')
ax.set_facecolor('#fffaf0')

#Add image
#Load image
colinImg = plt.imread('images\\colin.png')
#Set zoom factor for image
zoomFac = 0.5
#Create offset image
imOffset = OffsetImage(colinImg, zoom = zoomFac)
#Create annotation box
annBox = AnnotationBbox(imOffset, (1,0),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (1,0),
                        xycoords = fig.transFigure,
                        #boxcoords = 'offset points',
                        pad = 0)
#Add the image
ax.add_artist(annBox)
    
#Add figure title using text
fig.text(0.05, 0.98, 'Does Colin Jenkins become more prominent as the season progresses?',
         fontsize = 12, fontweight = 'bold', ha = 'left', va = 'top')
fig.text(0.05, 0.95, 'Data presented are mean and standard deviation for Colin ''sightings'' per match',
         fontsize = 8, fontweight = 'normal', ha = 'left', va = 'top')


#Save figure
plt.savefig('vol4_example.png', format = 'png', 
            facecolor = fig.get_facecolor(), edgecolor = 'none',
            dpi = 300)
    
#Close figure
# plt.close()

# %% ---- End of vol4_example.py -----