# Results from the Time Machine

Take a step back in time and review the end of season results from past seasons of the ANZ Championship and Suncorp Super Netball. This volumes dataset contains the end of season ladder data from each team in these competitions across the years. The dataset is fairly general in nature, so offers up a range of opportunities to investigate general factors related to competition performance over time — so do whatever you feel is appropriate!

As is the general goal with this program, the idea of working with this dataset is to produce some new informative knowledge through data and/or statistical analyses, or produce a neat data visualisation to communicate your findings.

### Get the Data

The dataset — 'resultsFromTheTimeMachine.csv' — can be viewed online by clicking the link above. To download the data, you can [clone this repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository) or directly download the file by:
- Clicking the link above to view the dataset
- Right click on the 'Raw' button and 'Save link as...'
- Save the file wherever you like. It may be necessary to change the file extension from '.txt' to '.csv' for easier use

### Data Dictionary

## `resultsFromTheTimeMachine.csv`

|Variable         |Data Type |Description |
|:----------------|:---------|:-----------|
|team             |string    | Name of team |
|played           |numeric   | Number of games played in regular season |
|win              |numeric   | Number of games won in regular season |
|draw             |numeric   | Number of drawn games in regular season |
|loss             |numeric   | Number of games lost in regular season |
|GF               |numeric   | Number of goals for in regular season |
|GA               |numeric   | Number of goals against in regular season |
|Gdiff            |numeric   | Goal difference in regular season |
|Gper             |numeric   | Calculated percentage from the regular season |
|pts              |numeric   | Total ladder points earned in the regular season |
|bonusPts         |numeric   | Bonus ladder points earned in the regular season (for applicable seasons) |
|finalsWin        |numeric   | Number of finals won for the year |
|finalsLoss       |numeric   | Number of finals lost for the year |
|year             |numeric   | Year of the season |
|coach            |string    | Coach for the team during the season<sup>a</sup> |
|minorPremiership |string    | Yes/No for whether team won minor premiership |
|premiership      |string    | Yes/No for whether team won premiership |
|runnerUp         |string    | Yes/No for whether team was runner-up for grand final |
|competition      |string    | ANZC or SSN to indicate ANZ Championship or Suncorp Super Netball |

<sup>a</sup> Michelle den Dekker listed as coach for 2016 Thunderbirds season despite only coaching the first 5 rounds. Debbie Fuller listed as coach for Mystics in 2011, but was replaced for 2 games during the season. Janine Southby listed as coach for Steel in 2012, but this role was shared with Natalie Avellino.