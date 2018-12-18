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
        for i in range(int(voltages)) :
            start = (i*dataPktLen)
            stop  = start + dataPktLen
            self.data.append( dataTmp[start:stop] )

    def getData( self ) :
        return self.data



def handler( clientsocket, clientaddr, buf, tests, clients ):

    board = cBoard()
    tests.append( board )

    print ("Accepted connection from: "), (clientaddr)
    while True:
        rawData = clientsocket.recv( buf ).decode('utf-8')
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







