# Plot code

# Load Libraries
library(here)
library(tidyverse)
library(ggridges)
library(ggforce)

# Helper functions
calc_dist <- function(x0,x1,y0,y1){
  
  # Convert to meters
  # 200 units / 30.5 meters length of netball court
  x0 = x0 * 0.1525
  x1 = x1 * 0.1525
  y0 = y0 * 0.1525
  y1 = y1 * 0.1525
  
  # Pythagorous theorem to calculate straight line distance
  pass_dist = sqrt((x1-x0)^2 + (y1 - y0)^2)
  return(sqrt((x1-x0)^2 + (y1 - y0)^2))
}

# Add netball ggplot elements
add_forward_third <- function() geom_rect(xmin = 0,xmax = 100,ymin = 133,ymax = 200,fill = "white",col = "black")
add_centre_third <- function() geom_rect(xmin = 0,xmax = 100,ymin = 67,ymax = 133,fill = "white",col = "black")
add_forward_goal_circle <- function() geom_arc_bar(aes(x0 = 50,y0 = 200,r0 = 0, r = 4.9/0.1525,start = pi/2,end = 3/2*pi), inherit.aes = F)
add_centre_circle <- function() geom_circle(aes(x0 = 50, y0 = 100,r = 0.45/0.1525),col = "black",fill = "white",inherit.aes = F)
add_forward_ring <- function() geom_circle(aes(x0 = 50, y0 = 197,r = 0.19/0.1525),col = "black",fill = "white",inherit.aes = F)

# Load data

first_two_passes <- read_csv(here('datasets/vol2/askAndYouShallReceive.csv')) %>% 
  mutate(
    # Calculate pass length
    first_pass_len = calc_dist(50, centrePassX, 100, centrePassY),
    second_pass_len = calc_dist(centrePassX, secondPhaseX, centrePassY, secondPhaseY),
    # Determine if point in the goal circle (x1 - centre GC)^2 + (y1 - centre GC) < r^2
    in_circle = (secondPhaseX - 50)^2 + (secondPhaseY - 200)^2 < (4.9/0.1525)^2,
    # Order positions for plot legend
    centrePassRec = factor(centrePassRec,level = c("GS","GA","WA","C","WD","GD","GK","S","UNKNOWN"),ordered = T),
    secondPhaseRec = factor(secondPhaseRec,level = c("GS","GA","WA","C","WD","GD","GK","S","UNKNOWN"),ordered = T))

# Each team's 10 longest passes
first_two_passes %>% 
  filter(!is.na(secondPhaseX)) %>% 
  group_by(teamName) %>% 
  arrange(teamName,-second_pass_len) %>% 
  slice(1:20) %>%
  mutate(id = as.character(1:n())) %>% 
  ungroup() %>% 
  pivot_longer(cols = c(centrePassX,centrePassY,secondPhaseX,secondPhaseY),names_to = c("phase","dimension"),names_pattern = "(.*)(.$)") %>% 
  pivot_wider(names_from = dimension,values_from = value) %>% 
  mutate(position = if_else(phase == "centrePass",centrePassRec,secondPhaseRec)) %>% 
  ggplot(aes(x = X,y = Y,group = id)) +
  add_forward_third() +
  add_centre_third() +
  add_forward_goal_circle() +
  add_forward_ring() +
  add_centre_circle() +
  geom_point(aes(col = position),size = 3) +
  scale_color_brewer(palette = "Spectral") +
  geom_line() +
  coord_fixed(ylim = c(67,200)) +
  theme_void() +
  facet_wrap(~teamName,nrow = 2) +
  labs(title = "Long bombs",
       subtitle = "Each teams 20 longest second phase passes",
       caption = "Data courtesy of Aaron Fox (@aaron_s_fox)",
       colour = "Player position") +
  theme(plot.title = element_text(hjust = 0.5, size = 15),
        plot.subtitle = element_text(hjust = 0.5,size = 12))



