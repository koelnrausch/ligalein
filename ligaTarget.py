
bVerbose = False  # set true for verbose outputs
bDebug = False  # set true for verbose outputs
bForced = False

strLeagueIdentifier = "bl1"




def ligaTarget():
    #strStableTarget = "Production"      #set to use koelnrausch.de
    #strStableTarget = "ProductionAWS"      #set to use aws
    strLigaTarget = "ProductionAWS_VPN"      #set to use aws
    #strStableTarget = "DebugMacBook"  #set to use debug localhost on MacBook
    if (bDebug):
        strLigaTarget = "DebugMac"   #set to use debug localhost on iMac5k

    return(strLigaTarget)

#  baseUrl = "https://api.openligadb.de/GetCurrentGroup/bl1"
#   https://api.openligadb.de/getmatchdata/bl1/2020/8
def getBaseURL(strLigaTarget):
    if (strLigaTarget == 'Production'):
        baseurl = "https://api.openligadb.de/"
    elif (strLigaTarget == 'DebugMac'):
        baseurl = "https://api.openligadb.de/"
    elif (strLigaTarget == 'ProductionAWS'):
        baseurl = "https://api.openligadb.de/"
    elif (strLigaTarget == 'ProductionAWS_VPN'):
        baseurl = "https://api.openligadb.de/"
    else:
        baseurl = "https://api.openligadb.de/"

    return baseurl

def getApiGetCurrentGroupURL(strLigaTarget):
    strURL = getBaseURL(strLigaTarget) + "GetCurrentGroup/"+strLeagueIdentifier + "/"
    return strURL

def getApiGetmatchdata(strLigaTarget):
    strURL = getBaseURL(strLigaTarget) + "GetCurrentGroup/"+strLeagueIdentifier+"/"
    return strURL


def getSerial():
    cpuserial="0000000000000000"
    try:
        f=open('/proc/cpuinfo','r')
        for line in f:
            if line[0:6]=='Serial':
                cpuserial=line[10:26]
        f.close()
    except:
        cpuserial="Error_000"
    return cpuserial