# In The Zone

This volumes dataset focuses on shooting data from Super Netball since 2018 through to round 6 of 2022. Every shot taken across this period, who it was taken by, the zone it was taken from, and the shot result have been included in this dataset.

There are a number of different questions you might consider and be able to answer with these data:

- Who or which team has taken the most shots during this time overall and from different shooting zones?
- Who or which team is the most efficient from the various shooting zones?
- Where are the different teams and players taking their shots from?
- Have shooting strategies changed over the years?
- Does the quarter or time in the quarter influence where players are taking their shots from?
- Are players better or worse shooters during regular season versus finals matches?

As is the general goal with this challenge, the idea of working with this dataset is to produce some new informative knowledge through data and/or statistical analyses, or produce a neat data visualisation to communicate your findings — so good luck! 

### Get the Data

The dataset — 'inTheZone.csv' or 'inTheZone.xlsx' — can be viewed online by clicking the link above. To download the data, you can [clone this repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository) or directly download the file by:
- Clicking the link above to view the dataset
- Right click on the 'Raw' button and 'Save link as...'
- Save the file wherever you like. It may be necessary to change the file extension from '.txt' to '.csv' for easier use

### Data Dictionary

## `inTheZone.csv` & `inTheZone.xlsx`

The `inTheZone.csv` and `inTheZone.xlsx` files contains a complete list of all recorded shots in Super Netball matches from 2018 through to round 6 of the 2022 season. Within the dataset, each row of data corresponds to one individual shot by a player during a match.

The files are identical, but simply provided in different file extension formats. Both are easily accessible and openable in Microsoft Excel and other file reader applications.  The following table describes the variables included in the dataset.

|Variable         |Data Type |Description |
|:----------------|:---------|:-----------|
|matchId	|numeric	| Unique Champion Data identifier for match	|
|year           |numeric   | Year of season for match                                     |
|matchType             |string    | Indicator of whether match was a 'regular' season match or 'final'                                    |
|squadName |string | Team of the player for the match |
|playerId              |numeric   | A unique ID number allocated to the player. This is the most reliable indicator of an individual player, as names may change over time (e.g. Tippett to Bueta) |
|playerName             |string   | Name of the player in initial.last format (e.g. A.Player) |
|shotLocation             |string    | Indicator for where the shot was taken from **(see table below)**                              |
|roundNo             |numeric    | Round of season/finals series for match                                    |
|gameNo             |numeric    | Game number for the relevant round                                    |
|period           |numeric   | Quarter of the match (i.e. 1 through 4) when the shot was taken                                     |
|periodSeconds           |numeric   | Time (in seconds) into the quarter when shot was taken (i.e. 0 = start of quarter; 900 = 15 mins into quarter)                                     |
|scoreName           |string   | Indicator of shot result being a 'goal', 'miss', '2pt Goal' or '2pt Miss'                                     |
|scoreValue               |numeric   | Total goals value for the shot (i.e. 0, 1 or 2)                                     |
|shotResult               |string   | Basic outcome for the shot of 'successful' or 'unsuccessful'                                        |

The below table provides more detailed descriptions for the shooting zone locations present in the data under the `shotLocation` variable. Note that all descriptions for position (i.e. left, middle, right) are relative to if you were **standing at the top of the shooting circle facing the goal post**.

|Shot Location	|Description |
|:--------------|:-----------|
|left-short		| Taken in the approximate left third wedge of the shooting circle from < ~3m distance |
|middle-short		| Taken in the approximate middle third wedge of the shooting circle from < ~3m distance	|
|right-short		| Taken in the approximate right third wedge of the shooting circle from < ~3m distance	|
|left-long		| Taken in the approximate left third wedge of the shooting circle from > ~3m distance |
|middle-long		| Taken in the approximate middle third wedge of the shooting circle from > ~3m distance	|
|right-long		| Taken in the approximate right third wedge of the shooting circle from > ~3m distance	|
|left-baseline-short		| Taken from close to the baseline to the left of the goal post from < ~3m distance	|
|right-baseline-short		| Taken from close to the baseline to the right of the goal post from < ~3m distance	|
|left-baseline-long		| Taken from close to the baseline to the left of the goal post from > ~3m distance	|
|right-baseline-long		| Taken from close to the baseline to the right of the goal post from > ~3m distance	|
