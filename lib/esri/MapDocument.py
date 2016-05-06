import arcpy
import os

def export_and_append(export_location, final_pdf, document = None ):
    """exports a temporary map document, then appends it to an existing pdf document"""
    if not document:
        document = arcpy.mapping.MapDocument("CURRENT")
    temp = os.path.join(export_location, 'temp.pdf')
    arcpy.AddMessage('Exporting pdf: {}'.format(document.title))
    arcpy.mapping.ExportToPDF(document, temp)
    #append it
    final_pdf.appendPages(temp)
    #remove the temp
    arcpy.Delete_management(temp)

def add_map_layer(file_name, symbol_layer, name='layer', data_frame = None):
    """creates and adds a symbolized layer to a data frame"""
    if not data_frame:
        data_frame = arcpy.mapping.ListDataFrames(arcpy.mapping.MapDocument("CURRENT"))[0]
    layer = arcpy.mapping.Layer(file_name)
    layer.name = name
    arcpy.ApplySymbologyFromLayer_management(layer, symbol_layer)
    arcpy.mapping.AddLayer(data_frame, layer)
    return layer
