# The 12 Super Netballers of Christmas

This volumes dataset takes player stats from every regular season game of Super Netball from 2017 through 2021 from the Champion Data match centre. 

Christmas is coming! I've tried my best to think of a Christmas themed challenge — and come up with very little! In general, this challenge has provided a dataset with very little instruction as to what to do with it. For this volume though, there is a **<u>specific challenge</u>** — pick your **<u>12 Super Netballers of Christmas</u>** from across all years of the Super Netball competition. There's a couple of different ways you could go about this:

- Pick a specific 12-player squad designed to play as a team with a starting 7 and bench
- Pick the 'best' 12-players you can from across the competition irrespective of playing position

To make this interesting, each players years should be considered in isolation. For example, if you want Liz Watson in your 12 — you need to pick the year you want from her based on the data (or your opinion). Importantly, you can only take one 'version' of a player (i.e. you can't have a shooting circle of Fowler from 2020 combined with Fowler from 2021!). 

Put your 12 Super Netballers of Christmas together by either:

- Inspecting the data and creating your best group
- Pick your group based on opinion and present the data on your group
- Simply pick your group based on opinion and intuition

For those who want to keep it simple, post your 12 players on Twitter using the `#NetballNumbers` hashtag and tell us why you picked them. For those who wish to present the data that supports their 12 players — think of a creative way to visualise it and post using the `#NetballNumbers` hashtag. And given it's a Christmas challenge, perhaps try using some festive colours!

### Get the Data

The dataset — 'superNetballersOfChristmas.csv' or 'superNetballersOfChristmas.xlsx' — can be viewed online by clicking the link above. To download the data, you can [clone this repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository) or directly download the file by:
- Clicking the link above to view the dataset
- Right click on the 'Raw' button and 'Save link as...'
- Save the file wherever you like. It may be necessary to change the file extension from '.txt' to '.csv' for easier use

### Data Dictionary

## `superNetballersOfChristmas.csv` & `superNetballersOfChristmas.xlsx`

The `superNetballersOfChristmas.csv` and `superNetballersOfChristmas.xlsx` files contain the player stats data from regular season Super Netball matches from 2017 through 2021. The files are identical, but simply provided in different file extension formats. Both are easily accessible and openable in Microsoft Excel and other file reader applications. 

Across competition years there are some slight differences in how Champion Data collated statistics. Variables in ***bold-italics*** in the table below are those that vary across years.

|Variable         |Data Type |Description |
|:----------------|:---------|:-----------|
|playerName             |string    | Display name of the player in initial-last name format (e.g. A.Player) |
|squadName           |string   | Squad nickname for the players team |
|year              |numeric   | Year of season for match |
|round             |numeric   | Round of season for match |
|startingPosition             |string   | Starting court position for player. Bench indicated by '-' |
|minutesPlayed               |numeric   | Minutes on court during match (*NB: full match seems to be recorded as 61 mins*) |
|squadID               |numeric   | Numeric squad ID for players team |
|playerID            |numeric   | Numeric ID for the player. Useful for players with name changes (e.g. Tippett to Bueta) |
|centrePassReceives |numeric | Total number of centre pass receives by player in match |
|feeds |numeric | Total number of circle feeds by player in match |
|***feedsWithAttempt*** |***numeric*** | ***Total number of circle feeds with a shot attempt by player in match (2018 onwards)*** |
|***deflections*** |***numeric*** | ***Total number of deflections by player in match (2017 only)*** |
|***deflectionWithGain*** |***numeric*** | ***Total number of deflections with a gain by player in match (2018 onwards)*** |
|***deflectionWithNoGain*** |***numeric*** | ***Total number of deflections with no gain by player in match (2018 onwards)*** |
|gain |numeric | Total number of gains by player in match |
|goalAssists |numeric | Total number of goal assists by player in match |
|goalAttempts |numeric | Total number of goal attempts by player in match |
|goalMisses |numeric | Total number of missed goal attempts by player in match |
|goals |numeric | Total number of made goals by player in match (*NB: this doesn't appear to allocate 2 goals for Super Shots*) |
|***turnovers*** |***numeric*** | ***Total number of turnovers by player in match (2017 only)*** |
|***generalPlayTurnovers*** |***numeric*** | ***Total number of turnovers by player in match (2018 onwards version of 'turnovers')*** |
|intercepts |numeric | Total number of intercepts by player in match |
|obstructionPenalties |numeric | Total number of obstruction penalties by player in match |
|offsides |numeric | Total number of offside penalties by player in match |
|contactPenalties |numeric | Total number of contact penalties by player in match |
|penalties |numeric | Total number of all penalties by player in match |
|***netPoints*** |***numeric*** | ***Total number of Nissan Netpoints accumulated by player in match (2018 onwards)*** |
|rebounds |numeric | Total number of rebounds by player in match |
