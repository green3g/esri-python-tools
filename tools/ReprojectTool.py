from arcpy import Parameter
from lib.esri import Geodatabase
from arcpy import AddMessage, AddWarning, Exists, FeatureClassToFeatureClass_conversion, ExecuteError

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
        AddMessage('{}; {}; {};'.format(
            parameters[reproject_from_db].valueAsText,
            parameters[reproject_to_db].valueAsText,
            parameters[reproject_projection].valueAsText))
        from_db = parameters[reproject_from_db].valueAsText
        to_db = parameters[reproject_to_db].valueAsText
        projection = parameters[reproject_projection].valueAsText

        self.reproject(from_db, to_db, projection)

    def reproject(from_db, to_db, projection):
        #run the functions
        Geodatabase.clean(to_db)
        if not Exists(projection):
            AddMessage('Projection file {} does not exist'.format(projection))
            return

        def foreach_layer(from_dataset_path, to_dataset_path, feature_class):
            from_feature_path = '{}/{}'.format(from_dataset_path, feature_class)
            to_feature_path = '{}/{}'.format(to_dataset_path, to_feature_class)
            AddMessage('Reprojecting Featureclass: {} to {}'.format(from_feature_path, to_feature_path))

            if Exists(to_feature_path):
                AddMessage('Skipping feature class {} because it already exists'.format(to_feature_path))
                return
            try:
                FeatureClassToFeatureClass_conversion(from_feature_path, to_dataset_path, to_feature_class)
            except ExecuteError as e:
                AddWarning('Failed to process {}, {}'.format(feature_class, e))
        #call the create datasets function passing the foreach layer function to it
        Geodatabase.process_datasets(from_db,
            to_db,
            projection,
            foreach_layer = foreach_layer)
