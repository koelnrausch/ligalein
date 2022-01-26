# Schreibe hier Deinen Code :-)
import os
import time
import pytz
import uuid

import getCurrentMatchDay 
import getCurrentMatchDayRoster

from datetime import datetime

#import MySQLdb as mdb
from time import sleep
#import syslogLiga
import ligaTarget
import requests

import coloredOutput
def waitForMatchDayStart(nextLocal):
    now = datetime.now()
    nowCET = local_timezone.localize(now)
    diff = nextLocal - nowCET
    if (ligaTarget.bVerbose):
        print ("time to next game")
        print (diff)

    days, seconds = diff.days, diff.seconds
    if (ligaTarget.bVerbose):
        print ("Days:    " + str (days))
        print ("Seconds: " + str (seconds))

    hours = days * 24 + (seconds /3600) 
    Waitseconds = days * 24 * 60 * 60 + seconds
    if (ligaTarget.bVerbose):
        print ("sleep:   " + str (Waitseconds))
    

    return


def earliestGame(matchDay):
    if (ligaTarget.bVerbose):
        print("->  monitorMatchDay.py/earliestGame()")    
    earlyGame = matchDay[0]["matchDateTimeUTC"]

    
    for match in matchDay:
        if (match["matchDateTimeUTC"] < earlyGame):
            earlyGame = match["matchDateTimeUTC"]
            if (ligaTarget.bVerbose):
                 print ("Game         :   " + str( match["matchID"]) )
                 print ("Earliest Game:   " + str( match["matchDateTimeUTC"]) )



    if (ligaTarget.bVerbose):
        print("<-  getCurrentMatchDayRoster.py/earliestGame()")       
    return earlyGame


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
    parser.add_argument("-f","--force", action="count", help="force immediate start")
    parser.add_argument("-d","--day", action="store", help="matchday")
    parser.add_argument("-y","--year", action="store", help="year")
    parser.add_argument("-t","--team", action="store", help="favorite Team")

    args = parser.parse_args()


    strHostVerbose = "False"

    if args.verbosity:
        strHostVerbose="True"
        coloredOutput.printSuperVerbose("verbosity turned on")
        ligaTarget.bVerbose=True

    if (ligaTarget.bVerbose):
        coloredOutput.printLog("\n*** getCurrentMatchDay.py***")
    
    if args.force:
        bForced ="True"
        coloredOutput.printSuperVerbose("forced mode turned on")
        #ligaTarget.bVerbose=True
    
    strMatchDay = ""

    if args.day:
        strMatchDay = args.day
        coloredOutput.printSuperVerbose("Matchday: " + strMatchDay + " (OVERRIDE)")
    else:
        strMatchDay = str(getCurrentMatchDay.getCurrentMatchDay())
        coloredOutput.printSuperVerbose("Matchday: " + strMatchDay )

    if args.year:
        strMatchYear=args.year
    else:
        strMatchYear = "2021"

    

    if (ligaTarget.bVerbose):
        coloredOutput.printSuperVerbose("Message: " + strMatchYear + " will be used as year.")
    if (ligaTarget.bVerbose):
        coloredOutput.printSuperVerbose("Macthday: " + strMatchDay + " will be used.")
    
    matchDay = getCurrentMatchDayRoster.getMatchDayRoster(int(strMatchDay))

    if (getCurrentMatchDayRoster.isMatchDayFinished(matchDay)):
        coloredOutput.printWarning("Match Day is finished.")
    else:
        LOCAL_TIMEZONE = datetime.now().astimezone().tzinfo
        if ligaTarget.bVerbose:
            print("Match Day is not yet finished.")
        

        earlyGame = earliestGame(matchDay)
        timeNextGame = datetime.strptime(earlyGame,"%Y-%m-%dT%H:%M:%SZ")
        
        zulu_timezone = pytz.timezone("UTC")
        local_timezone = pytz.timezone("CET")
        now = datetime.now()
        nowCET = local_timezone.localize(now)
        nextUTC =zulu_timezone.localize(timeNextGame)
        nextLocal = nextUTC.astimezone(LOCAL_TIMEZONE)

        diff = nextLocal - nowCET
        if (ligaTarget.bVerbose):
            print ("time to next game")
            print (diff)

        days, seconds = diff.days, diff.seconds
        hours = days * 24 + (seconds /3600)
        Waitseconds = days * 24 * 60 * 60 + seconds
        if (hours > 23):
            coloredOutput.printWarning(str(int(hours)) + " hours to go - tune back in 24hrs before game day" )
            exit
        else:
            coloredOutput.printSuperVerbose(str(int(hours)) + " hours to go ... kicking it off" )
            #waitForMatchDayStart(nextLocal)
            #monitorMatchday()

        if (bForced):
            coloredOutput.printSuperVerbose(str(int(hours)) + " hours to go ... kicking it off" )
            waitForMatchDayStart(nextLocal)
            #monitorMatchday()



        if (ligaTarget.bVerbose):
            print("End of monitorMatchDay.py")
    