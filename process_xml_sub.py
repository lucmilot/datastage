#!/usr/bin/env python

#
# Generated Wed Jul 25 07:31:25 2018 by generateDS.py version 2.29.17.
# Python 3.6.4 |Anaconda, Inc.| (default, Jan 16 2018, 10:22:32) [MSC v.1900 64 bit (AMD64)]
#
# Command line options:
#   ('-f', '')
#   ('--super', 'testluc')
#   ('-o', 'testluc.py')
#   ('-s', 'testluc_sub.py')
#   ('--member-specs', 'list')
#
# Command line arguments:
#   datastage.xsd
#
# Command line:
#   C:\LUC\Python\generateDS-2.29.17\generateDS.py -f --super="testluc" -o "testluc.py" -s "testluc_sub.py" --member-specs="list" datastage.xsd
#
# Current working directory (os.getcwd()):
#   generateDS-2.29.17
#


#&lt;DataSource ...   &gt;<![CDATA[  ...  ]]>&lt;/DataSource&gt;
#&lt;Database         &gt;<![CDATA[  ...  ]]>&lt;/Database&gt;


#&lt;SelectStatement   <![CDATA[   ]]>&lt;    &lt;/SelectStatement
#&lt;BeforeSQL         <![CDATA[              &lt;/BeforeSQL


import sys
from lxml import etree as etree_

import process_xml as supermod


    
#
# Globals
#

def setf2(f2_in):
    global f2
    f2 = f2_in  



ExternalEncoding = ''

Header_Cur = None
Job_Cur = {'Identifier': None, 'DateModified': None, 'TimeModified': None}
StageTypes_Cur = None
TableDefinitions_Cur = None
ParameterSets_Cur = None

Collection_Cur = {'Name': None,  'Type' : None }    

Record_Cur = {'Job_Identifier': None,  'Identifier': None , 'Type': None, 'Name': None }
        



def parsexml_(infile, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        parser = etree_.ETCompatXMLParser()
    doc = etree_.parse(infile, parser=parser, **kwargs)
    return doc

def split_cdata(se , key):
    rt = None
    key1 = '<' + key
    key2 = '/' + key + '>'
    t1a = (se.split(key1))
    if len(t1a) > 1:              
        t1b = t1a[1].split(key2)
        if len(t1b) > 1:
            t2a = t1b[0].split('<![CDATA[')
            if len(t2a) > 1:
                t2b = t2a[1].split(']]>')
                if len(t2b) > 1:  
                    rt = t2b[0]
    return rt



#
# Data representation classes
#


#
# Data representation classes
#


class DSExportSub(supermod.DSExport):
    def __init__(self, Header=None, Job=None, StageTypes=None, TableDefinitions=None, ParameterSets=None):
        super(DSExportSub, self).__init__(Header, Job, StageTypes, TableDefinitions, ParameterSets, )	
      
    def export(self, outfile, level, namespace_='', name_='DSExport', namespacedef_='', pretty_print=True):
        imported_ns_def_ = supermod.GenerateDSNamespaceDefs_.get('DSExport')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
            
        #f2.write('%s: %s%s' % ('>>>>DSExportSub',  self.eol_)      
        #f2.write('>>>>DSExportSub' )   
        #f2.write(eol_ )  
        #value = supermod.find_attr_value_('Identifier', node)
            
        supermod.showIndent(outfile, level, pretty_print)
        #outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='DSExport')
        if self.hasContent_():
            #outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespace_='', name_='DSExport', pretty_print=pretty_print)
            supermod.showIndent(outfile, level, pretty_print)
            #outfile.write('</%s%s>%s' % (namespace_, name_, eol_))
        else:
            #outfile.write('/>%s' % (eol_, ))
            pass
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='DSExport'):
        pass        
    def exportChildren(self, outfile, level, namespace_='', name_='DSExport', fromsubclass_=False, pretty_print=True):
        global Header_Cur, Job_Cur, StageTypes_Cur, TableDefinitions_Cur, ParameterSets_Cur, Cur_MainTag
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
            
        if self.Header is not None:
            Cur_MainTag = 'Header' 
            self.Header.export(outfile, level, namespace_, name_='Header', pretty_print=pretty_print)
			
        for Job_ in self.Job:
            Cur_MainTag = 'Job'
            Job_.export(outfile, level, namespace_, name_='Job', pretty_print=pretty_print)	     
            
        if self.StageTypes is not None:
            Cur_MainTag = 'StageTypes'
            pass
        
        if self.TableDefinitions is not None:
            Cur_MainTag = 'TableDefinitions'              
            self.TableDefinitions.export(outfile, level, namespace_, name_='TableDefinitions', pretty_print=pretty_print)
            
        if self.ParameterSets is not None:   
            Cur_MainTag = 'ParameterSets'  
            self.ParameterSets.export(outfile, level, namespace_, name_='ParameterSets', pretty_print=pretty_print)
		
