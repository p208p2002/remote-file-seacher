import socket
import sys
import argparse
from socket_comm import checkMsgSign,SOCKET_MSG_END
from socket_event import REQUIRE_FILE_LIST,END_CONNECT
import time

host = 'localhost'
data_payload = 5
backlog = 5
default_port = 8080

def parseEvent(eventName,client):
    if(eventName == REQUIRE_FILE_LIST):
        pass
    elif(eventName == END_CONNECT):
        client.close()

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

    print ("Waiting to receive message from client")
    client, address = sock.accept()
    recvText = ''
    while True:
        data = client.recv(data_payload)
        if(len(data)>0):
            print(data)
            recvText = recvText + data.decode()
        if(checkMsgSign(recvText)):
            print(recvText)
            client.send(SOCKET_MSG_END.encode())
            recvText = ''





        # client.close()


        # data = client.recv(data_payload)
        # if data:
        #     print ("Data: %s" %data)
        #     client.send(data)
        #     print ("sent %s bytes back to %s" % (data, address))
        # # end connection
        # client.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Socket Server Example')
    parser.add_argument('--port', action="store", dest="port", type=int, default=default_port)
    given_args = parser.parse_args()
    port = given_args.port
    echo_server(port)