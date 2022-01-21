   
#ping with id to show that stable is alive and identify
import urllib.request
import requests
import json
import ligaTarget
from datetime import datetime

import argparse

from syslogLiga import syslogLiga
#from stableConfig import isClientActive
#from stableConfig import getClientUid

import coloredOutput

# start of actual python code when inviked by CLI
if __name__ == '__main__':
    strLigaTarget = ligaTarget.ligaTarget()
    parser = argparse.ArgumentParser(description='requestLastChanged.py - This tool checks for last changes on match day')
    parser.add_argument("-c","--cmd", action='store', help="Specify the command to config. <ping> <cleanup>",default='ping')
    parser.add_argument("-v","--verbosity", action="count", help="increase output verbosity")
    parser.add_argument("-m","--message", action="store", help="add a message to the host, will appear in log", default='')

    args = parser.parse_args()
    strMessage = ''

    if (args.cmd):
        strCmd = args.cmd
        coloredOutput.printSuperVerbose("CMD: '" + strCmd + "'")

    strHostVerbose = "False"

    if args.verbosity:
        strHostVerbose="True"
        coloredOutput.printSuperVerbose("verbosity turned on")
        ligaTarget.bVerbose=True

    if args.message:
        strMessage = args.message
        coloredOutput.printLog("Message to be delivered to host:" + strMessage)

    strLigaTarget = ligaTarget.stableTarget()
    if (ligaTarget.bVerbose):
        coloredOutput.printSuperVerbose("Target:       " + strLigaTarget)

    baseurl = ligaTarget.getBaseURL(strLigaTarget)

    if (ligaTarget.bVerbose or ligaTarget.bDebug):
        coloredOutput.printSuperVerbose("base_url:     " + baseurl)

    id=ligaTarget.getSerial()
    ts= datetime.now()

    if (strCmd == ''):
        if (ligaTarget.bVerbose or ligaTarget.bDebug):
            coloredOutput.printSuperVerbose("Enforcing PING command by default")
        strCmd = 'ping'

    #url = baseurl + "?id=" + str(id)
    clientUid = getClientUid(id)

    if ((stableTarget.bVerbose) or (stableTarget.bDebug)):
        coloredOutput.printLog("CPU ID:       " + str(id))
        coloredOutput.printLog("Local Time:   " + str(ts))
        coloredOutput.printLog("Calling home: " + str(baseurl))
        coloredOutput.printLog("Command:      " + str(strCmd))
        coloredOutput.printLog("ClientUID:    " + str(clientUid))
        coloredOutput.printLog("Messsage2Host:" + str(strMessage))

    params={'id':id, 'cmd':strCmd, 'clientuid':clientUid, 'msg':strMessage, 'verbose':strHostVerbose, 'format':'xml', 'tslocal':ts}
    #headers={'content-type':'application/json'}
    syslogStable("pingHostStable()","1","ID: "+id)

    if isClientActive(id):

        response = requests.get(baseurl,params=params)
        if ((stableTarget.bVerbose) or (stableTarget.bDebug)):
            coloredOutput.printFromHost("Status: " + str(response.status_code) + "\ntext:  " + response.text)
        syslogStable("pingHostStable()","1","Host Responded with Status: "+str(response.status_code))

        if (response.status_code <200 or response.status_code>299):
            coloredOutput.printFromHost(" Status is not 200: "+str(response.status_code))
            syslogStable("pingHostStable()","7","Status is not 200: "+str(response.status_code))

    else:
        coloredOutput.printError("Client not Active")
        syslogStable("pingHostStable()","4","Client is not active.")