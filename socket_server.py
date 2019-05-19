import socket
import sys
import argparse
from socket_comm import checkMsgSign,SOCKET_MSG_END,msgFilter
from socket_event import REQUIRE_FILE_LIST,END_CONNECT
import time

host = 'localhost'
data_payload = 5
backlog = 5
default_port = 8080

class ClientManager(object):
    def __init__(self,socket_client):
        self.searchType = None
        self.client = socket_client

    def setSearchType(self,searchType:int):
        self.searchType = searchType

    def parseEvent(self,eventName):
        client = self.client
        if(eventName == REQUIRE_FILE_LIST):
            msg = 'send'+SOCKET_MSG_END
            client.sendall(msg.encode('utf-8'))
        elif(eventName == END_CONNECT):
            client.sendall(SOCKET_MSG_END.encode('utf-8'))
            return 1
        else:
            client.sendall(SOCKET_MSG_END.encode('utf-8'))
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
        recvText = ''
        while True:
            data = client.recv(data_payload)
            if(len(data)>0):
                print(data)
                recvText = recvText + data.decode('utf-8')
            if(checkMsgSign(recvText)): #檢測到SOCKET_MSG_END
                print(recvText)

                #分析事件並答覆Client然後清空recvText
                cManager = ClientManager(client)
                event = cManager.parseEvent(msgFilter(recvText))
                recvText = ''
                if(event == 1):
                    break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Socket Server Example')
    parser.add_argument('--port', action="store", dest="port", type=int, default=default_port)
    given_args = parser.parse_args()
    port = given_args.port
    echo_server(port)