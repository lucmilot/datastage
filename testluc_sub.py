#!/usr/bin/env python

#
# Generated Wed Aug  1 09:14:51 2018 by generateDS.py version 2.29.17.
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
#   generateDS.py -f --super="testluc" -o "testluc.py" -s "testluc_sub.py" --member-specs="list" datastage.xsd
#
# Current working directory (os.getcwd()):
#   python
#

import sys
from lxml import etree as etree_

import testluc as supermod

def parsexml_(infile, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        parser = etree_.ETCompatXMLParser()
    doc = etree_.parse(infile, parser=parser, **kwargs)
    return doc

#
# Globals
#

ExternalEncoding = ''

#
# Data representation classes
#


class DSExportSub(supermod.DSExport):
    def __init__(self, Header=None, Job=None, StageTypes=None, TableDefinitions=None, ParameterSets=None):
        super(DSExportSub, self).__init__(Header, Job, StageTypes, TableDefinitions, ParameterSets, )
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
supermod.Record.subclass = RecordSub
# end class RecordSub


class CollectionSub(supermod.Collection):
    def __init__(self, Name=None, Type=None, SubRecord=None):
        super(CollectionSub, self).__init__(Name, Type, SubRecord, )
supermod.Collection.subclass = CollectionSub
# end class CollectionSub


class SubRecordSub(supermod.SubRecord):
    def __init__(self, Property=None):
        super(SubRecordSub, self).__init__(Property, )
supermod.SubRecord.subclass = SubRecordSub
# end class SubRecordSub


class PropertySub(supermod.Property):
    def __init__(self, Name=None, PreFormatted=None, valueOf_=None, mixedclass_=None, content_=None):
        super(PropertySub, self).__init__(Name, PreFormatted, valueOf_, mixedclass_, content_, )
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
        sys.stdout.write('#from testluc import *\n\n')
        sys.stdout.write('import testluc as model_\n\n')
        sys.stdout.write('rootObj = model_.rootClass(\n')
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
