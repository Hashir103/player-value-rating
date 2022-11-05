import re
from bs4 import BeautifulSoup
import requests

def getHTMLVer(url):
    return requests.get(url).text

doc = getHTMLVer("https://usportshoops.ca/history/show-game-report.php?Gender=MBB&Season=2022-23&Gameid=M20221104QUENIP")
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

print(val1)
print()
print(val2)