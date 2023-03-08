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
from dac import dac_ops
 
plt.style.use('fivethirtyeight')

index = count()

freq = 0 #Default frequency
amp = 0 #Default amplitude
tank_len=0 #default length
dac_ops.dac_write(0) #motor off by default

def animate(i):
    data = pd.read_csv('data.csv')
    x = data['x_value']
    y1 = data['total_1']
    y2 = data['total_2']

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
    
def set_freq_value(length_list): #Sets the new freq when enter button is pressed
    global freq, tank_len
    selection_tuple = freq_listbox.curselection()
    selection_index = selection_tuple[0]
    freq_tuple = freq_listbox.get(selection_index)
    freq = float(freq_tuple[0])
    tank_len=length_list[selection_index]
    tank_len=round(tank_len[0],2)
    print(freq)
    update_run_button()
    
def update_run_button(): #Updates the "Run Tank" button to reflect the updated freq/amp values.
    run_tank['text'] = "Run Tank \n (With Freq=" + str(freq) + "rpm & \n Amp=" + str(amp) + "m) \n Tank length should be \n set to " + str(round(tank_len*39.37,2)) + "in"
    
def set_amp_value(): #Sets the new freq when enter button is pressed
    global amp
    selection_tuple = freq_listbox.curselection()
    selection_index = selection_tuple[0]
    amp_tuple = freq_listbox.get(selection_index)
    amp = float(amp_tuple[0])
    print(amp)
    update_run_button()
    
def turn_motor_on(f):
    dac_ops.dac_write(f)
    
def update_long_params():
    global water_height_var, tank_length_var, track_length_var, num_length_settings_var, min_modes_var, max_modes_var, freq_list, mode_list, length_list
    water_height = str(water_height_var.get())
    tank_length = str(tank_length_var.get())
    track_length = str(track_length_var.get())
    num_length_settings = str(num_length_settings_var.get())
    min_modes = str(min_modes_var.get())
    max_modes = str(max_modes_var.get())
    
    params_list = [water_height, tank_length, track_length, num_length_settings, min_modes, max_modes]
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
    [freq_list, mode_list, length_list]=read_nLf()
    
def read_nLf():
    #Creates CSV of allowed frequencies
    create_csv
    mode_list = pd.read_csv('nLfA_sort.csv', header=None, usecols=[0])
    mode_list=mode_list.values.tolist()
    
    length_list = pd.read_csv('nLfA_sort.csv', header=None, usecols=[1])
    length_list=length_list.values.tolist()
    
    freq_list = pd.read_csv('nLfA_sort.csv', header=None, usecols=[2])
    freq_list=round(freq_list, 2)
    freq_list=freq_list.values.tolist()
    
    return freq_list, mode_list, length_list

#Initializing available frequencies, modes, and tank lengths for given
#long term parameters
[freq_list, mode_list, length_list]=read_nLf()

def update_long_params_w():
    global water_height_var, tank_length_var, track_length_var, num_length_settings_var, min_modes_var, max_modes_var
    update_w = Toplevel(root, bg="#6CD300")
    
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
         
    params_frame = Frame(update_w, bg='#6CD300')
    params_frame.grid(row=0, column=0, columnspan=2, rowspan=6, sticky='news')
    
    # Creating entries for user input and labels for each
    height_label = Label(params_frame, text = 'Still Water Height', font=('calibre',10, 'bold'))
    height_entry = Entry(params_frame, textvariable = water_height_var, font=('calibre',10,'normal'))
      
    tank_l_label = Label(params_frame, text = 'Full Tank Length', font = ('calibre',10,'bold'))
    tank_l_entry = Entry(params_frame, textvariable = tank_length_var, font = ('calibre',10,'normal'))
    
    track_l_label = Label(params_frame, text = 'Track Length', font=('calibre',10, 'bold'))
    track_l_entry = Entry(params_frame, textvariable = track_length_var, font=('calibre',10,'normal'))
      
    num_length_settings_label = Label(params_frame, text = '# of Length Settings', font = ('calibre',10,'bold'))
    num_length_settings_entry = Entry(params_frame, textvariable = num_length_settings_var, font = ('calibre',10,'normal'))
    
    min_modes_label = Label(params_frame, text = 'Min # of Normal Modes', font=('calibre',10, 'bold'))
    min_modes_entry = Entry(params_frame, textvariable = min_modes_var, font=('calibre',10,'normal'))
      
    max_modes_label = Label(params_frame, text = 'Max # of Normal Modes', font = ('calibre',10,'bold'))
    max_modes_entry = Entry(params_frame, textvariable = max_modes_var, font = ('calibre',10,'normal'))
    
      
    # creating a button using the widget
    # Button that will call the submit function
    sub_btn= Button(params_frame,text = 'Submit', command = update_long_params)
      
    # placing the label and entry in
    # the required position using grid
    # method
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
    
    sub_btn.grid(row=6,column=1, sticky='news')
    
    update_w.columnconfigure(0, weight=1)
    update_w.rowconfigure(0, weight=1)

