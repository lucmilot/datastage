# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 10:20:05 2018

@author: XT21586
"""

import glob
import pprint, pickle
import os
import sys

import tkinter as tk   # Python 3
import tkinter.ttk as ttk

from tkinter import messagebox


from contextlib import contextmanager

@contextmanager
def stdout_redirected(new_stdout):
    save_stdout = sys.stdout
    sys.stdout = new_stdout
    try:
        yield None
    finally:
        sys.stdout = save_stdout


class Mapping(dict):
   def __init__(self,*arg,**kw):
      super(Mapping, self).__init__(*arg, **kw)

def loadall(filename):
    with open(filename, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break


def select_project():  
     
    def clicked_Submit():
        global choice_return
        choice_return = pkl_list[listbox_widget.curselection()[0]]
        master.destroy()

    global choice_return 
    
    choice_return = "" 
     
    pathx = "C:\\Users\\XT21586\\Documents\\document\\Data Stage\\python\\"
    os.chdir(pathx)  
    
    pkl_list = []
    [pkl_list.append(fname) for fname in glob.glob("*.pkl")]
    
    master=tk.Tk()
    
    label=tk.Label(master, text="Select Project"). pack()
    button=tk.Button(master, text="Submit",command=clicked_Submit).pack()
    #checkbox=tkinter.Checkbutton(master, text="CheckBox").pack()
    
    listbox_widget = tk.Listbox(master,selectmode = tk.SINGLE, height = 20, width = 100)
    
    for entry in pkl_list:
        listbox_widget.insert(tk.END, entry)
    
    listbox_widget.pack()
    
    
    master.mainloop()
    
    return choice_return



choice_return = select_project()

if choice_return == "": 
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Information", "NOTHING_SELECTED")
    root.destroy()
    sys.exit()

#to use in test 
#path = os.getcwd()
#os.chdir("..\\")
#pathx = os.getcwd() + "\\"
pathx = 'C:\\Users\\XT21586\\Documents\\document\\Data Stage\\python\\'    
filpkl = pathx + choice_return

    
filename = 'tata'
with open(filename, "w") as f:
    with stdout_redirected(f):
        for obj in loadall(filpkl):
            #if obj['tag'] == '\\job':
            pprint.pprint(obj)       

print('DONE')    