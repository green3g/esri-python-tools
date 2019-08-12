#Geodatabase tools

def get_name(name):
    """
    retrieves a file gdb friendly name with no '.' dots

    """
    return name.split('.')[-1:][0]


def delete_existing(path):
    from arcpy import Exists, Delete_management, AddMessage
    if Exists(path):
        AddMessage('File exists and will be removed: {}'.format(path))
        Delete_management(path)

def copy_tables(input_ws, output_ws, foreach_table = None):
    """
    copies tables or sends each table to a function
        input_ws - the input database
        output_ws - the output database
        foreach_table - the optional function to process each table
    """
    from arcpy import env, ListTables, AddMessage, AddWarning, \
        TableToGeodatabase_conversion, GetCount_management, \
        TableToTable_conversion
    from os.path import join 

    env.workspace = input_ws
    for table in ListTables():
        AddMessage('Processing table: {}'.format(table))
        
        if env.skipAttach and '_attach' in table.lower():
            AddWarning('Skipping attachments table {}'.format(table))
            continue
        
        if env.skipEmpty:
            count = int(GetCount_management(table)[0])
            if count == 0:
                AddWarning('Skipping because table is empty: {} (empty)'.format(table))
                continue
        
        try:
            if foreach_table:
                foreach_table(input_ws, output_ws, table)
            else:
                output_path = join(output_ws, get_name(table))
                delete_existing(output_path)
                TableToTable_conversion(table, output_ws, get_name(table))
        except Exception as e:
            AddWarning('Error on table: {} - {}'.format(table, e))
            pass

def process_feature_classes(input_ws, output_ws, foreach_layer = None):
    """
    processes each featureclass with an optional function
    input_ws - the database or dataset path to process feature classes
    output_ws - the output for the feature classes
    foreach_layer - the function to process the feature classes
    """
    from arcpy import env, ListFeatureClasses, FeatureClassToGeodatabase_conversion, \
        AddWarning, AddMessage, GetCount_management, FeatureClassToFeatureClass_conversion
    from os.path import join
    env.workspace = input_ws
    feature_classes = ListFeatureClasses()
    for feature_class in feature_classes:
        
        AddMessage('Processing {}...'.format(feature_class))
        if env.skipEmpty:
            count = int(GetCount_management(feature_class)[0])
            if count == 0:
                AddWarning('Skipping because table is empty: {}'.format(feature_class))
                continue
        try:
            if foreach_layer:
                foreach_layer(input_ws, output_ws, feature_class)
            else:
                #copy each feature class over
                output_path = join(output_ws, get_name(feature_class))
                delete_existing(output_path)
                FeatureClassToFeatureClass_conversion(feature_class, output_ws, get_name(feature_class))
        except Exception as e:
            AddWarning('Error processing feature class {} - {}'.format(feature_class, e))


def process_datasets(from_db,
        to_db = None,
        foreach_layer = None,
        foreach_table = None,
        foreach_dataset = None):
    """
    creates the projected datasets necessary and then calls the function
    to perform additional functions on each layer and table
    from_db - the input database to pull from
    to_db - the output database to place the processed data
    foreach_layer - the function to process each layer with
    foreach_table - the function to process each table with
    """
    #get the datasets in the input workspace
    from arcpy import AddMessage, AddWarning, CreateFeatureDataset_management, ListDatasets, Exists, env, ExecuteError
    AddMessage('Workspace: {}'.format(env.workspace))

    #handle feature classes at the top level. these are moved into _top dataset for
    #automatic projection handling
    AddMessage('Processing tables...')
    copy_tables(from_db, to_db, foreach_table)

    AddMessage('Processing feature classes...')
    process_feature_classes(from_db, to_db, foreach_layer)

    AddMessage('Processing datasets...') 
    in_datsets = ListDatasets()
    if len(in_datsets):
        for dataset in in_datsets:
            to_dataset = get_name(dataset)
            from_dataset_path = '{}/{}'.format(from_db, dataset)
            to_dataset_path = '{}/{}'.format(to_db, to_dataset)
            AddMessage('Processing Dataset: {}'.format(from_dataset_path))
            try:
                if foreach_dataset:
                    foreach_dataset(from_db, to_db, dataset, skip_empty)
                else:
                    CreateFeatureDataset_management(to_db, to_dataset, env.outputCoordinateSystem)
            except ExecuteError as e:
                AddWarning('Could not create dataset {}, {}'.format(to_dataset, e))

            process_feature_classes(from_dataset_path, to_dataset_path, foreach_layer)


def check_exists(output, name):
    from arcpy import Exists, CreateFileGDB_management, AddMessage
    from os.path import join
    if not Exists(join(output, name)):
        AddMessage('GDB does not exist, creating...')
        CreateFileGDB_management(output, name)