supermod.DSExport.subclass = DSExportSub
# end class DSExportSub


class HeaderSub(supermod.Header):
    def __init__(self, CharacterSet=None, Date=None, ExportingTool=None, ServerName=None, ServerVersion=None, Time=None, ToolInstanceID=None, ToolVersion=None):
        super(HeaderSub, self).__init__(CharacterSet, Date, ExportingTool, ServerName, ServerVersion, Time, ToolInstanceID, ToolVersion, )
supermod.Header.subclass = HeaderSub
# end class HeaderSub


class JobSub(supermod.Job):
    def __init__(self, DateModified=None, Identifier=None, TimeModified=None, Record=None):
        super(JobSub, self).__init__(DateModified, Identifier, TimeModified, Record, )
             
    def export(self, outfile, level, namespace_='', name_='Job', namespacedef_='', pretty_print=True):
        global Job_Cur
        Job_Cur = {'Identifier': self.Identifier, 'DateModified': self.DateModified, 'TimeModified': self.TimeModified}
        
        f2.write('\n<job Identifier="%s" \tDateModified="%s" \tTimeModified="%s">' % (Job_Cur['Identifier'],Job_Cur['DateModified'],Job_Cur['TimeModified']))                       
        
        imported_ns_def_ = supermod.GenerateDSNamespaceDefs_.get('Job')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        supermod.showIndent(outfile, level, pretty_print)
        #outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='Job')
        if self.hasContent_():
            #outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespace_='', name_='Job', pretty_print=pretty_print)
            supermod.showIndent(outfile, level, pretty_print)
            #outfile.write('</%s%s>%s' % (namespace_, name_, eol_))
        else:
            #outfile.write('/>%s' % (eol_, ))
            pass
            
            

        f2.write('\n</job>\n')               
            
        Job_Cur = {'Identifier': None, 'DateModified': None, 'TimeModified': None}    
            
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='Job'):
        if self.DateModified is not None and 'DateModified' not in already_processed:
            already_processed.add('DateModified')
            #outfile.write(' DateModified="%s"' % self.gds_format_date(self.DateModified, input_name='DateModified'))
        if self.Identifier is not None and 'Identifier' not in already_processed:
            already_processed.add('Identifier')
            #outfile.write(' Identifier=%s' % (supermod.quote_attrib(self.Identifier), ))
        if self.TimeModified is not None and 'TimeModified' not in already_processed:
            already_processed.add('TimeModified')
            #outfile.write(' TimeModified=%s' % (self.gds_encode(self.gds_format_string(supermod.quote_attrib(self.TimeModified), input_name='TimeModified')), ))

        
    def exportChildren(self, outfile, level, namespace_='', name_='Job', fromsubclass_=False, pretty_print=True):

        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Record_ in self.Record:
            Record_.export(outfile, level, namespace_, name_='Record', pretty_print=pretty_print) 
            
                
        
supermod.Job.subclass = JobSub
# end class JobSub


class StageTypesSub(supermod.StageTypes):
    def __init__(self):
        super(StageTypesSub, self).__init__()
supermod.StageTypes.subclass = StageTypesSub
# end class StageTypesSub


class TableDefinitionsSub(supermod.TableDefinitions):
    def __init__(self, Record=None):
        super(TableDefinitionsSub, self).__init__(Record, )
supermod.TableDefinitions.subclass = TableDefinitionsSub
# end class TableDefinitionsSub


