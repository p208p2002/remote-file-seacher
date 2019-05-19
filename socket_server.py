import socket
import sys
import argparse
from socket_comm import checkMsgSign,SOCKET_MSG_END,msgFilter
from socket_event import REQUIRE_FILE_LIST,END_CONNECT,SET_SEARCH_TYPE,SET_PATTERN_KEY,SEARCH_TARGET
import time
import os
import re

host = 'localhost'
data_payload = 5
backlog = 5
default_port = 8080

class ClientManager(object):
    def __init__(self,socket_client):
        self.searchType = None
        self.patternKey = None
        self.client = socket_client

    def setSearchType(self,searchType:int):
        print("set search type:"+str(searchType))
        self.searchType = searchType

    def setPatternKey(self,key):
        key = str(key)
        print("set pattern key type:"+ key)
        self.patternKey = key

    def sendMsg(self,msg=''):
        client = self.client
        msg = msg + SOCKET_MSG_END
        msg = msg.encode('utf-8')
        client.sendall(msg)

    def __searchTarget(self):
        path = 'd:\\111\\'
        files = []
        searchType = self.searchType
        searchStr = self.patternKey
        # r=root, d=directories, f = files
        for r, d, f in os.walk(path):
            searchTarget = 0
            if(searchType == 1):
                searchTarget = f
            elif(searchType == 2):
                searchTarget = d

            for target in searchTarget:
                patternStr = re.compile(searchStr)
                results = patternStr.findall(target)
                if(len(results)>0):
                    files.append(os.path.join(r, target))
        counter = 0
        if(len(files)==0):
            print("no match result")
            sys.exit(0)
        msg = ''
        for f in files:
            print(counter,f)
            msg=msg+str(counter)+' '+str(f)+'\n'
            counter += 1
        return msg

    def parseEvent(self,recvMsg,eventName:str):
        msg = ''
        if(eventName == REQUIRE_FILE_LIST):
            msg = 'send'+SOCKET_MSG_END

        elif(eventName == SET_SEARCH_TYPE):
            self.setSearchType(int(recvMsg))

        elif(eventName == SET_PATTERN_KEY):
            self.setPatternKey(str(recvMsg))

        elif(eventName == SEARCH_TARGET):
            msg = self.__searchTarget()

        elif(eventName == END_CONNECT):
            msg = 'bye'
            self.sendMsg(msg)
            return 1

        else:
            print('Uknow event')
        #
        self.sendMsg(msg)
        return 0

def echo_server(port):
    """ A simple echo server """
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Enable reuse address/port
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to the port
    server_address = (host, port)
    print ("Starting up echo server  on %s port %s" % server_address)
    sock.bind(server_address)
    # Listen to clients, backlog argument specifies the max no. of queued connections
    sock.listen(backlog)

    while True:
        print ("Waiting to receive message from client")
        client, address = sock.accept()
        cManager = ClientManager(client)
        recvText = ''
        while True:
            data = client.recv(data_payload)
            if(len(data)>0):
                # print(data)
                recvText = recvText + data.decode('utf-8')
            if(checkMsgSign(recvText)): #檢測到SOCKET_MSG_END
                # print(recvText)
                #分析事件並答覆Client然後清空recvText
                recvMsg,recvEvent = msgFilter(recvText)
                event = cManager.parseEvent(recvMsg,recvEvent)
                recvText = ''
                if(event == 1):
                    break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Socket Server Example')
    parser.add_argument('--port', action="store", dest="port", type=int, default=default_port)
    given_args = parser.parse_args()
    port = given_args.port
    echo_server(port)