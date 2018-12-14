import tkinter as tk
import tkinter.ttk as ttk
import matplotlib as mpl
import numpy as np
import sys
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg

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

        # Create a canvas
        w, h = 300, 200
        canvas = tk.Canvas(f1, width=w, height=h)
        canvas.pack()

        # Generate some example data
        X = np.linspace(0, 2 * np.pi, 50)
        Y = np.sin(X)

        # Create the figure we desire to add to an existing canvas
        fig = mpl.figure.Figure(figsize=(2, 1))
        ax = fig.add_axes([0, 0, 1, 1])
        ax.plot(X, Y)
        
        # Keep this handle alive, or else figure will disappear
        fig_x, fig_y = 100, 100
        fig_photo = draw_figure(canvas, fig, loc=(fig_x, fig_y))
        fig_w, fig_h = fig_photo.width(), fig_photo.height()

        
        # Add more elements to the canvas, potentially on top of the figure
        canvas.create_line(200, 50, fig_x + fig_w / 2, fig_y + fig_h / 2)
        canvas.create_text(200, 50, text="Zero-crossing", anchor="s")

    def show_results(self):
        print("Showing results")


    def draw_figure(canvas, figure, loc=(0, 0)):
        """ Draw a matplotlib figure onto a Tk canvas
        
        loc: location of top-left corner of figure on canvas in pixels.
        Inspired by matplotlib source: lib/matplotlib/backends/backend_tkagg.py
        """
        figure_canvas_agg = FigureCanvasAgg(figure)
        figure_canvas_agg.draw()
        figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
        figure_w, figure_h = int(figure_w), int(figure_h)
        photo = tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)
        
        # Position: convert from top-left anchor to center anchor
        canvas.create_image(loc[0] + figure_w/2, loc[1] + figure_h/2, image=photo)

        # Unfortunately, there's no accessor for the pointer to the native renderer
        tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)
        
        # Return a handle which contains a reference to the photo object
        # which must be kept live or else the picture disappears
        return photo
        
root = tk.Tk()
tb_gui = TestBoardGUI(root)

root.mainloop()
