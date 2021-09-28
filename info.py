import requests #                   used to fetch API from server
import json     #                   api is accessed as .json file extension so json library is neccasarry

margin = 0.8

auth_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiYzUzYTU0ZWQzOWVjMTQ3MTFmZWYyOTVhZjNiNjU1MTQ5OTNjOWMwNTFjZWNkMzQyNzk2ZjkxZTFhZjUyZjJhYmEwOGM3MzZmODQ0YmExZWEiLCJpYXQiOjE2MzA1ODAyMTEuNzExNDUzOSwibmJmIjoxNjMwNTgwMjExLjcxMTQ1NywiZXhwIjoyNTc3MjY4NjExLjYxODg4MzEsInN1YiI6IjkyODE0Iiwic2NvcGVzIjpbXX0.FjfcYrk3_6VCyN-KGbK1Y6B_5BK-P8fhHb6RpH-VxfXdMPWyr09ldmispBEM3auQ3hQ9o_wNlldiZ__VOXDvsB8plr0VfgbvSQgPbhHCDm4SbexQxmu40SJ-0jw3cZ5dGt85WJlV5kL05rg7gXObURIQsIMCUhRtYWmklS05Rjw2zipIpGyGAoqPrlK0k4ZxQUZTk37YuPZEKIQ5o0lDt5PCV3LEAqLHBYqE6Y3zoQh4_xXKOrSzllbuXsA_skRbEN3f37xNCpEf8XwzNOvLk01b9qg4F6OPEL58KF8IxMCznElSU17Xcz6eiY3x9lPyLFgfiO36HuhhNmOKDd6JJBqIxSzow004bFe0RPvTIFUxlkV1emIdIjiKgSJ0QosxYqvjEDqTm3UEHcOcG7uZjFJdn-adBKSGGLzsdAWXYaiYLSJr-RfXAIWtfI_6KJcTYcR9YDQB6-SaEUxAxDMICnHA4Enqiwy3blchcPwPQPFdos6tXB_6nfX15i-Lzxgcvl_zj7rZI7xRdxAf1TNpNE6EExz3DEl3EfCOLT--sGGfunjVPGWLWNgHIRpaN7Hr3jBoGotAlCN5q-R23zbu0EWxdVGIdp-bSkpPfHAVvF3qQ6ARlvsfNfketPSzMMyQ-vKsa0TRb5yPVKTQJkSUReVBMIXtIpUwFahaGtxxVeY" #Robot Events API auth token

url_base = "https://www.robotevents.com/api/v2/"
#Robot Events API server

headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(auth_token)}

def get_info(meta):

    api_url = '{0}{1}'.format(url_base, meta)

    response = requests.get(api_url, headers=headers)
    try:
        if response.status_code == 200:
            api_json = json.loads(response.content.decode('utf-8'))
            return api_json
        else:
            print("oops! Http Error {0} Occured".format(response.status_code))
    except:
        print("Request Failed", Exception)
        print("oops! Http Error {0} Occured".format(response.status_code))


def get_last_page(api_json):

    last_page = api_json["meta"]["last_page"]

    return last_page


def get_recent_event_info(api_json,last_page, page):

    all_info = []

    for i in range(int(last_page)-page, int(last_page)):
        all_info.append(get_info("events?page={0}".format(i)))

    return( all_info )

def check_empty(s):
    if len(str(s)) == 0 or str(s) == None:
        return "Unspecified"
    else:
        return s


def extract_event_data(event_data):
    event = []

    event.append("id: " + check_empty(str(event_data["id"])))
    event.append("name: " + check_empty(event_data["name"]))
    event.append("date: " + check_empty(event_data["start"].split("T")[0]))
    event.append("city: " + check_empty(event_data["location"]["city"]))
    event.append("country: " + check_empty(event_data["location"]["country"]))

    return event

    
def extract_team_data(team_data):
    team = []

    team.append("id: " + check_empty(str(team_data['id'])))
    team.append("number: " + check_empty(str(team_data['number'])))
    team.append("team name: " + check_empty(str(team_data['team_name'])))
    team.append("robot name: " + check_empty(str(team_data['robot_name'])))
    team.append("location: " + check_empty(str(team_data['location']['country'])))
    team.append("program: " + check_empty(str(team_data['program']['code'])))

    return team

def search_event_info(request, page, search):
    results = []


    try:
        result = get_info(request)

        results.append(result["meta"]["current_page"])
        results.append(result["meta"]["last_page"])

        for event in range(len(result["data"])):
            results.append(extract_event_data(result["data"][event]))
    except:
        pass

    return results
                

def search_team_info(request,page):
    results = []
       
    try:
        result = get_info(request)

        results.append(result["meta"]["current_page"])
        results.append(result["meta"]["last_page"])

        for team in range(len(result["data"])):
            results.append(extract_team_data(result["data"][team]))
    except:
        pass
    return results

def search_team_events(id):
    results = []

    try:
        result = get_info("teams/{0}/rankings?per_page=100".format(id))

        for event in range(len(result['data'])):
            eventresults = []
            eventresults.append(result['data'][event]["event"]["name"]) #event name
            eventresults.append(result['data'][event]["rank"]) #team ranking
            eventresults.append("wins: {0} losses: {1} ties: {2}".format(result["data"][event]["wins"],result["data"][event]["losses"],result["data"][event]["ties"])) # team win/loss/tie

            

            results.append(eventresults)
    except:
        pass

    return results

def search_team_awards(id):
    results = []

    try:
        result = get_info("teams/{0}/awards?per_page=100".format(id))
        for award in range(len(result['data'])):
            awardresults = []
            awardresults.append(result["data"][award]["event"]["name"]) #event
            awardresults.append(result["data"][award]["title"])         #award title

            results.append(awardresults)
    except:
        pass

    return results

def search_team_skills(id):
    pass

def search_event_teams(id):
    results = []

    try:
        result = get_info("events/{0}/teams?per_page=250".format(id))
        for team in range(len(result["data"])):
            teamresults = []
            teamresults.append(result["data"][team]["number"])
            teamresults.append(result["data"][team]["team_name"])

            results.append(teamresults)

    except:
        pass

    return results

def search_event_awards(id):
    results = []

    try:
        result = get_info("events/{0}/awards?per_page=250".format(id))
        for award in range(len(result["data"])):
            awardresults = []
            winners = []
            for team in range(len(result["data"][award]["teamWinners"])):
                winners.append(", " + result["data"][award]["teamWinners"][team]["team"]["name"])
            awardresults.append(result["data"][award]["title"])
            awardresults.append("".join(winners))

            print(awardresults)

            results.append(awardresults)
    except:
        pass

    return results