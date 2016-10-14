import arcpy
from xml.dom.minidom import parse
#set local variables
dir = arcpy.GetInstallInfo("desktop")["InstallDir"]
translator = dir + "Metadata/Translator/ESRI_ISO2ISO19139.xml"
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)
temp_path = "C:/temp"
for layer in arcpy.mapping.ListLayers(mxd, "*", df[0]):
    if not layer.isGroupLayer:
        description_text = ""
        path = temp_path + '/' + layer.datasetName + '.xml'
        print path
        arcpy.ExportMetadata_conversion(layer.dataSource, translator, path)
        dom = parse(path)
        fields = ('abstract', 'purpose', 'credit')
        for field in fields:
            tags = dom.getElementsByTagName(field)
            print str( len(tags) ) + ' | ' + str( tags )
            if len(tags):
                tag_string = tags[0].getElementsByTagName('gco:CharacterString')[0].childNodes[0].nodeValue
                description_text = "{} <br /> <p><strong>{}</strong>: {}</p>".format(description_text, field.capitalize(), tag_string)
                if field == 'credit':
                    layer.credit = tag_string
        print description_text
        layer.description = description_text