def amp_and_freq_w(freq_or_amp, list_values):
    global freq_listbox, amp_listbox, freq_list, mode_list, length_list
    
    ########## Making the freq and amp input window ############
    freq_and_amp_w = Toplevel(root, bg="#6CD300")
    
    
    freq_and_amp_w_width= freq_and_amp_w.winfo_screenwidth()
    freq_and_amp_w_height= freq_and_amp_w.winfo_screenheight()
    freq_and_amp_w.geometry("%dx%d" % (freq_and_amp_w_width, freq_and_amp_w_height))
    
    ############ Freq Scrollbar/Listbox creation and labeling ################
    style=ttk.Style()
    style.theme_use('classic')
    style.configure("Vertical.TScrollbar", arrowsize=50, background="#D2FA04", bordercolor="green", troughcolor="#020202", width=130)
    
    #Setting up frames and their layouts
    freq_frame = Frame(freq_and_amp_w, bg="#6CD300")
    buttons_frame = Frame(freq_and_amp_w, bg="#6CD300")
    
    freq_frame.grid(row=0, column=0, padx=20, pady=10, ipadx=1, ipady=5)
    buttons_frame.grid(row=0, column=1, padx=5, pady=5)
    
    #Creating directions as well as enter and back button
    titlestr="Select desired " + freq_or_amp + ", then press enter."
    l1 = Label(freq_frame, text = titlestr, font=freq_title_font, bg="#6CD300", height=2)
    l1.grid(row=0, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5)

    if freq_or_amp == 'frequency (rpm)':
        freq_enter = Button(buttons_frame, text = "Enter", font=enter_font, bg = "#D2FA04", fg = "black", command= lambda:[set_freq_value(length_list), amp_and_freq_w('amplitude (in)', freq_list)])
        freq_enter.grid(row=0, column=0)
    
        freq_back = Button(buttons_frame, text = "Back", font=back_font, bg = "#FF0303", fg = "black", command=freq_and_amp_w.destroy)
        freq_back.grid(row=1, column=0, sticky='ew')
    else:
        amp_enter = Button(buttons_frame, text = "Enter", font=enter_font, bg = "#D2FA04", fg = "black", command= lambda:[set_amp_value()])
        amp_enter.grid(row=0, column=0)
    
        amp_back = Button(buttons_frame, text = "Back", font=back_font, bg = "#FF0303", fg = "black", command=freq_and_amp_w.destroy)
        amp_back.grid(row=1, column=0, sticky='ew')

    freq_listbox = Listbox(freq_frame, activestyle=NONE, selectmode=SINGLE, selectbackground="#D2FA04", font=listbox_font, height= 13)
    freq_scrollbar = ttk.Scrollbar(freq_frame, orient='vertical', command=freq_listbox.yview)
    freq_listbox.configure(yscrollcommand=freq_scrollbar.set)
    freq_listbox.grid(row=1, column=0, padx=5, pady=5, ipadx=5, ipady=5)
      
    freq_scrollbar.grid(row=1, column=1, sticky='ns')
    freq_scrollbar.config(command=freq_listbox.yview)

    # freq_list = pd.read_csv('nLfA_sorted.CSV', header=None, usecols=[2])
    # freq_list=round(freq_list, 2)
    # freq_list=freq_list.values.tolist()

    #Populating freq listbox
    for value in list_values:
        freq_listbox.insert(END, value)        
    freq_scrollbar.config(command=freq_listbox.yview)
        
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

#Setting up fonts for buttons/labels/etc.
runningTideFont = font.Font(family='Helvetica Neue', size=40, weight='bold')
listbox_font = font.Font(family='Helvetica Neue', size=45, weight='bold')
enter_font = font.Font(family='Helvetica Neue', size=60, weight='bold')
back_font = font.Font(family='Helvetica Neue', size=60, weight='bold')
freq_title_font = font.Font(family='Helvetica Neue', size=32, weight='bold')

############ Making Buttons ####################

stop = Button(root, text = "Stop Tank", font= runningTideFont, width= 115,
             height= 26, bg = "#6CD300", fg = "red", command= lambda: [turn_motor_on(0)])

input_freq_amp = Button(root, text = "Input Frequency/ \n Amplitude", font= runningTideFont, width= 115,
                        height= 26, bg = "#6CD300", fg = "black", command= lambda: [amp_and_freq_w('frequency (rpm)',freq_list)])

update_dimensions = Button(root, text = "Update Tank Dimensions \n or Motor Specs", font= runningTideFont, width= 115,
                        height= 26, bg = "#6CD300", fg = "black", command=update_long_params_w)

run_tank = Button(root, text = "Run Tank \n (With Freq=" + str(freq) + "rpm & \n Amp=" + str(amp) + "m) \n Tank length should be \n set to " + str(tank_len) + "m", font= runningTideFont, width= 115,
                        height= 26, bg = "#6CD300", fg = "black", command= lambda: [turn_motor_on(freq)])

# set Button grid
stop.grid(column=1, row=1, sticky="NSEW" )
input_freq_amp.grid(column=0, row=0, sticky="NSEW")
update_dimensions.grid(column=0, row=1, sticky="NSEW")
run_tank.grid(column=1, row=0, sticky="NSEW")


root.mainloop()