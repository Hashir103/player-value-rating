from bs4 import BeautifulSoup, SoupStrainer
import requests
import time
# import re
import json

'''teamImages.py: This script, when possible, scrapes all the team images and stores them into their respective JSON Files'''

start_time = time.time()

def getTeamURL(url):
    return requests.get(url).text

rosters = {
    "type_1":{
        "toronto":"https://varsityblues.ca/sports/mens-basketball/roster?path=mbball",
        "mcmaster":"https://marauders.ca/sports/mens-basketball/roster?path=mbball",
        "brock":"https://gobadgers.ca/sports/mens-basketball/roster",
        "nipissing":"https://nulakers.ca/sports/mens-basketball/roster",
        "ontario tech":"https://goridgebacks.com/sports/mens-basketball/roster",
        "queens":"https://gogaelsgo.com/sports/mens-basketball/roster",
        "tmu":"https://tmubold.ca/sports/mens-basketball/roster",
        "waterloo":"https://athletics.uwaterloo.ca/sports/mens-basketball/roster",
        "western":"https://westernmustangs.ca/sports/mens-basketball/roster",
        "wilfrid":"https://laurierathletics.com/sports/mens-basketball/roster",
        "york":"https://yorkulions.ca/sports/mens-basketball/roster"
    },

    "type_2":{
        "algoma":"https://algomathunderbirds.ca/sports/mens-basketball/roster?path=mbball",
        "guelph":"https://gryphons.ca/sports/basketball-men/roster",
        "windsor":"https://golancers.ca/sports/mens-basketball/roster"
    },

    "type_3":{
        "carleton":"https://goravens.ca/teams/mens-basketball/roster/"
    },

    "type_4":{
        "lakehead":"http://thunderwolves.ca/view-roster/basketball-m/"
    },

    "type_5":{
        "laurentian":"https://www.luvoyageurs.com/sports/mbkb/2022-23/roster", 
        "ottawa":"https://teams.geegees.ca/sports/mbkb/2022-23/roster"
    },
   
}

def getTeamType1(url):
    '''
    Params: - url is a string containing the url of the team page
    Returns: None

    This function dumps the team names/pictures into a json file for the type 1 websites. (shown above)
    '''
    if ".com" in url:
        urlString=url[:url.index(".com")+4]
    else:
        urlString=url[:url.index(".ca")+3]
    url= getTeamURL(url)
    restriction = SoupStrainer(attrs={"class":"lazyload"})
    soup = str(BeautifulSoup(url, "lxml", parse_only=restriction))
    soup = soup.split("<img alt=")

    team = {}

    for x in range(len(soup)):
        if "data-src" in soup[x] and "?width=80" in soup[x]:
            soup[x] = soup[x].replace(" class=\"lazyload\" data-src=", "")
            soup[x] = soup[x].replace("\"", "")
            soup[x] = soup[x].replace("/>", "")
            soup[x] = soup[x].replace("?width=80", "")

            name=soup[x][:soup[x].index("/")]
            img=urlString+soup[x][soup[x].index("/"):]

            '''This was a regex solution for Nipissing which did not have alt tag on their images.'''
            # name =img[37:-4]
            # name = re.sub(r'[0-9]+', '', name)
            # name = name.replace("_", " ").strip()

            team[name] = img

    '''JSON Dump - do not use unless nec'''
    with open("teams/error.json", "w") as outfile:
        json.dump(team, outfile)       
    
def getTeamType2(url):
    '''
    Params: - url is a string containing the url of the team page
    Returns: None

    This function dumps the team names/pictures into a json file for the type 2 websites. (shown above)
    '''
    if ".com" in url:
        urlString=url[:url.index(".com")+4]
    else:
        urlString=url[:url.index(".ca")+3]
    url= getTeamURL(url)
    restriction = SoupStrainer(attrs={"class":"sidearm-roster-player-image-container"})
    soup = str(BeautifulSoup(url, "lxml", parse_only=restriction)).split('\n')

    team = {}

    for x in soup:
        if "sidearm-roster-player-image relative lazy" in x:
            img = x[84:]
            if ".png" in img:
                img = img[:img.index(".png")+4]
            else:
                img = img[:img.index(".")+4]
                img = urlString+img
        if "sidearm-roster-player-bio-link" in x:
            name = x[x.index("title=")+7:x.index("- View")].strip()
            team[name] = img

    '''JSON Dump - do not use unless nec'''
    with open("teams/guelph.json", "w") as outfile:
        json.dump(team, outfile)   

def getTeamType3():
    '''
    Params: - url is a string containing the url of the team page
    Returns: None

    This function dumps the team names/pictures into a json file for the type 3 websites. (shown above)
    '''   
    
    # turns out carleton already has a json with the information we need. but there's extra stuff we need to modify
    f = open("teams/carleton.json")
    teamData = json.load(f)

    team = {}

    for player in teamData['records']:
        name = player['fields']['Calculation'] + " " + player['fields']['Last Name']
        img = player['fields']['Photo']
        team[name] = img

    '''JSON Dump - do not use unless nec'''
    with open("teams/carleton2.json", "w") as outfile:
        json.dump(team, outfile)

def getTeamType4(url):
    '''
    Params: - url is a string containing the url of the team page
    Returns: None

    This function dumps the team names/pictures into a json file for the type 4 websites. (shown above)
    '''   

    if ".com" in url:
        urlString=url[:url.index(".com")+4]
    else:
        urlString=url[:url.index(".ca")+3]
    url= getTeamURL(url)
    restriction = SoupStrainer(attrs={"class":"card"})
    soup = str(BeautifulSoup(url, "lxml", parse_only=restriction)).split('\n')

    team = {}

    for x in soup:
        if "img" in x:
            img = x[46:x.index(".jpg")+4]
        if "h2" in x:
            name = x[x.index("#")+1:x.index("</a>")]
            name = name[name.index(" ")+1:]

            team[name] = img


    '''JSON Dump - do not use unless nec'''
    with open("teams/lakehead.json", "w") as outfile:
        json.dump(team, outfile)

# laurentian and ottawa 403 so we do this manually

print(f"\nExeuction completed in {time.time() - start_time} seconds")
