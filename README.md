# Player Value Rating - #1 Overall Project @ NewHacks 2022
###### Created by Hashir, Akshayan, Yash, & Ryan

Created for NewHacks 2022, this project focuses on promoting Canadian Basketball athletics using our own statistic. The Player Valuability Rating (PVR) helps determine an individual basketball player's impact to their team by comparing their statistics relative to their teams'. In addition, true shooting is considered along with increased relevance of special stats (turnovers, blocks, steals, fouls), where the more often they occur, the more they influence the stat. Using this statistic along with our webpage, we hope to easily show scouts the best performing athletes of the week.

## How does it work?

Using Pandas and Python, we retrieved box score game data for each Ontario University's most recent 5 games. With this information, we calculated the average statistics of the player's 5 games and applied it to our Player Valuability Rating formula. This data was then formatted and posted on our web application using HTML/CSS, JavaScript and BootStrap.

The statistic itself is very thorough. Here is the formula we created to calculate each player's PVR.

![PVR Formula](/static/img.png)

## Why use this stat over hundreds of other advanced metrics?

Player Valuability Rating is the only stat that accounts for player's value by percentages. It's also the only statistic that focuses on statistics that have more variability and thus require changes to account for that (i.e. using exponential functions for turnovers, fouls etc.)

## What are the next steps?

After finishing with the initial project, our plan is to increase the scope drastically by retrieving information from other regions in Canada and applying the PVR to them as well. In addition, we hope to promote Women's Basketball in the future as it is heavily underrepresented.

## How can I use this application?

Install everything in the main branch and run the main.py file. After a slight delay, the local server should be running. Note: __We plan on releasing this to the public once a finished version is ready.__
 
