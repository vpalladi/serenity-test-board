import tkinter as tk
import tkinter.ttk as ttk


# from tkinter import *
# from tkinter.ttk import *

class TestBoardGUI:
    def __init__(self, master):
        self.master = master
        master.title("HGCal Board Tester v0.1")
        master.geometry("400x300")
        
        self.frame = tk.Frame(master)
        self.frame.pack()
        
        self.label = tk.Label(self.frame, text="Run Board Tests")
        self.label.pack()

        self.test_button = tk.Button(self.frame, text="Test", command=self.test)
        self.test_button.pack()

        self.run_button = tk.Button(self.frame, text="Run", command=self.run)
        self.run_button.pack()

        self.results_button = tk.Button(self.frame, text="Results", command=self.show_results)
        self.results_button.pack()

        self.plot_button = tk.Button(self.frame, text="Plot", command=self.plot_window)
        self.plot_button.pack()
        
        self.close_button = tk.Button(self.frame, text="Exit Application", command=master.quit)
        self.close_button.pack()

        
        
        
    def show_results(self):
        print("Showing results")

    def run(self):
        print("Run")

    def test(self):
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

        self.notebook = ttk.Notebook(self)
        f1 = tk.Frame(self.notebook)   # first page, which would get widgets gridded into it
        f2 = tk.Frame(self.notebook)   # second page
        self.notebook.add(f1, text='Voltage 1')
        self.notebook.add(f2, text='Voltage 2')
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.results_button = tk.Button(f1, text="Results", command=self.show_results)
        self.results_button.pack()

    def show_results(self):
        print("Showing results")
        
root = tk.Tk()
tb_gui = TestBoardGUI(root)

root.mainloop()
