#! /usr/bin/env python3
# udp demo server.  Modified from Kurose/Ross by Eric Freudenthal 2016
import sys

from socket import *

# default params
serverAddr = ("", 50000)


def usage():
    print("usage: %s [--serverPort <port>]"  % sys.argv[0])
    sys.exit(1)

try:
    args = sys.argv[1:]
    while args:
        sw = args[0]; del args[0]
        if sw == "--serverPort":
            serverAddr = ("", int(args[0])); del args[0]
        else:
            print("unexpected parameter %s" % args[0])
            usage();
except:
    usage()

print("binding datagram socket to %s" % repr(serverAddr))

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(serverAddr)
print("ready to receive")
while 1:
    message, clientAddrPort = serverSocket.recvfrom(2048)
    print("from %s: rec'd '%s'" % (repr(clientAddrPort), message.decode()))
    modifiedMessage = message.decode().upper().encode()
    serverSocket.sendto(modifiedMessage, clientAddrPort)
    
                
