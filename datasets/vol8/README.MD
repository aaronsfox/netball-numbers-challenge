# The Games

This volumes dataset focuses on statistics from the recent 2022 Commonwealth Games tournament. Team and player statistics from all pool and placement (inc. semi-finals and medal matches) matches are included in the dataset. There are three files which relate to player statistics from each match, team statistics from each match (by quarter), and cumulative team statistics across the quarters played (see 'Datasets' below).

There are a number of different questions you might consider and be able to answer with these data:

- Which teams or players led the games in various statistical categories?
- Were certain match-ups more or less favourable from a statistical perspective?
- Was there a difference statistically between pool and placement matches?
- Did certain teams possess a specific statistical style?

As is the general goal with this challenge, the idea of working with this dataset is to produce some new informative knowledge through data and/or statistical analyses, or produce a neat data visualisation to communicate your findings — so good luck! 

### Get the Data

The dataset — 'theGames_playerData.csv', 'theGames_teamData.csv' or 'theGames_teamDataCumulative.csv' — can be viewed online by clicking the link above. To download the data, you can [clone this repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository) or directly download the file by:
- Clicking the link above to view the dataset
- Right click on the 'Raw' button and 'Save link as...'
- Save the file wherever you like. It may be necessary to change the file extension from '.txt' to '.csv' for easier use

### Datasets

#### `theGames_playerData.csv`

The `theGames_playerData.csv` file contains a complete list of player statistics from all games during the 2022 Commonwealth Games. Within the dataset, each row of data corresponds to one individual player during a match. The following table describes the variables included in the dataset:

|Variable         |Data Type |Description |
|:----------------|:---------|:-----------|
|matchNo	|numeric	| Unique match number ID. These are mostly in order from the competition.	|
|team           |factor   | The team of the player |
|opponent             |factor    | The opposition team for the given match |
|matchType |factor | The specification for the match (i.e. Pool, Classification, Semi Final, Medal) |
|surname              |string   | Surname of the player |
|givenNames             |string   | Given name(s) of the player |
|courtPosition_Q1             |factor    | Court position (abbreviated) for the player during the first quarter, including interchange (i.e. I) |
|courtPosition_Q2 |factor | Court position (abbreviated) for the player during the second quarter, including interchange (i.e. I) |
|courtPosition_Q3 |factor | Court position (abbreviated) for the player during the third quarter, including interchange (i.e. I) |
|courtPosition_Q4 |factor | Court position (abbreviated) for the player during the fourth quarter, including interchange (i.e. I) |
|minutesPlayed |numeric | Minutes played during the match by player |
| goalsScored          | numeric   | Goals scored during the match by player                      |
| goalsAttempted       | numeric   | Total goals attempted during the match by player             |
| goalsMissed          | numeric   | Goal attempts missed during the match by player              |
| shootingPer          | numeric   | Shooting percentage (i.e. goalsScore / goalsAttempted) of player during the match |
| goalAssists          | numeric   | Total goal assists by the player during the match            |
| feeds                | numeric   | Total feeds into the shooting circle by player during the match |
| centrePassReceives   | numeric   | Total centre pass receives by player during the match        |
| gains                | numeric   | Total number of gains from opposition by the player during the match |
| intercepts           | numeric   | Total number of interceptions by the player during the match |
| deflections          | numeric   | Total number of defensive deflections by the player during the match |
| attackingRebounds    | numeric   | Total number of rebounds off own teams shots during the match by the player |
| defensiveRebounds    | numeric   | Total number of rebounds off opponents shots during the match by the player |
| totalRebounds        | numeric   | Total number of rebounds during the match by the player      |
| pickups              | numeric   | Total number of loose ball pickups by the player during the match |
| contactPenalties     | numeric   | Total number of contact penalties called on the player during the match |
| obstructionPenalties | numeric   | Total number of obstruction penalties called on the player during the match |
| totalPenalties       | numeric   | Total number of penalties (contact + obstruction) called on the player during the match |
| offsides             | numeric   | Total number of offside errors by player                     |
| badHands             | numeric   | Total number of errors relating to bad handling by player    |
| footwork             | numeric   | Total number of footwork errors by player                    |
| otherErrors          | numeric   | Total number of errors not specified in above categories by player |
| totalErrors          | numeric   | Total number of errors across all categories by player       |

#### `theGames_teamData.csv`

The `theGames_teamData.csv` file contains a complete list of team statistics split by quarter from all games during the 2022 Commonwealth Games. Within the dataset, each row of data corresponds to one team during a quarter of the match. The following table describes the variables included in the dataset:

| Variable             | Data Type | Description                                                  |
| :------------------- | :-------- | :----------------------------------------------------------- |
| matchNo              | numeric   | Unique match number ID. These are mostly in order from the competition. |
| team                 | factor    | The team of the player                                       |
| opponent             | factor    | The opposition team for the given match                      |
| matchType            | factor    | The specification for the match (i.e. Pool, Classification, Semi Final, Medal) |
| quarter              | factor    | Quarter of the match the statistics are from                 |
| goalsScored          | numeric   | Goals scored during the quarter by the team                  |
| intercepts           | numeric   | Total number of interceptions by the team during the quarter |
| deflections          | numeric   | Total number of defensive deflections by the team during the quarter |
| contactPenalties     | numeric   | Total number of contact penalties called on the team during the quarter |
| obstructionPenalties | numeric   | Total number of obstruction penalties called on the team during the quarter |
| totalPenalties       | numeric   | Total number of penalties (contact + obstruction) called on the team during the match |
| totalErrors          | numeric   | Total number of errors by the team during the quarter        |
| timeInPossessionSecs | numeric   | Total time the team had possession of the ball (in seconds) during the quarter |

#### `theGames_teamDataCumulative.csv`

The `theGames_teamDataCumulative.csv` dataset was developed from the above-mentioned team data. The variables contained in the dataset are the same as those outlined in the above table, but are a cumulative sum across the quarters played in the tournament by the respective teams. An additional variable of 'quartersPlayed' is therefore in this dataset to indicate the progression of the teams through the tournament as the statistics are summed.
