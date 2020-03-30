# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 12:46:19 2018

@author: XT21586
"""
import glob
import pprint, pickle
import os
from html.parser import HTMLParser

#import csv
#import win32com.client as win32
#import re



class Mapping(dict):
   def __init__(self,*arg,**kw):
      super(Mapping, self).__init__(*arg, **kw)


rc_file_nm = ""
line_cum = ""

sw_columns = False
sw_property = False
sw_orchestratecode_sql = False
sw_xmlproperties = False
sw_tablename = False
sw_job = False
property_name = ""
o = None
o_job = None

class MyHTMLParser(HTMLParser):
    #the HTMLParser parent class allow us to parse the html with: attrs, etc
    
    def handle_starttag(self, tag, attrs):
        global sw_job, sw_columns, sw_orchestratecode_sql,sw_xmlproperties,sw_property, sw_tablename, property_name, o, o_job
        f1.write("Start tag:" + tag + "\n")

        # for the job we use o_job as it encompass all tags and the search_block function only return one row 
        # the o_job will be picled at the end tag 
        if tag == 'job':
            sw_job = True
            o_job = Mapping()
            o_job['tag'] = "job"
            o_job['attributes'] = []
            for attr in attrs:
                o_job['attributes'].append(dict([(attr[0],attr[1])]))
            f1.write("     attr:" + "(" + attr[0] +"," + attr[1] + ")\n")   
            #the job encompass everythin and we therefore only check for the tag, not the full encompassing data 
            #o_job is settup ins the handle_starttag routine 
    
            pickle.dump(o_job, outputpkl)
            o_job['tag'] = "\job" 
            # this will be pickled when the end job tag will be hit in the handle_endtag routine 
        
            sw_job = False 

             
        if tag == 'columns':
            #ex:
            #{'attributes': [{'job_identifier': 'DSPD21GG_030_Prepare_Lkps_T2_PSC_SHIP_ADD_ATTR_REL_Job_orig'},
            #                {'rc_identifier': 'V628S2P1'},
            #                {'rc_type': 'CustomOutput'},
            #                {'rc_name': 'lnk_RevPart_Ref'}],
            # 'property_attributes': [{'Name': 'DW_UPD_RUN_DT'},
            #                         {'TableDef': 'Database\\NETZDEV\\ADMIN.V3_PSC_REV_PAYR_CURR_REL'},
            #                         {'ColumnReference': 'DW_UPD_RUN_DT'}],
            # 'tag': 'columns'}
            sw_columns = True
            o = Mapping()
            o['tag'] = tag
            o['attributes'] = []
            o['property_attributes'] = []
            for attr in attrs:
                o['attributes'].append(dict([(attr[0],attr[1])]))
            f1.write("     attr:" + "(" + attr[0] +"," + attr[1] + ")\n")
            
            
        if tag == 'tablename':
            #ex:
            #{'attributes': [{'job_identifier': 'DB2_To_DB2_V1_CRLD_SHIP_EVT'},
            #                {'rc_identifier': 'V3S0P2'},
            #                {'rc_type': 'CustomInput'},
            #                {'rc_name': 'lnk_Transfer_Data'}],
            # 'property_attributes': [],
            # 'tag': 'tablename'}
            sw_tablename = True
            o = Mapping()
            o['tag'] = tag
            o['attributes'] = []
            o['property_attributes'] = []
            for attr in attrs:
                o['attributes'].append(dict([(attr[0],attr[1])]))
            f1.write("     attr:" + "(" + attr[0] +"," + attr[1] + ")\n")
            
        
        if tag == 'orchestratecode_sql':
            #ex:
            #{'attributes': [{'job_identifier': 'DSPD21GG_030_Prepare_Lkps_T2_PSC_SHIP_ADD_ATTR_REL_Job_orig'},
            #                {'stg_header': 'DB_NZ_V3_PSC_REV_PAYR_CURR_REL'}],
            # 'data': '\n'
            #         'SELECT\n'
            #         '  part.AWB_KEY,\n'
            #         '  part.PAYR_CUST_NBR,\n'
            #         '  part.DW_UPD_RUN_DT,\n'
            #         '  True AS FoundRevPart\n'
            #         'FROM\n'
            #         '  VPSC_BINT wrk\n'
            #         '  INNER JOIN V3_PSC_REV_PAYR_CURR_REL part ON(wrk.K1_BINT = '
            #         'part.AWB_KEY)\n'
            #         'WHERE\n'
            #         '  wrk.ESP_JOB_ID = [&"ESP_JOB_ID"]\n'
            #         '  AND wrk.STEP_ID = [&"STEP_ID"]\n'
            #         'ORDER BY AWB_KEY\n'
            #         '\n'
            #         '--[&"BI_Common.ESP_JobID"]\n'
            #         '-- Expected : 100K records daily\n',
            # 'tag': 'orchestratecode_sql'}     
            sw_orchestratecode_sql = True
            o = Mapping()
            o['tag'] = tag
            o['attributes'] = []
            o['data'] = ' '
            #
            for attr in attrs:
                o['attributes'].append(dict([(attr[0],attr[1])]))
            f1.write("     attr:" + "(" + attr[0] +"," + attr[1] + ")\n")   
            
        if tag == 'xmlproperties':
            #ex:
            #{'attributes': [{'job_identifier': 'DB2_To_DB2_V1_CRLD_SHIP_EVT_Native'},
            #                {'rc_identifier': 'V0S19'},
            #                {'rc_type': 'CustomStage'},
            #                {'rc_name': 'Src_Table'}],
            # 'data': '\n'
            #         'select * from DW.V1_CRLD_SHIP_EVT where DW_CRT_RUN_DT = '
            #         "'#WhatDay#'\n",
            # 'tag': 'xmlproperties'}
            sw_xmlproperties = True
            o = Mapping()
            o['tag'] = tag
            o['attributes'] = []
            o['data'] = ' '
            #
            for attr in attrs:
                o['attributes'].append(dict([(attr[0],attr[1])]))
            f1.write("     attr:" + "(" + attr[0] +"," + attr[1] + ")\n")               
            
        
        #property under column tag        
        if (tag == 'property' and sw_columns == True) or  (tag == 'property' and sw_tablename == True):  
            sw_property = True
            #there is only one attribute for property , the loop will be done once
            for attr in attrs:
                #this is a global variable
                property_name = attr[1]
            f1.write("     attr:" + "(" + attr[0] +"," + attr[1] + ")\n")       

    def handle_endtag(self, tag):
        global sw_job, sw_columns, sw_orchestratecode_sql,sw_xmlproperties,sw_property, sw_tablename, property_name, o, o_job
        f1.write("End tag  :" + tag + "\n")
        
        #pprint.pprint(o)
    
        if tag == 'job': 
            #the job encompass everythin and we therefore only check for the tag, not the full encompassing data 
            #o_job is settup ins the handle_starttag routine 
            sw_job = False 
            pickle.dump(o_job, outputpkl)
            o_job = None
            
        if tag == 'columns':
            sw_columns = False 
            pickle.dump(o, outputpkl)
            o = None

        if tag == 'tablename':
            sw_tablename = False 
            pickle.dump(o, outputpkl)
            o = None

        if tag == 'property':
            sw_property = False 
            
        if tag == 'orchestratecode_sql':
            sw_orchestratecode_sql = False 
            pickle.dump(o, outputpkl)
            o = None
            
        if tag == 'xmlproperties':
            sw_xmlproperties = False 
            pickle.dump(o, outputpkl)
            o = None


    def handle_data(self, data):
        global sw_job, sw_columns, sw_orchestratecode_sql,sw_xmlproperties,sw_property, sw_tablename, property_name, o
        f1.write("Data     :" + data + "\n")
        
        if (sw_property == True and sw_columns == True) or (sw_property == True and sw_tablename == True) :
            o['property_attributes'].append(dict([(property_name,data)]))
            
        if sw_orchestratecode_sql == True  :    
            o['data'] = data

        if sw_xmlproperties == True  :  
            o['data'] = data            
            

def search_block(f):
    global sw_job, sw_columns, sw_orchestratecode_sql,sw_xmlproperties,sw_property, sw_tablename, property_name, o
 
 #when we hit a start tag we put the sw flag to True and line_cum to ""
 #coresponding to that sw flag every line is cumulated up until we hit the end tag
 # for the job tag we dont accumulate since it encompass every thing . 
    

    line_cum = ""
    sw_orchestratecode_sql = False
    sw_xmlproperties = False
    sw_columns = False 
    sw_job = False 
    # Looping through the file line by line
    for line in f:
        print ("::::",line)
        
        if "<job" in line:
            sw_job = True
            line_cum = ""            
            line_cum += line
            yield line_cum
        if "</job" in line:
            sw_job = False
            line_cum = ""            
            line_cum += line            
            yield line_cum
 
        
        if "<OrchestrateCode_SQL" in line:
            sw_orchestratecode_sql = True  
            line_cum = ""
        if sw_orchestratecode_sql :
            line_cum += line
            if "</OrchestrateCode_SQL>" in line:
                sw_orchestratecode_sql = False 
                yield line_cum
            
                
        if "<columns" in line:
            sw_columns = True
            line_cum = ""            
        if sw_columns :
            line_cum += line
            if "</columns>" in line:
                sw_columns = False 
                yield line_cum          
                
        if "<tablename" in line:
            sw_tablename = True
            line_cum = ""            
        if sw_tablename :
            line_cum += line
            if "</tablename>" in line:
                sw_tablename = False 
                yield line_cum        
        
        if "<XMLProperties" in line:
            sw_xmlproperties = True
            line_cum = ""            
        if sw_xmlproperties :
            line_cum += line
            if "</XMLProperties>" in line:
                sw_xmlproperties = False 
                yield line_cum    
             



path = os.getcwd()
os.chdir("..\\")
pathx = os.getcwd() + "\\"
#path1 = pathx + "export\\export_reduced_wrk_bidev_ACCT\\"
path1 = pathx + "export\\export_reduced_wrk_test\\"

#path1 = "C:\\Users\\XT21586\\Documents\\document\\Data Stage\\export1\\data_mapping\\"


outfilename1 = path1 + "debug.txt"
outfilpkl = pathx + "pickle1.pkl"


parser = MyHTMLParser()

os.chdir(path1)    

with open(outfilename1, "w") as f1:
    with open(outfilpkl, 'wb') as outputpkl:
        for fname in glob.glob("*.html"): 
            print(">>>>>", fname)
            with open(fname, 'r') as f :  
                print(f.name)
                gen1 = search_block(f)    
                for linex in gen1:
                    #debug
                    print(linex)
                    parser.feed(linex)  
            gen1 = None
            f.close()
            f = None
            

print('DONE')