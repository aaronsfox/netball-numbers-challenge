# Who Do You Play For?

This volumes dataset focuses on the various players who have taken the court across the ANZ Championship and Super Netball — who they are, what rounds and year they played in, for which team, and how many minutes they played. 

There are a number of different questions you might consider and be able to answer with these data:

- Who has played the most games total or across the various teams? 
- Who has played for the most teams?
- What pairs or trios of players have played the most games together?
- What is the most common name or set of initials across the ANZ Championship and/or Super Netball?
- Who has played the most minutes across the years of the ANZ Championship and/or Super Netball?

As is the general goal with this challenge, the idea of working with this dataset is to produce some new informative knowledge through data and/or statistical analyses, or produce a neat data visualisation to communicate your findings — so good luck! 

### Get the Data

The dataset — 'whoDoYouPlayFor.csv' or 'whoDoYouPlayFor.xlsx' — can be viewed online by clicking the link above. To download the data, you can [clone this repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository) or directly download the file by:
- Clicking the link above to view the dataset
- Right click on the 'Raw' button and 'Save link as...'
- Save the file wherever you like. It may be necessary to change the file extension from '.txt' to '.csv' for easier use

### Data Dictionary

## `whoDoYouPlayFor.csv` & `whoDoYouPlayFor.xlsx`

The `whoDoYouPlayFor.csv` and `whoDoYouPlayFor.xlsx` files contains a complete list of the players who have been on-court during every match of the ANZ Championship and Super Netball. Note that I specifically mention **on-court** as the dataset only includes players that played in the match, rather than all the players listed for the match (i.e. if the player played zero minutes they are not included for that round). Within the dataset, each row of data corresponds to one individual match that the player has played in.

The files are identical, but simply provided in different file extension formats. Both are easily accessible and openable in Microsoft Excel and other file reader applications.  The following table describes the variables included in the dataset.

|Variable         |Data Type |Description |
|:----------------|:---------|:-----------|
|matchId	|numeric	| Unique Champion Data identifier for match	|
|round             |numeric    | Round of season/finals series for match                                    |
|matchType             |string    | Indicator of whether match was a 'Regular' season match or 'Final'                                    |
|year           |numeric   | Year of season for match                                     |
|competition           |string   | Indicator of whether match was from ANZ Championship (ANZC) or Super Netball (SSN)                                     |
|playerId              |numeric   | A unique ID number allocated to the player. This is the most reliable indicator of an individual player, as names may change over time (e.g. Tippett to Bueta) |
|displayName             |string   | Display name of the player in initial.last name format (e.g. A.Player) |
|firstName               |string   | First name of the player                                     |
|surname               |string   | Surname of the player                                        |
|minutesPlayed            |numeric   | Total number of minutes player spent on court during the match |
|squadName |string | Team of the player for the match |