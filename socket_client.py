import socket
import sys
import re
import argparse
from socket_comm import SOCKET_MSG_END,checkMsgSign,msgFilter
from socket_event import REQUIRE_FILE_LIST,END_CONNECT,SET_SEARCH_TYPE_A,SET_SEARCH_TYPE_B
import time

host = 'localhost'
default_port = 8080

class ServerManager():
    def __init__(self,sock):
        self.sock = sock

    def sendMsg(self,msg=''):
        sock = self.sock
        msg = msg+SOCKET_MSG_END
        msg = msg.encode('utf-8')
        sock.sendall(msg)

    def recvSockText(self):
        sock = self.sock
        recvText = ""
        while (not checkMsgSign(recvText,SOCKET_MSG_END)):
            recvText = recvText + sock.recv(5).decode('utf-8')
        return (msgFilter(recvText,SOCKET_MSG_END))





def echo_client(port):
    """ A simple echo client """
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the server
    server_address = (host, port)
    sock.connect(server_address)
    sManager = ServerManager(sock)
    # Send data
    try:
        # 詢問搜尋類型 1:檔案 2:資料夾
        # searchType = input("[1]:search files  [2]:search dir  ")
        # searchType = int(searchType)
        # if(searchType == 1):
        #     pass
            # message = SET_SEARCH_TYPE_A
        # print("What file/dir do you want to search?")
        # print("*RegExp is also support*")
        # print("input example:[.pdf] [.jpg] [foo.jpg] [bar]")
        # searchStr = input()



        message = REQUIRE_FILE_LIST
        print ("Sending %s" % message)
        sManager.sendMsg(message)
        recvText = sManager.recvSockText()
        print(recvText)
        # time.sleep(1)

        # message = END_CONNECT+SOCKET_MSG_END
        # print ("Sending %s" % message)
        # sock.sendall(message.encode('utf-8'))
        # recvText = recvSockText(sock)
        # print(recvText)


    except socket.error as e:
        print ("Socket error: %s" %str(e))
    except Exception as e:
        print ("Other exception: %s" %str(e))
    finally:
        print ("Closing connection to the server")
        sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Socket Server Example')
    parser.add_argument('--port', action="store", dest="port", type=int, default=default_port)
    given_args = parser.parse_args()
    port = given_args.port
    echo_client(port)