class ParameterSetsSub(supermod.ParameterSets):
    def __init__(self, Record=None):
        super(ParameterSetsSub, self).__init__(Record, )
supermod.ParameterSets.subclass = ParameterSetsSub
# end class ParameterSetsSub


class RecordSub(supermod.Record):
    

    def __init__(self, DateModified=None, Identifier=None, Readonly=None, TimeModified=None, Type=None, Property=None, Collection=None):
        super(RecordSub, self).__init__(DateModified, Identifier, Readonly, TimeModified, Type, Property, Collection, )

    def export(self, outfile, level, namespace_='', name_='Record', namespacedef_='', pretty_print=True):
        global Record_Cur
        Record_Cur = {'Job_Identifier': Job_Cur['Identifier'], 'Identifier': self.Identifier , 'Type': self.Type, 'Name': None }
        
        imported_ns_def_ = supermod.GenerateDSNamespaceDefs_.get('Record')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        supermod.showIndent(outfile, level, pretty_print)
        #outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='Record')
        if self.hasContent_():
            #outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespace_='', name_='Record', pretty_print=pretty_print)
            supermod.showIndent(outfile, level, pretty_print)
            #outfile.write('</%s%s>%s' % (namespace_, name_, eol_))
        else:
            #outfile.write('/>%s' % (eol_, ))
            pass
            
        Record_Cur = {'Job_Identifier': None, 'Identifier': None , 'Type': None, 'Name': None }
     

    def exportChildren(self, outfile, level, namespace_='', name_='Record', fromsubclass_=False, pretty_print=True):
        global Record_Cur
        
        def out_case_1(self, outfile): 
            for Property_ in self.Property:
                if  (Property_.Name) == 'Name':
                    Record_Cur['Name'] = Property_.valueOf_
 
                   
#            f2.write('<record: \t')
#            comma_sw = ''
#            for kv in Record_Cur.items():
#                f2.write('%s%s=%s' % (comma_sw, kv[0], kv[1]) )
#                comma_sw = ', \t'
#            f2.write('>')
                  

        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
          
        out_case_1(self, outfile) 

            
        for Property_ in self.Property:
            Property_.export(outfile, level, namespace_, name_='Property', pretty_print=pretty_print)
            
        for Collection_ in self.Collection:
            Collection_.export(outfile, level, namespace_, name_='Collection', pretty_print=pretty_print)


supermod.Record.subclass = RecordSub
# end class RecordSub


class CollectionSub(supermod.Collection):
    def __init__(self, Name=None, Type=None, SubRecord=None):
        super(CollectionSub, self).__init__(Name, Type, SubRecord, )
        

    def exportChildren(self, outfile, level, namespace_='', name_='Collection', fromsubclass_=False, pretty_print=True):
        global Collection_Cur
        #we dont check the self content , we thus comment out
        #if not fromsubclass_:
        #    for item_ in self.content_:
        #        item_.export(outfile, level, item_.name, namespace_, pretty_print=pretty_print)r

        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
            
        Collection_Cur = {'Name': self.Name,  'Type' : self.Type }
        #f2.write('>>>>Collection: ' + Collection_Cur['Col_Name'] + eol_)   
        
        for SubRecord_ in self.SubRecord:
            SubRecord_.export(outfile, level, namespace_, name_='SubRecord', pretty_print=pretty_print)
          
        Collection_Cur = {'Name': None,  'Type' : None }      
        
        
        
supermod.Collection.subclass = CollectionSub
# end class CollectionSub


