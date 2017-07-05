from lib.esri import Geodatabase
from arcpy import Parameter, AddMessage, Exists, Clip_analysis, Delete_management, FeatureClassToFeatureClass_conversion, env

#arcpy toolbox
#parameter indexes
clip_from_db = 0
clip_to_db = 1
clip_projection = 2
clip_clip_layer = 3

class Clip(object):
    """arcpy toolbox for clipping an entire database"""
    def __init__(self):
        self.label = 'Clip Geodatabase'
        self.description = """
            Clip an entire database preserving datasets and
            feature class names
        """
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
        ), Parameter(
            displayName = 'Clipping Layer',
            name = 'clip_layer',
            direction = 'Input',
            datatype = 'DEFeatureClass',
            parameterType = 'Required',
        )]
    def execute(self, parameters, messages):
        AddMessage('{}; {}; {};'.format(
            parameters[clip_from_db].valueAsText,
            parameters[clip_to_db].valueAsText,
            parameters[clip_projection].valueAsText))
        from_db = parameters[clip_from_db].valueAsText
        to_db = parameters[clip_to_db].valueAsText
        projection = parameters[clip_projection].valueAsText
        clip_layer = parameters[clip_clip_layer].valueAsText

        self.clip(from_db, to_db, projection, clip_layer)

    def clip(self, from_db, to_db, projection, clip_layer):

        if not Exists(projection):
            AddMessage('Projection file {} does not exist'.format(projection))
            return
        def foreach_layer(from_dataset_path, to_dataset_path, feature_class):
            from_feature_path = '{}/{}'.format(from_dataset_path, feature_class)
            to_feature_path = '{}/{}'.format(to_dataset_path, feature_class.split('.')[-1:][0])

            Clip_analysis('{}/{}'.format(from_dataset_path, feature_class), clip_layer, to_feature_path)

        Geodatabase.process_datasets(from_db,
            to_db,
            projection,
            foreach_layer=foreach_layer)
