def getAvg(l1, l2):
    
    teamTotals = calcLofLs(l2, len(l2))

    playerTotals = {}

    for d in l1:
        for key in d:
            if key not in playerTotals:
                playerTotals[key] = [[]]

    for d in l1:
        for key in d:
            playerTotals[key].append(d[key])

    for key in playerTotals:
        if "team" in key:
            playerTotals.pop(key)
            break
        else:
            del playerTotals[key][0]

    for key in playerTotals:
        playerTotals[key] = calcLofLs(playerTotals[key], len(l1))

                
    return [playerTotals, teamTotals]

def calcLofLs(l2, gameAmt):
    teamTotals = [[]]

    for x in range(15):
        teamTotals.append(0)

    teamTotals[1] = "0-0"
    teamTotals[3] = "0-0"
    teamTotals[5] = "0-0"
    teamTotals[0] = 0

    CalcOk = True
    for x in range(len(l2)):
        for y in range(len(l2[x])):
            if "-" not in l2[x][y]:
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
    
    for x in range(1, 6, 2):
        val = teamTotals[x].split("-")
        
        if float(val[1]) == 0:
            teamTotals[x+1] = 0
        else:
            teamTotals[x+1] = (float(val[0])/float(val[1]))*100

    return teamTotals