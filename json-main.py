from multiprocessing.connection import wait
#import psutil
import platform
from datetime import datetime
import socket
from tkinter import E
import urllib.request
import requests
import coloredOutput
import json
import ligaTarget
from datetime import datetime
import time
import xml.etree.ElementTree as ET

id=ligaTarget.getSerial()
ts= datetime.now()

uname=platform.uname()
print("System:    ",uname.system)
print("Node Name: ",uname.node)
print("Release:   ",uname.release)
print("Version:   ",uname.version)
print("Machine:   ",uname.machine)
print("Processor: ",uname.processor)
print("\n")
print("Hostname:  ",socket.gethostname())

#params={'id':id, 'format':'json', 'tslocal':ts}
#headers={'content-type':'application/json'}
# syslogStable("pingHostStable()","1","ID: "+id)
baselinetime = ""

# füllen von baslineMatches - alle matches des spieltags
baselineMatches = [];
baseurlMatchDay = "https://www.openligadb.de/api/getmatchdata/bl1/2021/20"
responseMatchDay = requests.get(baseurlMatchDay)
jsonResp = responseMatchDay.json()
for match in jsonResp:
    #print (match["MatchID"])
    baselineMatches.append(match)


while True:
    baseurlLastChange = "https://www.openligadb.de/api/getlastchangedate/bl1/2021/20"
    baseurlMatchDay = "https://www.openligadb.de/api/getmatchdata/bl1/2021/20"
    
    try:
        responseLastChange = requests.get(baseurlLastChange)
    except requests.exceptions.HTTPError as e:
        print( e)

    try:
        responseMatchDay = requests.get(baseurlMatchDay)
    except requests.exceptions.HTTPError as e:
        print( e)
    
    
    #print (response.content)
    jsonResp = responseMatchDay.json()
    #print (jsonResp)
    ##root = ET.fromstring(response.content)
    #print ("2")
    #print (len(jsonResp))
    #print (jsonResp[2])
    #lUp = datetime.strftime(response.text)
    st = responseLastChange.text
    st = st.strip('"')
    if (st != baselinetime) :
        ts= datetime.now()
        coloredOutput.printWarning("local time: "+ ts.strftime("%Y-%m-%d  %H:%M:%S"))
        baselinetime = st

        coloredOutput.printFromHost("Status: " + str(responseLastChange.status_code) + "\ntext:  " + responseLastChange.text)
        lUp=datetime.strptime(st,"%Y-%m-%dT%H:%M:%S.%f").timetuple()
        coloredOutput.printFromHost("Host changed at:    "+ st)

        for i in range(len(jsonResp)):
            print ("read "+str(i))
            if jsonResp[i] != baselineMatches[i]:
                print("changed: " + str(i))
                print (jsonResp[i])
    else:
        print (".",end="")

    time.sleep(2)

