#!/usr/bin/env python

"""main.py: This file executes the main python code to run the PVR stat on all teams and display the output on a web application using flask."""

from flask import Flask, render_template, redirect, url_for
import json
import time
import pandas as pd
import re
import math

def getAvg(l1, l2):
    '''
    Params: l1 - A list of dictionaries containing all the player stats
            l2 - A list of lists containing all the team stats
    Returns: a list with indice 0 containing a dictionary of player averages and indice 1 containing a list of team averages
    
    This function gets the averages of a team and their individual players.
    '''

    # calculate team averages
    teamTotals = calcLofLs(l2, len(l2))

    playerTotals = {}

    # first, add all the players to the final dict
    for d in l1:
        for key in d:
            if key not in playerTotals:
                playerTotals[key] = [[]]

    # then add only their individual stats
    for d in l1:
        for key in d:
            playerTotals[key].append(d[key])
            if len(playerTotals[key][0]) == 0:
                del playerTotals[key][0]


    # now average the stats and return them
    for key in playerTotals:
        playerTotals[key] = calcLofLs(playerTotals[key], len(playerTotals[key]))

                
    return [playerTotals, teamTotals]

def calcLofLs(l2, gameAmt):
    '''
    Params: l2 - A list of dictionaries
    Returns: A list containing averaged stats

    This function serves as the driver code for get average as it is universal between the dictionary and list types,
    which are modified in getAvg()
    '''
    teamTotals = [[]]

    for x in range(15):
        teamTotals.append(0)

    teamTotals[1] = "0-0"
    teamTotals[3] = "0-0"
    teamTotals[5] = "0-0"
    teamTotals[0] = 0

    CalcOk = True

    # calcualte the averages
    for x in range(len(l2)):
        for y in range(len(l2[x])):
            if "-" not in l2[x][y]:
                
                # this calc ok clause prevents us from accidentally averaging percentages
                if CalcOk:
                    teamTotals[y] += float(l2[x][y])/gameAmt
                else:
                    CalcOk = True
            else:
                CalcOk = False
                val = l2[x][y].split("-")
                val[0] = float(val[0]) / gameAmt
                val[1] = float(val[1]) / gameAmt

                teamTotals[y] = str(
                    val[0] + float(teamTotals[y].split("-")[0])
                ) + "-" + str(
                    val[1] + float(teamTotals[y].split("-")[1])
                )
    
    # calculate the averages for the fg attempts and makes
    for x in range(1, 6, 2):
        val = teamTotals[x].split("-")
        
        if float(val[1]) == 0:
            teamTotals[x+1] = 0
        else:
            teamTotals[x+1] = (float(val[0])/float(val[1]))*100

    teamTotals.append(gameAmt)

    return teamTotals

def calculatePVR(p,t):
    '''
    Params: p - is a dictionary of lists that contains the player stats
            t - is a list of the team stats

    This function calculates the player valuability rating using our formula (see about page on webapp)
    '''

    newList = [[]]

    # iterate through dictionary of players
    for key in p:

        # all the variables necessary for calculations
        name = key
        p_FGM_FGA = (p[name][3].split('-'))
        p_FGA = float(p_FGM_FGA[-1])
        p_FTM_FTA = (p[name][5].split('-'))
        p_FTA = float(p_FTM_FTA[-1])
        p_Off_Rebounds = float(p[name][7])
        p_Def_Rebounds = float(p[name][8])
        p_Rebounds = float(p[name][9])
        p_PF = float(p[name][10])
        p_Assists = float(p[name][11])
        p_Turnovers = float(p[name][12])
        p_Blocks = float(p[name][13])
        p_Steals = float(p[name][14])
        p_Points = float(p[name][15])
        t_FGM_FGA= t[3].split('-')
        t_fgMade = float(t_FGM_FGA[0])
        t_Off_Rebounds = float(t[7])
        t_Def_Rebounds = float(t[8])
        t_Turnovers = float(t[12])
        t_Blocks = float(t[13])
        t_Steals = float(t[14])
        t_Points = float(t[15])


        # calculate fg made stat
        if t_fgMade==0:
            s_Assist = 0
            
        else:
            s_Assist = (p_Assists / t_fgMade) * t_Points
        
        # calculate points stat
        if t_Points == 0:
            s_Point = 0

        else:
            s_Point = p_Points * (1 + (p_Points/t_Points))
        
        # calculating rebounding stat
        if  t_Off_Rebounds == 0 and t_Def_Rebounds == 0:
            s_Rebound = 0
        
        elif t_Off_Rebounds == 0 and t_Def_Rebounds > 0:
            ((p_Def_Rebounds/t_Def_Rebounds)+1) * p_Def_Rebounds
        
        elif t_Off_Rebounds > 0 and t_Def_Rebounds ==0:
            s_Rebound = ((p_Off_Rebounds/t_Off_Rebounds) + 1)* p_Off_Rebounds * 1.25
        
        else:
            s_Rebound = ((p_Off_Rebounds/t_Off_Rebounds) + 1)* p_Off_Rebounds * 1.25 + ((p_Def_Rebounds/t_Def_Rebounds)+1) * p_Def_Rebounds

        # calculate steal stats
        if t_Steals == 0:
            s_Steals = 0
        else:
            s_Steals = math.exp(p_Steals/t_Steals) * p_Steals * 2

        if t_Blocks == 0:
            s_Blocks = 0
        else:
            s_Blocks = math.exp(p_Blocks/t_Blocks) * p_Blocks * 2
        
        # calculate assists vs turnovers stats
        if p_Assists > 0 and t_Turnovers > 0:
            s_Turnover = math.exp(p_Turnovers/t_Turnovers) * (p_Turnovers/p_Assists + 1) * p_Turnovers
        
        elif p_Assists == 0 and t_Turnovers > 0:
            s_Turnover = math.exp(p_Turnovers/t_Turnovers) * p_Turnovers
        
        elif p_Assists > 0 and t_Turnovers == 0:
            s_Turnover = (p_Turnovers/p_Assists + 1) * p_Turnovers
        
        else:
            s_Turnover = 0


        # calculate fouls stats 
        s_PF = math.exp(p_PF/6)*p_PF
        
        # calculate true shooting stats
        if p_FTA == 0 or p_FGA == 0:
            s_Efficiency = 0
            
        else:
            s_Efficiency = (((0.5*p_Points)/(p_FGA+0.475*p_FTA))+1)*p_Points

        # sum total
        PVR = s_Assist + s_Point + s_Rebound + s_Steals + s_Blocks + s_Efficiency - s_Turnover - s_PF
        
        # add name, pvr, points, assists, repbound, games played
        newList.append([name, round(PVR, 2), round(p_Points, 2), round(p_Assists, 2), round(p_Rebounds, 2), p[name][16]])
    
    # remove starting bracket
    del newList[0]

    # get top pvr list
    PVR_list = []
    for pvr in newList:
        PVR_list.append(pvr[1])
    
    top_PVR_List = sorted(PVR_list, reverse=True)
    
    # add to final array in order
    MAIN_RETURN = [[]]
    for x in range(len(newList)):
        MAIN_RETURN.append(newList[PVR_list.index(top_PVR_List[x])])
    
    # remove starting bracket
    del MAIN_RETURN[0]

    # return sorted top players
    return MAIN_RETURN


