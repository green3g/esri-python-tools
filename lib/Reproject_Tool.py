import arcpy
from Esri import Geodatabase

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
            parameters[reproject_from_db].valueAsText,
            parameters[reproject_to_db].valueAsText,
            parameters[reproject_projection].valueAsText))
        from_db = parameters[reproject_from_db].valueAsText
        to_db = parameters[reproject_to_db].valueAsText
        projection = parameters[reproject_projection].valueAsText

        #run the functions
        Geodatabase.clean(to_db)
        self.reproject(from_db, to_db, projection)

    def reproject(self, from_db, to_db, projection):
        """reprojects an entire geodatabase's datasets"""
        if not arcpy.Exists(projection):
            arcpy.AddMessage('Projection file {} does not exist'.format(projection))
            return

        def foreach_layer(from_dataset_path, to_dataset_path, feature_class):
            from_feature_path = '{}/{}'.format(from_dataset_path, feature_class)
            to_feature_path = '{}/{}'.format(to_dataset_path, feature_class)
            arcpy.AddMessage('Reprojecting Featureclass: {}'.format(from_feature_path))

            if arcpy.Exists(to_feature_path):
                arcpy.AddMessage('Skipping feature class {} because it already exists'.format(to_feature_path))
                return
            arcpy.FeatureClassToFeatureClass_conversion(from_feature_path, to_dataset_path, feature_class)

        #call the create datasets function passing the foreach layer function to it
        Geodatabase.process_datasets(from_db,
            to_db,
            projection,
            foreach_layer = foreach_layer)
