def getAvg(l1, l2):
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
                    teamTotals[y] += float(l2[x][y])/len(l2)
                else:
                    CalcOk = True
            else:
                CalcOk = False
                val = l2[x][y].split("-")
                val[0] = float(val[0]) / len(l1)
                val[1] = float(val[1]) / len(l1)

                teamTotals[y] = str(
                    val[0] + float(teamTotals[y].split("-")[0])
                ) + "-" + str(
                    val[1] + float(teamTotals[y].split("-")[1])
                )
    
    for x in range(1, 6, 2):
        val = teamTotals[x].split("-")
        
        if val[1] == 0:
            teamTotals[x+1] = 0
        else:
            teamTotals[x+1] = (float(val[0])/float(val[1]))*100


    for d in l1:
        for key in d:
            for val in range(len(d[key])):
                if "-" not in d[key][val]:
                    d[key][val] = float(d[key][val])
    
    new_d = l1[0]

    toCalc1 = True
    for key in new_d:
        for x in range(len(new_d[key])):
            if "-" not in str(new_d[key][x]):
                if toCalc1:
                    new_d[key][x] = (new_d[key][x])/len(l1)
                else:
                    toCalc1 = True
            else:
                    val = ''.join(new_d[key][x])
                    val = val.split("-")
                    val[0] = float(val[0]) / len(l1)
                    val[1] = float(val[1]) / len(l1)
                    new_d[key][x] = str(val[0]) + "-" + str(val[1])
                    if (val[1]+float(new_d[key][x].split("-")[1])) != 0:
                        percentage = (val[0]+float(new_d[key][x].split("-")[0]))/(val[1]+float(new_d[key][x].split("-")[1]))
                    else:
                        percentage = 0
                        new_d[key][x+1] = percentage
                        toCalc1 = False

    toCalc = True
    for p in range(1, len(l1)):
        for key in l1[p]:
            if key not in new_d:
                new_d[key] = l1[p][key]
            else:
                for x in range(len(new_d[key])):
                        if "-" not in str(new_d[key][x]):
                            if toCalc:
                                new_d[key][x] += (l1[p][key][x])/len(l1)
                            else:
                                toCalc = True
                        else:
                            val = ''.join(l1[p][key][x])
                            val = val.split("-")
                            val[0] = float(val[0]) / len(l1)
                            val[1] = float(val[1]) / len(l1)
                            
                            if (val[1]+float(new_d[key][x].split("-")[1])) != 0:
                                percentage = (val[0]+float(new_d[key][x].split("-")[0]))/(val[1]+float(new_d[key][x].split("-")[1]))
                            else:
                                percentage = 0
                            new_d[key][x+1] = percentage
                            toCalc = False
                            new_d[key][x] = str(val[0]+float(new_d[key][x].split("-")[0])) + "-"+str(val[1]+float(new_d[key][x].split("-")[1]))
            

    return [new_d, teamTotals]
