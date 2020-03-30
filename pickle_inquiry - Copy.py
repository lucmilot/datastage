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

try:
  import Tkinter              # Python 2
  import ttk
except ImportError:
  import tkinter as Tkinter   # Python 3
  import tkinter.ttk as ttk


import xlsxwriter

import re

from time import perf_counter as pc


class Mapping(dict):
   def __init__(self,*arg,**kw):
      super(Mapping, self).__init__(*arg, **kw)


rc_file_nm = ""
line_cum = ""

sw_columns = False
sw_property = False
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
    global job_row, columns_row, tablename_row, orchestratecode_sql_row , xmlproperties_row, table_hit_list
    
    if input_search_string != "":
        re_attribute = r".*"+input_search_string+r".*"
        srch_re_pattern = re.compile(re_attribute,re.MULTILINE | re.DOTALL | re.IGNORECASE)
    else :
        srch_re_pattern = None

    tup_h = ('identifier', 'datemodified',  'timemodified', 'search_found')
    [worksheet_job.write_string(job_row,i,item) for i, item in enumerate(tup_h)]
    job_row += 1

    if (process_type == "columns") or (process_type == "all") :
        tup_h = ('job_identifier', 'rc_identifier',  'rc_type',  'rc_name' ,  'column_name','table_def','column_reference')
        [worksheet_columns.write_string(columns_row,i,item) for i, item in enumerate(tup_h)]
        columns_row += 1

    if (process_type == "all") :
        tup_h = ('job_identifier', 'rc_identifier',  'rc_type',  'rc_name' ,  'tablename')
        [worksheet_tablename.write_string(tablename_row,i,item) for i, item in enumerate(tup_h)]
        tablename_row += 1
    
    if (process_type == "select") or (process_type == "all") :
        tup_h = ('job_identifier', 'stg_header', 'sql')
        [worksheet_orchestratecode_sql.write_string(orchestratecode_sql_row,i,item) for i, item in enumerate(tup_h)]
        orchestratecode_sql_row += 1

    if (process_type == "select") or (process_type == "all") :    
        tup_h = ('job_identifier', 'rc_identifier',  'rc_type',  'rc_name' )
        [worksheet_xmlproperties.write_string(xmlproperties_row,i,item) for i, item in enumerate(tup_h)]
        xmlproperties_row += 1
    


    t0 = pc()
    t_slot = 1
    for obj in loadall(outfilpkl):
        if pc() - t0 > 1:
            t_slot += 1
            t0 = pc()
            print(''.join(["." for num in range(t_slot)]))
            
            pb.step()

        
        # job tag is present in the pickle only on the end tag, therefore we can use the job_hit_list
        if obj['tag'] == 'job':
            identifier         = [d for diciter in obj['attributes']          for (k,d) in diciter.items() if k == 'identifier'][0] 
            datemodified       = [d for diciter in obj['attributes']          for (k,d) in diciter.items() if k == 'datemodified'][0] 
            timemodified       = [d for diciter in obj['attributes']          for (k,d) in diciter.items() if k == 'timemodified'][0] 
            found_ind = ''
            if len(job_hit_list) > 0:
                if identifier in job_hit_list:
                    found_ind = 'Search Found'
            tup = (identifier,datemodified, timemodified,found_ind)
            for i, item in enumerate(tup):
                if item is not None: 
                    worksheet_job.write_string(job_row ,i,item)
            job_row  += 1

        
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
            tupsrch = (job_identifier, column_name, table_def, column_reference)
            #print(tup)
            if (process_type == "columns") or (process_type == "all") :
                if chk_if_search_key(job_identifier,tupsrch,srch_re_pattern):
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
            tupsrch = (job_identifier,table_info)
            #print(tup)
            if (process_type == "all") :
                if chk_if_search_key(job_identifier,tupsrch,srch_re_pattern):
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
            tupsrch = (job_identifier,sql)
            if (process_type == "select") or (process_type == "all") :
                if chk_if_search_key(job_identifier,tupsrch,srch_re_pattern):
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
            tupsrch = (job_identifier,sql)
            if (process_type == "select") or (process_type == "all") :
                if chk_if_search_key(job_identifier,tupsrch,srch_re_pattern):
                    [worksheet_xmlproperties.write_string(xmlproperties_row,i,item) for i, item in enumerate(tup)]
                    xmlproperties_row += 1


#txt.focus()
#txt = Entry(window,width=10, state='disabled')

def clicked_columns():
    global columns_search_string
    columns_search_string = txt.get()
    lbl.configure(text= "")
    #window.quit()
    window.destroy()
    
def clicked_select():
    global select_search_string
    select_search_string = txt.get()
    lbl.configure(text= "")
    #window.quit()
    window.destroy()
    
