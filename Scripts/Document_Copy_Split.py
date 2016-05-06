from arcpy.da import SearchCursor
from arcpy import Parameter, AddMessage, ListFields
from lib.util.File_Operations import extract_page, copy_file
from os.path import join, split

def copy_layer_filepath(layer, output_base, fields, log_file=None):
    """
    copies files in a path to a new path and splits the required pages into
    separate files for quicker loading
        layer - the path to the layer or layer name in workspace
        field - the name of the field to use
        input_base - the base path to the input file
        output_base - the base path to the output file
        fields = [path, name, doc_id, page_num]
        log_file - an open file or class with a `write` method
    """
    cursor = SearchCursor(layer, fields)
    print('Scanning layer - {}'.format(layer))
    if log_file:
        print 'Writing logfile - {}'.format(log_file)
        log_file.write('Problem,Layer,Plan,Page\n')
    # a dict to keep track of which files/pages to copy
    # each key references a file, and the value is a list of pages to copy
    file_list = {}
    for row in cursor:
        folder = row[0]
        name = row[1]
        doc_id = row[2]
        page_num = row[3]

        plan = join(folder, name)

        #make sure the plan isn't already in the dict
        if not doc_id in file_list:
            file_list[doc_id] = {
                'pages': [],
                'folder': folder,
                'filename': name
            }

        #add the page index to the list
        #page numbers are one more than the page index so we
        #subtract 1 because the index is one less than the page number
        try:
            page_num = int(page_num) - 1
            if page_num < 0:
                page_num = 0
        except:
            #handle invalid values (null)
            page_num = 0
        if not page_num in file_list[doc_id]['pages']:
            file_list[doc_id]['pages'].append(page_num)

    for plan, props in file_list.iteritems():
        input_folder = props['folder']
        pages = props['pages']
        filename = props['filename']
        input_file = join(input_folder, filename)
        output_folder = join(output_base, filename)

        #copy the entire file
        #log errors
        if not copy_file(input_folder, output_folder, filename) and log_file:
            log_file.write('Copy file failed,{},{},{} \n'.format(layer, plan, -99))
        for page in pages:
            # and split the pages
            #log errors for future purposes
            #functions return false if error occurs
            if not extract_page(input_file, page, output_folder) and log_file:
                 log_file.write('Extract page failed,{},{},{} \n'.format(layer, plan, page))
    print '----Done-----!\n\n'

if __name__ == '__main__':
    # location to copy the documents
    output_location = '//my-network/output_location'

    # table to join the data to
    join_table = 'C:/data.gdb/documents_table'

    #field in the join table that references folder's path
    folder_field = "_PLAN_INDEX$.Folder_Path"

    # field in the join table that references the documents file name
    file_field = "_PLAN_INDEX$.File_Name"

    # field in the join table that references the document id
    # this is the join field
    document_id = "_PLAN_INDEX$.Document_ID"

    #  the input workspace for layers to join to the join table
    workspace = 'C:/data.gdb'

    # the layers to iterate through
    layers = [
        'UtilitySanitary/sswr_pipe',
        'UtilitySanitary/sswr_struc',
        'UtilityStorm/storm_struc',
        'UtilityStorm/storm_pipe',
        'UtilityWater/water_struc',
        'UtilityWater/water_pipe',
    ]
    arcpy.MakeTableView_management(join_table, 'plans')
    for layer in layers:
        fields = [
            folder_field,
            file_field,
            document_id,
            '{}.Plan_Page_Number'.format(layer.split('/')[1])
        ]
        log_file = open('C:/temp_data/errors/{}.csv'.format(layer.replace('/', '')), 'w')
        layer_name = layer.split('/')[1]
        arcpy.MakeFeatureLayer_management(join(workspace, layer), layer_name)
        arcpy.AddJoin_management(layer_name, 'Plan_ID', 'plans', 'Document_ID', 'KEEP_COMMON')
        copy_layer_filepath(layer_name, output_location, fields, log_file)
        log_file.close()
