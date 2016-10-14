from xml.dom.minidom import parse
from arcpy import GetInstallInfo, AddError
import sys
try:
    from arcpy.mapping import MapDocument, ListDataFrames, ListLayers
    from arcpy import ExportMetadata_conversion
except ImportError as e:
    AddError('This tool requires ArcMap: {}'.format(e))
    print('This tool requires ArcMap: {}'.format(e))

def update_metadata(document='CURRENT'):
    """
    updates metadata in an arcmap document
        document - (optional) the path to an arcmap document or the keyword 'CURRENT'.
            The default is 'CURRENT'
    """
    #set local variables
    dir = GetInstallInfo("desktop")["InstallDir"]
    translator = dir + "Metadata/Translator/ESRI_ISO2ISO19139.xml"
    mxd = MapDocument(document)
    df = ListDataFrames(mxd)
    temp_path = "C:/temp"
    for layer in ListLayers(mxd, "*", df[0]):
        if not layer.isGroupLayer:
            description_text = ""
            path = temp_path + '/' + layer.datasetName + '.xml'
            print(path)
            ExportMetadata_conversion(layer.dataSource, translator, path)
            dom = parse(path)
            fields = ('abstract', 'purpose', 'credit')
            for field in fields:
                tags = dom.getElementsByTagName(field)
                print(str( len(tags) ) + ' | ' + str( tags ))
                if len(tags):
                    tag_string = tags[0].getElementsByTagName('gco:CharacterString')[0].childNodes[0].nodeValue
                    description_text = "{} <br /> <p><strong>{}</strong>: {}</p>".format(description_text, field.capitalize(), tag_string)
                    if field == 'credit':
                        layer.credit = tag_string
            print(description_text)
            layer.description = description_text

if __name__ == '__main__':
    update_metadata(sys.argv[1])
