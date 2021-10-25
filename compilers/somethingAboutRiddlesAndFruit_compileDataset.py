# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 20:02:50 2021

@author:
    Aaron Fox
    Centre for Sport Research
    Deakin University
    aaron.f@deakin.edu.au
    
    Script uses a Python 3.8 environment that houses the snscrape package among others
    
"""

# %% Import packages

import os
import snscrape
import pandas as pd
from datetime import datetime
from dateutil import parser

# %% Get hashtag tweets

#Get tweets using SSNTrade and SSNSignings hashtags
#Requires using OS library to call CLI commands in Python
#Use dates of the signing period: September 6th - October 8th
os.system("snscrape --jsonl --since 2021-09-06 twitter-search \"(#SSNTrade OR #SSNSignings) until:2021-10-9\" > tweets.json")

#Convert collected tweets to dataframe
df_genTweets = pd.read_json('tweets.json', lines = True)

#Move the .json version to the data folder
os.rename('tweets.json','..\\Datasets\\vol3\\somethingAboutRiddlesAndFruit.json')

#Create a new column that takes user from the url
userName = []
for user in df_genTweets['url']:
    userName.append(user.split('https://twitter.com/')[-1].split('/')[0])
df_genTweets['username'] = userName
    
#Drop unwanted columns
df_cleanTweets = df_genTweets.drop(labels = ['_type','user','source','sourceUrl','sourceLabel',
                                              'tcooutlinks','media','inReplyToTweetId',
                                              'inReplyToUser', 'mentionedUsers', 'coordinates',
                                              'place', 'cashtags', 'retweetedTweet', 'quotedTweet'],
                                   axis = 1)

#Export to csv
df_cleanTweets.to_csv('..\\Datasets\\vol3\\somethingAboutRiddlesAndFruit.csv',
                      encoding = 'utf-8-sig', index = False)

# %% Get team account tweets

#Set team accounts dictionary
teamDict = {'Fever': 'WestCoastFever',
            'Firebirds': 'FirebirdsQld',
            'GIANTS': 'GIANTS_Netball',
            'Lightning': 'sc_lightning',
            'Magpies': 'collingwoodsn',
            'Swifts' : 'NSWSwifts',
            'Thunderbirds': 'AdelaideTBirds',
            'Vixens': 'MelbourneVixens'}

#Set list to store each teams tweets in
teamTweets = []

#Get tweets using team accounts
#Requires using OS library to call CLI commands in Python
#Use dates of the signing period: September 6th - October 8th
for team in list(teamDict.keys()):
    
    #Get team account
    account = teamDict[team]
    
    #Scrape tweets    
    os.system(f"snscrape --jsonl --since 2021-09-06 twitter-user \"{account}\" > tweets.json")
    
    #Convert to dataframe
    tweetData = pd.read_json('tweets.json', lines = True)
    
    #Create a datetime version of the date column
    tweetData['date'] = tweetData['date'].astype(str)
    tweetData['date'] = [pd.Timestamp(parser.parse(longDate)).tz_convert('Australia/Sydney') for longDate in list(tweetData['date'])]
    
    #Drop those outside of end date range
    tweetData = tweetData[(tweetData['date'] < pd.Timestamp(datetime(2021, 10, 9, 0)).tz_localize('Australia/Sydney'))]
    
    #Append to list
    teamTweets.append(tweetData)
               
    #Remove .json file
    os.remove('tweets.json')

#Flatten the team tweets into one dataframe
df_teamTweets = pd.concat(teamTweets).reset_index(drop = True)

#Create a new column that takes user from the url
userName = []
for user in df_teamTweets['url']:
    userName.append(user.split('https://twitter.com/')[-1].split('/')[0])
df_teamTweets['username'] = userName
    
#Drop unwanted columns
df_teamTweets = df_teamTweets.drop(labels = ['_type','user','source','sourceUrl','sourceLabel',
                                             'tcooutlinks','media','inReplyToTweetId',
                                             'inReplyToUser', 'mentionedUsers', 'coordinates',
                                             'place', 'cashtags', 'retweetedTweet', 'quotedTweet'],
                                   axis = 1)

#Export to .json
df_teamTweets.to_json('..\\datasets\\vol3\\somethingAboutRiddlesAndFruit_teamTweets.json')

#Export to csv
df_teamTweets.to_csv('..\\datasets\\vol3\\somethingAboutRiddlesAndFruit_teamTweets.csv',
                     encoding = 'utf-8-sig', index = False)

# %% ----- End of somethingAboutRiddlesAndFruit_compileDataset.py -----