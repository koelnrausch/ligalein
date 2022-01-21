bVerbose = False  # set true for verbose outputs
bDebug = False  # set true for verbose outputs


def ligaTarget():
    #strStableTarget = "Production"      #set to use koelnrausch.de
    #strStableTarget = "ProductionAWS"      #set to use aws
    strLigaTarget = "ProductionAWS_VPN"      #set to use aws
    #strStableTarget = "DebugMacBook"  #set to use debug localhost on MacBook
    if (bDebug):
        strLigaTarget = "DebugMac"   #set to use debug localhost on iMac5k

    return(strLigaTarget)

def getBaseURL(strLigaTarget):
    if (strLigaTarget == 'Production'):
        baseurl = "http://www.koelnrausch.de/smartstable/api/"
    elif (strLigaTarget == 'DebugMac'):
        baseurl = "http://alinn-imac5k.local/smartstable/API/"
    elif (strLigaTarget == 'ProductionAWS'):
        baseurl = "http://18.195.91.245/smartstable/API/"
    elif (strLigaTarget == 'ProductionAWS_VPN'):
        baseurl = "http://10.8.0.1/smartstable/API/"
    else:
        baseurl = "http://www.koelnrausch.de/smartstable/api/"

    return baseurl


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