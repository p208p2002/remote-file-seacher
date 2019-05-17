import socket
import sys
import re
import argparse
from socket_core import SOCKET_MSG_END,checkMsgSign,msgFilter

host = 'localhost'
default_port = 8080

def echo_client(port):
    """ A simple echo client """
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the server
    server_address = (host, port)
    sock.connect(server_address)

    # Send data
    try:
        # Send data
        message = "Test message. This will be echoed"+SOCKET_MSG_END
        print ("Sending %s" % message)
        sock.sendall(message.encode('utf-8'))
        # Look for the response
        recvText = ""
        while (not checkMsgSign(recvText,SOCKET_MSG_END)):
            recvText = recvText + sock.recv(5).decode()
            print(recvText)
        print(msgFilter(recvText,SOCKET_MSG_END))

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