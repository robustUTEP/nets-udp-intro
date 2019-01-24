#! /usr/bin/env python3
# udp demo -- simple select-driven uppercase and lowercase server

# Eric Freudenthal with mods by Adrian Veliz

import sys
from socket import *
from select import select

# default params
upperServerAddr = ("", 50000)   # any addr, port 50,000
lowerServerAddr = ("", 50001)   # any addr, port 50,001
    
    
def uppercase(sock):
	message, clientAddrPort = sock.recvfrom(2048)
	print("from %s: rec'd '%s'" % (repr(clientAddrPort), message))
	modifiedMessage = message.upper()
	sock.sendto(modifiedMessage, clientAddrPort)
	
def lowercase(sock):
	message, clientAddrPort = sock.recvfrom(2048)
	print("from %s: rec'd '%s'" % (repr(clientAddrPort), message))
	modifiedMessage = message.lower()
	sock.sendto(modifiedMessage, clientAddrPort)


upperServerSocket = socket(AF_INET, SOCK_DGRAM)
upperServerSocket.bind(upperServerAddr)
upperServerSocket.setblocking(False)

lowerServerSocket = socket(AF_INET, SOCK_DGRAM)
lowerServerSocket.bind(lowerServerAddr)
lowerServerSocket.setblocking(False)


# map socket to function to call when socket is....
readSockFunc = {}               # ready for reading
writeSockFunc = {}              # ready for writing
errorSockFunc = {}              # broken

timeout = 5                     # seconds

readSockFunc[upperServerSocket] = uppercase
readSockFunc[lowerServerSocket] = lowercase

print("ready to receive")
while 1:
	readRdySet, writeRdySet, errorRdySet = select(list(readSockFunc.keys()),
                                                      list(writeSockFunc.keys()), 
                                                      list(errorSockFunc.keys()),
                                                      timeout)
        if not readRdySet and not writeRdySet and not errorRdySet:
                print("timeout: no events")
	for sock in readRdySet:
                readSockFunc[sock](sock)