class SubRecordSub(supermod.SubRecord):
    
    srch_subrecord_list1a = [('Name','Schema')]
    srch_subrecord_list1b = [('Value')]
    
    srch_subrecord_list2a = [('TableDef')]
    srch_subrecord_list2b = [('Name'),('TableDef'),('ColumnReference')]
    
    srch_subrecord_list3a = [('Name','XMLProperties')]
    srch_subrecord_list3b = [('Value')]
    
    srch_subrecord_list4a = [('Name','tablename')]
    srch_subrecord_list4b = [('Value')]   
    
    def __init__(self, Property=None):
        super(SubRecordSub, self).__init__(Property, )
        
    def exportChildren(self, outfile, level, namespace_='', name_='SubRecord', fromsubclass_=False, pretty_print=True):
  
        
        def out_case_1(self, outfile): 
            fndsw = False
            for Property_ in self.Property:
                for tup1 in SubRecordSub.srch_subrecord_list1a:
                    if  (Property_.Name, Property_.valueOf_) == tup1:
                        fndsw = True   
            if fndsw == True:    
                f2.write('\n<schema Job_Identifier="%s" \tRc_Identifier="%s" \tRc_Type="%s" \tRc_Name="%s">' % (Job_Cur['Identifier'],Record_Cur['Identifier'],Record_Cur['Type'],Record_Cur['Name'] ))                       
                for Property_ in self.Property:
                    if (Property_.Name) in SubRecordSub.srch_subrecord_list1b:
                        f2.write('\n <property Name="%s">%s</property>' % (Property_.Name,Property_.valueOf_))
                f2.write('\n</schema>\n')              
            
        def out_case_2(self, outfile): 
            fndsw = False    
            if Collection_Cur['Name'] =='Columns':   
                 
                for Property_ in self.Property:
                    for tup1 in SubRecordSub.srch_subrecord_list2a:
                        if  (Property_.Name) == tup1:
                            fndsw = True   
                if fndsw == True:    
                    # get record identifier, type and name 
                    f2.write('\n<columns \tJob_Identifier="%s" \tRc_Identifier="%s" \tRc_Type="%s" \tRc_Name="%s" >' % (Job_Cur['Identifier'],Record_Cur['Identifier'],Record_Cur['Type'],Record_Cur['Name'] ))                         
                    for Property_ in self.Property:
                        if (Property_.Name) in SubRecordSub.srch_subrecord_list2b:
                            f2.write('\n <property Name="%s">%s</property>' % (Property_.Name,Property_.valueOf_))
                    f2.write('\n</columns>\n') 
                             
                    
        def out_case_3(self, outfile): 
            fndsw = False
            for Property_ in self.Property:
                for tup1 in SubRecordSub.srch_subrecord_list3a:
                    if  (Property_.Name, Property_.valueOf_) == tup1:
                        fndsw = True  
            if fndsw == True:    
                for Property_ in self.Property:
                    if (Property_.Name) in SubRecordSub.srch_subrecord_list3b:
                        cdata = split_cdata(Property_.valueOf_, 'SelectStatement')
                        if cdata is not None:
                            f2.write('\n<XMLProperties \tJob_Identifier="%s" \tRc_Identifier="%s" \tRc_Type="%s" \tRc_Name="%s" >\n%s\n</XMLProperties>\n' % (Job_Cur['Identifier'],Record_Cur['Identifier'],Record_Cur['Type'],Record_Cur['Name'],cdata ))                       
                        cdata = split_cdata(Property_.valueOf_, 'BeforeSQL')
                        if cdata is not None:
                            f2.write('\n<XMLProperties \tJob_Identifier="%s" \tRc_Identifier="%s" \tRc_Type="%s" \tRc_Name="%s" >\n%s\n</XMLProperties>\n' % (Job_Cur['Identifier'],Record_Cur['Identifier'],Record_Cur['Type'],Record_Cur['Name'],cdata ))                       
                        cdata = split_cdata(Property_.valueOf_, 'AfterSQL')
                        if cdata is not None:
                            f2.write('\n<XMLProperties \tJob_Identifier="%s" \tRc_Identifier="%s" \tRc_Type="%s" \tRc_Name="%s" >\n%s\n</XMLProperties>\n' % (Job_Cur['Identifier'],Record_Cur['Identifier'],Record_Cur['Type'],Record_Cur['Name'],cdata ))                       

        def out_case_4(self, outfile): 
            fndsw = False
            for Property_ in self.Property:
                for tup1 in SubRecordSub.srch_subrecord_list4a:
                    if  (Property_.Name, Property_.valueOf_) == tup1:
                        fndsw = True   
            if fndsw == True:    
                f2.write('\n<tablename Job_Identifier="%s" \tRc_Identifier="%s" \tRc_Type="%s" \tRc_Name="%s">' % (Job_Cur['Identifier'],Record_Cur['Identifier'],Record_Cur['Type'],Record_Cur['Name'] ))                       
                for Property_ in self.Property:
                    if (Property_.Name) in SubRecordSub.srch_subrecord_list4b:
                        f2.write('\n <property Name="%s">%s</property>' % (Property_.Name,Property_.valueOf_))
                f2.write('\n</tablename>\n')      

                
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
  
        out_case_1(self, outfile)
         
        out_case_2(self, outfile)
        
        out_case_3(self, outfile)
        
        out_case_4(self, outfile)
            
        for Property_ in self.Property:    
            Property_.export(outfile, level, namespace_, name_='Property', pretty_print=pretty_print)   
            
       
        
