
class color:
   PURPLE = '\033[1;35;48m'
   CYAN = '\033[1;36;48m'
   BOLD = '\033[1;37;48m'
   BLUE = '\033[1;34;48m'
   GREEN = '\033[1;32;48m'
   YELLOW = '\033[1;33;48m'
   RED = '\033[1;31;48m'
   BLACK = '\033[1;30;48m'
   UNDERLINE = '\033[4;37;48m'
   END = '\033[1;37;0m'

def printError( msg):
    print(color.BOLD + color.RED + msg + color.END )

def printLog( msg):
    print(msg)

def printQry( msg):
    print(color.BOLD + msg + color.END)

def printFromHost(msg):
    print(color.BLUE + msg + color.END)

def printWarning(msg):
    print(color.UNDERLINE + msg + color.END)

def printSuperVerbose(msg):
    print(color.YELLOW + msg + color.END)

if __name__ == '__main__':
    printSuperVerbose("Superverbose")
    printError("printError")
    printLog("printLog")
    printQry("printQry")
    printWarning("printWarning")
    printFromHost("printFromHost")
