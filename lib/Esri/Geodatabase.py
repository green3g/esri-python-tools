#Geodatabase tools

import arcpy
from arcpy import env

def copy_tables(input_ws, output_ws, foreach_table = None):
    """
    copies tables or sends each table to a function
        input_ws - the input database
        output_ws - the output database
        foreach_table - the optional function to process each table
    """
    env.workspace = input_ws
    feature_tables = arcpy.ListTables()
    for table in feature_tables:
        if(foreach_table):
            foreach_table(input_ws, output_ws, table)
        else:
            arcpy.TableToTable_conversion('{}/{}'.format(input_ws, table), output_ws, table)

def process_feature_classes(input_ws, output_ws, foreach_layer = None):
    """
    processes each featureclass with an optional function
    input_ws - the database or dataset path to process feature classes
    output_ws - the output for the feature classes
    foreach_layer - the function to process the feature classes
    """
    env.workspace = input_ws
    feature_classes = arcpy.ListFeatureClasses()
    if foreach_layer:
        #copy each feature class over
        for feature_class in feature_classes:
            foreach_layer(input_ws, output_ws, feature_class)

def process_datasets(from_db,
        to_db = None,
        projection = None,
        foreach_layer = None,
        foreach_table = None,
        foreach_dataset = None):
    """
    creates the projected datasets necessary and then calls the function
    to perform additional functions on each layer and table
    from_db - the input database to pull from
    to_db - the output database to place the processed data
    projection - the projection file to use for creating the output datasets
    foreach_layer - the function to process each layer with
    foreach_table - the function to process each table with
    """
    #get the datasets in the input workspace
    arcpy.AddMessage('Workspace: {}'.format(env.workspace))

    #handle feature classes at the top level. these are moved into _top dataset for
    #automatic projection handling
    arcpy.CreateFeatureDataset_management(to_db, '_top', projection)
    to_dataset_path = '{}/_top'.format(to_db)
    copy_tables(from_db, to_db, foreach_table)

    process_feature_classes(from_db, to_dataset_path, foreach_layer)

    in_datsets = arcpy.ListDatasets()
    if len(in_datsets):
        for dataset in in_datsets:
            from_dataset_path = '{}/{}'.format(from_db, dataset)
            to_dataset_path = '{}/{}'.format(to_db, dataset)
            arcpy.AddMessage('Processing Dataset: {}'.format(from_dataset_path))
            if foreach_dataset:
                foreach_dataset(from_db, to_db, dataset)
            else:
                #skip existing datasets
                if arcpy.Exists(to_dataset_path):
                    arcpy.AddMessage('Skipping dataset {} because it already exists'.format(to_dataset_path))
                    continue
                #create the new dataset with the defined projection
                arcpy.CreateFeatureDataset_management(to_db, dataset, projection)
            process_feature_classes(from_dataset_path, to_dataset_path, foreach_layer)

def clean(to_db):
    """
    removes all datasets and layers from the to_db
    to_db - the database to remove datasets and layers from
    """
    env.workspace = to_db
    feature_classes = arcpy.ListFeatureClasses()
    #delete each feature class
    for feature_class in feature_classes:
        arcpy.AddMessage('Removing {}/{}'.format(env.workspace, feature_class))
        arcpy.Delete_management('{}/{}'.format(env.workspace, feature_class))
    datasets = arcpy.ListDatasets()
    if len(datasets):
        def remove(input_ws, output_ws, feature_class):
            arcpy.AddMessage('Removing {}/{}'.format(output_ws, feature_class))
            arcpy.Delete_management('{}/{}'.format(output_ws, feature_class))
        for dataset in datasets:
            path = '{}/{}'.format(to_db, dataset)

            #process each feature class
            process_feature_classes(path, path, remove)

            #delete the dataset
            arcpy.AddMessage('Removing {}'.format(env.workspace))
            arcpy.Delete_management(env.workspace)
