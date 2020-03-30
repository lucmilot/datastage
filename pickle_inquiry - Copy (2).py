# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 12:46:19 2018

@author: XT21586
"""
import glob
import pprint, pickle
import os
from html.parser import HTMLParser

import csv

import win32com.client as win32

#import tkinter as tk
#from tkinter import ttk
#from tkinter import *


import tkinter as tk   # Python 3
import tkinter.ttk as ttk

from tkinter import messagebox




from tkinter import *

import xlsxwriter

import re

from time import perf_counter as pc

from queue import Queue 
    
import threading
import time


class Mapping(dict):
   def __init__(self,*arg,**kw):
      super(Mapping, self).__init__(*arg, **kw)


rc_file_nm = ""
line_cum = ""

sw_columns = False
sw_property = False

sw_job_type_full  = False

property_name = ""
o = None

job_hit_list = []
table_hit_list = []

def loadall(filename):
    with open(filename, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break



def chk_if_search_key(job_identifier, tup, srch_re_pattern):
    global job_hit_list
    
    if srch_re_pattern is None:
        return True
    else:
        for x in tup:
            if x is not None:
                m = srch_re_pattern.search(x)
                if m:
                    #listx(0) always contain job_identifier
                    if job_identifier not in job_hit_list:
                        job_hit_list.append(job_identifier)
                    return True
        return False
        


def process_selection(process_type, input_search_string ) :
    global job_row, job_search_row, job_hit_list_row, columns_row, tablename_row, orchestratecode_sql_row , xmlproperties_row, table_hit_list, sw_job_type_full 
    
    if input_search_string != "":
        re_attribute = r".*"+input_search_string+r".*"
        srch_re_pattern = re.compile(re_attribute,re.MULTILINE | re.DOTALL | re.IGNORECASE)
    else :
        srch_re_pattern = None

    tup_h = ('identifier', 'datemodified',  'timemodified', 'search_found')
    [worksheet_job.write_string(job_row,i,item) for i, item in enumerate(tup_h)]
    job_row += 1
    tup_h = ('Job with a search Hit',)
    [worksheet_job_hit_list.write_string(job_hit_list_row,i,item) for i, item in enumerate(tup_h)]
    job_hit_list_row += 1
    
    if (process_type == "job") or (process_type == "all") :
        tup_h = ('job_identifier',)
        [worksheet_job_search.write_string(job_search_row,i,item) for i, item in enumerate(tup_h)]
        job_search_row += 1

    if (process_type == "job") or (process_type == "columns") or (process_type == "all") :
        tup_h = ('job_identifier', 'rc_identifier',  'rc_type',  'rc_name' ,  'column_name','table_def','column_reference')
        [worksheet_columns.write_string(columns_row,i,item) for i, item in enumerate(tup_h)]
        columns_row += 1

    if (process_type == "job") or (process_type == "all") :
        tup_h = ('job_identifier', 'rc_identifier',  'rc_type',  'rc_name' ,  'tablename')
        [worksheet_tablename.write_string(tablename_row,i,item) for i, item in enumerate(tup_h)]
        tablename_row += 1
    
    if (process_type == "job") or (process_type == "select") or (process_type == "all") :
        tup_h = ('job_identifier', 'stg_header', 'sql')
        [worksheet_orchestratecode_sql.write_string(orchestratecode_sql_row,i,item) for i, item in enumerate(tup_h)]
        orchestratecode_sql_row += 1

    if (process_type == "job") or (process_type == "select") or (process_type == "all") :    
        tup_h = ('job_identifier', 'rc_identifier',  'rc_type',  'rc_name' )
        [worksheet_xmlproperties.write_string(xmlproperties_row,i,item) for i, item in enumerate(tup_h)]
        xmlproperties_row += 1
    


#    t0 = pc()
#    t_slot = 1
    for obj in loadall(outfilpkl):
#        if pc() - t0 > 1:
#            t_slot += 1
#            t0 = pc()
#            print(''.join(["." for num in range(t_slot)]))
    
        # job tag doesnt encompass data as detailed in htmlparser_picle.py, 
        # therefore we have start end end tag to process this special case 
        # see htmlparser_picle.py
        
        #start tag
        if obj['tag'] == 'job':
            identifier         = [d for diciter in obj['attributes']          for (k,d) in diciter.items() if k == 'identifier'][0] 
            datemodified       = [d for diciter in obj['attributes']          for (k,d) in diciter.items() if k == 'datemodified'][0] 
            timemodified       = [d for diciter in obj['attributes']          for (k,d) in diciter.items() if k == 'timemodified'][0] 
            found_ind = ''
            #if  process_type == "job" we setup sw_job_type_full that will be used to show all info in all tag for that job 
            #note that if process_type == "all" we also light up that switch
            tup = (identifier,datemodified, timemodified,found_ind)
            tupsrch = (identifier,)
            if (process_type == "job")  or (process_type == "all") :
                if chk_if_search_key(identifier,tupsrch,srch_re_pattern):
                    for i, item in enumerate(tup):
                        if item is not None: 
                            worksheet_job_search.write_string(job_search_row ,i,item)
                    job_search_row  += 1
                    sw_job_type_full = True

        #end tag
        #on the end tage we process the job_hit_list
        if obj['tag'] == '\\job':
            identifier         = [d for diciter in obj['attributes']          for (k,d) in diciter.items() if k == 'identifier'][0] 
            datemodified       = [d for diciter in obj['attributes']          for (k,d) in diciter.items() if k == 'datemodified'][0] 
            timemodified       = [d for diciter in obj['attributes']          for (k,d) in diciter.items() if k == 'timemodified'][0] 
            found_ind = ''
            #in worksheet_job_hit_list we show all job that were involved in a  hit  
            if len(job_hit_list) > 0:
                if identifier in job_hit_list:
                    found_ind = 'Search Found'
                    # we also put job that got a hit in its own datasheet
                    worksheet_job_hit_list.write_string(job_hit_list_row ,0,identifier)
                    job_hit_list_row  += 1                   
            #in worksheet_job we show all job that were looped in , even if no hit 
            tup = (identifier,datemodified, timemodified,found_ind)
            tupsrch = (identifier,)
            for i, item in enumerate(tup):
                if item is not None: 
                    worksheet_job.write_string(job_row ,i,item)
            job_row  += 1   
            sw_job_type_full = False
            
        
        if obj['tag'] == 'columns':
            job_identifier     = [d for diciter in obj['attributes']          for (k,d) in diciter.items() if k == 'job_identifier'][0] 
            rc_identifier      = [d for diciter in obj['attributes']          for (k,d) in diciter.items() if k == 'rc_identifier'][0] 
            rc_type            = [d for diciter in obj['attributes']          for (k,d) in diciter.items() if k == 'rc_type'][0] 
            rc_name            = [d for diciter in obj['attributes']          for (k,d) in diciter.items() if k == 'rc_name'][0] 
            column_name        = [d for diciter in obj['property_attributes'] for (k,d) in diciter.items() if k == 'Name'][0]
            table_def          = [d for diciter in obj['property_attributes'] for (k,d) in diciter.items() if k == 'TableDef'][0]         
            #some time not present
            buf_column_reference = [d for diciter in obj['property_attributes'] for (k,d) in diciter.items() if k == 'ColumnReference']
            if len(buf_column_reference) > 0 :
                column_reference   = buf_column_reference[0]  
            else:
                column_reference = None  
            tup = (job_identifier,rc_identifier ,rc_type,  rc_name, column_name, table_def, column_reference)
            tupsrch = (column_name, column_reference)
            #print(tup)
            if (process_type == "columns") or (process_type == "all")  or (sw_job_type_full == True):
                if (chk_if_search_key(job_identifier,tupsrch,srch_re_pattern) == True) or (sw_job_type_full == True):
                    for i, item in enumerate(tup):
                        if item is not None: 
                            worksheet_columns.write_string(columns_row,i,item)
                    columns_row += 1
                    
                    table_def_x = table_def.split("\\")[-1].split(".")[-1]
                    if (table_def_x,job_identifier) not in table_hit_list:
                        table_hit_list.append((table_def_x,job_identifier))
                 
                    
                                 
        if obj['tag'] == 'tablename':
            job_identifier     = [d for diciter in obj['attributes']          for (k,d) in diciter.items() if k == 'job_identifier'][0] 
            rc_identifier      = [d for diciter in obj['attributes']          for (k,d) in diciter.items() if k == 'rc_identifier'][0] 
            rc_type            = [d for diciter in obj['attributes']          for (k,d) in diciter.items() if k == 'rc_type'][0] 
            rc_name            = [d for diciter in obj['attributes']          for (k,d) in diciter.items() if k == 'rc_name'][0] 
            table_info         = [d for diciter in obj['property_attributes'] for (k,d) in diciter.items() if k == 'Value'][0]
            tup = (job_identifier,rc_identifier ,rc_type,  rc_name,  table_info)
            tupsrch = (table_info,)
            #print(tup)
            if (process_type == "all") or (sw_job_type_full == True) or (sw_job_type_full == True):
                if (chk_if_search_key(job_identifier,tupsrch,srch_re_pattern) == True) or (sw_job_type_full == True):
                    for i, item in enumerate(tup):
                        if item is not None: 
                            worksheet_tablename.write_string(tablename_row ,i,item)
                    tablename_row  += 1                    

            
        if obj['tag'] == 'orchestratecode_sql':
            job_identifier     = [d for diciter in obj['attributes']          for (k,d) in diciter.items() if k == 'job_identifier'][0] 
            stg_header         = [d for diciter in obj['attributes']          for (k,d) in diciter.items() if k == 'stg_header'][0] 
            dqote='"'
            sql                = dqote+obj['data']+dqote          
            tup = (job_identifier,stg_header , sql)
            tupsrch = (sql,)
            if (process_type == "select") or (process_type == "all") or (sw_job_type_full == True):
                if (chk_if_search_key(job_identifier,tupsrch,srch_re_pattern) == True) or (sw_job_type_full == True):
                    [worksheet_orchestratecode_sql.write_string(orchestratecode_sql_row,i,item) for i, item in enumerate(tup)]
                    orchestratecode_sql_row += 1
      
            
        if obj['tag'] == 'xmlproperties':
            job_identifier     = [d for diciter in obj['attributes']          for (k,d) in diciter.items() if k == 'job_identifier'][0] 
            rc_identifier      = [d for diciter in obj['attributes']          for (k,d) in diciter.items() if k == 'rc_identifier'][0] 
            rc_type            = [d for diciter in obj['attributes']          for (k,d) in diciter.items() if k == 'rc_type'][0] 
            rc_name            = [d for diciter in obj['attributes']          for (k,d) in diciter.items() if k == 'rc_name'][0] 
            dqote='"'
            sql                = dqote+obj['data']+dqote       
            tup = (job_identifier,rc_identifier ,rc_type,  rc_name, sql)
            tupsrch = (sql,)
            if (process_type == "select") or (process_type == "all") or (sw_job_type_full == True):
                if (chk_if_search_key(job_identifier,tupsrch,srch_re_pattern) == True) or (sw_job_type_full == True):
                    [worksheet_xmlproperties.write_string(xmlproperties_row,i,item) for i, item in enumerate(tup)]
                    xmlproperties_row += 1


#txt.focus()
#txt = Entry(window,width=10, state='disabled')

def clicked_job():
    global job_search_string
    job_search_string = txt.get()
    lbl.configure(text= "")
    window.destroy()

def clicked_columns():
    global columns_search_string
    columns_search_string = txt.get()
    lbl.configure(text= "")
    window.destroy()
    
def clicked_select():
    global select_search_string
    select_search_string = txt.get()
    lbl.configure(text= "")
    window.destroy()
    
def clicked_all():
    global all_search_string
    all_search_string = txt.get()
    lbl.configure(text= "")
    window.destroy()
 
    
 
    
#-------------------------------------------------------------------------------------   
#when promoted  we want to point to the main directory 
pathx = os.getcwd() + "\\"

#to use in test 
#path = os.getcwd()
#os.chdir("..\\")
#pathx = os.getcwd() + "\\"

outfilpkl = pathx + "pickle1.pkl"

#root = tk.Tk()
#root.withdraw()
#messagebox.showerror("Indicator", outfilpkl +" is the pickle that was used")
#root.destroy()

fpref = "result1"
outfilxls1 = pathx + fpref + ".xls"

if os.path.exists(outfilxls1):
    try:
        os.remove(outfilxls1)
    except: 
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Warning", "file :" + outfilxls1 + " is open.  we will open ...result2 \n PLEASE CLOSE :" + outfilxls1 + " for further run " )
        root.destroy() 
        fpref = "result2"
        outfilxls1 = pathx + fpref + ".xls"        
        


#input_search_string = "V1_LEAS_EQP_REF"
all_search_string = "NOTHING_SELECTED"
job_search_string = "NOTHING_SELECTED"
columns_search_string = "NOTHING_SELECTED"
select_search_string = "NOTHING_SELECTED"
    
    
window = tk.Tk()
window.title("Search Datastage Job for Data Related stuff ")
#window.geometry('100x200')
window.config(height=100, width=200, bg="#C2C2D6")
 
lbl = Label(window, text="Enter the search key or nothing for all \n --then press the proper button--", font=("Arial Bold", 12))
#lbl.pack(padx=100, pady=100, side = 'top')
lbl.grid(column=1, row=1)

txt = Entry(window,width=70)
txt.grid(column=1, row=2)
#txt.pack(padx=100, pady=100, side = 'bottom')

btn = Button(window, text="Searh in \n Job", bg="white", fg="green",  height = 2, width = 10, command=clicked_job)
btn.grid(column=2, row=1)
#btn.pack(padx=10, pady=10, side = 'right')

btn = Button(window, text="Searh in \n Columns", bg="white", fg="green",  height = 2, width = 10, command=clicked_columns)
btn.grid(column=2, row=2)
#btn.pack(padx=10, pady=10, side = 'right')

btn = Button(window, text="Searh in \n Select", bg="white", fg="green", height = 2, width = 10,  command=clicked_select)
btn.grid(column=2, row=3)
#btn.pack(padx=10, pady=10, side = 'right')

btn = Button(window, text="Searh in \n All", bg="white", fg="green", height = 2, width = 10,  command=clicked_all)
btn.grid(column=2, row=4)
#btn.pack(padx=10, pady=10, side = 'right')

window.mainloop()





# Function to check state of thread1 and to update progressbar #
def process_selection_with_progress_bar(thread, root):
    # starts thread #
    thread.start()
    
    root.title("Progressbar ------------")
    root.config(bg = '#F0F0F0')  
                
    canvas = tk.Canvas(root, relief = tk.FLAT, background = "#D2D2D2",
                                            width = 800, height = 20)
                       
    pb1 = ttk.Progressbar(canvas, orient=tk.HORIZONTAL,
                                      length=800, mode="indeterminate"                                     
                                      )

    canvas.create_window(1, 1, anchor=tk.NW, window=pb1)
    canvas.grid()

    # places and starts progress bar #
    pb1.pack()
    pb1.start()

    # checks whether thread is alive #
    while thread.is_alive():
        root.update()
        pass

    # once thread is no longer active, remove pb1 and place the '100%' progress bar #
    pb1.destroy()

    root.destroy()
    
    return 


job_row = 0
job_hit_list_row = 0
job_search_row = 0
columns_row = 0
orchestratecode_sql_row = 0
xmlproperties_row = 0
tablename_row = 0


if (job_search_string == "NOTHING_SELECTED") and (columns_search_string == "NOTHING_SELECTED") and (select_search_string == "NOTHING_SELECTED")  and (all_search_string == "NOTHING_SELECTED"):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Information", "NOTHING_SELECTED")
    root.destroy()
else:
    try:  
        
        with xlsxwriter.Workbook(outfilxls1) as workbook:
            worksheet_job = workbook.add_worksheet('job')
            worksheet_job_hit_list = workbook.add_worksheet('job_hit_list')

            if job_search_string != "NOTHING_SELECTED" :
                worksheet_job_search = workbook.add_worksheet('job search hit')
                worksheet_columns = workbook.add_worksheet('columns')
                worksheet_orchestratecode_sql = workbook.add_worksheet('orchestratecode_sql')
                worksheet_xmlproperties = workbook.add_worksheet('xmlproperties')
                worksheet_tablename = workbook.add_worksheet('tablename')
                argx = ('job',job_search_string)
                
            if columns_search_string != "NOTHING_SELECTED" :
                worksheet_columns = workbook.add_worksheet('columns')
                worksheet_tablename = workbook.add_worksheet('tablename')                
                argx = ('columns',columns_search_string)
                
            elif select_search_string != "NOTHING_SELECTED":
                worksheet_orchestratecode_sql = workbook.add_worksheet('orchestratecode_sql')
                worksheet_xmlproperties = workbook.add_worksheet('xmlproperties')
                argx = ('select',select_search_string)
                
            elif all_search_string != "NOTHING_SELECTED":
                worksheet_job_search = workbook.add_worksheet('job search hit')
                worksheet_columns = workbook.add_worksheet('columns')
                worksheet_orchestratecode_sql = workbook.add_worksheet('orchestratecode_sql')
                worksheet_xmlproperties = workbook.add_worksheet('xmlproperties')
                worksheet_tablename = workbook.add_worksheet('tablename')    
                argx = ('all',all_search_string)
                

#  to debug comment out this                  
            thread1 = threading.Thread(target=process_selection, args=argx)
            pg = tk.Tk()
            process_selection_with_progress_bar(thread1, pg)
            pg.mainloop()    
#  to debug use this    
#            process_selection(argx[0],argx[1])
            
    
            worksheet_tab_list = workbook.add_worksheet('table_job_list')            
            table_hit_list.sort() 
            table_job_list_row = 0
            
            i = 0
            j = 0
            e = 0
            k = 0
            for e,item in enumerate(table_hit_list):
                if e == 0 :
                    worksheet_tab_list.write_string(i,j,item[0])
                    worksheet_tab_list.write_string(i,j+1,item[1])
                else:    
                    if table_hit_list[e][0] ==  table_hit_list[e - 1][0]:
                        k += 1
                        worksheet_tab_list.write_string(i,k,item[1])
                    else:
                        j = 0
                        i += 1
                        k = 1
                        worksheet_tab_list.write_string(i,j,item[0])
                        worksheet_tab_list.write_string(i,j+1,item[1])
    except: 

        workbook.close()
        
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", outfilxls1 +" is already open - or error in processing python code")
        root.destroy()
   
            

    #
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Information", "Calling Excel, should come up soon")
    root.destroy()
        

    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(outfilxls1)
       
    ws = wb.Worksheets("job")
    ws.Columns.AutoFit()  
    ws.Range("A1").AutoFilter
    

    
    if (job_search_string == "NOTHING_SELECTED") and(columns_search_string == "NOTHING_SELECTED") and (select_search_string == "NOTHING_SELECTED")  and (all_search_string == "NOTHING_SELECTED"):
        root = tkinter.Tk()
        root.withdraw()
        messagebox.showinfo("Information","Nothing Selected")
        
    else :
        if (columns_search_string != "NOTHING_SELECTED") :
            ws = wb.Worksheets("columns")
            ws.Columns.VerticalAlignment = win32.constants.xlTop
            ws.Columns.AutoFit()  
            
            ws = wb.Worksheets("table_job_list")
            ws.Columns.ColumnWidth = 30
            ws.Columns.VerticalAlignment = win32.constants.xlTop 
            #ws.Columns.AutoFit()  
            ws.Columns.WrapText = True
            
            
        elif (select_search_string != "NOTHING_SELECTED") :
            ws = wb.Worksheets("orchestratecode_sql")
            ws.Columns.AutoFit()  
            ws.Columns(3).ColumnWidth = 150
            ws.Columns.VerticalAlignment = win32.constants.xlTop
            ws.Columns(3).WrapText = True  
            
            ws = wb.Worksheets("xmlproperties")
            ws.Columns.AutoFit()  
            ws.Columns(5).ColumnWidth = 150
            ws.Columns.VerticalAlignment = win32.constants.xlTop
            ws.Columns(5).WrapText = True
            
            
        elif (all_search_string != "NOTHING_SELECTED") or (job_search_string != "NOTHING_SELECTED") :
            ws = wb.Worksheets("columns")
            ws.Columns.VerticalAlignment = win32.constants.xlTop
            ws.Columns.AutoFit()  
            
            ws = wb.Worksheets("tablename")
            ws.Columns.VerticalAlignment = win32.constants.xlTop
            ws.Columns.AutoFit()  
            
            ws = wb.Worksheets("orchestratecode_sql")
            ws.Columns.AutoFit()  
            ws.Columns(3).ColumnWidth = 150
            ws.Columns.VerticalAlignment = win32.constants.xlTop
            ws.Columns(3).WrapText = True  
            
            ws = wb.Worksheets("xmlproperties")
            ws.Columns.AutoFit()  
            ws.Columns(5).ColumnWidth = 150
            ws.Columns.VerticalAlignment = win32.constants.xlTop
            ws.Columns(5).WrapText = True
            
            ws = wb.Worksheets("table_job_list")
            ws.Columns.ColumnWidth = 30
            ws.Columns.VerticalAlignment = win32.constants.xlTop 
            #ws.Columns.AutoFit()  
            ws.Columns.WrapText = True
            
    
    ws = wb.Worksheets("job_hit_list")
    ws.Columns.ColumnWidth = 30
    ws.Columns.VerticalAlignment = win32.constants.xlTop 
    #ws.Columns.AutoFit()  
    ws.Columns.WrapText = True    
    
    excel.Visible = True   
    
    #wb.save
    
    #excel.Quit
    

     
print ('DONE') 