# Passes to goal circle on second pass
## Create labels for plot
goals_in_second <- first_two_passes %>%
  filter(in_circle) %>% 
  count(teamName,secondPhaseRec) %>% 
  filter(secondPhaseRec %in% c("GA","GS")) %>% 
  arrange(teamName,secondPhaseRec) %>% 
  group_by(teamName) %>% 
  summarise(lab = paste(secondPhaseRec,n,sep = ": ",collapse = "\n"))

first_two_passes %>% 
  # Filter for only passes that end up in the goal circle
  filter(in_circle) %>% 
  # Add pass event ID
  mutate(id = as.character(1:n())) %>% 
  pivot_longer(cols = c(centrePassX,centrePassY,secondPhaseX,secondPhaseY),names_to = c("phase","dimension"),names_pattern = "(.*)(.$)") %>% 
  pivot_wider(names_from = dimension,values_from = value) %>% 
  mutate(position = if_else(phase == "centrePass",centrePassRec,secondPhaseRec)) %>% 
  ggplot(aes(x = X,y = Y,group = id)) +
  add_forward_third() +
  add_centre_third() +
  add_forward_goal_circle() +
  add_forward_ring() +
  add_centre_circle() +
  geom_point(aes(col = position),size = 3) +
  scale_color_brewer(palette = "Spectral") +
  geom_line() +
  geom_text(data = goals_in_second, aes(x = 15,y = 80,label = lab),inherit.aes = F) +
  coord_fixed(ylim = c(67,200)) +
  theme_void() +
  facet_wrap(~teamName,nrow = 2) +
  labs(title = "Go for goal",
       subtitle = "All second phase passes that enter the goal circle",
       caption = "Inset numbers are goaler pass recieved counts. Data courtesy of Aaron Fox (@aaron_s_fox)",
       colour = "Player position") +
  theme(plot.title = element_text(hjust = 0.5,size = 15),
        plot.subtitle = element_text(hjust = 0.5,size = 12))


# Swifts exploratory plot

first_two_passes %>% 
  filter(centrePassRec != "UNKNOWN",!is.na(secondPhaseX)) %>% 
  mutate(quadrant = case_when(
    centrePassX <= 50 & centrePassY <= 100 ~ "BL",
    centrePassX > 50 & centrePassY <= 100 ~ "BR",
    centrePassX <= 50 & centrePassY > 100 ~ "TL",
    centrePassX > 50 & centrePassY > 100 ~ "TR",
    TRUE ~ "Error"
  ),
  id = as.character(1:n())) %>% 
  filter(teamName == "Swifts",quadrant == "TR",centrePassRec == "GA") %>% 
  pivot_longer(cols = c(centrePassX,centrePassY,secondPhaseX,secondPhaseY),
               names_to = c("phase","dimension"),
               names_pattern = "(.*)(.$)") %>% 
  pivot_wider(names_from = dimension,values_from = value) %>%
  mutate(position = if_else(phase == "centrePass",centrePassRec,secondPhaseRec)) %>% 
  ggplot(aes(x = X,y = Y,group = id)) +
  add_forward_third() +
  add_centre_third() +
  add_forward_goal_circle() +
  add_forward_ring() +
  add_centre_circle() +
  geom_line(alpha = 0.3) +
  geom_point(aes(col = position),size = 3, alpha = 0.8) +
  scale_color_brewer(palette = "Spectral") +
  coord_fixed(ylim = c(67,200),clip = "off") +
  theme_void() +
  labs(title = "Hit that circle edge",
       subtitle = "Swifts goal attack second phase passes from top right quadrant",
       caption = "Data courtesy of Aaron Fox (@aaron_s_fox)",
       colour = "Player position") +
  theme(plot.title = element_text(hjust = 0.5,size = 15),
        plot.subtitle = element_text(hjust = 0.5,size = 12),
        plot.caption = element_text(hjust = 1))
