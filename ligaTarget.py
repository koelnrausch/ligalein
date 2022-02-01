
bVerbose = False  # set true for verbose outputs
bDebug = False  # set true for verbose outputs
bForced = False

strLeagueIdentifier = "bl1"
strLeagueYear = "2021"
strMatchDay = "1"






def ligaTarget():
    #strStableTarget = "Production"      #set to use koelnrausch.de
    #strStableTarget = "ProductionAWS"      #set to use aws
    strLigaTarget = "ProductionAWS_VPN"      #set to use aws
    #strStableTarget = "DebugMacBook"  #set to use debug localhost on MacBook
    if (bDebug):
        strLigaTarget = "DebugMac"   #set to use debug localhost on iMac5k

    return(strLigaTarget)

# baseUrl get dcurrentgropu = "https://api.openligadb.de/GetCurrentGroup/bl1"
# baseurl get macth data   "https://api.openligadb.de/getmatchdata/bl1/2020/8"
# baseurlLastChange = "https://www.openligadb.de/api/getlastchangedate/bl1/2021/20"
# baseurl getavailteams "https://www.openligadb.de/api/getavailableteams/bl1/2016"

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

def getAPIGetLastChangeDate(strLigaTarget):
    baseurlLastChange = getBaseURL(strLigaTarget) + "getlastchangedate" + strLeagueIdentifier + "/"
    return baseurlLastChange

def getApiGetCurrentGroupURL(strLigaTarget):
    strURL = getBaseURL(strLigaTarget) + "GetCurrentGroup/"+strLeagueIdentifier + "/"
    return strURL

def getApiGetmatchdata(strLigaTarget):
    strURL = getBaseURL(strLigaTarget) + "GetCurrentGroup/"+strLeagueIdentifier+"/"
    return strURL

def getAPIGetTeams(strLigaTarget):
    strURL = getBaseURL(strLigaTarget) + "getavailableteams/"+strLeagueIdentifier+"/" 


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