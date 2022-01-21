from multiprocessing.connection import wait
import psutil
import platform
from datetime import datetime
import socket
import urllib.request
import requests
import coloredOutput
import json
import ligaTarget
from datetime import datetime
import time
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

#params={'id':id, 'format':'xml', 'tslocal':ts}
#headers={'content-type':'application/json'}
# syslogStable("pingHostStable()","1","ID: "+id)
baselinetime = ""

while True:
    baseurl = "https://www.openligadb.de/api/getlastchangedate/bl1/2021/20"
    response = requests.get(baseurl)
    
    #lUp = datetime.strftime(response.text)
    st = response.text
    st = st.strip('"')
    if (st != baselinetime) :
        ts= datetime.now()
        coloredOutput.printWarning("local time: "+ ts.strftime("%Y-%m-%d  %H:%M:%S"))
        baselinetime = st
        #st = "2011-11-30T09:15:55.596"

        coloredOutput.printFromHost("Status: " + str(response.status_code) + "\ntext:  " + response.text)
        lUp=datetime.strptime(st,"%Y-%m-%dT%H:%M:%S.%f").timetuple()
        coloredOutput.printFromHost("Host changed at:    "+ st)
    else:
        print (".",end="")

    time.sleep(2)

