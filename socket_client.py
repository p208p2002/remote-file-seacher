import socket
import sys
import re
import argparse
from socket_comm import SOCKET_MSG_END,checkMsgSign,msgFilter
from socket_event import REQUIRE_FILE_LIST,END_CONNECT,SET_SEARCH_TYPE,SET_PATTERN_KEY,SEARCH_TARGET,SELECT_TARGETS
import time

HOST = 'localhost'
DEFAULT_PORT = 8080

class ServerManager():
    def __init__(self,host,port):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the server
        server_address = (host, port)
        sock.connect(server_address)
        self.sock = sock

    def sendMsg(self,msg=''):
        sock = self.sock
        msg = msg+SOCKET_MSG_END
        # print('send:'+ msg)
        msg = msg.encode('utf-8')
        sock.sendall(msg)
        #recv text
        recvText = ""
        while (not checkMsgSign(recvText,SOCKET_MSG_END)):
            recvText = recvText + sock.recv(5).decode('utf-8')
        recvMsg,recvEvent = msgFilter(recvText,SOCKET_MSG_END,False)
        return (recvMsg)

    def close(self):
        message = END_CONNECT
        return self.sendMsg(message)


def client(port):
    try:
        sManager = ServerManager(HOST,port)
        # 搜尋類型 1:檔案 2:資料夾
        searchType = input("[1]:search files  [2]:search dir  ")
        searchType = int(searchType)
        if(searchType >= 1 and searchType <=2):
            message = SET_SEARCH_TYPE
            sManager.sendMsg(message+str(searchType))
        else:
            print("invaild")
            sys.exit(0)

        #搜尋條件
        print("What file/dir do you want to search?")
        print("*RegExp is also support*")
        print("input example:[.pdf] [.jpg] [foo.jpg] [bar]")
        searchStr = input()
        message = SET_PATTERN_KEY
        sManager.sendMsg(message+searchStr)

        #搜尋目標
        print("Start searching...")
        result = sManager.sendMsg(SEARCH_TARGET)
        print(result)

        #選擇目標
        if(searchType == 1):
            print("*use space to split muilt-target*")
            selectTargets = input("Choose what you want to upload: ")
            # selectTargets = selectTargets.split()
            print("Picked:"+str(selectTargets))
            sManager.sendMsg(SELECT_TARGETS+str(selectTargets))



    except socket.error as e:
        print ("Socket error: %s" %str(e))
    except Exception as e:
        print ("Other exception: %s" %str(e))
    finally:
        print ("Closing connection to the server")
        sManager.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Socket Server Example')
    parser.add_argument('--port', action="store", dest="port", type=int, default=DEFAULT_PORT)
    given_args = parser.parse_args()
    port = given_args.port
    client(port)