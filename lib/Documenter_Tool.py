import arcpy
from Esri import Geodatabase

documentor_db = 0
documentor_output = 1

class Documenter(object):
    """Document a geodatabases layers, fields, and eventually more"""
    def __init__(self):
        self.label = "Geodatabase Documenter"
        self.description = """Document a geodatabases layers, fields, and eventually more"""
        
    def getParameterInfo(self):
        return [arcpy.Parameter(
            displayName = 'Database',
            name = 'db',
            direction = 'Input',
            datatype = 'Workspace',
            parameterType = 'Required',
        )]