import math
# p = { "Player Name":[0 MINS,1 3PA-3PM, 2 P%, 3 FGM-FGA, 4 FG%, 5 FTM-FTA, 6 FT%, 7 OREB, 8 DREB, 9 TREB, 10 PF, 11 A, 12 TO,13 BLK, 14 STL , 15 PTS]  
# t = [0 MINS, 1 3PM-3PA, 2 3P%, 3 FGM-FGA, 4 FG%, 5 FTM-FTA, 6 FT%, 7 OREB, 8 DREB, 9 TREB, 10 PF, 11 A, 12 TO, 13 BLK, 14 STL, 15 PTS]


p = {'Luka Syllas': ['37', '0-0', '0.0', '10-20', '50.0', '4-6', '66.7', '2', '2', '4', '3', '5', '0', '0', '1', '24'], 
    'Connor Keefe': ['30', '0-0', '0.0', '7-18', '38.9', '7-11', '63.6', '4', '6', '10', '2', '2', '2', '0', '0', '21'], 
    'Connor Kelly': ['29', '4-7', '57.1', '5-9', '55.6', '0-0', '0.0', '1', '4', '5', '5', '0', '0', '0', '2', '14'], 
    'Cameron Bett': ['29', '1-8', '12.5', '1-10', '10.0', '5-6', '83.3', '0', '2', '2', '3', '3', '2', '0', '0', '8'], 
    'Sebastian Campbell': ['8', '0-1', '0.0', '1-7', '14.3', '3-5', '60.0', '3', '5', '8', '1', '1', '0', '0', '0', '5'], 
    'Gianni Itegeli': ['11', '0-0', '0.0', '2-3', '66.7', '0-0', '0.0', '0', '1', '1', '0', '0', '0', '0', '0', '4'], 
    'Michael Kelvin': ['11', '0-1', '0.0', '1-2', '50.0', '0-0', '0.0', '1', '1', '2', '1', '0', '0', '0', '0', '2'], 
    'Samuel Kong': ['0', '0-0', '0.0', '1-1', '100.0', '0-0', '0.0', '0', '0', '0', '0', '0', '0', '0', '1', '2'], 
    'Isaac Krueger': ['15', '0-0', '0.0', '0-2', '0.0', '1-2', '50.0', '0', '4', '4', '4', '1', '1', '1', '0', '1'], 
    'David Ayon': ['16', '0-1', '0.0', '0-1', '0.0', '0-0', '0.0', '2', '2', '4', '1', '0', '2', '0', '0', '0'], 
    'Ryan Heim': ['10', '0-1', '0.0', '0-1', '0.0', '0-0', '0.0', '0', '0', '0', '2', '0', '3', '0', '0', '0'], 
    'Scott Jenkins': ['6', '0-0', '0.0', '0-0', '0.0', '0-0', '0.0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], 
    'Filip Subotic': ['1', '0-0', '0.0', '0-0', '0.0', '0-0', '0.0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    'my king': ['47', '3-7', '43.9', '19-32', '59.4', '10-11', '90.9', '4', '4', '8', '2', '8', '5', '1', '1', '51']} 
    


t =  ['203', '10-37', '27', '44-99', '44.4', '16-22', '72.7', '19', '34', '53', '18', '18', '11', '3', '5', '200']


def calculatePVR(p,t):
    # p is dictionary of players
    # t is the list of the stats

    # p = { "Player Name":[0 MINS,1 3PA-3PM,3 FGM-FGA,4 FG%,5 FTM-FTA,6 FT%,7 OREB,8 DREB,9 TREB,10 PF,11 A,12 TO,13 BLK,14 STL ,29 PTS]  
    # t = [0 MINS, 1 3PA, 2 3PM, 3 FGM/FGA, 4 FG%, 5 FTM/FTA, 6 FT%, 7 OREB, 8 DREB, 9 TREB, 10 PF, 11 A, 12 TO, 13 BLK, 14 STL, 15 PTS]

    newList = [[]]
    for key in p:

        name = key
        p_minutesPlayed = p[name][0]
        p_3PM_3PA= (p[name][1].split('-'))
        p_3PM = int(p_3PM_3PA[0])
        p_3PA = float(p_3PM_3PA[-1])
        p_FGM_FGA = (p[name][3].split('-'))
        p_FGM = float(p_FGM_FGA[0])
        p_FGA = float(p_FGM_FGA[-1])
        p_fgPercent = float(p[name][4]) # DONT NEED I THINK
        p_FTM_FTA = (p[name][5].split('-'))
        p_FTM = int(p_FTM_FTA[0])
        p_FTA = int(p_FTM_FTA[1])
        p_ftPercent = float(p[name][6])
        p_Off_Rebounds = int(p[name][7])
        p_Def_Rebounds = int(p[name][8])
        p_Rebounds = int(p[name][9])
        p_PF = int(p[name][10])
        p_Assists = int(p[name][11])
        p_Turnovers = int(p[name][12])
        p_Blocks = int(p[name][13])
        p_Steals = int(p[name][14])
        p_Points = int(p[name][15])

        #t_minutesPlayed = t[name][0]
        #t_threePointsAttempted = p[name][1]
        #t_threePointsMade = p[name][2]
        t_FGM_FGA= t[3].split('-')
        t_fgMade = float(t_FGM_FGA[0])
        #t_fgPercent = p[name][4] # DONT NEED I THINK
        #t_FTM_FTA = t[name][5].split('-')
        #t_ftm_hyphin_fta = t_FTM_FTA[1]
        #t_ftPercent = p[name][6]
        t_Off_Rebounds = int(t[7])
        t_Def_Rebounds = int(t[8])
        t_PF = int(t[10])
        t_Assists = int(t[11])
        t_Turnovers = int(t[12])
        t_Blocks = int(t[13])
        t_Steals = int(t[14])
        t_Points = int(t[15])


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
        

        print(s_Assist)
        print(s_Point)
        print(s_Rebound)
        print(s_Steals)
        print(s_Blocks)
        print(s_Efficiency)
        print(s_Turnover)
        print(s_PF)

        PVR = s_Assist + s_Point + s_Rebound + s_Steals + s_Blocks + s_Efficiency - s_Turnover - s_PF
        

        # add name, pvr, points, assists, repbound
        newList.append([name, PVR, p_Points, p_Assists, p_Rebounds])
    del newList[0]
    print(newList)

    PVR_list = []
    for pvr in newList:
        PVR_list.append(pvr[1])
    
    top_PVR_List = sorted(PVR_list, reverse=True)
    
    MAIN_RETURN = [[]]
    for x in range(10):
        MAIN_RETURN.append(newList[PVR_list.index(top_PVR_List[x])])
    
    
    del MAIN_RETURN[0]
    
    print()
    print(top_PVR_List)
    print()
    print(MAIN_RETURN)

    return MAIN_RETURN





# p = { "Player Name":[0 MINS,1 3PA-3PM, 2 FGM-FGA, 3 FG%, 4 FTM-FTA, 5 FT%, 6 OREB, 7 DREB, 8 TREB, 9 PF, 10 A, 11 TO,12 BLK, 13 STL , 14 PTS]  
# t = [0 MINS, 1 3PA-3PM, 2 FGM/FGA, 3 FG%, 4 FTM-FTA, 5 FT%, 6 OREB, 7 DREB, 8 TREB, 9 PF, 10 A, 11 TO, 12 BLK, 13 STL, 14 PTS]


calculatePVR(p,t)