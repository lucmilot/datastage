# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 13:43:46 2018

@author: XT21586
"""
import win32com.client as win32

pathx = "C:\\Users\\XT21586\Documents\\document\\Data Stage\\python\\build\\exe.win-amd64-3.6\\"

excel = win32.gencache.EnsureDispatch('Excel.Application')

outfilxls1 = pathx + "result1.xls"

wb = excel.Workbooks.Open(outfilxls1)

#try:
#    wb = excel.Workbooks.Open(outfilxls1)
#except:
#    print (outfilxls1 +" is already open!")


excel.Visible = True  