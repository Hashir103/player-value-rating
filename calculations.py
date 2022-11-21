"""calculations.py: This file contains all the functions required for calculations for the main project"""

from webParsing import getTeamBoxScore
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

