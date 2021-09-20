# Ask and You Shall Receive

This dataset was part of a notational analysis of the 2018 Suncorp Super Netball season led by [Lyndell Bruce](https://twitter.com/LyndellBruce). This dataset contains patterns of play for each team across the season around centre pass receptions and second phase. Each row in the dataset corresponds to single play, where the playing position and court location for the centre pass reception and second phase are listed. Additional characteristics of the round, match number and quarter number are also included for each data point. Note that not every data point has a second phase entry, as the play may not have reached this point. For playing position, sometimes this could not be determined and hence has been labelled as 'UNKNOWN'. The XY coordinates for the court location are defined as per the following axes:

![](C:\+GitRepos+\netball-numbers-challenge\datasets\vol2\images\courtAxes.png)

For example, the centre circle would be at the XY coordinate of 50,100, and the third lines along Y coordinates of approximately 67 and 133. All data is oriented so that the top or north end of the court (i.e. higher Y coordinates) is the attacking direction, while the bottom or south end of the court (i.e. lower Y coordinates) is the defensive direction.

As is the general goal with this program, the idea of working with this dataset is to produce some new informative knowledge through data and/or statistical analyses, or produce a neat data visualisation to communicate your findings.

### Get the Data

The dataset — 'askAndYouShallReceive.csv' — can be viewed online by clicking the link above. To download the data, you can [clone this repository](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository) or directly download the file by:
- Clicking the link above to view the dataset
- Right click on the 'Raw' button and 'Save link as...'
- Save the file wherever you like. It may be necessary to change the file extension from '.txt' to '.csv' for easier use

### Data Dictionary

## `askAndYouShallReceive.csv`

|Variable         |Data Type |Description |
|:----------------|:---------|:-----------|
|roundNo             |numeric    | Round number from season the match was played in |
|matchNo           |numeric   | Match ID number |
|quarterNo              |numeric   | Quarter within the match the play data comes from |
|teamName             |string   | Name of team the play relates to |
|centrePassRec             |string   | Playing position for centre pass receiver ('UNKNOWN' if could not be determined) |
|centrePassX               |numeric   | X coordinate for where on court centre pass was received |
|centrePassY               |numeric   | Y coordinate for where on court centre pass was received |
|secondPhaseRec            |numeric   | Playing position for second phase receiver ('UNKNOWN' if could not be determined) |
|secondPhaseX             |numeric   | X coordinate for where on court second phase was received |
|secondPhaseY              |numeric   | Y coordinate for where on court centre pass was received |
