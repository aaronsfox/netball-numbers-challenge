#This script loads the team cumulative data from the vol. 8 challenge and creates animated line plots
#of certain variables from the dataset.

#Import libraries
library(ggplot2)
library(geomtextpath)
library(gganimate)
library(ggimage)
library(ggthemes)
library(here)
library(dplyr)
library(showtext)

#Import fonts
font_import()

#Load the cumulative stats dataset
#Add the image files as a new column
teamDataCumulative <- read.csv(paste0(here(),"/datasets/vol8/theGames_teamDataCumulative.csv")) %>%
  mutate(image = paste0(here(),"/examples/vol8/images/",team,"_cropped.png"))

#Create team colour palettes
teamCols <- c("Australia" = "#018752",
              "Barbados" = "#00267f",
              "England" = "#ce1124",
              "Jamaica" = "#ffb81c",
              "Malawi" = "#000000",
              "New Zealand" = "#000000",
              "Northern Ireland" = "#cc0000",
              "Scotland" = "#005eb8",
              "South Africa" = "#007847",
              "Trinidad and Tobago" = "#da1a35",
              "Uganda" = "#fcdc04",
              "Wales" = "#00b140")

#Create the plot
animatedPlot <- teamDataCumulative %>%
  #Set the basic aesthetics
  ggplot(aes(x = quartersPlayed,
             y = goalDifferential,
             group = team)) +
  #Add dashed line at y = 0
  geom_hline(yintercept = 0, size = 0.5, linetype = 2) +
  #Add vertical line at pool matches end
  geom_vline(xintercept = 20, size = 0.5, linetype = 2) +
  #Add label to specify end of pool matches
  annotate("text", x = 19.75, y = -305, label = "End of Pool Matches", hjust = 1, vjust = 1, size = 3) +
  #Add the line geom
  geom_line(size = 1.5, aes(color = team)) +
  #Add the flag images
  #Includes fix for aspect ratio specified lower down
  geom_image(aes(image = image),
             asp = 2,
            size = 0.04
            ) +
  #Scale the colours by the specific team values
  scale_color_manual(values = teamCols) +
  #Add a labels
  labs(x = "Quarters Played",
       y = "Cumulative Goal Differential",
       title = "Cumulative goal differential through quarters in 2022 Commonwealth Games",
       subtitle = "Score differential cumulatively summed at the end of each quarter") +
  #Set the theme
  theme_fivethirtyeight() +
  #Edit the theme
  theme(
    #Remove the legend
    legend.position = "none",
    #Specify grid and add border
    axis.line = element_line(colour = "black"),
    panel.grid.major.x = element_blank(),
    panel.grid.major.y = element_line(colour = "black", size = 0.5, linetype = 3),
    panel.grid.minor = element_blank(),
    panel.border = element_blank(),
    axis.line.x = element_line(colour = "black", size = 1),
    axis.line.y = element_blank(),
    #Axis title font & alignment
    axis.title.x = element_text(face = "bold", hjust = 0.99),
    axis.title.y = element_text(face = "bold", hjust = 0.99),
    #Remove x-ticks and labels
    axis.text.x = element_blank(),
    axis.ticks.x = element_blank(),
    #Edit y-tick labels
    axis.text.y = element_text(face = "bold")
    ) +
  #Set the animation to reveal across quarters played
  transition_reveal(quartersPlayed)

#Create the animation from the plot
animate(plot = animatedPlot,
        #Set the number of frames
        nframes = 100,
        #Set and end pause of quarter length total frames
        end_pause = 25,
        #Set the dimensions
        height = 800, width = 1600,
        #Set the resolution
        res = 150)

#Save the animation
anim_save(paste0(here(),"/examples/vol8/vol8_example.gif"))
