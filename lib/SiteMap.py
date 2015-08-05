import arcpy
import csv
import os
from subprocess import Popen
from Geometry import Extent
from lib.General import String

###
# Esri Toolbox
###

#parameter indexes. Change here once and be done 
#when updating parameter order
p_layer = 0
p_export_location = 1
p_buffer_dist = 2
p_title = 3
p_title_field = 5
p_individual = 4

#symbol layers
symbols = {
    'red': 'N:/ArcGIS10/Layerfiles/Generic/Red_Boundary.lyr',
    'gray': 'N:/ArcGIS10/Layerfiles/Generic/Gray_Boundary.lyr',
}
class SiteMapGenerator(object):
    def __init__(self):
        self.label = 'Generate Site Maps and CSV'
        self.description = """
            Generates a site map buffering where necessary
            """
        self.canRunInBackground = False
    def getParameterInfo(self):        
        params = [arcpy.Parameter(
            displayName = 'Layer',
            name = 'layer',
            direction = 'Input',
            datatype = 'GPLayer',
            parameterType = 'Required',
        ), arcpy.Parameter(
            displayName = 'Export Folder',
            name = 'export_location',
            direction = 'Input',
            datatype = 'DEFolder',
            parameterType = 'Required',
        ), arcpy.Parameter(
            displayName = 'Buffer Distance (include units, example: 350 Feet)',
            name = 'buffer_dist',
            direction = 'Input',
            datatype = 'GPString',
            parameterType = 'Optional',
        ), arcpy.Parameter(
            displayName = 'Document Title',
            name = 'title',
            direction = 'Input',
            datatype = 'GPString',
            parameterType = 'Optional',
        ), arcpy.Parameter(
            displayName = 'Include individual maps of selected features?',
            name = 'individual',
            direction = 'Input',
            datatype = 'GPBoolean',
            parameterType = 'Required',
        ), arcpy.Parameter(
            displayName = 'Title Field (field to use as individual map document title)',
            name = 'title_field',
            direction = 'Input',
            datatype = 'GPString',
            parameterType = 'Optional',
        )]
	params[p_layer].value = 'parcel'
	params[p_export_location].value = 'J:/'
	params[p_buffer_dist].value = '350 Feet'
	params[p_title_field].filter.type = 'valueList'
	params[p_title_field].filter.list = []
	params[p_title_field].enabled = False
	params[p_individual].value = False
        
	return params
    
    def updateMessages(self, parameters):
        if not parameters[p_layer].hasError() and parameters[p_layer].valueAsText:
            parameters[p_title_field].filter.list = [f.baseName for f in arcpy.Describe(parameters[p_layer].valueAsText).fields]
            
        parameters[p_title_field].enabled = ( parameters[p_individual].valueAsText == 'true' )
        
    def execute(self, parameters, messages):
		arcpy.AddMessage(len(parameters))
		self.generate(
			parameters[p_layer].valueAsText,
			parameters[p_export_location].valueAsText,
			parameters[p_buffer_dist].valueAsText,
			parameters[p_title_field].valueAsText,
                        parameters[p_individual].valueAsText)
                        
    def export_and_append(self, document, export_location, final_pdf):
        temp = os.path.join(export_location, 'temp.pdf')
        arcpy.AddMessage('Exporting pdf: {}'.format(document.title))
        arcpy.mapping.ExportToPDF(document, temp)
        #append it
        final_pdf.appendPages(temp)
        #remove the temp
        arcpy.Delete_management(temp)

    def buffer_and_select(self, layer, file_gdb, file_name, buffer_dist):
        #buffer and select features
        arcpy.AddMessage('Buffering: layer={}, {}/buffer_{}'.format(layer, file_gdb, file_name))
        arcpy.Buffer_analysis(layer, 
                              '{}/buffer_{}'.format(file_gdb, file_name), 
                              buffer_dist, 'FULL', 'ROUND', 'ALL')
        arcpy.AddMessage('Selecting: layer={}, {}/buffer_{}'.format(layer, file_gdb, file_name))
        arcpy.SelectLayerByLocation_management(layer, 'INTERSECT',
                                               '{}/buffer_{}'.format(file_gdb, file_name),
                                               0, 'NEW_SELECTION')
        return arcpy.mapping.Layer('{}/buffer_{}'.format(file_gdb, file_name))
    
    def add_map_layer(self, file_name, symbol_layer, data_frame ):
        layer = arcpy.mapping.Layer('{}/buffer_selected_{}'.format(file_gdb, file_name))
        arcpy.ApplySymbologyFromLayer_management(layer, symbol_layer)
        arcpy.mapping.AddLayer(data_frame, layer)
    
    def execute(self, parameters, messages):
        """generates the site map pdf and csv files"""
        arcpy.AddMessage('{}; {}; {}; {}; {};'.format(
                parameters[p_layer].valueAsText,
                parameters[p_export_location].valueAsText,
                parameters[p_buffer_dist].valueAsText,
                parameters[p_title_field].valueAsText,
                parameters[p_individual].valueAsText))
        
        layer = parameters[p_layer].valueAsText
        export_location = parameters[p_export_location].valueAsText
        buffer_dist = parameters[p_buffer_dist].valueAsText
        title_field = parameters[p_title_field].valueAsText
        individual = parameters[p_individual].valueAsText
        document_title = parameters[p_title].valueAsText
        file_name = String.get_safe_string(document_title)
        current_document = arcpy.mapping.MapDocument(map_document)
        data_frame = arcpy.mapping.ListDataFrames(current_document)[0]

        #generate the output workspace
        arcpy.AddMessage('Creating temp workspace: {}/data_{}.gdb'.format(export_location, file_name))
        arcpy.CreateFileGDB_management(export_location, 'data_{}.gdb'.format(file_name))
        file_gdb = '{}/data_{}.gdb'.format(export_location, file_name)

        #activate export view
        current_document.activeView = 'PAGE_LAYOUT'

        #export the selected features
        arcpy.AddMessage('Exporting: layer={}, {}/selected_{}'.format(layer, file_gdb, file_name))
        arcpy.FeatureClassToFeatureClass_conversion(layer, file_gdb, 'selected_{}'.format(file_name))

        #perform buffer if necessary
        if buffer_dist:
            buffer = self.buffer_and_select(layer, file_gdb, file_name, buffer_dist)
            arcpy.ApplySymbologyFromLayer_management(buffer, 'N:/ArcGIS10/Layerfiles/Generic/Orange_Boundary.lyr')
            arcpy.mapping.AddLayer(data_frame, buffer)

        #export the selected features
        arcpy.AddMessage('Exporting: layer={}, {}/buffer_selected_{}'.format(layer, file_gdb, file_name))
        arcpy.FeatureClassToFeatureClass_conversion(layer, file_gdb, 'buffer_selected_{}'.format(file_name))
        buffer_selected = self.add_map_layer('{}/buffer_selected_{}'.format(layer, file_gdb, file_name), 
            symbols['gray'], data_frame)

        #add original selection
        selected = self.add_map_layer('{}/selected_{}'.format(file_gdb, file_name),
            symbols['red'], data_frame)

        #prep output pdf
        final_pdf = arcpy.mapping.PDFDocumentCreate(os.path.join(export_location, 'Final_{}.pdf'.format(file_name)))
        arcpy.AddMessage('exporting pdf file Final_{}.pdf to {}'.format(file_name, export_location))
        data_frame.extent = Extent.expand(buffer_selected.getExtent(), 10)
        current_document.title = document_title
        arcpy.SelectLayerByAttribute_management(layer, "CLEAR_SELECTION")
        self.export_and_append(current_document, export_location, final_pdf)

        rows = []
        cursor = arcpy.da.SearchCursor('{}/buffer_selected_{}'.format(file_gdb, file_name), ['SHAPE@', '*'])
        for row in cursor:
            rows.append(row)
            if individual == 'false':
                continue
            #generate the pdf
            if title_field in cursor.fields:
                current_document.title = row[cursor.fields.index(title_field)]
            data_frame.extent = Extent.expand(row[0].extent, 10)
            self.export_and_append(current_document, export_location, final_pdf)

        #write out csv rows
        arcpy.AddMessage('Exporting csv: output_{}.csv to {}'.format(file_name, export_location))
        #open csv file as binary so it avoids windows empty lines
        csv_output = open(os.path.join(export_location, 'output_{}.csv'.format(file_name)), 'wb')
        csv_writer = csv.writer(csv_output, delimiter='|', quotechar='|', 
                                quoting=csv.QUOTE_MINIMAL, dialect = 'excel')
        csv_writer.writerow(cursor.fields)
        csv_writer.writerows(rows)

        #save the outputs
        csv_output.close()
        final_pdf.saveAndClose()

        #open explorer
        Popen('explorer "{}"'.format(export_location))

        #clean up
        del cursor