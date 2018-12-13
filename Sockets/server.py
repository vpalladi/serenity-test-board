#!/usr/bin/python

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import thread
import time
import datetime


def handler( clientsocket, clientaddr, buf ):
    
    print "Accepted connection from: ", clientaddr
    while True:
        rawData = clientsocket.recv( buf )
       
        if not rawData:
            break 
        else:
            data = rawData.split(',')
            print rawData
            for i, d in enumerate(data) :
                #if( i%3 == 0 ) :
                #    print '\n'
                print d,
            #clientsocket.send("ECHO: " + data + '\n')

    clients.remove( clientsocket )
    clientsocket.close()

def push():
    while True:
        for i in clients:
            if i is not serversocket: # neposilat sam sobe
                i.send("Current date and time: " + str(datetime.datetime.now()) + '\n')
        time.sleep(10) # [s]

host = 'localhost'
port = 26
addr = ( host, port )

### server socket ###
serversocket = socket( AF_INET, SOCK_STREAM )
serversocket.setsockopt( SOL_SOCKET, SO_REUSEADDR, 1 )
serversocket.bind( addr )
serversocket.listen( 10 )

clients = [serversocket]

buf = 10000

while True:
    try:
        print "Server is listening for connections\n"
        clientsocket, clientaddr = serversocket.accept()
        clients.append( clientsocket )
        thread.start_new_thread( handler, (clientsocket, clientaddr, buf) )
    except KeyboardInterrupt: # Ctrl+C # FIXME: vraci "raise error(EBADF, 'Bad file descriptor')"
        print "Closing server socket..."
        serversocket.close()

