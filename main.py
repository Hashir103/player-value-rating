import re
from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template
from getPlayerStat import *
from updateStats import *
from hackathon_calculatePVR import *

def getHTMLVer(url):
    return requests.get(url).text
# Dictionary indices:
# 0 - String to main web page (will get scraped initially for stats)
# 1 - List of 5 most recent games webpages (will get scraped for stats)
teams = {
    "algoma":[],
    "brock":[],
    "carleton":[],
    "guelph":[],
    "lakehead":[],
    "laurentian":[],
    "mcmaster":[],
    "nipissing":[],
    "ontario tech":[],
    "ottawa":[],
    "queens":[],
    "toronto metropolitan":[],
    "toronto":[],
    "waterloo":[],
    "western":[],
    "wilfrid laurier":[],
    "windsor":[],
    "york":[]
    }

for key in teams:
    if key == "wilfrid laurier":
        link = "https://usportshoops.ca/history/teamseason.php?Gender=MBB&Season=2022-23&Team=" + "WLUTeam"
    elif key == "toronto metropolitan":
        link = "https://usportshoops.ca/history/teamseason.php?Gender=MBB&Season=2022-23&Team=" + "TMUnow"
    else:
        link = "https://usportshoops.ca/history/teamseason.php?Gender=MBB&Season=2022-23&Team=" + re.sub(r'[^a-zA-Z\s]', '', key)
    teams[key].append(link)

def getGameLinks(team):
    doc = getHTMLVer(teams[team][0])
    soup = BeautifulSoup(doc, "html.parser")

    games = []
    for tag in soup.find_all('a'):
        if tag.string == "Stats":
            games.append(str(tag).replace("amp;", ""))

    games = games[-5:]
    toAdd = []
    for game in games:
        toAdd.append("https://usportshoops.ca" + str(game)[9:-11])

    teams[team].append(toAdd)

for team in teams:
    getGameLinks(team)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("webpage.html")

@app.route("/oua-central")
def choice_1():
    return render_template("ouacentral.html")

@app.route("/oua-eastern")
def choice_2():
    return render_template("ouaeast.html")

@app.route("/oua-western")
def choice_3():
    return render_template("ouawest.html")

@app.route("/about")
def choice_4():
    return render_template("about.html")

@app.route("/teams/<name>")
def user(name):
    if str(name) in teams:
        # totals = []
        # for game in teams[str(name).lower()][1]:
        #     totals.append(getPlyTeamStats(name, game))

        # l1 = []
        # l2 = []
        # for game in totals:
        #     l1.append(game[0])
        #     l2.append(game[1])

        # avg = getAvg(l1, l2)
        # pvr = calculatePVR(avg[0], avg[1])

        template = str(name) + ".html"

        return render_template(template)



    else:
        return f"Error! {name} is not a valid team."
    


if __name__ == "__main__":
    app.run(debug=True)

