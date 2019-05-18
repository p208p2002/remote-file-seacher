import re

SOCKET_MSG_END = "$__MSG_END"

def checkMsgSign(testMsg,sign=SOCKET_MSG_END):
    patternStr = re.compile("\\"+sign+"$")
    if(len(patternStr.findall(testMsg))<=0):
        return False
    return True

def msgFilter(socketMsg,targetStr=SOCKET_MSG_END):
    return str(socketMsg).replace(targetStr,'')
