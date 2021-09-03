
<!-- README.md is generated from README.Rmd. Please edit that file -->

# Percentage Difference Over Time (Walkthrough)

This document steps through the code to produce the figure in
[README.md](./README.md). The output (.md/.html files) can be generated
from the input (.Rmd files) using the following commands:

``` r
rmarkdown::render('./walkthrough.Rmd')
rmarkdown::render('./README.Rmd')
```

The first thing we need are some libraries to munge the data and create
the graphic:

``` r
## tidyverse brings in a bunch of useful packages
## here provides easy to use relative paths (to the .git folder)
## install.packages('tidyverse'); install.packages('here')
library(tidyverse)
library(here)
```

OK. Let’s read in the data that Aaron’s provided and take a quick look
at it:

``` r
time_machine <- read_csv(here('datasets/vol1/resultsFromTheTimeMachine.csv'))
#> 
#> ── Column specification ────────────────────────────────────────────────────────────────
#> cols(
#>   team = col_character(),
#>   played = col_double(),
#>   win = col_double(),
#>   draw = col_double(),
#>   loss = col_double(),
#>   GF = col_double(),
#>   GA = col_double(),
#>   Gdiff = col_double(),
#>   Gper = col_double(),
#>   pts = col_double(),
#>   bonusPts = col_double(),
#>   finalsWin = col_double(),
#>   finalsLoss = col_double(),
#>   year = col_double(),
#>   coach = col_character(),
#>   minorPremiership = col_character(),
#>   premiership = col_character(),
#>   runnerUp = col_character(),
#>   competition = col_character()
#> )
glimpse(time_machine)
#> Rows: 130
#> Columns: 19
#> $ team             <chr> "Magic", "Swifts", "Thunderbirds", "Vixens", "Firebir…
#> $ played           <dbl> 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 1…
#> $ win              <dbl> 10, 10, 9, 9, 7, 7, 5, 5, 2, 0, 12, 11, 10, 8, 8, 5, …
#> $ draw             <dbl> 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,…
#> $ loss             <dbl> 3, 3, 4, 4, 6, 6, 8, 8, 10, 12, 1, 2, 3, 5, 5, 8, 8, …
#> $ GF               <dbl> 687, 727, 652, 673, 693, 617, 625, 607, 605, 471, 769…
#> $ GA               <dbl> 599, 652, 577, 620, 645, 616, 637, 678, 697, 636, 614…
#> $ Gdiff            <dbl> 88, 75, 75, 53, 48, 1, -12, -71, -92, -165, 155, 111,…
#> $ Gper             <dbl> 114.69, 111.50, 113.00, 108.55, 107.44, 100.16, 98.12…
#> $ pts              <dbl> 20, 20, 18, 18, 14, 14, 10, 10, 5, 1, 24, 22, 20, 16,…
#> $ bonusPts         <dbl> NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, N…
#> $ finalsWin        <dbl> 1, 2, 1, NA, NA, NA, NA, NA, NA, NA, 2, NA, 2, 1, NA,…
#> $ finalsLoss       <dbl> 2, NA, 1, 1, NA, NA, NA, NA, NA, NA, NA, 2, 1, NA, NA…
#> $ year             <dbl> 2008, 2008, 2008, 2008, 2008, 2008, 2008, 2008, 2008,…
#> $ coach            <chr> "Noeline Taurua", "Julie Fitzgerald", "Jane Woodlands…
#> $ minorPremiership <chr> "Yes", "No", "No", "No", "No", "No", "No", "No", "No"…
#> $ premiership      <chr> "No", "Yes", "No", "No", "No", "No", "No", "No", "No"…
#> $ runnerUp         <chr> "Yes", "No", "No", "No", "No", "No", "No", "No", "No"…
#> $ competition      <chr> "ANZC", "ANZC", "ANZC", "ANZC", "ANZC", "ANZC", "ANZC…
```
