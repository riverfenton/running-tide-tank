# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 18:25:24 2023

@author: rfent
"""

from tkinter import *
import tkinter.font as font
# import random
# from PIL import ImageTk, Image
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
# import numpy
 
plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []

index = count()

freq = 0 #Default frequency
amp = 0 #Default amplitude

def animate(i):
    data = pd.read_csv('data.csv')
    x = data['x_value']
    y1 = data['total_1']
    y2 = data['total_2']

    # x=pd.Series.to_series(x)
    # y1=pd.Series.to_series(y1)
    # y2=pd.Series.to_series(y2)

    plt.cla()

    plt.plot(x, y1, label='Channel 1')
    plt.plot(x, y2, label='Channel 2')

    plt.legend(loc='upper left')
    plt.tight_layout()
    
def test():
    global ani
    ani = FuncAnimation(plt.gcf(), animate, interval=1000)
    plt.tight_layout()
    plt.show()
    
def set_freq_value(): #Sets the new freq when enter button is pressed
    selection_tuple = freq_listbox.curselection()
    selection_index = selection_tuple[0]
    freq = selection_index
    print(freq)
    
def set_amp_value(): #Sets the new freq when enter button is pressed
    selection_tuple = amp_listbox.curselection()
    selection_index = selection_tuple[0]
    amp = selection_index
    print(amp)

def amp_and_freq_w():
    global freq_listbox, amp_listbox
    ########## Making the freq and amp input window ############
    freq_and_amp_w = Toplevel(root)
      
    ############ Freq Scrollbar creation and labeling ################
    freq_frame = Frame(freq_and_amp_w)

    freq_scrollbar = Scrollbar(freq_frame, orient='vertical')

    freq_listbox = Listbox(freq_frame, selectmode=SINGLE, width=50, yscrollcommand=freq_scrollbar.set)
    freq_listbox.pack(side = LEFT, fill = BOTH)
      
    freq_scrollbar.pack(side = RIGHT, fill = Y)
    freq_frame.pack()
    l1 = Label(freq_and_amp_w, text = "Select Desired Frequency")
    l1.pack()

    freq_enter = Button(freq_and_amp_w, text = "Enter", width=15,
                 height=2, bg = "#6CD300", fg = "black", command=set_freq_value)
    freq_enter.pack()

    for values in range(100):
        freq_listbox.insert(END, values)
        
    ############ Amp Scrollbar creation and labeling ################
      
    amp_frame = Frame(freq_and_amp_w)

    amp_scrollbar = Scrollbar(amp_frame, orient='vertical')

    amp_listbox = Listbox(amp_frame, selectmode=SINGLE, width=50, yscrollcommand=amp_scrollbar.set)
    amp_listbox.pack(side = LEFT, fill = BOTH)
      
    amp_scrollbar.pack(side = RIGHT, fill = Y)
    amp_frame.pack()
    l2 = Label(freq_and_amp_w, text = "Select Desired Amplitude")
    l2.pack()

    amp_enter = Button(freq_and_amp_w, text = "Enter", width=15,
                 height=2, bg = "#6CD300", fg = "black", command=set_amp_value)
    amp_enter.pack()

    for values in range(100):
        amp_listbox.insert(END, values)
        
def resize(e): #Resizes buttons and their fonts when window size changes
     
    # get window width
    size = e.width/10
 
    # define text size on different condition
 
    # if window height is greater
    # than 300 and less than 400 (set font size 40)
    if e.height <= 400 and e.height > 300:
        plot.config(font = ("Helvetica Neue", 40))
        input_freq_amp.config(font = ("Helvetica Neue", 40))
        update_dimensions.config(font = ("Helvetica Neue", 40))
        run_tank.config(font = ("Helvetica Neue", 40))
 
    # if window height is greater than
    # 200 and less than 300 (set font size 30)
    elif e.height < 300 and e.height > 200:
        plot.config(font = ("Helvetica Neue", 20))
        input_freq_amp.config(font = ("Helvetica Neue", 20))
        update_dimensions.config(font = ("Helvetica Neue", 20))
        run_tank.config(font = ("Helvetica Neue", 20))
 
    # if window height is less
    # than 200 (set font size 40)
    elif e.height < 200:
        plot.config(font = ("Helvetica Neue", 10))
        input_freq_amp.config(font = ("Helvetica Neue", 10))
        update_dimensions.config(font = ("Helvetica Neue", 10))
        run_tank.config(font = ("Helvetica Neue", 10))

# create root window
root = Tk()
root.title("Welcome")
root.bind('<Configure>', resize) #Calls upon the resize function to change button size/font when window size is changed

#Configuring grid of root window
Grid.columnconfigure(root, index = 0,
                     weight = 1)        ##For columns
Grid.columnconfigure(root, index = 1,
                     weight = 1)
Grid.rowconfigure(root, 0,
                  weight = 1)
Grid.rowconfigure(root, 1,              ##For rows
                  weight = 1)

#Setting up root window's geometry to fit the screen of the monitor
s_width= root.winfo_screenwidth()
s_height= root.winfo_screenheight()
root.geometry("%dx%d" % (s_width, s_height))

#Setting up font for buttons/labels/etc.
runningTideFont = font.Font(family='Helvetica Neue', size=40, weight='bold')
 
plot = Button(root, text = "Plot", font= runningTideFont, width= 115,
             height= 26, bg = "#6CD300", fg = "black", command=test)

input_freq_amp = Button(root, text = "Input Frequency/Amplitude", font= runningTideFont, width= 115,
                        height= 26, bg = "#6CD300", fg = "black", command=amp_and_freq_w)

update_dimensions = Button(root, text = "Update Tank Dimensions \n or Motor Specs", font= runningTideFont, width= 115,
                        height= 26, bg = "#6CD300", fg = "black", command=test)

run_tank = Button(root, text = "Run Tank", font= runningTideFont, width= 115,
                        height= 26, bg = "#6CD300", fg = "black", command=test)

# set Button grid
plot.grid(column=1, row=1, sticky="NSEW" )
input_freq_amp.grid(column=0, row=0, sticky="NSEW")
update_dimensions.grid(column=0, row=1, sticky="NSEW")
run_tank.grid(column=1, row=0, sticky="NSEW")


root.mainloop()