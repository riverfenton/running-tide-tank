# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 18:25:24 2023

@author: rfent
"""
import tkinter
from tkinter import *
from tkinter import ttk
import tkinter.font as font
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import create_nLf_LUT as create_csv
from fileOperations import fileOperations
import numpy as np
from dac import dac_ops

freq = 0 #Default frequency
amp = 0 #Default amplitude
mode = 0 #default mode
tank_len=0 #default length
stroke_len=0 #default stroke
dac_ops.dac_write(0) #Makes sure motor is off by default

#EXPERIMENTAL: Could be used to read in a CSV data of desired data and display
#it as a pop-up plot. Would need to be bound to a button if implemented.
def animate(i):
    plt.style.use('fivethirtyeight')
    data = pd.read_csv('data.csv')
    x = data['x_value']
    y1 = data['total_1']
    y2 = data['total_2']

    plt.cla()

    plt.plot(x, y1, label='Channel 1')
    plt.plot(x, y2, label='Channel 2')

    plt.legend(loc='upper left')
    plt.tight_layout()
    
#EXPERIMENTAL: Test for the above experimental function
def test():
    global ani
    
    ani = FuncAnimation(plt.gcf(), animate, interval=1000)
    plt.tight_layout()
    plt.show()
    
#Sets the new freq when enter button is pressed. Takes in list of adjustable
#back wall lengths that is populated in the CSV file created by read_nLf()
def set_freq_value(length_list):
    global freq, tank_len, allowable_stroke, allowable_amp, mode
    
    selection_tuple = listbox.curselection()
    selection_index = selection_tuple[0]
    freq_tuple = listbox.get(selection_index)
    freq = float(freq_tuple[0])
    mode=mode_list[selection_index]
    tank_len=length_list[selection_index]
    tank_len=round(tank_len[0],2)
    [allowable_stroke, allowable_amp]=gen_amp_sel_list(amp_list, selection_index)
    
    update_run_button() #Makes sure the run button reflects new freq selection
    
def gen_amp_sel_list(amp_list, selection_index):
    whole_TF=amp_list[selection_index]
    [_, _, _, _, _, _, _, crank_shaft, num_stroke]=fileOperations.load_params()
    allowable_stroke=np.linspace(0,crank_shaft,num_stroke)
    allowable_amp=np.around(allowable_stroke*whole_TF,2)
    
    return allowable_stroke, allowable_amp

#Updates the "Run Tank" button to reflect the updated freq/amp values.
def update_run_button(): 
    run_tank['text'] = "Run Tank \n (With Freq=" + str(freq) + "rpm & \n Amp="\
        + str(amp) + "in) \n Tank length: "\
            + str(round(tank_len*39.37,2)) + "in \n" + "Stroke Length:" + \
            str(stroke_len) + "in \n" + "Mode: " + str(int(mode[0]))
    
#Sets the new freq when enter button is pressed
def set_amp_value(): 
    global amp, allowable_stroke, stroke_len
    
    selection_tuple = listbox.curselection()
    selection_index = selection_tuple[0]
    amp_tuple = listbox.get(selection_index)
    amp = float(amp_tuple)
    print(amp)
    stroke_len=allowable_stroke[selection_index]
    
    update_run_button() #Makes sure the run button reflects the new amp
                        #selection
                        
    
#Turns the motor on (or off if f=0) with desired freq by writing to the DAC
def turn_motor_on(f):
    dac_ops.dac_write(f)
    
#EXPERIMENTAL: This is the function to eventually be used to update and rewrite
#the long term parameters. It will be bound to a submit button in the
#update_long_params_w() window once complete. Right now, the .txt file can be
#rewritten successfuly, but the CSV file does not update as intended. We have
#used a dummy params_test.txt file, as well as a dummy nLfA_sort.csv file for
#testing this function. However, until this is fixed, the params.txt file
#should be edited directly from the repository if long-term parameters wish to
#be updated. Please note that updating the file directly can be tricky, as the
#current code is pretty rigid in the values it can take. Our README goes
#further into how to properly update this file
def update_long_params():
    global water_height_var, tank_length_var, track_length_var, \
        num_length_settings_var, min_modes_var, max_modes_var, freq_list, \
            mode_list, length_list, amp_list
            
    water_height = str(water_height_var.get())
    tank_length = str(tank_length_var.get())
    track_length = str(track_length_var.get())
    num_length_settings = str(num_length_settings_var.get())
    min_modes = str(min_modes_var.get())
    max_modes = str(max_modes_var.get())
    
    params_list = [water_height, tank_length, track_length, \
                   num_length_settings, min_modes, max_modes]
        
    print(water_height)
    print(tank_length)
    print(track_length)
    print(num_length_settings)
    print(min_modes)
    print(max_modes)
    
    f= open("params_test.txt","w+")
    for param in params_list:
        f.write(param + '\n')
    f.close()
    
    #Problem is here. Doesn't seem to update the CSV file as desired.
    [freq_list, mode_list, length_list, amp_list]=read_nLf()
    
#Creates CSV of allowed frequencies based on long-term parameters.
def read_nLf():
    create_csv
    mode_list = pd.read_csv('nLfA_sort.csv', header=None, usecols=[0])
    mode_list=mode_list.values.tolist()
    
    length_list = pd.read_csv('nLfA_sort.csv', header=None, usecols=[1])
    length_list=length_list.values.tolist()
    
    freq_list = pd.read_csv('nLfA_sort.csv', header=None, usecols=[2])
    freq_list=round(freq_list, 2)
    freq_list=freq_list.values.tolist()
    
    amp_list = pd.read_csv('nLfA_sort.csv', header=None, usecols=[3])
    amp_list=round(amp_list, 2)
    amp_list=amp_list.values.tolist()
    
    return freq_list, mode_list, length_list, amp_list

#Initializing available frequencies, modes, and tank lengths for given
#long term parameters
[freq_list, mode_list, length_list, amp_list]=read_nLf()

#EXPERIMENTAL: This window will eventually be responsible for letting the user
#update the long-term parameters. It is currently under development, as
#apparent when the button is pressed from the home screen.
def update_long_params_w():
    global water_height_var, tank_length_var, track_length_var, \
    num_length_settings_var, min_modes_var, max_modes_var
    
    #Window creation
    update_w = Toplevel(root, bg="#6CD300")
    
    #Configuring the screen to fit the width of the interface
    update_w_width = update_w.winfo_screenwidth()
    update_w_height= update_w.winfo_screenheight()
    update_w.geometry("%dx%d" % (update_w_width, update_w_height))
      
    #Creating long-term variables to store user inputs
    water_height_var = StringVar()
    tank_length_var = StringVar()
    track_length_var = StringVar()
    num_length_settings_var = StringVar()
    min_modes_var = StringVar()
    max_modes_var = StringVar()
    
    #Creating and placing frame that will contain the selection menu
    params_frame = Frame(update_w, bg='#6CD300')
    params_frame.grid(row=0, column=0, columnspan=2, rowspan=6, sticky='news')
    
    # Creating entries for user input and labels for each
    height_label = Label(params_frame, text = 'Still Water Height', \
                         font=('calibre',10, 'bold'))
    height_entry = Entry(params_frame, textvariable = water_height_var, \
                         font=('calibre',10,'normal'))
      
    tank_l_label = Label(params_frame, text = 'Full Tank Length', font = \
                         ('calibre',10,'bold'))
    tank_l_entry = Entry(params_frame, textvariable = tank_length_var, \
                         font = ('calibre',10,'normal'))
    
    track_l_label = Label(params_frame, text = 'Track Length', \
                          font=('calibre',10, 'bold'))
    track_l_entry = Entry(params_frame, textvariable = track_length_var, \
                          font=('calibre',10,'normal'))
      
    num_length_settings_label = Label(params_frame, \
                                      text = '# of Length Settings', \
                                          font = ('calibre',10,'bold'))
    num_length_settings_entry = Entry(params_frame, textvariable = \
                                      num_length_settings_var, \
                                          font = ('calibre',10,'normal'))
    
    min_modes_label = Label(params_frame, text = 'Min # of Normal Modes', \
                            font=('calibre',10, 'bold'))
    min_modes_entry = Entry(params_frame, textvariable = min_modes_var, \
                            font=('calibre',10,'normal'))
      
    max_modes_label = Label(params_frame, text = 'Max # of Normal Modes', \
                            font = ('calibre',10,'bold'))
    max_modes_entry = Entry(params_frame, textvariable = max_modes_var, \
                            font = ('calibre',10,'normal'))
    
      
    #Creating submit button that executes the experimental update_long_params()
    #function
    sub_btn= Button(params_frame,text = 'Submit', command = update_long_params)
      
    #Placing labels and their corresponding entry bars
    height_label.grid(row=0,column=0)
    height_entry.grid(row=0,column=1)
    tank_l_label.grid(row=1,column=0)
    tank_l_entry.grid(row=1,column=1)
    track_l_label.grid(row=2,column=0)
    track_l_entry.grid(row=2,column=1)
    num_length_settings_label.grid(row=3,column=0)
    num_length_settings_entry.grid(row=3,column=1)
    min_modes_label.grid(row=4,column=0)
    min_modes_entry.grid(row=4,column=1)
    max_modes_label.grid(row=5,column=0)
    max_modes_entry.grid(row=5,column=1)
    
    #Placing button
    sub_btn.grid(row=6,column=1, sticky='news')
    
    #Configuring columns
    update_w.columnconfigure(0, weight=1)
    update_w.rowconfigure(0, weight=1)

#Responsible for creating amplitude and freq selection windows. Takes in
#whether the window should be for amplitude or frequency and takes in the list
#of values to be used in populating the listbox
def amp_and_freq_w(freq_or_amp, list_values):
    global listbox, freq_list, mode_list, length_list
    
    ########## Making the freq and amp input window ############
    freq_and_amp_w = Toplevel(root, bg="#6CD300")
    
    freq_and_amp_w_width= freq_and_amp_w.winfo_screenwidth()
    freq_and_amp_w_height= freq_and_amp_w.winfo_screenheight()
    freq_and_amp_w.geometry("%dx%d" % (freq_and_amp_w_width, \
                                       freq_and_amp_w_height))
    
    ############ Freq Scrollbar/Listbox creation and labeling ################
    style=ttk.Style()
    style.theme_use('classic')
    style.configure("Vertical.TScrollbar", arrowsize=50, background="#D2FA04",\
                    bordercolor="green", troughcolor="#020202", width=130)
    
    #Setting up frames and their layouts
    freq_frame = Frame(freq_and_amp_w, bg="#6CD300")
    buttons_frame = Frame(freq_and_amp_w, bg="#6CD300")
    
    freq_frame.grid(row=0, column=0, padx=20, pady=10, ipadx=1, ipady=5)
    buttons_frame.grid(row=0, column=1, padx=5, pady=5)
    
    #Creating title and placing it accordingly
    titlestr="Select desired " + freq_or_amp + ", then press enter."
    
    l1 = Label(freq_frame, text = titlestr, font=freq_title_font, \
               bg="#6CD300", height=2)
    l1.grid(row=0, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5)

    #Creating logic that chooses whether to customize the page for frequency
    #selection or amplitude selection. Note that it is hardcoded to read in
    #'frequency (rpm)' and should likely be changed to just frequency in the
    #future. This could be reused in the future if any other selection menus
    #are needed
    if freq_or_amp == 'frequency (rpm)':
        #Creates enter button which automatically takes user to the amplitude
        #selection menu and updates the global freq according to their
        #selection in the listbox
        freq_enter = Button(buttons_frame, text = "Enter", font=enter_font, \
                            bg = "#D2FA04", fg = "black", command= \
                                lambda:[set_freq_value(length_list), \
                                        amp_and_freq_w('amplitude (in)', \
                                                       allowable_amp)])
        freq_enter.grid(row=0, column=0)
    
        #Creates back button which exits out of the window and leads back to 
        #the home screen
        freq_back = Button(buttons_frame, text = "Back", font=back_font, \
                           bg = "#FF0303", fg = "black", \
                               command=freq_and_amp_w.destroy)
        freq_back.grid(row=1, column=0, sticky='ew')
    else:
        #Creating enter button for amplitude window.
        amp_enter = Button(buttons_frame, text = "Enter", font=enter_font, \
                           bg = "#D2FA04", fg = "black", command= \
                               lambda:[set_amp_value()])
        amp_enter.grid(row=0, column=0)
    
        #Creates back button which exits out of the window and leads back to
        #the frequency selection menu
        amp_back = Button(buttons_frame, text = "Back", font=back_font, \
                          bg = "#FF0303", fg = "black", \
                              command=freq_and_amp_w.destroy)
        amp_back.grid(row=1, column=0, sticky='ew')

    #Creating listbox for frequency or amplitude options to be populated into
    listbox = Listbox(freq_frame, activestyle=NONE, selectmode=SINGLE, \
                      selectbackground="#D2FA04", font=listbox_font, \
                          height= 13)
        
    #Making and configuring scrollbar for user to naviagte up & down the 
    #listbox options. Also configuring and placing the listbox here
    freq_scrollbar = ttk.Scrollbar(freq_frame, orient='vertical', \
                                   command=listbox.yview)
    listbox.configure(yscrollcommand=freq_scrollbar.set)
    listbox.grid(row=1, column=0, padx=5, pady=5, ipadx=5, ipady=5)
      
    freq_scrollbar.grid(row=1, column=1, sticky='ns')
    freq_scrollbar.config(command=listbox.yview)

    #Populating listbox with given values, whether they be frequencies or
    #amplitudes
    for value in list_values:
        listbox.insert(END, value)        
    freq_scrollbar.config(command=listbox.yview)
        
#EXTRA FEATURE: This function is currently only responsible for resizing the
#buttons in the home screen if the window changes sizes. Is really only needed
#when a mouse and keyboard is being used and the user decides to resize the
#window manually
def resize(e):
     
    size = e.width/10
 
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

########################## CREATING HOME SCREEN ##############################
root = Tk()
root.title("Running Tide Wave Tank")

#Calls upon the resize function to change button size/font when window size is 
#changed
root.bind('<Configure>', resize) 

#Configuring grid of root window
Grid.columnconfigure(root, index = 0,
                     weight = 1)        #For columns
Grid.columnconfigure(root, index = 1,
                     weight = 1)
Grid.rowconfigure(root, 0,
                  weight = 1)
Grid.rowconfigure(root, 1,              #For rows
                  weight = 1)

#Setting up root window's geometry to fit the screen of the monitor
s_width= root.winfo_screenwidth()
s_height= root.winfo_screenheight()
root.geometry("%dx%d" % (s_width, s_height))

#Setting up fonts for buttons/labels/etc.
runningTideFont = font.Font(family='Helvetica Neue', size=40, weight='bold')
listbox_font = font.Font(family='Helvetica Neue', size=45, weight='bold')
enter_font = font.Font(family='Helvetica Neue', size=60, weight='bold')
back_font = font.Font(family='Helvetica Neue', size=60, weight='bold')
freq_title_font = font.Font(family='Helvetica Neue', size=32, weight='bold')

############ Making Home Screen Buttons ######################################

stop = Button(root, text = "Stop Tank", font= runningTideFont, width= 115,
             height= 26, bg = "#6CD300", fg = "red", \
                 command= lambda: [turn_motor_on(0)])

input_freq_amp = Button(root, text = "Input Frequency/ \n Amplitude", \
                        font= runningTideFont, width= 115,
                        height= 26, bg = "#6CD300", fg = "black", \
                            command= lambda: \
                                [amp_and_freq_w('frequency (rpm)',freq_list)])

update_dimensions = Button(root, \
                           text = "Update Tank Dimensions \n or Motor Specs", \
                               font= runningTideFont, width= 115, \
                                   height= 26, bg = "#6CD300", \
                                       fg="black",command=update_long_params_w)

run_tank = Button(root, text = "Run Tank \n (With Freq=" + str(freq) + \
                  "rpm & \n Amp=" + str(amp) + "in) \n Tank length: "\
                      + str(round(tank_len*39.37,2)) + "in \n" + \
                      "Stroke Length:" + str(round(stroke_len,2)) + "in \n" + "Mode: "\
                      + str(mode), font= runningTideFont, width= 115,\
                                  height= 26, bg = "#6CD300", fg = "black", \
                                      command= lambda: [turn_motor_on(freq)])

#Placing buttons in grid
stop.grid(column=1, row=1, sticky="NSEW" )
input_freq_amp.grid(column=0, row=0, sticky="NSEW")
update_dimensions.grid(column=0, row=1, sticky="NSEW")
run_tank.grid(column=1, row=0, sticky="NSEW")

root.mainloop()