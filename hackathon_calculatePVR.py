import math
# p = { "Player Name":[0 MINS,1 3PA-3PM, 2 P%, 3 FGM-FGA, 4 FG%, 5 FTM-FTA, 6 FT%, 7 OREB, 8 DREB, 9 TREB, 10 PF, 11 A, 12 TO,13 BLK, 14 STL , 15 PTS]  
# t = [0 MINS, 1 3PM-3PA, 2 3P%, 3 FGM-FGA, 4 FG%, 5 FTM-FTA, 6 FT%, 7 OREB, 8 DREB, 9 TREB, 10 PF, 11 A, 12 TO, 13 BLK, 14 STL, 15 PTS]

def calculatePVR(p,t):
    # p is dictionary of players
    # t is the list of the stats
    newList = [[]]
    for key in p:

        name = key
        p_minutesPlayed = p[name][0]
        p_3PM_3PA= (p[name][1].split('-'))
        p_3PM = float(p_3PM_3PA[0])
        p_3PA = float(p_3PM_3PA[-1])
        p_FGM_FGA = (p[name][3].split('-'))
        p_FGM = float(p_FGM_FGA[0])
        p_FGA = float(p_FGM_FGA[-1])
        p_fgPercent = str(p[name][4]) # DONT NEED I THINK
        p_FTM_FTA = (p[name][5].split('-'))
        p_FTM = float(p_FTM_FTA[0])
        
        p_FTA = float(p_FTM_FTA[-1])
        p_ftPercent = float(p[name][6])
        p_Off_Rebounds = float(p[name][7])
        p_Def_Rebounds = float(p[name][8])
        p_Rebounds = float(p[name][9])
        p_PF = float(p[name][10])
        p_Assists = float(p[name][11])
        p_Turnovers = float(p[name][12])
        p_Blocks = float(p[name][13])
        p_Steals = float(p[name][14])
        p_Points = float(p[name][-1])

        #t_minutesPlayed = t[name][0]
        #t_threePointsAttempted = p[name][1]
        #t_threePointsMade = p[name][2]
        t_FGM_FGA= t[3].split('-')
        t_fgMade = float(t_FGM_FGA[0])
        #t_fgPercent = p[name][4] # DONT NEED I THINK
        #t_FTM_FTA = t[name][5].split('-')
        #t_ftm_hyphin_fta = t_FTM_FTA[1]
        #t_ftPercent = p[name][6]
        t_Off_Rebounds = float(t[7])
        t_Def_Rebounds = float(t[8])
        t_PF = float(t[10])
        t_Assists = float(t[11])
        t_Turnovers = float(t[12])
        t_Blocks = float(t[13])
        t_Steals = float(t[14])
        t_Points = float(t[15])


        if t_fgMade==0:
            s_Assist = 0
            
        else:
            s_Assist = (p_Assists / t_fgMade) * t_Points
        
        if t_Points == 0:
            s_Point = 0

        else:
            s_Point = p_Points * (1 + (p_Points/t_Points))
        
        if  t_Off_Rebounds == 0 and t_Def_Rebounds == 0:
            s_Rebound = 0
        
        elif t_Off_Rebounds == 0 and t_Def_Rebounds > 0:
            ((p_Def_Rebounds/t_Def_Rebounds)+1) * p_Def_Rebounds
        
        elif t_Off_Rebounds > 0 and t_Def_Rebounds ==0:
            s_Rebound = ((p_Off_Rebounds/t_Off_Rebounds) + 1)* p_Off_Rebounds * 1.25
        
        else:
            s_Rebound = ((p_Off_Rebounds/t_Off_Rebounds) + 1)* p_Off_Rebounds * 1.25 + ((p_Def_Rebounds/t_Def_Rebounds)+1) * p_Def_Rebounds


        if t_Steals == 0:
            s_steals = 0
        else:
            s_Steals = math.exp(p_Steals/t_Steals) * p_Steals * 2

        if t_Blocks == 0:
            s_Blocks = 0
        else:
            s_Blocks = math.exp(p_Blocks/t_Blocks) * p_Blocks * 2
        
        if p_Assists > 0 and t_Turnovers > 0:
            s_Turnover = math.exp(p_Turnovers/t_Turnovers) * (p_Turnovers/p_Assists + 1) * p_Turnovers
        
        elif p_Assists == 0 and t_Turnovers > 0:
            s_Turnover = math.exp(p_Turnovers/t_Turnovers) * p_Turnovers
        
        elif p_Assists > 0 and t_Turnovers == 0:
            s_Turnover = (p_Turnovers/p_Assists + 1) * p_Turnovers
        
        else:
            s_Turnover = 0


        s_PF = math.exp(p_PF/6)*p_PF
        
        if p_FTA == 0 or p_FGA == 0:
            s_Efficiency = 0
            
        else:
            s_Efficiency = (((0.5*p_Points)/(p_FGA+0.475*p_FTA))+1)*p_Points

        PVR = s_Assist + s_Point + s_Rebound + s_Steals + s_Blocks + s_Efficiency - s_Turnover - s_PF
        

        # add name, pvr, points, assists, repbound
        newList.append([name, PVR, p_Points, p_Assists, p_Rebounds])
    del newList[0]

    PVR_list = []
    for pvr in newList:
        PVR_list.append(pvr[1])
    
    top_PVR_List = sorted(PVR_list, reverse=True)
    
    MAIN_RETURN = [[]]
    for x in range(10):
        MAIN_RETURN.append(newList[PVR_list.index(top_PVR_List[x])])
    
    
    del MAIN_RETURN[0]

    return MAIN_RETURN
