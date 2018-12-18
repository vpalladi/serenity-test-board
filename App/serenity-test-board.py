#!/usr/local/bin/python3
import matplotlib
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure
import tkinter as tk
import tkinter.ttk as ttk
import sys
import copy

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import threading as thread
#import thread
import time
import datetime
import argparse
from subprocess import call

#sys.path.insert(0, "../Sockets")
import server as srv

# from tkinter import *
# from tkinter.ttk import *

class TestBoardGUI:
    def __init__(self, master):
        self.master = master
        master.title("HGCal Board Tester v0.1")
        master.geometry("400x300")

        self.data = []
        
        self.frame = tk.Frame(master)
        self.frame.pack()

        self.label = tk.Label(self.frame, text="Run Board Tests")
        self.label.grid(row=0)

        self.port_number = tk.IntVar() 
        self.port_label = tk.Label(self.frame, text="Port").grid(row=2,column=2)
        self.port_entry = tk.Entry(self.frame, textvariable=self.port_number, width=5)
        self.port_entry.delete(0,tk.END)
        self.port_entry.insert(tk.INSERT,1025)
        self.port_entry.grid(row=2,column=3) 
        
        ### server socket ###
        self.user_input = self.port_number.get()
        self.host = 'localhost'
        self.addr = ( self.host, self.user_input )
        self.serversocket = socket( AF_INET, SOCK_STREAM )
        self.serversocket.setsockopt( SOL_SOCKET, SO_REUSEADDR, 1 )
        self.serversocket.bind( self.addr )
        self.serversocket.listen( 10 )
        self.clients = [self.serversocket]

        self.test_button = tk.Button(self.frame, text="Start Test", command=self.test)
        self.test_button.grid(row=2) 


        self.plot_button = tk.Button(self.frame, text="Plot", command=self.plot_window)
        self.plot_button.grid(row=4) 
        
        self.close_button = tk.Button(self.frame, text="Exit Application", command=master.quit)
        self.close_button.grid(row=5) 

        

        
    def show_results(self):
        print("Showing results")

    def run(self):
        print("Run")

    def test(self):
#        parser = argparse.ArgumentParser(description='Serenity test-board server.')

        buf = 1000000
        tests = [] 

        print ("Server is listening for connections\n")
        clientsocket, clientaddr = self.serversocket.accept()
        self.clients.append( clientsocket )

        th = thread.Thread(target=srv.handler, args=(clientsocket, clientaddr, buf, tests,self.clients,)) 
        th.start()
        th.join()
                
        if(len(tests)>0) :                    

            self.data = (tests[-1].getData())
            print (self.data)
            print("Test Completed")
            self.plot_window()


    def plot_window(self):
        self.window = PlotWindow(self.master,self.data)


class PlotWindow(tk.Toplevel):
    def __init__(self, master, data):        
        self.master = master
        tk.Toplevel.__init__(self)
        self.geometry("800x600")

        self.close_button = tk.Button(self, text="Close Plot Window", command=self.destroy)
        self.close_button.pack()

        self.exit_button = tk.Button(self, text="Exit Application", command=master.quit)
        self.exit_button.pack()

        self.notebook = ttk.Notebook(self)
        f1 = tk.Frame(self.notebook)   # first page, which would get widgets gridded into it
        f2 = tk.Frame(self.notebook)   # second page
        f3 = tk.Frame(self.notebook)   # second page
        f4 = tk.Frame(self.notebook)   # second page
        self.notebook.add(f1, text='X0')
        self.notebook.add(f2, text='X1')
        self.notebook.add(f3, text='Services')
        self.notebook.add(f4, text='Artix')
        self.notebook.pack(fill=tk.BOTH, expand=True)

        x0=[]
        x1=[]
        services=[]
        artix=[]
        for i in range(len(data)):
            if data[i][0].find('X0') != -1:
                x0.append(data[i])
            if data[i][0].find('X1') != -1:
                x1.append(data[i])
            if data[i][0].find('SERVICES') != -1 or data[i][0].find('SCALED') != -1:
                services.append(data[i])
            if data[i][0].find('ARTIX') != -1:
                artix.append(data[i])
        
        self.make_figure(f1, x0)
        self.make_figure(f2, x1)
        self.make_figure(f3, services)
        self.make_figure(f4, artix)


        
    def show_results(self):
        print("Showing results")

    def make_figure(self, frame, data):
    
        fig = Figure(figsize=(5, 4), dpi=100)
        t = np.arange(0, 3, .01)
        plt.tight_layout()

        dataTmp = copy.deepcopy(data)
        
        for i in range(len(data)):
            title = dataTmp[i][0]
            dataTmp[i].pop(0)
            row,col=3,4
            if title.find('SERVICES')!=-1 or title.find('SCALED')!=-1:
                col=3
            if title.find('ARTIX')!=-1:
                row=1
                col=2
            subfig = fig.add_subplot(row,col,i+1)
            subfig.plot( (dataTmp[i] ) )
            subfig.set_title(title)
            subfig.set_ylabel('Voltage')

        fig.subplots_adjust(hspace=0.5, wspace=0.4)
            
        canvas = FigureCanvasTkAgg(fig, frame)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        toolbar = NavigationToolbar2Tk(canvas, frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        
root = tk.Tk()
tb_gui = TestBoardGUI(root)

root.mainloop()
