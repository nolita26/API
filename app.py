import datetime
import requests
import json

acccess_token = 'c051d79a07484d10219f86aacd41'

urlToHit = 'https://candidate.hubteam.com/candidateTest/v3/problem/dataset?userKey='+acccess_token

response = requests.get(urlToHit)
data= json.loads(response.content)


allEvents = data['events']

allVisitorsSessions = {}
for event in allEvents:
    currVisitorID = event['visitorId']
    currPage = event['url']
    currTS = event['timestamp']
    if(currVisitorID not in allVisitorsSessions.keys()):
        allVisitorsSessions[currVisitorID] = {}
        
    allVisitorsSessions[currVisitorID][currTS] = currPage

toSendJson = {}

for visitor in allVisitorsSessions:
    # print(visitor)
    sessionsByGroup = []
    prevTimeStamp = None
    for timestamp in sorted (allVisitorsSessions[visitor].keys()) :
        # print(timestamp)
        page_url = allVisitorsSessions[visitor][timestamp]
        if(prevTimeStamp == None):
            group = {
                "duration": 0,
                "pages": [page_url],
                "startTime" : timestamp
            }
            prevTimeStamp = timestamp
            sessionsByGroup.append(group)
        else:
            converted_timestamp = datetime.datetime.fromtimestamp(round(timestamp / 1000))
            converted_prevTimeStamp = datetime.datetime.fromtimestamp(round(prevTimeStamp / 1000))
            if ((converted_timestamp - converted_prevTimeStamp).total_seconds() <= 600.0):
                groupToUpdate = sessionsByGroup[len(sessionsByGroup)-1]
                duration = timestamp-groupToUpdate['startTime']
                groupToUpdate["duration"] = duration
                groupToUpdate["pages"].append(page_url)

                sessionsByGroup[len(sessionsByGroup)-1] = groupToUpdate
                prevTimeStamp = timestamp
            else:
                group = {
                    "duration": 0,
                    "pages": [page_url],
                    "startTime" : timestamp
                }
                prevTimeStamp = timestamp
                sessionsByGroup.append(group)

    toSendJson[visitor] = sessionsByGroup
    # break

finalDictionary = {
    "sessionsByUser" : toSendJson
}
jsonObject = json.dumps(finalDictionary)

payload = jsonObject
headers = {'Content-type': 'application/json'}
finalResponse = requests.post('https://candidate.hubteam.com/candidateTest/v3/problem/result?userKey=c051d79a07484d10219f86aacd41',
                data=payload,
                headers=headers)

print(finalResponse.content)
print("***********************************")
print("***********************************")
print("***********************************")
print(finalResponse.status_code)





    
        





