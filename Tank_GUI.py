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
#from dac import dac_ops
 
plt.style.use('fivethirtyeight')

index = count()

freq = 0 #Default frequency
amp = 0 #Default amplitude

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
    
def set_freq_value(): #Sets the new freq when enter button is pressed
    global freq
    selection_tuple = freq_listbox.curselection()
    selection_index = selection_tuple[0]
    freq_tuple = freq_listbox.get(selection_index)
    freq = float(freq_tuple[0])
    print(freq)
    update_run_button()
    
    #dac_ops.dac_write(freq)
    
def update_run_button(): #Updates the "Run Tank" button to reflect the updated freq/amp values.
    run_tank['text'] = "Run Tank \n (With Freq=" + str(freq) + "rpm & \n Amp=" + str(amp) + "m)"
    
def set_amp_value(): #Sets the new freq when enter button is pressed
    global amp
    selection_tuple = freq_listbox.curselection()
    selection_index = selection_tuple[0]
    amp_tuple = freq_listbox.get(selection_index)
    amp = float(amp_tuple[0])
    print(amp)
    update_run_button()
    
def read_nLf():
    #Creates CSV of allowed frequencies
    create_csv
    mode_list = pd.read_csv('nLfA_sort.csv', header=None, usecols=[0])
    mode_list=mode_list.values.tolist()
    
    length_list = pd.read_csv('nLfA_sort.csv', header=None, usecols=[1])
    #length_list=mode_list.values.tolist()
    
    freq_list = pd.read_csv('nLfA_sort.csv', header=None, usecols=[2])
    freq_list=round(freq_list, 2)
    freq_list=freq_list.values.tolist()
    
    return freq_list, mode_list, length_list

#Initializing available frequencies, modes, and tank lengths for given
#long term parameters
[freq_list, mode_list, length_list]=read_nLf()

def update_long_params():
    update_w = Toplevel(root, bg="#6CD300")
    
    update_w_width = update_w.winfo_screenwidth()
    update_w_height= update_w.winfo_screenheight()
    update_w.geometry("%dx%d" % (update_w_width, update_w_height))
      
    # declaring int variable
    # for storing name and password
    name_var = IntVar()
    passw_var = IntVar()
     
    #name=name_var.get()
    #password=passw_var.get()
         
    # creating a label for
    # name using widget Label
    name_label = tk.Label(root, text = 'Username', font=('calibre',10, 'bold'))
      
    # creating a entry for input
    # name using widget Entry
    name_entry = tk.Entry(root,textvariable = name_var, font=('calibre',10,'normal'))
      
    # creating a label for password
    passw_label = tk.Label(root, text = 'Password', font = ('calibre',10,'bold'))
      
    # creating a entry for password
    passw_entry=tk.Entry(root, textvariable = passw_var, font = ('calibre',10,'normal'), show = '*')
      
    # creating a button using the widget
    # Button that will call the submit function
    sub_btn=tk.Button(root,text = 'Submit', command = submit)
      
    # placing the label and entry in
    # the required position using grid
    # method
    name_label.grid(row=0,column=0)
    name_entry.grid(row=0,column=1)
    passw_label.grid(row=1,column=0)
    passw_entry.grid(row=1,column=1)
    sub_btn.grid(row=2,column=1)

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
        freq_enter = Button(buttons_frame, text = "Enter", font=enter_font, bg = "#D2FA04", fg = "black", command= lambda:[set_freq_value(), amp_and_freq_w('amplitude (in)', freq_list)])
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

plot = Button(root, text = "Stop Tank", font= runningTideFont, width= 115,
             height= 26, bg = "#6CD300", fg = "red", command=test)

input_freq_amp = Button(root, text = "Input Frequency/ \n Amplitude", font= runningTideFont, width= 115,
                        height= 26, bg = "#6CD300", fg = "black", command= lambda: [amp_and_freq_w('frequency (rpm)',freq_list)])

update_dimensions = Button(root, text = "Update Tank Dimensions \n or Motor Specs", font= runningTideFont, width= 115,
                        height= 26, bg = "#6CD300", fg = "black", command=test)

run_tank = Button(root, text = "Run Tank \n (With Freq=" + str(freq) + "rpm & \n Amp=" + str(amp) + "m)", font= runningTideFont, width= 115,
                        height= 26, bg = "#6CD300", fg = "black", command=test)

# set Button grid
plot.grid(column=1, row=1, sticky="NSEW" )
input_freq_amp.grid(column=0, row=0, sticky="NSEW")
update_dimensions.grid(column=0, row=1, sticky="NSEW")
run_tank.grid(column=1, row=0, sticky="NSEW")


root.mainloop()