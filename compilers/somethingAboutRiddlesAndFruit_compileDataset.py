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

# %% Test

# Using OS library to call CLI commands in Python
#6th September = starting date of signing period
#8th October = when all players need to be signed
os.system("snscrape --jsonl --max-results 500 --since 2021-09-06 twitter-search \"(#SSNTrade OR #SSNSignings) until:2021-10-9\" > tweets.json")

#Reads the json generated from the CLI commands above and creates a pandas dataframe
df_tweets = pd.read_json('tweets.json', lines = True)

### TODO: clean-up, remove max results, run at appropriate time

### TODO: can probably delete .json after exporting into .csv

### Example analysis:
    # - most likes/retweets for teams/non-team accounts
    # - most mentioned player, cross check last names with squad list
    # - most mentioned words
    # - top 5 most liked tweets