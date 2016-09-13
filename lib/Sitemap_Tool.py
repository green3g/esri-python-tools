from arcpy import Parameter

###
# Esri Toolbox
###

# parameter indexes. Change here once and be done
# when updating parameter order
p_layer = 0
p_export_location = 1
p_buffer_dist = 2
p_title = 3
p_title_field = 5
p_individual = 4

# default tool field values
d_layer = 'parcel'
d_export_location = 'N:/PlanningZoning/SiteMaps/2015'
d_buffer_dist = '350 Feet'

# symbol layers
symbols = {
    'red': 'N:/ArcGIS10/Layerfiles/Generic/Red_Boundary.lyr',
    'gray': 'N:/ArcGIS10/Layerfiles/Generic/Gray_Boundary.lyr',
    'orange': 'N:/ArcGIS10/Layerfiles/Generic/Orange_Boundary.lyr',
}


class SiteMapGenerator(object):
    """
    Buffers, selects, and exports a map or set of individual maps
    for chosen features, and a csv with the rows.
    """
    def __init__(self):
        self.label = 'Generate Site Maps and CSV'
        self.description = """
            Generates a site map buffering where necessary
            """
        self.canRunInBackground = False

    def getParameterInfo(self):
        params = [Parameter(
            displayName='Layer',
            name='layer',
            direction='Input',
            datatype='GPLayer',
            parameterType='Required',
        ), Parameter(
            displayName='Export Folder',
            name='export_location',
            direction='Input',
            datatype='DEFolder',
            parameterType='Required',
        ), Parameter(
            displayName='Buffer Distance (include units, example: 350 Feet)',
            name='buffer_dist',
            direction='Input',
            datatype='GPString',
            parameterType='Optional',
        ), Parameter(
            displayName='Document Title and Export Folder (Insert Document Title into layout)',
            name='title',
            direction='Input',
            datatype='GPString',
            parameterType='Optional',
        ), Parameter(
            displayName='Include individual maps of selected features?',
            name='individual',
            direction='Input',
            datatype='GPBoolean',
            parameterType='Required',
        ), Parameter(
            displayName='Title Field (field to use as individual map document title)',
            name='title_field',
            direction='Input',
            datatype='GPString',
            parameterType='Optional',
        )]
        params[p_layer].value = d_layer
        params[p_export_location].value = d_export_location
        params[p_buffer_dist].value = d_buffer_dist
        params[p_title_field].filter.type = 'valueList'
        params[p_title_field].filter.list = []
        params[p_title_field].enabled = False
        params[p_individual].value = False

        return params

    def updateMessages(self, parameters):
        if not parameters[p_layer].hasError() and parameters[p_layer].valueAsText:
            parameters[p_title_field].filter.list = [
                f.baseName for f in Describe(parameters[p_layer].valueAsText).fields]

        parameters[p_title_field].enabled = (
            parameters[p_individual].valueAsText == 'true')

    def execute(self, parameters, messages):
        """generates the site map pdf and csv files"""

        from arcpy.da import SearchCursor
        from arcpy import AddMessage, CreateFileGDB_management, FeatureClassToFeatureClass_conversion, SelectLayerByAttribute_management, mapping
        import csv
        import os
        import time
        from subprocess import Popen
        from .esri import Extent, MapDocument
        from .util import String, File_Operations

        # set up local vars for easy access
        layer = parameters[p_layer].valueAsText
        export_location = parameters[p_export_location].valueAsText
        buffer_dist = parameters[p_buffer_dist].valueAsText
        title_field = parameters[p_title_field].valueAsText
        individual = parameters[p_individual].valueAsText
        document_title = parameters[p_title].valueAsText
        current_document = mapping.MapDocument("CURRENT")
        data_frame = mapping.ListDataFrames(current_document)[0]

        AddMessage("""layer={}; export_location={}; buffer_dist={};
                title_field={}; individual={}; document_title={};""".format(
            layer, export_location, buffer_dist, title_field, individual,
            document_title))

        # generate the output workspace
        if document_title and document_title != '':
            File_Operations = document_title
            file_name = String.get_safe_string(document_title)
        else:
            File_Operations = time.strftime('%m-%d-%y-(%H.%M)')
            file_name = time.strftime('%m-%d-%y-(%H.%M)')

        export_location = os.path.join(export_location, File_Operations)
        File_Operations.verify_path_exists(export_location)
        AddMessage(
            'Creating temp workspace: {}/{}_data.gdb'.format(export_location, file_name))
        CreateFileGDB_management(
            export_location, '{}_data.gdb'.format(file_name))
        file_gdb = '{}/{}_data.gdb'.format(export_location, file_name)

        # activate export view
        current_document.activeView = 'PAGE_LAYOUT'

        # export the selected features
        AddMessage(
            'Exporting: layer={}, {}/selected'.format(layer, file_gdb))
        FeatureClassToFeatureClass_conversion(
            layer, file_gdb, 'selected')

        # perform buffer if necessary
        if buffer_dist:
            # buffer and select features
            AddMessage(
                'Buffering and Selecting: layer={}, {}/buffer'.format(layer, file_gdb))
            Buffer_analysis(layer, '{}/buffer'.format(file_gdb),
                                  buffer_dist, 'FULL', 'ROUND', 'ALL')
            SelectLayerByLocation_management(layer, 'INTERSECT',
                                                   '{}/buffer'.format(file_gdb), 0, 'NEW_SELECTION')
            buffer = MapDocument.add_map_layer('{}/buffer'.format(file_gdb),
                                               symbols['orange'], '{} Buffer'.format(buffer_dist))

        # export the selected features
        AddMessage(
            'Exporting: layer={}, {}/buffer_selected'.format(layer, file_gdb))
        FeatureClassToFeatureClass_conversion(
            layer, file_gdb, 'buffer_selected')
        buffer_selected = MapDocument.add_map_layer('{}/buffer_selected'.format(file_gdb),
                                                    symbols['gray'], 'Buffered Features')

        # add original selection
        selected = MapDocument.add_map_layer('{}/selected'.format(file_gdb),
                                             symbols['red'], 'Selected Features')

        # prep output pdf
        final_pdf = mapping.PDFDocumentCreate(os.path.join(
            export_location, '{}_Final.pdf'.format(file_name)))
        AddMessage('exporting pdf file {}_Final.pdf to {}'.format(
            file_name, export_location))
        data_frame.extent = Extent.expand(buffer_selected.getExtent(), 10)
        current_document.title = document_title
        SelectLayerByAttribute_management(layer, "CLEAR_SELECTION")
        MapDocument.export_and_append(export_location, final_pdf)

        rows = []
        cursor = SearchCursor(
            '{}/buffer_selected'.format(file_gdb, file_name), ['SHAPE@', '*'])
        for row in cursor:
            rows.append(row)
            if individual == 'false':
                continue
            # generate the pdf
            if title_field in cursor.fields:
                current_document.title = row[cursor.fields.index(title_field)]
            data_frame.extent = Extent.expand(row[0].extent, 10)
            MapDocument.export_and_append(export_location, final_pdf)

        # write out csv rows
        AddMessage('Exporting csv: {}_output.csv to {}'.format(
            file_name, export_location))
        # open csv file as binary so it avoids windows empty lines
        csv_output = open(os.path.join(
            export_location, '{}_output.csv'.format(file_name)), 'wb')
        csv_writer = csv.writer(csv_output, delimiter=',',
                                quoting=csv.QUOTE_ALL, dialect='excel')
        csv_writer.writerow(cursor.fields)
        csv_writer.writerows(rows)

        # save the outputs
        csv_output.close()
        final_pdf.saveAndClose()

        # open explorer
        Popen('explorer "{}"'.format(export_location.replace('/', '\\')))

        # clean up
        del cursor
