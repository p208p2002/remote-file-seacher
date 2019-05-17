import re

SOCKET_MSG_END = "$__MSG_END"
SOCKET_CLOSE_CONNECT = "$__CLOSE_CONNECT"

def checkMsgSign(testMsg,sign):
    patternStr = re.compile("\\"+sign+"$")
    if(len(patternStr.findall(testMsg))<=0):
        return False
    return True

def msgFilter(socketMsg,targetStr):
    return str(socketMsg).replace(targetStr,'')
