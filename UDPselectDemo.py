# udp demo simple select server -- Adrian Veliz, modified from code by Eric Freudenthal
import sys
from socket import *
from select import select

# default params
upperServerAddr = ("", 50000)   # any addr, port 50,000
    
    
def uppercase(sock):
	message, clientAddrPort = sock.recvfrom(2048)
	print "from %s: rec'd '%s'" % (repr(clientAddrPort), message)
	modifiedMessage = message.upper()
	sock.sendto(modifiedMessage, clientAddrPort)
	

upperServerSocket = socket(AF_INET, SOCK_DGRAM)
upperServerSocket.bind(upperServerAddr)
upperServerSocket.setblocking(False)

readSockFunc = {}               # dictionaries from socket to function 
writeSockFunc = {}
errorSockFunc = {}
timeout = 5                     # seconds

readSockFunc[upperServerSocket] = uppercase

print "ready to receive"
while 1:
	readRdySet, writeRdySet, errorRdySet = select(readSockFunc.keys(),
                                                      writeSockFunc.keys(), 
                                                      errorSockFunc.keys(),
                                                      timeout)
        if not readRdySet and not writeRdySet and not errorRdySet:
                print "timeout: no events"
	for sock in readRdySet:
                readSockFunc[sock](sock)

