# Schreibe hier Deinen Code :-)
import os
import uuid
#import MySQLdb as mdb
from time import sleep
#import syslogLiga
import ligaTarget
import requests

import coloredOutput



def getCurrentMatchDay():
    iMatchDay = 0

    baseUrl = "https://api.openligadb.de/GetCurrentGroup/bl1"

    responseMatchDay = requests.get(baseUrl)

    try:
        responseMatchDay = requests.get(baseUrl)
    except requests.exceptions.HTTPError as e:
        print( e)

    jsonResp = responseMatchDay.json()

    if (ligaTarget.bVerbose):
        print (jsonResp["groupName"])
        print (jsonResp["groupOrderID"])
        print (jsonResp["groupID"])
    
    iMatchDay = int( jsonResp["groupOrderID"])

    return iMatchDay


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
    parser.add_argument("-d","--debug", action="count", help="Switch to debug System - data is not recorded on production host")
    parser.add_argument("-y","--year", action="store", help="year")

    args = parser.parse_args()


    strHostVerbose = "False"

    if args.verbosity:
        strHostVerbose="True"
        coloredOutput.printSuperVerbose("verbosity turned on")
        ligaTarget.bVerbose=True

    if (ligaTarget.bVerbose):
        coloredOutput.printLog("\n*** getCurrentMatchDay.py***")

    if args.debug:
        strHostVerbose="True"
        coloredOutput.printSuperVerbose("Debug mode activated")
        ligaTarget.bDebug=True

    if args.year:
        strText=args.year
    else:
        strText = "2021"

    if (ligaTarget.bVerbose):
        coloredOutput.printSuperVerbose("Message: " + strText + " will be used as year.")

    print("Matchday: " + str(getCurrentMatchDay()))

    if (ligaTarget.bVerbose):
        print("End of getCurrentMatchDay.py")