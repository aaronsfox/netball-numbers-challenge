# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 11:28:30 2021

@author:
    Aaron Fox
    Centre for Sport Research
    Deakin University
    aaron.f@deakin.edu.au
    
    This code looks at relative player mentions over subsequent time periods.
    After calculating we then plot a select group of players to demonstrate some
    of the key trends.
    
"""

# %% Import packages

import pandas as pd
import json
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.patches import Ellipse
from dateutil import parser
from datetime import datetime, timedelta
import numpy as np

# %% Define functions

#Function to progressively add X hours to datetime
def hourly_it(start, finish, hourSep):
    while finish > start:
        start = start + timedelta(hours = hourSep)
        yield start

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

#Read json file
tweets = []
for line in open('..\\..\\datasets\\vol3\\somethingAboutRiddlesAndFruit.json', 'r'):
    tweets.append(json.loads(line))
    
#Convert to dataframe
data = pd.DataFrame(tweets)

# %% Examine relative player mentions over time

#Read in supplementary data of player names to assist with searching
playerNames = pd.read_csv('..\\..\\datasets\\vol3\\supplementary\\playerList.csv')

#Create a dictionary with player name, date and count to store values in
mentionDict = {'player': [], 'date': [], 'totalMentions': [], 'relativeMentions': [], 'tweetRate': []}

#Create a datetime version of the date column
data['dateTime'] = [pd.Timestamp(parser.parse(longDate)).tz_convert('Australia/Sydney') for longDate in list(data['date'])]

# #Set datetime as index
# data.set_index(['dateTime'], inplace = True)

#Create a list of datetimes to search for across hours
hourSep = 6
startDate = datetime(2021, 9, 6, 0)
endDate = datetime(2021, 10, 9, 0)
hourlyList = [pd.Timestamp(datetime(2021, 9, 6, 0))] #set initial starting date
for hour in hourly_it(startDate, endDate, hourSep):
    hourlyList.append(pd.Timestamp(hour))
    
#Loop through pairs of dates
for ii in range(len(hourlyList)-1):
    
    #Get the two dates
    date1 = hourlyList[ii]
    date2 = hourlyList[ii+1]
    
    #Extract tweets from data between two dates
    currTweets = data[(data['dateTime'] > date1.tz_localize('Australia/Sydney')) &
                      (data['dateTime'] <= date2.tz_localize('Australia/Sydney'))]
    
    #Collect number of tweets in period
    nTweets = len(currTweets)
        
    #Loop through players for current timeframe
    for pp in range(len(playerNames)):
        
        #Get current player names & remove nan's
        #Drop the first name too as there are likely double-ups here
        playerLabels = [name for name in list(playerNames.drop(labels = 'firstName', axis = 1).iloc[pp].values) if not(pd.isnull(name)) == True]
        
        #Set player count variable as 0
        playerCount = 0
        
        #Loop through tweets if there are any for the current timeframe
        if nTweets > 0:
            for tweet in list(currTweets['content']):
                
                #Check for any player mentionsin tweet
                #Remove any upper case to avoid an issue with this
                if any(labels in tweet.lower() for labels in [playerLabels[ii].lower() for ii in range(len(playerLabels))]):
                    #Add to the count
                    playerCount += 1
                
        #Add details to data dictionary
        mentionDict['player'].append(playerLabels[0])
        mentionDict['date'].append(date1)
        mentionDict['totalMentions'].append(playerCount)
        #Set a limit of more than 25 tweets for it to be 'relevant' period to
        #calculate relative mentions
        if nTweets > 25:
            mentionDict['relativeMentions'].append(playerCount/nTweets)
        else:
            mentionDict['relativeMentions'].append(0)
        mentionDict['tweetRate'].append(playerCount/hourSep)

#Convert mention dictionary to dataframe
mentionsData = pd.DataFrame.from_dict(mentionDict)
    
#Find the most mentioned players
sumMentions = mentionsData.drop(['relativeMentions','tweetRate'],axis=1).groupby(['player']).sum().sort_values(by = 'totalMentions',
                                                                                                               ascending = False)
# %% Plot the relative mention trajectory of some big offseason movers

#Set players to plot
plotPlayers = ['Garbin',
               'Austin',
               'Dwan',
               'Dehaney']

#Set colours to plot based on new team locations
plotColours = ['#494b4a', #Magpies
               '#00a68e', #Vixens
               '#e54078', #Thunderbirds
               '#fdb61c'] #Lightning

#Set new team names
plotTeams = ['Magpies',
             'Vixens',
             'Thunderbirds',
             'Lightning']

#Create figure to map data to
fig, ax = plt.subplots(figsize = (8,6), nrows = len(plotPlayers), ncols = 1)

#Set vertical and horizontal spacing
plt.subplots_adjust(left = 0.1, right = 0.9, hspace = 0.45, bottom = 0.1)

#Loop through players and plot on each figure
for player in plotPlayers:
    
    #Extract players data - it will be in time order
    playerMentions = mentionsData.loc[mentionsData['player'] == player,].reset_index(drop = True)
    
    #Plot relative mentions against time
    ax[plotPlayers.index(player)].plot(np.linspace(0,len(playerMentions)-1,len(playerMentions)),
                                       playerMentions['relativeMentions'],
                                       c = plotColours[plotPlayers.index(player)],
                                       lw = 1.5, ls = '-',
                                       zorder = 10)
    
    #Set relevant y-limit across axes
    ax[plotPlayers.index(player)].set_ylim([ax[plotPlayers.index(player)].get_ylim()[0],0.3])
    
    #Set y-ticks
    ax[plotPlayers.index(player)].set_yticks([0,0.1,0.2,0.3])
    ax[plotPlayers.index(player)].set_yticklabels(['0%','10%','20%','30%'])
    
    #Get rid of ticks
    ax[plotPlayers.index(player)].tick_params(axis = 'y', length = 0)
    
    #Add horizontal lines
    for lineLevel in [0.1, 0.2, 0.3]:
        ax[plotPlayers.index(player)].axhline(y = lineLevel, c = 'lightgrey',
                                              lw = 0.5, ls = '--', zorder = 3)
    
    #Turn off axes lines we don't want
    ax[plotPlayers.index(player)].spines['top'].set_visible(False)
    ax[plotPlayers.index(player)].spines['left'].set_visible(False)
    ax[plotPlayers.index(player)].spines['right'].set_visible(False)
    
    #Set x-limits and x-ticks
    #Seems like things dry up after 102 periods, so stick to this spacing
    ax[plotPlayers.index(player)].set_xlim(0, 108)    
    ax[plotPlayers.index(player)].set_xticks(np.linspace(0, 108, int((108) / 4)+1))
    
    #Set xtick labels with dates if final axis
    if plotPlayers.index(player) == len(plotPlayers)-1:
        xLabels = []
        for setTime in hourlyList[0:108+4][::4]:
            xLabels.append(setTime.month_name()[0:3]+'. '+str(setTime.day))
        ax[plotPlayers.index(player)].set_xticklabels(xLabels, rotation = 45,
                                                      va = 'top', ha = 'right')
    else:
        ax[plotPlayers.index(player)].set_xticklabels([])
        
    #Add ellipse for player image
    #Set circle height relative to y-axis
    relCircleDiameter = 0.7
    #Add ellipse using data ratio to make circular
    #Add one with no edge and filled that sits behind player
    ax[plotPlayers.index(player)].add_artist(Ellipse((0.95,0.55),
                                                     relCircleDiameter * ax[plotPlayers.index(player)].get_data_ratio()*100/2,
                                                     relCircleDiameter,
                                                     ec = None, lw = 0,
                                                     fc = '#fffaf0',
                                                     transform = ax[plotPlayers.index(player)].transAxes,
                                                     zorder = 5,
                                                     clip_on = False))
    #Add one with edge and no fill that sits above player
    ax[plotPlayers.index(player)].add_artist(Ellipse((0.95,0.55),
                                                     relCircleDiameter * ax[plotPlayers.index(player)].get_data_ratio()*100/2,
                                                     relCircleDiameter,
                                                     ec = plotColours[plotPlayers.index(player)], lw = 2,
                                                     fc = 'none',
                                                     transform = ax[plotPlayers.index(player)].transAxes,
                                                     zorder = 7,
                                                     clip_on = False))
    
    
    #Add player image
    #Load image
    playerImg = plt.imread(f'images\\{player}.png')
    #Figure out zoom factor
    #Target height took a bit of experimentation
    zoomFac = 80 / playerImg.shape[1]
    #Create offset image
    imOffset = OffsetImage(playerImg, zoom = zoomFac)
    #Create annotation box
    annBox = AnnotationBbox(imOffset, (0.95,0.55),
                            #xybox = (0, 0),
                            frameon = False,
                            #box_alignment = (1,1),
                            xycoords = ax[plotPlayers.index(player)].transAxes,
                            #boxcoords = 'offset points',
                            pad = 0)
    annBox.zorder = 6
    #Add the image
    ax[plotPlayers.index(player)].add_artist(annBox)
    
    #Set axes face colour
    ax[plotPlayers.index(player)].set_facecolor('#fffaf0')
    
#Set figure colouring
fig.patch.set_facecolor('#fffaf0')
    
#Add figure title using text
fig.text(0.05, 0.98, 'Relative mentions (%) on Twitter of key players across the SSN signings period',
         fontsize = 12, fontweight = 'bold', ha = 'left', va = 'top')
fig.text(0.05, 0.95, 'Includes tweets that used the #SSNTrade or #SSNSignings hashtags',
         fontsize = 8, fontweight = 'normal', ha = 'left', va = 'top')
fig.text(0.05, 0.93, 'Data split into 6-hourly time periods. Time periods with less than 25 tweets excluded from calculations',
         fontsize = 8, fontweight = 'normal', ha = 'left', va = 'top')

#Add some custom annotations around peaks

#Garbin
#Announced leaving Swifts on Sep. 13
#Find x-index of start of September 13th
ptInd = np.where([currTime == pd.Timestamp(datetime(2021, 9, 13, 0)) for currTime in hourlyList])[0][0]
#Add lollipop style graphic at point
ax[plotPlayers.index('Garbin')].plot([ptInd,ptInd],
                                     [ax[plotPlayers.index('Garbin')].get_ylim()[0],0.25],
                                     lw = 1, ls = '-',
                                     c = 'darkgrey',
                                     zorder = 4)
ax[plotPlayers.index('Garbin')].scatter(ptInd,0.25,
                                        s = 10, c = 'darkgrey', zorder = 4)
#Add text annotation
ax[plotPlayers.index('Garbin')].text(ptInd-1, 0.25,
                                     'Garbin leaving Swifts',
                                     fontsize = 6, fontweight = 'normal', style = 'italic',
                                     va = 'center', ha = 'right',
                                     c = 'darkgrey')
#Signs with Magpies Sep. 17
#Find x-index of start of September 17th
ptInd = np.where([currTime == pd.Timestamp(datetime(2021, 9, 17, 0)) for currTime in hourlyList])[0][0]
#Add lollipop style graphic at point
ax[plotPlayers.index('Garbin')].plot([ptInd,ptInd],
                                     [ax[plotPlayers.index('Garbin')].get_ylim()[0],0.27],
                                     lw = 1, ls = '-',
                                     c = 'darkgrey',
                                     zorder = 4)
ax[plotPlayers.index('Garbin')].scatter(ptInd,0.27,
                                        s = 10, c = 'darkgrey', zorder = 4)
#Add text annotation
ax[plotPlayers.index('Garbin')].text(ptInd+1, 0.27,
                                     'Garbin signs with Magpies',
                                     fontsize = 6, fontweight = 'normal', style = 'italic',
                                     va = 'center', ha = 'left',
                                     c = 'darkgrey')

#Austin
#Signs with Vixens Sep 21
#Find x-index of start of September 21st
ptInd = np.where([currTime == pd.Timestamp(datetime(2021, 9, 21, 0)) for currTime in hourlyList])[0][0]
#Add lollipop style graphic at point
ax[plotPlayers.index('Austin')].plot([ptInd,ptInd],
                                     [ax[plotPlayers.index('Austin')].get_ylim()[0],0.25],
                                     lw = 1, ls = '-',
                                     c = 'darkgrey',
                                     zorder = 4)
ax[plotPlayers.index('Austin')].scatter(ptInd,0.25,
                                        s = 10, c = 'darkgrey', zorder = 4)
#Add text annotation
ax[plotPlayers.index('Austin')].text(ptInd-1, 0.25,
                                     'Austin signs with Vixens',
                                     fontsize = 6, fontweight = 'normal', style = 'italic',
                                     va = 'center', ha = 'right',
                                     c = 'darkgrey')

#Dwan
#Announced leaving Firebirds on Sep. 18
#Find x-index of start of September 18th
ptInd = np.where([currTime == pd.Timestamp(datetime(2021, 9, 18, 0)) for currTime in hourlyList])[0][0]
#Add lollipop style graphic at point
ax[plotPlayers.index('Dwan')].plot([ptInd,ptInd],
                                     [ax[plotPlayers.index('Dwan')].get_ylim()[0],0.25],
                                     lw = 1, ls = '-',
                                     c = 'darkgrey',
                                     zorder = 4)
ax[plotPlayers.index('Dwan')].scatter(ptInd,0.25,
                                        s = 10, c = 'darkgrey', zorder = 4)
#Add text annotation
ax[plotPlayers.index('Dwan')].text(ptInd-1, 0.25,
                                     'Dwan leaving Firebirds',
                                     fontsize = 6, fontweight = 'normal', style = 'italic',
                                     va = 'center', ha = 'right',
                                     c = 'darkgrey')
#Signs with Thunderbirds Sep. 23
#Find x-index of start of September 23rd
ptInd = np.where([currTime == pd.Timestamp(datetime(2021, 9, 23, 0)) for currTime in hourlyList])[0][0]
#Add lollipop style graphic at point
ax[plotPlayers.index('Dwan')].plot([ptInd,ptInd],
                                     [ax[plotPlayers.index('Dwan')].get_ylim()[0],0.15],
                                     lw = 1, ls = '-',
                                     c = 'darkgrey',
                                     zorder = 4)
ax[plotPlayers.index('Dwan')].scatter(ptInd,0.15,
                                        s = 10, c = 'darkgrey', zorder = 4)
#Add text annotation
ax[plotPlayers.index('Dwan')].text(ptInd+1, 0.15,
                                     'Dwan signs with Thunderbirds',
                                     fontsize = 6, fontweight = 'normal', style = 'italic',
                                     va = 'center', ha = 'left',
                                     c = 'darkgrey')

#Dehaney
#Signs with Lightning Sep 24
#Find x-index of start of September 24th
ptInd = np.where([currTime == pd.Timestamp(datetime(2021, 9, 24, 0)) for currTime in hourlyList])[0][0]
#Add lollipop style graphic at point
ax[plotPlayers.index('Dehaney')].plot([ptInd,ptInd],
                                     [ax[plotPlayers.index('Dehaney')].get_ylim()[0],0.25],
                                     lw = 1, ls = '-',
                                     c = 'darkgrey',
                                     zorder = 4)
ax[plotPlayers.index('Dehaney')].scatter(ptInd,0.25,
                                        s = 10, c = 'darkgrey', zorder = 4)
#Add text annotation
ax[plotPlayers.index('Dehaney')].text(ptInd-1, 0.25,
                                     'Dehaney signs with Lightning',
                                     fontsize = 6, fontweight = 'normal', style = 'italic',
                                     va = 'center', ha = 'right',
                                     c = 'darkgrey')
    
#Save figure
plt.savefig('vol3_example.png', format = 'png', 
            facecolor = fig.get_facecolor(), edgecolor = 'none',
            dpi = 300)
    
#Close figure
# plt.close()

# %% ---- End of vol3_example.py -----