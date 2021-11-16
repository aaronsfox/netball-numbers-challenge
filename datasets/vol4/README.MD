# Have You Seen Colin?

This volumes dataset looks at one of the most prominent features of Suncorp Super Netball over recent years — Colin Jenkins. These data (meticulously hand collected by [Libbi Bennett](https://twitter.com/BennettLibbi)) collate the number of Colin 'sightings' over Super Netball's 2021 season, and includes additional details such as the game day, result, and whether the match was viewed live or as a replay.

As is the general goal with this program, the idea of working with this dataset is to produce some new informative knowledge through data and/or statistical analyses, or produce a neat data visualisation to communicate your findings. This dataset is perhaps a little more tongue-in-cheek than previous volumes, but still provides some opportunities to test your data manipulation and visualisation skills. 

### Get the Data

The dataset — 'haveYouSeenColin.csv' — can be viewed online by clicking the link above. To download the data, you can [clone this repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository) or directly download the file by:
- Clicking the link above to view the dataset
- Right click on the 'Raw' button and 'Save link as...'
- Save the file wherever you like. It may be necessary to change the file extension from '.txt' to '.csv' for easier use

### Data Dictionary

## `haveYouSeenColin.csv`

The `haveYouSeenColin.csv` file contains the Colin 'sighting' over the 2021 Super Netball Season alongside some supplementary info.

|Variable         |Data Type |Description |
|:----------------|:---------|:-----------|
|round             |numeric    | Round number for the match |
|teamA           |string   | Home team for the match |
|teamB              |string   | Away team for the match |
|scoreA             |numeric   | Final score of the home team for the match |
|scoreB             |numeric   | Final score of the away team for the match |
|gameDay               |string   | Day of the week the match was played |
|colinSightings               |numeric   | Number of Colin 'sightings' throughout the match |
|format            |string   | String of 'live' vs. 'replay' for how the match was viewed |
