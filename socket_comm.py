import re

SOCKET_MSG_END = "$__MSG_END"

def checkMsgSign(testMsg,sign=SOCKET_MSG_END):
    patternStr = re.compile("\\"+sign+"$")
    if(len(patternStr.findall(testMsg))<=0):
        return False
    return True

def msgFilter(socketMsg,targetStr=SOCKET_MSG_END):
    socketMsg = str(socketMsg)
    event = re.compile("%__[A-Z|_]*%")
    event = event.findall(socketMsg)
    if(len(event)>0):
        event = event[0]
        event = str(event)
        socketMsg = socketMsg.replace(event,'')
    else:
        event = None
        event = str(event)

    socketMsg = socketMsg.replace(targetStr,'')
    print("event:"+ event)
    print("msg:"+socketMsg)

    return (socketMsg,event)
