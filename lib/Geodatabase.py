import arcpy
from arcpy import env

def clean(to_db):
    """removes all datasets and layers from the to_db"""
    env.workspace = to_db
    datasets = arcpy.ListDatasets()
    if len(datasets):
        for dataset in datasets:
            env.workspace = '{}/{}'.format(to_db, dataset)
            feature_classes = arcpy.ListFeatureClasses()
            #delete each feature class
            for feature_class in feature_classes:
                arcpy.AddMessage('Removing {}/{}'.format(env.workspace, feature_class))
                arcpy.Delete_management('{}/{}'.format(env.workspace, feature_class))
            #delete the dataset
            arcpy.AddMessage('Removing {}'.format(env.workspace))
            arcpy.Delete_management(env.workspace)

#arcpy toolbox
#parameter indexes
p_from_db = 0
p_to_db = 1
p_projection = 2

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
            parameters[p_from_db].valueAsText,
            parameters[p_to_db].valueAsText,
            parameters[p_projection].valueAsText))
        from_db = parameters[p_from_db].valueAsText
        to_db = parameters[p_to_db].valueAsText
        projection = parameters[p_projection].valueAsText
        
        #run the functions
        clean(to_db)
        self.reproject(from_db, to_db, projection)
        
    def reproject(self, from_db, to_db, projection):
        """reprojects an entire geodatabase's datasets"""
        if not arcpy.Exists(projection):
            arcpy.AddMessage('Projection file {} does not exist'.format(projection))
            return

        #get the datasets in the input workspace
        env.workspace = from_db
        arcpy.AddMessage('Workspace: {}'.format(env.workspace))
        in_datsets = arcpy.ListDatasets()
        if len(in_datsets):
            for dataset in in_datsets:
                from_dataset_path = '{}/{}'.format(from_db, dataset)
                to_dataset_path = '{}/{}'.format(to_db, dataset)
                arcpy.AddMessage('Creating Dataset: {}'.format(from_dataset_path))

                #skip existing datasets
                if arcpy.Exists(to_dataset_path):
                    arcpy.AddMessage('Skipping dataset {} because it already exists'.format(to_dataset_path))
                    continue

                #create the new dataset with the defined projection
                arcpy.CreateFeatureDataset_management(to_db, dataset, projection)
                env.workspace = from_dataset_path
                feature_classes = arcpy.ListFeatureClasses()
                #copy each feature class over
                for feature_class in feature_classes:
                    from_feature_path = '{}/{}'.format(from_dataset_path, feature_class)
                    to_feature_path = '{}/{}'.format(to_dataset_path, feature_class)
                    arcpy.AddMessage('Copying Featureclass: {}'.format(from_feature_path))

                    if arcpy.Exists(to_feature_path):
                        arcpy.AddMessage('Skipping feature class {} because it already exists'.format(to_feature_path))
                        continue
                    arcpy.FeatureClassToFeatureClass_conversion(from_feature_path, to_dataset_path, feature_class)
