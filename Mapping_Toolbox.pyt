import arcpy
from lib import SiteMap

class Toolbox(object):
    def __init__(self):
        self.label = 'Mapping Toolbox'
        self.alias = 'Mapping'
        self.tools = [SiteMapGenerator]

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
            displayName = 'Buffer Distance (include units, example: 10 Feet)',
            name = 'buffer_dist',
            direction = 'Input',
            datatype = 'GPString',
            parameterType = 'Optional',
        ), arcpy.Parameter(
            displayName = 'Title Field (field in the dataset to use as document title)',
            name = 'title_field',
            direction = 'Input',
            datatype = 'GPString',
            parameterType = 'Required',
        ),arcpy.Parameter(
            displayName = 'Include individual maps? Overall map will be exported automatically',
            name = 'individual',
            direction = 'Input',
            datatype = 'GPBoolean',
            parameterType = 'Required',
        ) ]
	params[0].value = 'parcel'
	params[1].value = 'C:/Temp'
	params[2].value = '100 Feet'
	params[3].filter.type = 'valueList'
	params[3].filter.list = []
	params[4].value = False
	return params
    def updateMessages(self, parameters):
        if not parameters[0].hasError() and parameters[0].valueAsText:
            parameters[3].filter.list = [f.baseName for f in arcpy.Describe(parameters[0].valueAsText).fields]
            
    def execute(self, parameters, messages):
		arcpy.AddMessage(len(parameters))
		arcpy.AddMessage('{}; {}; {}; {}; {};'.format(
			parameters[0].valueAsText,
			parameters[1].valueAsText,
			parameters[2].valueAsText,
			parameters[3].valueAsText,
			parameters[4]))
		SiteMap.generate(
			parameters[0].valueAsText,
			parameters[1].valueAsText,
			parameters[2].valueAsText,
			parameters[3].valueAsText,
                        parameters[4].valueAsText)
