#!/usr/bin/env python

"""main.py: This file executes the main python code to run the PVR stat on all teams and display the output on a web application using flask."""

from webParsing import *
from calculations import *
from flask import Flask, render_template, redirect, url_for
import json
import time

def main():
    '''This is the main function, where all execution of the code occurs'''

    start_time = time.time()

    # how many recent games do we check
    magic_number = 5

    # get the main team page for each team
    teams = getTeamPages()
    teamPVR = {}

    top_players = {}
    top_pvrs = []

    # get the teams most recent 5 games and their PVRs
    for team in teams:
        teams[team].append(getTeamGames(teams[team][0], magic_number))
        teamPVR[team] = getTeamPVR(team, teams[team][1])
        
        # we only want players who've played all games, and their photos
        if teamPVR[team][0][-1] == magic_number:
            toAdd = teamPVR[team][0]
            
            photoLink = "team-photos/" + team + ".json"

            data = json.load(open(photoLink))

            if teamPVR[team][0][0] in data:
                toAdd.append(data[teamPVR[team][0][0]])
            else:
                toAdd.append("https://www.pngitem.com/pimgs/m/504-5040528_empty-profile-picture-png-transparent-png.png")
                
                
            uniName = team
            if uniName == "wilfrid":
                uniName = "WLU"
            else:
                uniName = uniName.title()
            
            toAdd.append(uniName)

            top_players[teamPVR[team][0][1]] = toAdd
            top_pvrs.append(teamPVR[team][0][1])

    # get the top 3 PVRs in the league
    top_pvrs.sort()
    top_pvrs.reverse()
    top_pvrs = top_pvrs[:3]

    for x in range(len(top_pvrs)):
        top_pvrs[x] = top_players[top_pvrs[x]]

    app = Flask(__name__)

    @app.route("/")
    def home():
        return render_template("index.html", top=top_pvrs)

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
            tName = name
            return render_template("team.html", teamStats=teamPVR[tName])

        else:
            return redirect(url_for("home"))

    print(f"\nExecution finished in {time.time() - start_time} seconds")

    app.run()

if __name__ == "__main__":
    main()