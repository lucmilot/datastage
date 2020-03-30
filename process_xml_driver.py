

import glob
import sys
import os
import win32com.client as win32
import process_xml_sub as submod

def process(infilename):
    #doc = supermod.parsexml_(inFilename)
    doc = submod.parsexml_(infilename)
    rootNode = doc.getroot()
    rootClass = submod.DSExportSub
    rootObj = rootClass.factory()  #this acces supermod
   
    rootObj.build(rootNode)        #this acces supermod
    # Enable Python to collect the space used by the DOM.
    doc = None

    #rootObj.export(sys.stdout, outfilename1, 0)
    submod.setf2(f2)
    rootObj.export(f1, 0)

#    rootObj.export_small()
    
    #rootObj.set_up()
    #rootObj.walk_and_show(0)

    return rootObj



#--------------------------------------------------------------------------------

path = os.getcwd()

print(sys.path)

sys.path.append(os.getcwd()) 

os.chdir("..\\")
pathx = os.getcwd()

path1 = pathx + "\\export\\export_xml_bidev_ACCT\\"
path2 = pathx + "\\export\\export_reduced_wrk_bidev_ACCT\\"

tst = '"' + path1 + '"'

os.chdir(path1)
print(os.getcwd())

listofxmlfile = [f for f in glob.glob("*.xml")]

outfilename1 = path2 + "debug.txt"

for infilename_i in listofxmlfile:
    
    outfilename2 = path2 + (infilename_i.split('xml')[0] + "html")
    
    if os.path.exists(outfilename1):
        os.remove(outfilename1)
        
    if os.path.exists(outfilename2):
        os.remove(outfilename2)

    with open(outfilename1, "w") as f1:
        with open(outfilename2, "w") as f2:      
            infilename = path1 + infilename_i  
            print ('start proces of : ' + infilename)
            rootObject = process(infilename)


    #        rootObject = process(path1+'testlucdebug.xml')
    

print ('DONE')