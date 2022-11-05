from bs4 import BeautifulSoup
import requests
import re

def getPlyTeamStats(teamMod, link):
    def getHTMLVer(url):
        return requests.get(url).text

    team = teamMod
    doc = getHTMLVer(link)
    soup = BeautifulSoup(doc, "html.parser")

    val = str(soup.find_all('table')[5])
    replacements = [
        ("</td>", ""),
        ("<td>", ""),
        ("<tr>", ""),
        ("*", ""),
        ("</tr>", ""),
        ("<b>", ""),
        ("</b>", ""),
        ('</table>', ""),
        ('<td align="left" colspan="3">', ""),
        ("<td align=\"right\">", "|"),
        ("<td align=\"left\">", ""),
        ("<td align=\"center\">", "|"),
        ('<table border="0" cellpadding="1" cellspacing="1" width="100%">', ""),
        ('<td colspan="26">', ""),
        ('<th align="left" colspan="3">Player|<th>Mins|<th colspan="2">3 Pt|<th colspan="2">Total FG|<th colspan="2">Free throws|<th colspan="3">Rebounds|<th>PF|<th>A<th>TO<th>Blk<th>Stl|<th>Pts</th></th></th></th></th></th></th></th></th></th></th></th>', "")
    ]
    for old, new in replacements:
        val = val.replace(old, new)

    val = val.split("\n")

    for x in range(len(val)):
        if "Totals" in val[x]:
            cutOff = x
            break

    val1 = val[:cutOff+1]
    val2 = val[cutOff+1:]

    while "" in val1 or "" in val2:
        if "" in val1:
            del val1[val1.index("")]
        if "" in val2:
            del val2[val2.index("")]

    val1[0] = re.sub(r'\W+', '', val1[0])
    if len(val2) != 0:
        val2[0] = re.sub(r'\W+', '', val2[0])

    if team in val1[0].lower():
        val = val1
    else:
        val = val2

    del val[0]
    teamVal = None
    d = {}

    for x in val:
        if x != val[-1]:
            x = re.sub("[|]", ' ', x)
            x = x.split()
            x[0] = re.sub("[^a-z_A-Z]", "", x[0])
            x[0] = x[0] + " " + x[1]
            del x[1]
            name = x[0]
            del x[0]
            while len(x) > 16:
                del x[0]
            d[name] = x
        else:
            x = re.sub("[|]", ' ', x)
            x = x.split()
            x[0] = re.sub("[^a-z_A-Z]", "", x[0])
            x[0] = x[0] + " " + x[1]
            del x[1]
            name = x[0]
            del x[0]
            teamVal = x
    
    return [d, teamVal]