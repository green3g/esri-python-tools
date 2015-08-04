import arcpy
import csv
from datetime import datetime
import os
from Geometry import Extent

def export_and_append(document, data_frame, export_location, final_pdf):
    temp = os.path.join(export_location, 'temp.pdf')
    arcpy.AddMessage('Exporting pdf: {}'.format(document.title))
    arcpy.mapping.ExportToPDF(document, temp)
    #append it
    final_pdf.appendPages(temp)
    #remove the temp
    arcpy.Delete_management(temp)

def buffer_and_select(layer, file_gdb, seconds, buffer_dist):
    #buffer and select features
    arcpy.AddMessage('Buffering: layer={}, {}/buffer_{}'.format(layer, file_gdb, seconds))
    arcpy.Buffer_analysis(layer, 
                          '{}/buffer_{}'.format(file_gdb, seconds), 
                          buffer_dist, 'FULL', 'ROUND', 'ALL')
    arcpy.AddMessage('Selecting: layer={}, {}/buffer_{}'.format(layer, file_gdb, seconds))
    arcpy.SelectLayerByLocation_management(layer, 'INTERSECT',
                                           '{}/buffer_{}'.format(file_gdb, seconds),
                                           0, 'NEW_SELECTION')
    return arcpy.mapping.Layer('{}/buffer_{}'.format(file_gdb, seconds))

def generate(layer='parcel', export_location=r'C:/Temp/',
             buffer_dist='10 Feet', title_field='MAILADDR', 
             individual=False, map_document='CURRENT'):
    """generates the site map pdf and csv files"""
	
    arcpy.AddMessage("layer = '{}', export_location = '{}', individual = {}, buffer_dist = '{}', title_field = '{}', map_document = '{}'".format(
                     layer, export_location, individual, buffer_dist, title_field, map_document))

    seconds = datetime.now().second
    current_document = arcpy.mapping.MapDocument(map_document)
    data_frame = arcpy.mapping.ListDataFrames(current_document)[0]

    #generate the output workspace
    arcpy.AddMessage('Creating temp workspace: {}/data_{}.gdb'.format(export_location, seconds))
    arcpy.CreateFileGDB_management(export_location, 'data_{}.gdb'.format(seconds))
    file_gdb = '{}/data_{}.gdb'.format(export_location, seconds)

    #activate export view
    current_document.activeView = 'PAGE_LAYOUT'
    
    #export the selected features
    arcpy.AddMessage('Exporting: layer={}, {}/selected_{}'.format(layer, file_gdb, seconds))
    arcpy.FeatureClassToFeatureClass_conversion(layer, file_gdb, 'selected_{}'.format(seconds))
    selected = arcpy.mapping.Layer('{}/selected_{}'.format(file_gdb, seconds))
    arcpy.ApplySymbologyFromLayer_management(selected, 'N:/ArcGIS10/Layerfiles/Generic/Red_Boundary.lyr')
    arcpy.mapping.AddLayer(data_frame, selected)
    
    #perform buffer if necessary
    buffer = None
    if buffer_dist:
        buffer = buffer_and_select(layer, file_gdb, seconds, buffer_dist)
        arcpy.ApplySymbologyFromLayer_management(buffer, 'N:/ArcGIS10/Layerfiles/Generic/Orange_Boundary.lyr')
        arcpy.mapping.AddLayer(data_frame, buffer)
	
    #export the selected features
    arcpy.AddMessage('Exporting: layer={}, {}/buffer_selected_{}'.format(layer, file_gdb, seconds))
    arcpy.FeatureClassToFeatureClass_conversion(layer, file_gdb, 'buffer_selected_{}'.format(seconds))
    buffer_selected = arcpy.mapping.Layer('{}/buffer_selected_{}'.format(file_gdb, seconds))
    
    #prep output pdf
    final_pdf = arcpy.mapping.PDFDocumentCreate(os.path.join(export_location, 'Final_{}.pdf'.format(seconds)))
    arcpy.AddMessage('exporting pdf file Final_{}.pdf to {}'.format(seconds, export_location))
    data_frame.extent = Extent.expand(buffer_selected.getExtent(), 10)
    current_document.title = 'Selected Features'
    arcpy.SelectLayerByAttribute_management(layer, "CLEAR_SELECTION")
    export_and_append(current_document, data_frame, export_location, final_pdf)

    rows = []
    cursor = arcpy.da.SearchCursor('{}/buffer_selected_{}'.format(file_gdb, seconds), ['SHAPE@', '*'])
    if individual != 'false':
        for row in cursor:
            #generate the pdf
            current_document.title = row[cursor.fields.index(title_field)]
            data_frame.extent = Extent.expand(row[0].extent, 10)
            export_and_append(current_document, data_frame, export_location, final_pdf)
        rows.append(row)
	

    #write out csv rows
    arcpy.AddMessage('Exporting csv: output_{}.csv to {}'.format(seconds, export_location))
    csv_output = open(os.path.join(export_location, 'output_{}.csv'.format(seconds)), 'w')
    csv_writer = csv.writer(csv_output, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(cursor.fields)
    csv_writer.writerows(rows)

    #save the outputs
    csv_output.close()
    final_pdf.saveAndClose()
	
    #clean up
    del cursor
