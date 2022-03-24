# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 11:28:30 2021

@author:
    Aaron Fox
    Centre for Sport Research
    Deakin University
    aaron.f@deakin.edu.au
    
    This code looks at visualising player and team networks across ANZC & SSN.
    Specifically, network analysis is applied to connections between players (i.e. 
    those that have played games together) and uses a network graph to visualise
    these connections. Additionally, the transfer of players between teams is
    visualised via a chord diagram.
    
"""

# %% Import packages

import pandas as pd
import numpy as np
import holoviews as hv
from holoviews import opts
from bokeh.models import HoverTool
import bokeh.io
from bokeh.models import Title
import networkx as nx
import chromedriver_binary  # Adds chromedriver binary to path

#Set holoviews parameters
hv.extension('bokeh')
hv.output(size = 200)

# %% Set-up

#Load the dataset
playerData = pd.read_csv('..\\..\\datasets\\vol6\\whoDoYouPlayFor.csv')

#Create a list of the squad names
squadNames = list(playerData['squadName'].unique())

#Set up the colour map for the squad names
colourDict = {'Fever': '#00953b',
              'Firebirds': '#4b2c69',
              'GIANTS': '#f57921',
              'Lightning': '#fdb61c',
              'Magpies': '#494b4a',
              'Swifts': '#0082cd',
              'Thunderbirds': '#e54078',
              'Vixens': '#00a68e',
              'Magic': '#000000',
              'Mystics': '#0000cd',
              'Pulse': '#ffff00',
              'Steel': '#00b7eb',
              'Tactix': '#ee161f'}

#Map to squad names
squadCols = []
for squad in squadNames:
    squadCols.append(colourDict[squad])

# %% EXAMPLE 1: Create the chord graph for player movement between teams

#Create a zeroed source to target dataframe to fill
source = []
target = []
value = []
for sourceInd in range(len(squadNames)):
    for targetInd in range(len(squadNames)):
        if sourceInd != targetInd:
            source.append(sourceInd)
            target.append(targetInd)
            value.append(0)
links = pd.DataFrame(list(zip(source, target, value)),
                          columns = ['source', 'target', 'value'])

#Get a unique list of player Id's
allPlayerId = playerData['playerId'].unique()

#Loop through player Id's and extract transfer data
for playerId in allPlayerId:
    
    #Extract the current players data
    currPlayerData = playerData.loc[playerData['playerId'] == playerId, ]
    
    #Extract the teams the player has played for across years
    playerTeamData = {'year': [], 'team': []}
    for year in np.sort(currPlayerData['year'].unique()):
        playerTeamData['year'].append(year)
        playerTeamData['team'].append(currPlayerData.loc[currPlayerData['year'] == year,]['squadName'].unique()[0])
        
    #Loop through the players years and identify if there is a change in team
    if len(playerTeamData['year']) > 1:
        for ind in range(len(playerTeamData['year'])-1):
            #Check if player transferred to a different team the following year
            if playerTeamData['team'][ind] != playerTeamData['team'][ind+1]:
                #A change in team happened
                #Iedntify the source and target teams
                sourceTeam = squadNames.index(playerTeamData['team'][ind])
                targetTeam = squadNames.index(playerTeamData['team'][ind+1])
                #Add this change to the links values
                #Identify index and value
                linksInd = links.loc[(links['source'] == sourceTeam) &
                                     (links['target'] == targetTeam),].index[0]
                linksVal = links.loc[(links['source'] == sourceTeam) &
                                     (links['target'] == targetTeam),['value']].to_numpy()[0][0]
                #Replace value
                links.at[linksInd, 'value'] = linksVal + 1

#Create the nodes for grouping by team colours
nodes = []
for squad in squadNames:
    nodes.append({'name': squad, 'group': squadNames.index(squad)})
    
#Convert to holoviews dataset
nodesHV = hv.Dataset(pd.DataFrame(nodes), 'index')
# nodesHV.data

#Create the chord plot
chordPlot = hv.Chord((links, nodesHV))

#Set base options
chordPlot.opts(width = 380, height = 400)

#Set chord specific options
chordPlot.opts(opts.Chord(
        #Turn off toolbar
        toolbar = None,
        #Turn on hover tools
        tools = [HoverTool(tooltips = None)],
        #Set the title
        # title = 'Player Movement across the ANZ Championship & Super Netball',
        #Set the colours maps for the nodes and edges
        node_cmap = squadCols, edge_cmap = squadCols,
        #Set the base alpha for non-selected items
        edge_line_alpha = 0.4,
        #Set the base edge line colour for non-selected items (light grey)
        edge_line_color = '#aeaeae',
        edge_nonselection_line_color = '#aeaeae',
        #Set the edge line hover colour to correspond to target team
        edge_hover_line_color = 'target',
        #Set the edge line hover alpha to become more prominent
        edge_hover_line_alpha = 1.0,
        #Set the labels for the nodes
        labels = 'name',
        #Set label font size
        label_text_font_size = '10pt',
        #Set label font style
        label_text_font_style = 'bold',
        #Set the node colour to correspond to the team
        node_color = 'index',
        #Set the nodes to have no outline (via 0 alpha)
        node_line_alpha = 0.0,
        #Set the node hover colour to correspond to the team
        node_hover_fill_color = 'index',
        )
    )

#Create the title layouts
#Convert plot to rendered object
chordPlotRender = hv.render(chordPlot)

#Add sub-title
chordPlotRender.add_layout(Title(text = 'Line colours are indicative of the destination team',
                                 text_font_size = '12pt',
                                 text_font_style = 'italic'),
                           'above')
#Add title
chordPlotRender.add_layout(Title(text = 'Player movement in the ANZ Championship and Super Netball',
                                 text_font_size = '16pt',
                                 text_font_style="bold"),
                           'above')

#Save bokeh object
#HTML
bokeh.io.save(chordPlotRender, 'vol6_example_1.html', title = 'Player Movement in the ANZC and SSN')
#PNG
bokeh.io.export_png(chordPlotRender, filename = 'vol6_example_1.png')

# %% EXAMPLE 2: Create a network graph of team-mate connections

#Identify the top 100 most games played Id's
gamesDict = {'playerId': [], 'nGames': []}

#Loop through players
for playerId in list(playerData['playerId'].unique()):
    
    #Calculate the total number of games played
    nGames = len(playerData.loc[playerData['playerId'] == playerId,])
    
    #Append to dictionary with player Id
    gamesDict['playerId'].append(playerId)
    gamesDict['nGames'].append(nGames)
    
#Put into dataframe and sort values
nGames = pd.DataFrame.from_dict(gamesDict).sort_values(by = 'nGames',
                                                       ascending = False).reset_index(drop = True)

#Extract the top 100 player Id's
playerIds_top100 = list(nGames.iloc[0:100]['playerId'])

#Create an edge list between players that played together
A = []
B = []

#Get the lsit of match Id's
matchIds = list(playerData['matchId'].unique())

#Loop through match Id's and create connections based on player Id
for matchId in matchIds:
    
    #Extract the current match
    currMatch = playerData.loc[playerData['matchId'] == matchId,]
    
    #Extract the two teams
    squadNames = list(currMatch['squadName'].unique())
    
    #Loop through squads
    for squad in squadNames:
        
        #Extract current squad
        currSquad = currMatch.loc[currMatch['squadName'] == squad,]
    
        #Get player Id's
        playerIds = list(currSquad['playerId'].unique())
    
        #Sort player Id's numerically for consistency
        playerIds.sort()
    
        #Perform a sequentially reducing loop so that there aren't double ups of players
        for indA in range(len(playerIds)):
            for indB in range(indA+1,len(playerIds)):
                #Append to edge lists
                A.append(playerIds[indA])
                B.append(playerIds[indB])

#Place edge list in dataframe for easier manipulation
edgeList = pd.DataFrame(zip(A,B),
                        columns = ['A', 'B'])

#Keep values that include the top 100 players
edgeList_top100 = edgeList.loc[(edgeList['A'].isin(playerIds_top100)) &
                               (edgeList['B'].isin(playerIds_top100)),
                               ].reset_index(drop = True)

#Loop through players and map relevant values to dictionaries
#Map player Id and names to dictionary
namesDict = {}

#Loop through players
for playerId in playerIds_top100:
    
    #Extract player display name (select last most display name)
    displayName = playerData.loc[playerData['playerId'] == playerId
                                 ,]['displayName'].unique()[-1]
    
    #Append to dictionary with player Id as key
    namesDict[playerId] = displayName
    
#Determine the max number of games and scale the games dictionary values by this
maxGames = nGames['nGames'].max()
nGames['gamesScaled'] = nGames['nGames'] / maxGames

#Create the network graph
G = nx.Graph()

#Set parameters for scaling size
maxNodeSize = 30
maxEdgeWidth = 4.0

#Loop through and add the edges
for edgeInd in range(len(edgeList_top100)):
    G.add_edge(edgeList_top100['A'][edgeInd],
               edgeList_top100['B'][edgeInd])

#Create an indexed list for node colouring index mapped to squads
squadNodeCols = []
for squad in list(colourDict.keys()):
    squadNodeCols.append(colourDict[squad])

#Determine node size scaling and node colour values
for node in G.nodes():
    #Extract the player name and append to current node
    G.nodes[node]['Player'] = namesDict[node]
    #Extract the number of games and append to current node
    G.nodes[node]['nGames'] = nGames.loc[nGames['playerId'] == node,]['nGames'].values[0]
    #Extract the most common team for the current node
    squadCount = playerData.loc[playerData['playerId'] == node,
                                ['playerId','squadName']
                                ].groupby('squadName').count().reset_index().sort_values(
                                    by = 'playerId', ascending = False).reset_index(drop = True)
    maxSquad = squadCount['squadName'][0]
    #Add main team to node info
    G.nodes[node]['mainTeam'] = maxSquad
    #Extract the index in the squadCols dictionary and allocate to node
    G.nodes[node]['squadInd'] = list(colourDict.keys()).index(maxSquad)
    #Append sizing value to node
    G.nodes[node]['nodeSize'] = maxNodeSize * nGames.loc[nGames['playerId'] == node,]['gamesScaled'].values[0]

#Identify the highest total combination of matches together
maxConnection = np.max(edgeList_top100.reset_index(drop = False).groupby(['A', 'B']).count()['index'])

#Loop through edges to quantify number of connections between players
for edge in G.edges():
    #Extract the player Id's
    pId_1 = edge[0]
    pId_2 = edge[1]
    #Count the number of connections for current combination
    nConnections = len(edgeList_top100.loc[
        (edgeList_top100['A'] == pId_1) &
        (edgeList_top100['B'] == pId_2)
        ]) + \
        len(edgeList_top100.loc[
            (edgeList_top100['B'] == pId_1) &
            (edgeList_top100['A'] == pId_2)
            ])
    #Scale by max connections and append to edge
    G.edges()[edge]['lineWidth'] = maxEdgeWidth * nConnections / maxConnection

#Convert nextworkx graph to holoviews object
# networkGraph = hv.Graph.from_networkx(G, nx.layout.spring_layout)
networkGraph = hv.Graph.from_networkx(G, nx.layout.kamada_kawai_layout)

#Set base options
networkGraph.opts(width = 600, height = 400)

#Set hover tooltips
toolTips = [
    ('Name', '@Player'),
    ('No. of Games', '@nGames'),
    ('Main Team', '@mainTeam')
    ]

#Set graph specific options
networkGraph.opts(
    
    opts.Graph(
        
        #NODES
        
        #Set node colouring map
        node_cmap = squadNodeCols,
        #Link node fill to squadInd label on node
        node_fill_color = 'squadInd',
        #Set base node opacity to lowered alpha
        node_fill_alpha = 0.75, ###edges show up under nodes with opacity
        #Set node line edge coloring to squad values
        node_line_color = 'squadInd',
        #Set node line edge opacity to full
        node_line_alpha = 1.0,
        #Set node size to the size parameter attached to nodes
        node_size = 'nodeSize',
        
        #EDGES
        
        #Set line width
        edge_line_width = 'lineWidth',
        #Set edge line color
        edge_line_color = 'lightgrey',
        #Set edge line alpha
        edge_line_alpha = 1.0,
        
        #HOVER
        
        #Set the hover policy to be on the nodes
        inspection_policy = 'nodes',
        #Set edge hover line color to convert to black
        edge_hover_line_color = 'black',
        #Set node line edge hover color to black
        node_hover_line_color = 'black',
        #Set node hover color linked to squad colour
        node_hover_fill_color = 'squadInd',
        #Set node opacity to increase with hover
        node_hover_fill_alpha = 1.0,
        #Turn on hover tools
        tools = [HoverTool(tooltips = toolTips)],
        
        #AXES
        
        #Turn off x and y axes
        xaxis = 'bare',
        yaxis = 'bare'
        
        )
    )

#Render to Bokeh model
networkGraphRender = hv.render(networkGraph)

#Add sub-title
networkGraphRender.add_layout(Title(text = 'Edges connect players who have played a match together. Edge width reflective of the number of matches played together.',
                                 text_font_size = '12pt',
                                 text_font_style = 'italic'),
                           'above')

networkGraphRender.add_layout(Title(text = 'Node size reflective of the total matches played by player. Node colouring based on team they played the most matches for.',
                                 text_font_size = '12pt',
                                 text_font_style = 'italic'),
                           'above')

#Add title
networkGraphRender.add_layout(Title(text = 'Playing Connections from the ANZ Championship & Super Netball for Players in Top 100 for Matches Played',
                                 text_font_size = '16pt',
                                 text_font_style = 'bold'),
                           'above')

#Make axes invisible
networkGraphRender.axis.visible = False

#Save bokeh object
#HTML
bokeh.io.save(networkGraphRender, 'vol6_example_2.html', title = 'Playing Connections from the ANZ Championship & Super Netball')
#PNG
bokeh.io.export_png(networkGraphRender, filename = 'vol6_example_2.png')

# %% ---- End of vol6_example.py -----