def clicked_all():
    global all_search_string
    all_search_string = txt.get()
    lbl.configure(text= "")
    #window.quit()
    window.destroy()
 
    
 
    
#-------------------------------------------------------------------------------------   
#when promoted  we want to point to the main directory 
pathx = os.getcwd() + "\\"

#to use in test 
#path = os.getcwd()
#os.chdir("..\\")
#pathx = os.getcwd() + "\\"

outfilpkl = pathx + "pickle1.pkl"
fpref = "result1"
outfilxls1 = pathx + fpref + ".xls"

if os.path.exists(outfilxls1):
    try:
        os.remove(outfilxls1)
    except: 
        print ("file :" + outfilxls1 + " is open.  we will open ")
        print ("PLEASE CLOSE :" + outfilxls1 + " for further run " )
        fpref = "result2"
        outfilxls1 = pathx + fpref + ".xls"        
        


#input_search_string = "V1_LEAS_EQP_REF"
all_search_string = "NOTHING_SELECTED"
columns_search_string = "NOTHING_SELECTED"
select_search_string = "NOTHING_SELECTED"
    
    
window = Tk()
window.title("Search Datastage Job for Data Related stuff")
#window.geometry('100x200')
window.config(height=100, width=200, bg="#C2C2D6")
 
lbl = Label(window, text="Enter the search key or nothing for all", font=("Arial Bold", 10))
#lbl.pack(padx=100, pady=100, side = 'top')
lbl.grid(column=1, row=1)

txt = Entry(window,width=70)
txt.grid(column=1, row=2)
#txt.pack(padx=100, pady=100, side = 'bottom')

btn = Button(window, text="Srch \n Columns", bg="white", fg="green",  height = 2, width = 10, command=clicked_columns)
btn.grid(column=2, row=1)
#btn.pack(padx=10, pady=10, side = 'right')

btn = Button(window, text="Srch \n Select", bg="white", fg="green", height = 2, width = 10,  command=clicked_select)
btn.grid(column=2, row=2)
#btn.pack(padx=10, pady=10, side = 'right')

btn = Button(window, text="Srch \n All", bg="white", fg="green", height = 2, width = 10,  command=clicked_all)
btn.grid(column=2, row=3)
#btn.pack(padx=10, pady=10, side = 'right')

window.mainloop()



root = tk.Tk()
pb = ttk.Progressbar(root, orient='horizontal', mode='indeterminate')
pb.pack(expand=True, fill=tk.BOTH, side=tk.TOP)
pb.start(50)
pb.pack(expand=1, fill=tk.BOTH)






job_row = 0
columns_row = 0
orchestratecode_sql_row = 0
xmlproperties_row = 0
tablename_row = 0


if (columns_search_string == "NOTHING_SELECTED") and (select_search_string == "NOTHING_SELECTED")  and (all_search_string == "NOTHING_SELECTED"):
    print ("NOTHING_SELECTED")
else:
    try:  

        
        with xlsxwriter.Workbook(outfilxls1) as workbook:
            worksheet_job = workbook.add_worksheet('job')
        
            if columns_search_string != "NOTHING_SELECTED" :
                worksheet_columns = workbook.add_worksheet('columns')
                process_selection('columns',columns_search_string)
                
            elif select_search_string != "NOTHING_SELECTED":
                worksheet_orchestratecode_sql = workbook.add_worksheet('orchestratecode_sql')
                worksheet_xmlproperties = workbook.add_worksheet('xmlproperties')
                process_selection('select',select_search_string)
                
            elif all_search_string != "NOTHING_SELECTED":
                worksheet_columns = workbook.add_worksheet('columns')
                worksheet_orchestratecode_sql = workbook.add_worksheet('orchestratecode_sql')
                worksheet_xmlproperties = workbook.add_worksheet('xmlproperties')
                worksheet_tablename = workbook.add_worksheet('tablename')
                process_selection('all',all_search_string)   
        
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
        print (outfilxls1 +" is already open - or erro in processing python code")                
            


    pb.stop()


    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(outfilxls1)
       
    ws = wb.Worksheets("job")
    ws.Columns.AutoFit()  
    
    if (columns_search_string == "NOTHING_SELECTED") and (select_search_string == "NOTHING_SELECTED")  and (all_search_string == "NOTHING_SELECTED"):
        print ("NOTHING_SELECTED")
    else :
        if (columns_search_string != "NOTHING_SELECTED") :
            ws = wb.Worksheets("columns")
            ws.Columns.VerticalAlignment = win32.constants.xlTop
            ws.Columns.AutoFit()  
            
            
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
            
            
        elif all_search_string != "NOTHING_SELECTED":
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
    
    excel.Visible = True   
    
    #wb.save
    
    #excel.Quit
    

     
print ('DONE') 