def getTeamPVR(tName, team):
    '''
    Params: tName - String containing the team name
            team  - List containing the web links for games to check PVR for
    Returns: A list containing the PVRs of the team

    This program calls multiple functions in order to get team averages and then calculate the PVR.
    '''

    totals = []

    # add all the box score values to the totals
    for game in team:
        totals.append(getTeamBoxScore(tName, game))

    l1 = []
    l2 = []

    # separate the box scores by type
    for game in totals:
        l1.append(game[0])
        l2.append(game[1][1:])
    
    # get the averages
    avg = getAvg(l1, l2)

    # calculate the pvr
    pvr = calculatePVR(avg[0], avg[1])

    return pvr




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


'''This is the main function, where all execution of the code occurs'''

start_time = time.time()

# how many recent games do we check
magic_number = 5

# get the main team page for each team
teams = getTeamPages()
teamPVR = {}

top_players = {}
top_pvrs = []

# get the teams most recent 5 games and their PVRs
for team in teams:
    teams[team].append(getTeamGames(teams[team][0], magic_number))
    teamPVR[team] = getTeamPVR(team, teams[team][1])
    
    # we only want players who've played all games, and their photos
    if teamPVR[team][0][-1] == magic_number:
        toAdd = teamPVR[team][0]
        
        photoLink = "team-photos/" + team + ".json"

        data = json.load(open(photoLink))

        if teamPVR[team][0][0] in data:
            toAdd.append(data[teamPVR[team][0][0]])
        else:
            toAdd.append("https://www.pngitem.com/pimgs/m/504-5040528_empty-profile-picture-png-transparent-png.png")
            
            
        uniName = team
        if uniName == "wilfrid":
            uniName = "WLU"
        else:
            uniName = uniName.title()
        
        toAdd.append(uniName)

        top_players[teamPVR[team][0][1]] = toAdd
        top_pvrs.append(teamPVR[team][0][1])

# get the top 3 PVRs in the league
top_pvrs.sort()
top_pvrs.reverse()
top_pvrs = top_pvrs[:3]

for x in range(len(top_pvrs)):
    top_pvrs[x] = top_players[top_pvrs[x]]

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", top=top_pvrs)

@app.route("/oua-central")
def choice_1():
    return render_template("ouacentral.html")

@app.route("/oua-eastern")
def choice_2():
    return render_template("ouaeast.html")

@app.route("/oua-western")
def choice_3():
    return render_template("ouawest.html")

@app.route("/about")
def choice_4():
    return render_template("about.html")

@app.route("/teams/<name>")
def user(name):
    if str(name) in teams:
        tName = name
        return render_template("team.html", teamStats=teamPVR[tName])

    else:
        return redirect(url_for("home"))

print(f"\nExecution finished in {time.time() - start_time} seconds")


if __name__ == "__main__":
    app.run()