#!/usr/bin/python

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import threading as thread
#import thread
import time
import datetime
import argparse


class cBoard :
    

    def __init__( self, nPoints=0 ) :
        self.setNpoints( nPoints )
        self.data = []


    def setNpoints( self, nPoints ) :
        self.nPoints = int(nPoints)

    def getNpoints( self ) :
        return self.nPoints

    def readData( self, dataTmp ) :
        del dataTmp[0]
        del dataTmp[-1]
        dataPktLen = (self.nPoints+1)
        voltages = len(dataTmp)/dataPktLen
        for i in range(voltages) :
            start = (i*dataPktLen)
            stop  = start + dataPktLen
            self.data.append( dataTmp[start:stop] )

    def getData( self ) :
        return self.data



def handler( clientsocket, clientaddr, buf, tests ):
    
    board = cBoard()
    tests.append( board )

    print "Accepted connection from: ", clientaddr
    while True:
        rawData = clientsocket.recv( buf )
        rawData = rawData.replace(' ', '')
        if not rawData:
            break 
        else:
            data = rawData.split(',')
            tests[-1].setNpoints( data[0] )
            tests[-1].readData( data )
            #clientsocket.send("ECHO: " + data + '\n')
    
    clients.remove( clientsocket )
    clientsocket.close()





def push():
    while True:
        for i in clients:
            if i is not serversocket:
                i.send("Current date and time: " + str(datetime.datetime.now()) + '\n')
        time.sleep(10) # [s]




######################


### option parsing ###
parser = argparse.ArgumentParser(description='Serenity test-board server.')
parser.add_argument('-p', '--port',
                    type=int, default=1025,
                    help='port to open')
parser.add_argument('-l', '--host',
                    default='localhost',
                    help='port to open')
args = parser.parse_args()
port = args.port
host = args.host
addr = ( host, port )

### server socket ###
serversocket = socket( AF_INET, SOCK_STREAM )
serversocket.setsockopt( SOL_SOCKET, SO_REUSEADDR, 1 )
serversocket.bind( addr )
serversocket.listen( 10 )

clients = [serversocket]

buf = 1000000
tests = [] 
        
while True:
    try:
        print "Server is listening for connections\n"
        clientsocket, clientaddr = serversocket.accept()
        clients.append( clientsocket )
#        thread.start_new_thread( handler, (clientsocket, clientaddr, buf, tests) )
        th = thread.Thread(target=handler, args=(clientsocket, clientaddr, buf, tests,)) 
        th.start()
        th.join()
#        time.sleep(2) 

        if(len(tests)>0) :
            print 'what?',tests[-1].getData()
    except KeyboardInterrupt: # Ctrl+C # FIXME: vraci "raise error(EBADF, 'Bad file descriptor')"
        print "Closing server socket..."
        serversocket.close()

while 1:
    pass
