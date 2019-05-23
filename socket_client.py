import socket
import sys
import re
import argparse
from socket_comm import SOCKET_MSG_END,checkMsgSign,msgFilter
from socket_event import REQUIRE_FILE_LIST,END_CONNECT,SET_SEARCH_TYPE,SET_PATTERN_KEY,SEARCH_TARGET,SELECT_TARGETS,SET_MAIL_RECVER,SET_SEARCH_ROOT_PATH
import time
import signal

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 8080
BUFF_SIZE = 1024

def interruptHandler(sig, frame):
    sys.exit(0)

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
        recvText = "".encode('utf-8')
        while (not checkMsgSign(recvText,SOCKET_MSG_END)):
            recvText = recvText + sock.recv(BUFF_SIZE)
        recvText = recvText.decode('utf-8')
        recvMsg,recvEvent = msgFilter(recvText,SOCKET_MSG_END,False)
        return (recvMsg)

    def close(self):
        message = END_CONNECT
        self.sendMsg(message)
        self.sock.close()


def client(host,port):
    try:
        sManager = ServerManager(host,port)

        # 搜尋根目錄
        print("Search root path?")
        print("input example:[d:\] [d:\\foo\\bar\\]")
        searchPath = input("")
        message = SET_SEARCH_ROOT_PATH
        sManager.sendMsg(message+searchPath)

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
        if(len(result)==0):
            print('no match result')
            raise Exception()
        print(result)

        #選擇目標
        if(searchType == 1):
            print("*use space to split muilt-target*")
        elif(searchType == 2):
            pass
        selectTargets = input("Choose what you want to upload: ")
        print("Picked:"+str(selectTargets))
        sManager.sendMsg(SELECT_TARGETS+str(selectTargets))

        #設定收件者
        mailRecver = input("Mail to : ")
        sManager.sendMsg(SET_MAIL_RECVER+mailRecver)

    except socket.error as e:
        print ("Socket error: %s" %str(e))
    except Exception as e:
        pass
        # print ("Other exception: %s" %str(e))
    finally:
        print ("Closing connection to the server")
        sManager.close()
        return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Socket Server Example')
    parser.add_argument('--port', action="store", dest="port", type=int, default=DEFAULT_PORT)
    parser.add_argument('--host', action="store", dest="host", type=str, default=DEFAULT_HOST)
    signal.signal(signal.SIGINT, interruptHandler)
    given_args = parser.parse_args()
    port = given_args.port
    host = given_args.host
    client(host,port)