"""webParsing.py: This file contains all the functions required for parsing data from the internet for the PVR project."""

import pandas as pd
import re

def getTeamBoxScore(tName, link):
    '''
    Params: tName - String that represents the team name to look for
            link - String that represents the url of the box score (must follow usportshoops.ca)

    Returns: A list containing two elements: A dictionary with the player name as key and their statline as the value (in list form), and a list with the total team box score 

    This function takes a team name and the web page for their game and gets their box score.   
    '''

    # get pandas dataframe from the url
    tbl = pd.read_html(link)

    # fifth table is the box score on usportshoops
    box_score = tbl[5]

    # remove unnecessary columns, i.e. the ones that are just for formatting
    box_score = box_score.drop(columns=[0,2,3,5,8,11,14,18,20,25])

    # transpose data frame to easily access the box score data
    box_score = box_score.transpose()

    team = {}
    team_tot = []

    regex = re.compile('[^a-zA-Z]')

    # get box score data in the dictionary
    if (tName.upper() in regex.sub('', box_score[0][1]).upper()):
        for x in box_score:
            if not(isinstance(box_score[x][1], str)):
                break
            else:
                stats = box_score[x].to_list()
                if "team" not in stats[0] and stats[0] != stats[1]:
                    if "*" not in stats[0]:
                        team[stats[0]] = stats[1:]
                    else:
                        team_tot = stats

    # there is probably a more efficient way to do this
    else:
        secondBox = False
        for x in box_score:
            if not(isinstance(box_score[x][1], str)):
                secondBox = True
            else:
                if secondBox:
                    stats = box_score[x].to_list()
                    if "team" not in stats[0] and stats[0] != stats[1]:
                        if "*" not in stats[0]:
                            team[stats[0]] = stats[1:]
                        else:
                            team_tot = stats


    # remove the default player rows, does not contain any stats
    del team["Player"]
    
    return [team, team_tot]

def getTeamGames(tLink, magic_number):
    """
    Params: tLink - String that represents the main team page of the basketball team (usportshoops page)
            magic_number - Int that represents number of games back to check
    Returns: A list containing the 5 (or less) most recent games played by the team

    This function uses the main team page and gets their most recent regular season games played and returns them.
    """

    # get all the a href links from the body of the html of the webpage
    tbl = pd.read_html(tLink, extract_links="body")

    # get specific table of team -> same for all teams on usportshoops
    tbl = tbl[6]

    # transpose to access data easier
    tbl = tbl.transpose()

    games = []

    # get the regular season games and add them to games
    begin = False
    for x in tbl:
        if tbl[x][0][0] == "--- Regular Season Conference Games ---":
            begin=True
        if tbl[x][0][0] == "--- Games Yet to Play ---":
            begin=False
        if begin and tbl[x][0][0] != "Date" and tbl[x][0][0] != "--- Regular Season Conference Games ---" and isinstance(tbl[x][5][1], str):
            games.append("https://usportshoops.ca" + tbl[x][5][1])
    
    # return the last 5 games (or less)
    return games[(magic_number*-1):]

def getTeamPages():
    """
    Params: None
    Returns: A dictionary of lists containing one indice with the team's front page

    This function gets the teams main pages by appending the team name to a default string for the 2022-23 season.
    Will need to modify this in the future to support more teams.
    """

    # default team list, currently only supports OUA
    teams = {
        "algoma":[],
        "brock":[],
        "carleton":[],
        "guelph":[],
        "lakehead":[],
        "laurentian":[],
        "mcmaster":[],
        "nipissing":[],
        "ontario tech":[],
        "ottawa":[],
        "queens":[],
        "tmu":[],
        "toronto":[],
        "waterloo":[],
        "western":[],
        "wilfrid":[],
        "windsor":[],
        "york":[]
    }

    for key in teams:
        if key == "wilfrid":
            link = "https://usportshoops.ca/history/teamseason.php?Gender=MBB&Season=2022-23&Team=" + "WLUTeam"
        elif key == "tmu":
            link = "https://usportshoops.ca/history/teamseason.php?Gender=MBB&Season=2022-23&Team=" + "TMUnow"
        elif key == "ontario tech":
            link = "https://usportshoops.ca/history/teamseason.php?Gender=MBB&Season=2022-23&Team=" + "ontario%20tech"
        else:
            link = "https://usportshoops.ca/history/teamseason.php?Gender=MBB&Season=2022-23&Team=" + re.sub(r'[^a-zA-Z\s]', '', key)
        teams[key].append(link)

    return teams