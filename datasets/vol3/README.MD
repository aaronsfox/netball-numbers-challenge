# Something About Riddles and Fruit

This volumes dataset is a collection of Tweets scraped from the #SSNTrade and #SSNSignings hastags from across the SSN signing period (i.e. September 6th - October 8th). There are two versions of this dataset, a .json and .csv version. The .json file is more extensive, as this comes directly from the Python `snscrape` module and contains a few more columns of data - and may be more easily readable if experienced with this type of file. Note though that the .json file has multiple lines of content for each tweet, which can cause some error with basic loading approaches. Here is an except of Python code that imports the tweets in the .json file:

```
tweets = []
for line in open('somethingAboutRiddlesAndFruit.json', 'r'):
    tweets.append(json.loads(line))
```

The .csv is a more generally readable file but contains a smaller amount of columns (see Data Dictionary below). 

As is the general goal with this program, the idea of working with this dataset is to produce some new informative knowledge through data and/or statistical analyses, or produce a neat data visualisation to communicate your findings. This is a slightly different dataset to existing volumes, and opens up opportunities for both quantitative (e.g. like/reply/retweet counts) and qualitative (e.g. common terms, phrases) analyses.

### Get the Data

The dataset — 'somethingAboutRiddlesAndFruit.csv' — can be viewed online by clicking the link above. To download the data, you can [clone this repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository) or directly download the file by:
- Clicking the link above to view the dataset
- Right click on the 'Raw' button and 'Save link as...'
- Save the file wherever you like. It may be necessary to change the file extension from '.txt' to '.csv' for easier use

### Data Dictionary

## `somethingAboutRiddlesAndFruit.csv`

|Variable         |Data Type |Description |
|:----------------|:---------|:-----------|
|url             |string    | URL link to tweet |
|date           |dateTime   | Date and timestamp of tweet (likely in local Tweeters time) |
|content              |string   | Content of the tweet |
|renderedContent             |string   | Content of the tweet - but perhaps includes some additional rendered elements (e.g. icons) |
|id             |numeric   | Unique ID number of tweet |
|replyCount               |numeric   | Number of replies to tweet (as of October 25th) |
|retweetCount               |numeric   | Number of general retweets of tweet (as of October 25th)     |
|likeCount            |numeric   | Number of likes for tweet (as of October 25th)               |
|quoteCount             |numeric   | Number of quotes of tweet (as of October 25th)               |
|conversationID              |numeric   | Unique ID number of conversation (seems to be the same as 'id') |
|lang |string | Listed language of tweet (e.g. 'en' = English) |
|outlinks |list | List of weblinks included in tweet |
|hashtags |list | List of hashtags used in tweet |
|username |string | Username of tweeter (note this does not include the @ symbol at beginning) |
