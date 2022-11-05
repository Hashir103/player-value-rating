def givenVal(vals, vals2):

    stats_1 = vals[0]
    stats_2 = vals2[0]

    if len(stats_1) > len(stats_2):
        bigger = stats_1
        smaller = stats_2
    else:
        bigger = stats_2
        smaller = stats_1

    for key in bigger:
        if key in smaller:
            for x in range(len(bigger[key])):
                if "-" not in bigger[key][x]:
                    bigger[key][x] = str((float(bigger[key][x]) + float(smaller[key][x]))/2)
                else:
                    temp = bigger[key][x].split("-")
                    temp2 = smaller[key][x].split("-")

                    temp[0] = (float(temp[0]) + float(temp2[0]))/2
                    temp[1] = (float(temp[1]) + float(temp2[1]))/2

                    bigger[key][x] = f"{temp[0]}-{temp[1]}"


    for x in range(len(vals[1])):
        if "-" in vals[1][x]:
            temp = vals[1][x].split("-")
            temp2 = vals2[1][x].split("-")

            temp[0] = (float(temp[0]) + float(temp2[0]))/2
            temp[1] = (float(temp[1]) + float(temp2[1]))/2
            vals[1][x] = f"{temp[0]}-{temp[1]}"
        else:
            vals[1][x] = str((float(vals[1][x]) + float(vals2[1][x]))/2)

        
    return [bigger, vals[1]]