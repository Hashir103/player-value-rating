def getAvg(l1, l2):
    hypVals = [[]]
    for x in range(len(l2)):
        hypValsAdd = []
        for y in range(len(l2[x])):
            if "-" in l2[x][y]:
                broken= l2[x][y].split("-")
                broken= [float(broken[0]), float(broken[1])]
                hypValsAdd.append(broken)
                l2[x][y] = 0
            else:
                l2[x][y] = float(l2[x][y])
        hypVals.append(hypValsAdd)
    
    del hypVals[0]

    teamTotals = [ sum(x)/len(x) for x in zip(*l2) ]
    hypValsTotal = hypVals[0]
    for x in range(1, len(hypVals)):
        for y in range(len(hypVals[x])):
            hypValsTotal[y][0] += hypVals[x][y][0]
            hypValsTotal[y][1] += hypVals[x][y][1]

    for x in range(len(hypValsTotal)):
        for y in range(len(hypValsTotal[x])):
            hypValsTotal[x][y] /= len(hypVals)
    
    
    for x in range(len(teamTotals)):
        if x == 1:
            teamTotals[x] = str(hypValsTotal[0][0])+"-"+str(hypValsTotal[0][1])
        elif x == 3:
            teamTotals[x] = str(hypValsTotal[1][0])+"-"+str(hypValsTotal[1][1])
        elif x == 5:
            teamTotals[x] = str(hypValsTotal[2][0])+"-"+str(hypValsTotal[2][1])
        

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
