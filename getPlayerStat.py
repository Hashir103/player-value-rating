import re
from bs4 import BeautifulSoup
import requests

def getHTMLVer(url):
    return requests.get(url).text

doc = getHTMLVer("https://usportshoops.ca/history/show-game-report.php?Gender=MBB&Season=2022-23&Gameid=M20221104QUENIP")
soup = BeautifulSoup(doc, "html.parser")

print(soup.find_all('table')[5])
