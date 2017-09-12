from arcpy import Parameter
from lib.esri import Geodatabase

#arcpy toolbox
#parameter indexes
reproject_from_db = 0
reproject_to_db = 1
reproject_projection = 2

class Reproject(object):
    """arcpy toolbox for reprojecting an entire database"""
    def __init__(self):
        self.label = 'Reproject Geodatabase'
        self.description = """
            Reproject an entire geodatabase preserving datasets
            and layer names. Useful for reprojecting a geodatabase
            or converting from a .mdb or sde to a .gdb"""
    def getParameterInfo(self):
        return [Parameter(
            displayName = 'From Database',
            name = 'from_db',
            direction = 'Input',
            datatype = 'Workspace',
            parameterType = 'Required',
        ), Parameter(
            displayName = 'To Database (Existing features in here will be deleted!)',
            name = 'to_db',
            direction = 'Input',
            datatype = 'Workspace',
            parameterType = 'Required',
        ), Parameter(
            displayName = 'Projection File',
            name = 'projection',
            direction = 'Input',
            datatype = 'DEPrjFile',
            parameterType = 'Required',
        )]
    def execute(self, parameters, messages):

        from_db = parameters[reproject_from_db].valueAsText
        to_db = parameters[reproject_to_db].valueAsText
        projection = parameters[reproject_projection].valueAsText

        self.reproject(from_db, to_db, projection)

    def reproject(self, from_db, to_db, projection):

        # just set the output coordinate system and outputs
        # will be projected :)
        from arcpy import env, Exists
        env.outputCoordinateSystem = projection

        #run the functions
        if not Exists(projection):
            AddMessage('Projection file {} does not exist'.format(projection))
            return

        #call the create datasets function passing the foreach layer function to it
        Geodatabase.process_datasets(from_db, to_db)
