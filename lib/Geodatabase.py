######################################
# geodatabase tools
######################################

import arcpy
from arcpy import env

class Copier:
    """
    copies a geodatabase to another preserving dataset and layer names
    useful for reprojecting an entire database
    """
    def __init__(self, from_db, to_db):
        arcpy.AddMessage('Copier __init__')
        if not arcpy.Exists(from_db):
            arcpy.AddMessage('Workspace {} does not exist'.format(from_db))
            return
        if not arcpy.Exists(to_db):
            arcpy.AddMessage('Workspace {} does not exist. Tool will attempt to create it'.format(to_db))
            path = '/'.join(to_db.split('/')[:-1])
            file_path = ''.join(to_db.split('/')[-1:])
            arcpy.AddMessage('Path: {}, File: {}'.format(path, file_path))
            arcpy.CreateFileGDB_management(path, file_path)
        self.from_db = from_db
        self.to_db = to_db
        
    def __str__(self):
        return 'Copier: from_db={}; to_db={};'.format(self.from_db, self.to_db)
    
    def copy(self, projection):
        if not arcpy.Exists(projection):
            arcpy.AddMessage('Projection file {} does not exist'.format(projection))
            return
        
        #get the datasets in the input workspace
        env.workspace = self.from_db
        arcpy.AddMessage('Workspace: {}'.format(env.workspace))
        in_datsets = arcpy.ListDatasets()
        if len(in_datsets):
            for dataset in in_datsets:
                from_dataset_path = '{}/{}'.format(self.from_db, dataset)
                to_dataset_path = '{}/{}'.format(self.to_db, dataset)
                arcpy.AddMessage('Creating Dataset: {}'.format(from_dataset_path))

                #skip existing datasets
                if arcpy.Exists(to_dataset_path):
                    arcpy.AddMessage('Skipping dataset {} because it already exists'.format(to_dataset_path))
                    continue

                #create the new dataset with the defined projection
                arcpy.CreateFeatureDataset_management(self.to_db, dataset, projection)
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

    # removes all datasets and layers from the to_db
    def clean(self):
        env.workspace = self.to_db
        datasets = arcpy.ListDatasets()
        if len(datasets):
            for dataset in datasets:
                env.workspace = '{}/{}'.format(self.to_db, dataset)
                feature_classes = arcpy.ListFeatureClasses()
                #delete each feature class
                for feature_class in feature_classes:
                    arcpy.AddMessage('Removing {}/{}'.format(env.workspace, feature_class))
                    arcpy.Delete_management('{}/{}'.format(env.workspace, feature_class))
                #delete the dataset
                arcpy.AddMessage('Removing {}'.format(env.workspace))
                arcpy.Delete_management(env.workspace)
