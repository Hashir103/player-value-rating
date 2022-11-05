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
    ("</tr>", ""),
    ("<b>", ""),
    ("</b>", ""),
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

print(val)