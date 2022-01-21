# sysLogStable

import urllib.request
import requests
import sys
import getopt
import MySQLdb as mdb
import ligaTarget
import ligaDB

import argparse
import coloredOutput

from ligaConfig import getClientUid

strLogSource = ""
strLogText = ""
strLogSeverity = "0"

#Constants for categories
#cCATEGORY_SYSTEM =  1               # System message
#cCATEGORY_SYSTEM_BACKEND=3          # System messages
#cCATEGORY_SYSTEM_FRONTEND=5         # System messages
#cCATEGORY_SYSTEM_RPI=9              # System messages from RPis

#cCATEGORY_USER=16                   # Messages relevant to user
#cCATEGORY_USER_MESSAGE=48           # Messages from Users
#cCATEGORY_USER_BROADCAST=80         # Broadcasts to all users



def syslogStable(source, severity, content, category='9'):
    import stableDB

    strStableTarget = stableTarget.stableTarget()

    if (stableTarget.bVerbose):
        coloredOutput.printSuperVerbose("Target:       " + strStableTarget)

    baseurl = stableTarget.getBaseURL(strStableTarget)
    baseurl = baseurl + "log.php"

    if (stableTarget.bVerbose):
        coloredOutput.printSuperVerbose("Loglevel in log: " + str(severity))

    if (int(severity) > 0):
        sqlLocalLogWrite(source, severity, content, category)

    if (int(severity) >= 5):
        # report to home
        if (stableTarget.bVerbose):
            coloredOutput.printSuperVerbose("Issue with Severity > 5 will be reported to master")
            coloredOutput.printSuperVerbose("base_url:       " + baseurl)

        url = baseurl + "?id=" + str(stableTarget.getSerial())
        url = url + "&sev=" + str(severity)
        url = url + "&src=" + str(source)
        url = url + "&text=" + str(content)
        if (stableTarget.bVerbose):
            coloredOutput.printSuperVerbose("\nReporting with URL:" + url)


        #data = {"eventType":"AAS_PORTAL_START"}
        id=str(stableTarget.getSerial())
        clientUid = getClientUid(id)

        #category = 9    # RPi message category

        params={'id':str(stableTarget.getSerial()), 'category':category,'clientuid':clientUid, 'format':'xml', 'sev':severity, 'src':source, 'text':content}
        #headers={'content-type':'application/json'}
        #syslogStable("pingHostStable()","1","ID: "+id)


        response = requests.get(baseurl,params=params)
        #response = requests.get(baseurl, data={'id': id})

        if (stableTarget.bVerbose or stableTarget.bDebug):
            #print("URL: ", response.url)
            coloredOutput.printFromHost("Status: " + str(response.status_code) + "\ntext:  " + response.text)
	
        if (response.status_code != 200):
            coloredOutput.printError(" Status is not 200: "+str(response.status_code))
            #syslogStable.syslogStable("pingHostStable()" + str(response.status_code),"5","Status is not 200: "+str(response.status_code))



# Function sqlLocalLogwrite
def sqlLocalLogWrite(source, severity, content, category):
    client = 0 # for POC only local logs
    import stableDB
    db = mdb.connect(stableDB.strDB_host  \
                    ,stableDB.strDB_user  \
                    ,stableDB.strDB_pwd \
                    ,stableDB.strDB_dbName)
    cur = db.cursor()

    sqlQryInsertLog = "INSERT INTO " + stableDB.strDB_tblLog \
                    + "(clientId, logSrc, logSeverity, category, logText) "\
                    + "VALUES (" \
                    + " '"   + str(client) \
                    + "', '" + source \
                    + "', '" + severity \
                    + "', '" + category \
                    + "', '" + content \
                    + "')"

    if (stableTarget.bVerbose):
        coloredOutput.printQry("\nQuery to insert log item: " + sqlQryInsertLog)

    a = cur.execute(sqlQryInsertLog)
    db.commit()
    cur.close()
    db.close()


def syslogCleanup(interval):
    if (stableTarget.bVerbose):
        print("### cleaning up datatables ###")

    db = mdb.connect(stableDB.strDB_host  \
                    ,stableDB.strDB_user  \
                    ,stableDB.strDB_pwd \
                    ,stableDB.strDB_dbName)

    cur = db.cursor()

    sqlQry = "DELETE FROM " + stableDB.strDB_tblLog +" WHERE ts< (NOW() - INTERVAL 3 DAY)"

    if (stableTarget.bVerbose):
        coloredOutput.printQry(sqlQry)

    a = cur.execute(sqlQry)


    db.commit()
    cur.close()

    if (stableTarget.bVerbose):
        print("\nDB Committed.")

    syslogStable("syslogStable.py/syslogcleanup()", "1", \
                    "Deleted " + str(cur.rowcount) + " rows...")

    db.close()
    if (stableTarget.bVerbose):
        coloredOutput.printSuperVerbose("\nDB Closed.")

    if (stableTarget.bVerbose):
        coloredOutput.printLog("\nDone cleaning up...")


# start of actual python code when inviked by CLI
if __name__ == '__main__':
    strStableTarget = stableTarget.stableTarget()
    parser = argparse.ArgumentParser(description='syslogStable.py - Fire one log event into the stable system')
    parser.add_argument("-v","--verbosity", action="count", help="increase output verbosity")
    parser.add_argument("-d","--debug", action="count", help="set debug system to local test system")
    parser.add_argument("-m","--msg", action="store", help="Actual message into the log system")
    parser.add_argument("-c","--category", action="store", help="Category...(e.g. 9= RPi System)", default=9)
    parser.add_argument("-s","--source", action="store", help="Test to specify Source", default='syslogStable.py()')
    parser.add_argument("-l","--level", action="store", help="Level of log message", default='0')

    args = parser.parse_args()
    strMessage = ''

    strHostVerbose = "False"

    if args.verbosity:
        strHostVerbose="True"
        coloredOutput.printSuperVerbose("verbosity turned on")
        stableTarget.bVerbose=True

    if args.debug:
        coloredOutput.printWarning("DEBUG turned on")
        stableTarget.bDebug=True

    if args.category:
        strCategory = str(args.category)
        coloredOutput.printLog("Category for log:    " + strCategory)

    if args.msg:
        strMessage = args.msg
        coloredOutput.printLog("Message to be logged:" + strMessage)

    if args.source:
        strSource = args.source
        coloredOutput.printLog("Source for log msg:  " + strSource)

    if args.level:
        strLevel = args.level
        coloredOutput.printLog("Level for log msg:   " + strLevel)

    strStableTarget = stableTarget.stableTarget()
    if (stableTarget.bVerbose):
        coloredOutput.printSuperVerbose("Target:       " + strStableTarget)


    id=stableTarget.getSerial()
    clientUid = getClientUid(id)

    syslogStable(strSource, strLevel, strMessage, strCategory)