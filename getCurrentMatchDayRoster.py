# Schreibe hier Deinen Code :-)
import os
import uuid

import getCurrentMatchDay 

#import MySQLdb as mdb
from time import sleep
#import syslogLiga
import ligaTarget
import requests

import coloredOutput

def getMatchDayRoster(iMatchDay):
    baseURLMatchRoster= "https://api.openligadb.de/getmatchdata/bl1/2021/" + str (iMatchDay)
    if ligaTarget.bVerbose:
        coloredOutput.printQry(baseURLMatchRoster)

    try:
        responseMatchDay = requests.get(baseURLMatchRoster)
    except requests.exceptions.HTTPError as e:
        print( e)

    jsonResp = responseMatchDay.json()
    for match in jsonResp:
        print ("Match ID:     " + str( match["matchID"]) )
        print ("Date:         " + match["matchDateTimeUTC"])
        print ("Team 1:       " + str(match["team1"]["teamName"])  + ":" + str(match["team2"]["teamName"]) )
        #print ("Team 2:       " + str( match["team2"]) )

    jsMatchDay ={}
    return jsMatchDay

    return 0



# here we start with the actual process to
# - create a unique measurement UID
# - read all sensors
# - write sensor data into local DB with MeasurementID, ConfigId
#
# Next we will want to transfer results to the host. The sendTemperature()
# module will catch all sensors for given measurement ID and transfer to host
#
# 10000000e780fb4f - host id

import argparse

# start of actual python code when inviked by CLI
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='readTemperature.py - This tool reads temps on client and writes to DB and sends to host')
    parser.add_argument("-v","--verbosity", action="count", help="increase output verbosity")
    parser.add_argument("-d","--day", action="store", help="matchday")
    parser.add_argument("-y","--year", action="store", help="year")

    args = parser.parse_args()


    strHostVerbose = "False"

    if args.verbosity:
        strHostVerbose="True"
        coloredOutput.printSuperVerbose("verbosity turned on")
        ligaTarget.bVerbose=True

    if (ligaTarget.bVerbose):
        coloredOutput.printLog("\n*** getCurrentMatchDay.py***")

    strMatchDay = ""

    if args.day:
        strMatchDay = args.day
        coloredOutput.printSuperVerbose("Matchday: " + strMatchDay + " (OVERRIDE)")
    else:
        strMatchDay = str(getCurrentMatchDay.getCurrentMatchDay())
        print("Matchday: " + strMatchDay )

    if args.year:
        strMatchYear=args.year
    else:
        strMatchYear = "2021"

    

    if (ligaTarget.bVerbose):
        coloredOutput.printSuperVerbose("Message: " + strMatchYear + " will be used as year.")
    if (ligaTarget.bVerbose):
        coloredOutput.printSuperVerbose("Macthday: " + strMatchDay + " will be used.")

    getMatchDayRoster(int(strMatchDay))

    
    if (ligaTarget.bVerbose):
        print("End of getCurrentMatchDay.py")