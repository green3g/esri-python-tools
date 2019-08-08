from arcpy import AddField_management, ListFields, AddError, Describe, AddMessage
from arcpy.da import UpdateCursor, SearchCursor
from os.path import join
from ..util.File_Operations import verify_path_exists

def extract_attachments(att_table, out_folder, group_by_field=None):
    # [<Field>, ...]
    l_fields = ListFields(att_table)

    # [dbo.schema.fieldname, ...]
    field_names = [f.name for f in l_fields]

    # [DBO.SCHEMA.FIELDNAME, ...]
    uppercase = [f.upper() for f in field_names]


    data_field = None
    name_field = None
    id_field = None
    
    data_field = [f for f in uppercase if 'DATA' in f.split('.')][0]
    name_field = [f for f in uppercase if 'ATT_NAME' in f.split('.')][0]
    id_field = [f.name for f in l_fields if f.type == 'OID'][0]

    fields = [data_field, name_field, id_field]
    AddMessage(fields)
	
    if group_by_field:
        if not group_by_field in field_names:
            raise Exception('Field {} not found in fields. \n'.format(group_by_field, str(field_names)))
        fields.append(group_by_field)
        
    # verify path
    verify_path_exists(out_folder)

    with SearchCursor(att_table, fields) as cursor:
        for row in cursor:

            full_out_folder = out_folder
            if group_by_field:

                # get the field name
                group_folder = row[ fields.index(group_by_field) ]
                
                full_out_folder = join(out_folder, group_folder)

                # double check folder path
                verify_path_exists(full_out_folder)

            # get the attachment file and create a filename
            attachment = row[0]
            filename = 'ATT_{2}_{1}'.format(*row)

            # write the output file and update the row's value to the file name
            open(join(full_out_folder, filename), 'wb').write(attachment.tobytes())
            
            # cleanup
            del row
            del filename
            del attachment


