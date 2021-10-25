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
import matplotlib.pyplot as plt

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

# %% ----- End of somethingAboutRiddlesAndFruit_compileDataset.py -----