supermod.SubRecord.subclass = SubRecordSub
# end class SubRecordSub


class PropertySub(supermod.Property):
    def __init__(self, Name=None, PreFormatted=None, valueOf_=None, mixedclass_=None, content_=None):
        super(PropertySub, self).__init__(Name, PreFormatted, valueOf_, mixedclass_, content_, )
        


    def export(self, outfile, level, namespace_='', name_='Property', namespacedef_='', pretty_print=True):
        

        
        imported_ns_def_ = supermod.GenerateDSNamespaceDefs_.get('Property')
 
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
                    
        if self.original_tagname_ is not None:
            name_ = self.original_tagname_
        supermod.showIndent(outfile, level, pretty_print)
 

#&lt;DataSource ...   &gt;<![CDATA[  ...  ]]>&lt;/DataSource&gt;
#&lt;Database         &gt;<![CDATA[  ...  ]]>&lt;/Database&gt;
        
#<![CDATA[   ]]>

#&lt;SelectStatement   <![CDATA[   ]]>&lt;    &lt;/SelectStatement
#&lt;BeforeSQL         <![CDATA[              &lt;/BeforeSQL
      
        
        if self.Name == "OrchestrateCode" :
            s = self.valueOf_
            ls = s.split('#### STAGE:')
            for se in ls:
                t0 = (se.split(eol_))
                stg_head = t0[0].strip()
                cdata = split_cdata(se, 'SelectStatement')
                if cdata is not None:
                    f2.write('\n<OrchestrateCode_SQL Job_Identifier="%s" stg_header="%s">\n%s\n</OrchestrateCode_SQL>\n' % (Job_Cur['Identifier'],stg_head,split_cdata(se, 'SelectStatement')))

                
        #outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='Property')
        #outfile.write('>')
        self.exportChildren(outfile, level + 1, namespace_, name_, pretty_print=pretty_print)
        #outfile.write(self.convert_unicode(self.valueOf_))
        #outfile.write('</%s%s>%s' % (namespace_, name_, eol_))        
 
   
            
supermod.Property.subclass = PropertySub
# end class PropertySub


def get_root_tag(node):
    tag = supermod.Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = None
    rootClass = supermod.GDSClassesMapping.get(tag)
    if rootClass is None and hasattr(supermod, tag):
        rootClass = getattr(supermod, tag)
    return tag, rootClass


def parse(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DSExport'
        rootClass = supermod.DSExport
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='',
            pretty_print=True)
    return rootObj


def parseEtree(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DSExport'
        rootClass = supermod.DSExport
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    mapping = {}
    rootElement = rootObj.to_etree(None, name_=rootTag, mapping_=mapping)
    reverse_mapping = rootObj.gds_reverse_node_mapping(mapping)
    if not silence:
        content = etree_.tostring(
            rootElement, pretty_print=True,
            xml_declaration=True, encoding="utf-8")
        sys.stdout.write(content)
        sys.stdout.write('\n')
    return rootObj, rootElement, mapping, reverse_mapping


def parseString(inString, silence=False):
    if sys.version_info.major == 2:
        from StringIO import StringIO
    else:
        from io import BytesIO as StringIO
    parser = None
    doc = parsexml_(StringIO(inString), parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DSExport'
        rootClass = supermod.DSExport
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='')
    return rootObj


def parseLiteral(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DSExport'
        rootClass = supermod.DSExport
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:

        rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
        sys.stdout.write(')\n')
    return rootObj


USAGE_TEXT = """
Usage: python ???.py <infilename>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    parse(infilename)


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()
