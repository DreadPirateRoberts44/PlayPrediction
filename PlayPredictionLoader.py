""""
This code is for generating the feature and target data for the classifier

This is where we can:

    - experiement with different modifications while parsing the csv
    - try testing different datasets

"""

import csv
import numpy as np

""""
This function returns the status for a play type

-1 - the play type is not valid

0 - the play type is a pass (designated as the negative class)

1 - the play type is a rush (designated as the postive class)

play types are listed at https://collegefootballdata.com/exporter

extra points are excluded, might be their own model

penalaties, safties, fumbles can't be reliably determined from the available data
"""
def getPlayStatus(playType):    
    if playType.startswith('Rush'): return 1 #all rushes start with Rush
    if playType.startswith('Pass'): return 0 #passing plays either start with pass
    if playType == "Sack": return 0 # sacks count as passes from a play call perspective
    if playType.startswith('Interception'): return 0 #passing plays also start with interception
    return -1

"""
Returns a dictionary all teams, with the key being the name, value being the id
(needed when if/when team ids are included in the model)
"""
def getTeams():
    teams = {}
    with open("TeamIds.csv", mode='r', encoding='utf-8-sig') as file:
        teamCSV = csv.DictReader(file)
        for lines in teamCSV:
            teams[lines['School']] = lines["Id"]
    return teams


def getCurrentPlay(teams,currentLine,playStatus):
     
    #offense = int(teams[currentLine['Offense']])
    #defense = int(teams[currentLine['Defense']])
    timeRemaining = 60 * int(currentLine['Clock Minutes']) + int(currentLine['Clock Seconds'])
    if playStatus == 1 : yardsRushing += int(currentLine['Yards Gained'])
    else: yardsPassing += int(currentLine['Yards Gained'])
    currentPlay = [#offense, 
                #defense, 
                int(currentLine['Offense Score']),
                int(currentLine['Defense Score']), 
                int(currentLine['Period']), 
                timeRemaining, 
                int(currentLine['Offense Timeouts']),
                int(currentLine['Defense Timeouts']),
                int(currentLine['Yards To Goal']),
                int(currentLine["Down"]),
                int(currentLine['Distance']),
                ]
    return currentPlay



def getAllPlayData(teams):
    
    totalRows = 0
    validRows = 0
    playStatus = 0
  
    currentPlay = []

    #yardsPassing = 0 maybe revisit
    #yardsRushing = 0
    
    playList = []
    statusList = []
    with open("2023_OSU_At_IND_OSU_Plays_Only.csv", mode='r', encoding='utf-8-sig') as file:
            playCSV = csv.DictReader(file)
            for lines in playCSV:
                totalRows +=1 
                playStatus = getPlayStatus(lines['Play Type'])
                if playStatus == -1: continue #valid rows will not have a play status of -1, defined in getPlayStatus
                if lines['Offense Timeouts'] == "" or int(lines['Offense Timeouts']) < 0: continue
                if lines['Defense Timeouts'] == "" or int(lines['Defense Timeouts']) < 0: continue
                validRows += 1
                
                #"Scoring","Yards Gained" revisit scoring/Yards gained later
                # if we're going to care about those values, we're likely going to need to put the database in play order per game
                playList.append(currentPlay)
                statusList.append(playStatus)
    return playList,statusList
            
            


"""
The function to call to load all the training/testing data

returns the feature and target arrays following the expectation of sklearn as X,y

TODO segment into smaller functions

TODO experiment with ways to improve (duh)

"""
def getData():
    
    teams = getTeams()
    playList, statusList = getAllPlayData(teams)

    X = np.array(playList)
    y = np.array(statusList)
    return X,y