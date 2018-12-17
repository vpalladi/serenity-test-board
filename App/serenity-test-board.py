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

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import threading as thread
#import thread
import time
import datetime
import argparse


#sys.path.insert(0, "../Sockets")
import server as srv

# from tkinter import *
# from tkinter.ttk import *

class TestBoardGUI:
    def __init__(self, master):
        self.master = master
        master.title("HGCal Board Tester v0.1")
        master.geometry("400x300")
        
        self.frame = tk.Frame(master)
#        self.frame.grid(row=0,sticky=tk.NSEW)
        self.frame.pack()
        # self.frame.grid_rowconfigure(1, weight=1)
        # self.frame.grid_columnconfigure(1, weight=1)

        self.label = tk.Label(self.frame, text="Run Board Tests")
        self.label.grid(row=0)

#        self.test_counter = 0
        self.test_button = tk.Button(self.frame, text="Start Test", command=self.test)
        self.test_button.grid(row=2) 
        # self.stop_test_button = tk.Button(self.frame, text="Stop Test", command=self.stop_test)
        # self.stop_test_button.grid(row=3) 

        self.port_number = tk.IntVar() 
        self.port_label = tk.Label(self.frame, text="Port").grid(row=2,column=2)
        self.port_entry = tk.Entry(self.frame, textvariable=self.port_number, width=5)
        self.port_entry.delete(0,tk.END)
        self.port_entry.insert(tk.INSERT,1025)
        self.port_entry.grid(row=2,column=3) 

        # self.run_button = tk.Button(self.frame, text="Run", command=self.run)
        # self.run_button.pack()

        # self.results_button = tk.Button(self.frame, text="Results", command=self.show_results)
        # self.results_button.pack()


        self.plot_button = tk.Button(self.frame, text="Plot", command=self.plot_window)
        self.plot_button.grid(row=4) 
        
        self.close_button = tk.Button(self.frame, text="Exit Application", command=master.quit)
        self.close_button.grid(row=5) 

        

        
    def show_results(self):
        print("Showing results")

    def run(self):
        print("Run")

    # def stop_test(self):
    #     self.test_counter == 0;

    def test(self):
#        self.test_counter += 1;
        parser = argparse.ArgumentParser(description='Serenity test-board server.')
#        args = parser.parse_args()
        user_input = self.port_number.get()
        print (user_input)


        port = 1025
        host = 'localhost'
        addr = ( host, port )
        
        ### server socket ###
        serversocket = socket( AF_INET, SOCK_STREAM )
        serversocket.setsockopt( SOL_SOCKET, SO_REUSEADDR, 1 )
        serversocket.bind( addr )
        serversocket.listen( 10 )
        
        self.clients = [serversocket]
        
        buf = 1000000
        tests = [] 

        while True:
            try:
 #           print (self.test_counter)
                print ("Server is listening for connections\n")
                clientsocket, clientaddr = serversocket.accept()
                self.clients.append( clientsocket )
            #        thread.start_new_thread( handler, (clientsocket, clientaddr, buf, tests) )
                th = thread.Thread(target=srv.handler, args=(clientsocket, clientaddr, buf, tests,self.clients,)) 
                th.start()
                th.join()
                #        time.sleep(2) 
                
                if(len(tests)>0) :
                    print (tests[-1].getData())
                    print("Test Completed")

            except KeyboardInterrupt: # Ctrl+C # FIXME: vraci "raise error(EBADF, 'Bad file descriptor')"
                print ("Closing server socket...")
                serversocket.close()

                print("Test Completed")


    def plot_window(self):
        self.window = PlotWindow(self.master)


class PlotWindow(tk.Toplevel):
    def __init__(self, master):        
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
        self.notebook.add(f1, text='Voltage 1')
        self.notebook.add(f2, text='Voltage 2')
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # self.results_button = tk.Button(f1, text="Results", command=self.show_results)
        # self.results_button.pack()

        # Create a canvas
#        self.make_v1_figure(f1)
        self.make_v2_figure(f2)

        data = [['V1', 3, 4], ['V2',3, 3.2, 2.8], ['NextReading', 2, 2.1, 0.7, 2.4], ['test1',3, 4, 5, 6, 7], ['test2',3, 4, 5, 6, 7, 8]]
        
        self.make_figure(f1, data)

        
    def show_results(self):
        print("Showing results")

    def make_figure(self, frame, data):
    
        fig = Figure(figsize=(5, 4), dpi=100)
        t = np.arange(0, 3, .01)
        plt.tight_layout()
        
        for i in range(len(data)):
#            print ( (data[i]) )
            title = data[i][0]
            data[i].pop(0)
            subfig = fig.add_subplot(2,3,i+1)
            subfig.plot( (data[i] ) )
            subfig.set_title(title)
            subfig.set_ylabel('Voltage')

        fig.subplots_adjust(hspace=0.5, wspace=0.4)
            
        canvas = FigureCanvasTkAgg(fig, frame)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        toolbar = NavigationToolbar2Tk(canvas, frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def make_v2_figure(self, frame):
        fig = Figure(figsize=(5, 4), dpi=100)
        t = np.arange(0, 3, .01)
        fig.add_subplot(231).plot(t, 2 * np.sin(2 * np.pi * t))
        fig.add_subplot(233).plot(t, 4 * np.cos(2 * np.pi * t))
        
        
        canvas = FigureCanvasTkAgg(fig, frame)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        toolbar = NavigationToolbar2Tk(canvas, frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


        
root = tk.Tk()
tb_gui = TestBoardGUI(root)

root.mainloop()
