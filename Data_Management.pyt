from lib.Geodatabase import Copier
import arcpy

class Toolbox(object):
    def __init__(self):
        self.label = 'Data Management Toolbox'
        self.alias = 'Management'
        self.tools = [CopyGeodatabase]

class CopyGeodatabase(object):
    def __init__(self):
        self.label = 'Copy Geodatabase'
        self.description = """
            Copy an entire geodatabase preserving datasets
            and layer names. Useful for reprojecting a geodatabase
            or converting from a .mdb or sde to a .gdb"""
    def getParameterInfo(self):
        return [arcpy.Parameter(
            displayName = 'From Database',
            name = 'from_db',
            direction = 'Input',
            datatype = 'Workspace',
            parameterType = 'Required',
        ), arcpy.Parameter(
            displayName = 'To Database (Existing features in here will be deleted!)',
            name = 'to_db',
            direction = 'Input',
            datatype = 'Workspace',
            parameterType = 'Required',
        ), arcpy.Parameter(
            displayName = 'Projection File',
            name = 'projection',
            direction = 'Input',
            datatype = 'DEPrjFile',
            parameterType = 'Required',
        )]
    def execute(self, parameters, messages):
        arcpy.AddMessage('{}; {}; {};'.format(
            parameters[0].valueAsText,
            parameters[1].valueAsText,
            parameters[2].valueAsText))
        copier = Copier(parameters[0].valueAsText, parameters[1].valueAsText)
        arcpy.AddMessage(copier)
        copier.clean()
        copier.copy(parameters[2].valueAsText)
