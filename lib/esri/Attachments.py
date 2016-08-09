from arcpy import AddField_management, ListFields, AddError
from arcpy.da import UpdateCursor, SearchCursor
from os.path import join
from ..util.File_Operations import verify_path_exists

def extract_attachments(att_table, out_folder, att_field='file_name'):

    fields = ['DATA', 'ATT_NAME', 'ATTACHMENTID', att_field]

    # check for existence of required fields
    has_fields = [f.name for f in ListFields(att_table)]
    for f in fields:
        if f not in has_fields:
            AddError('Field {} is required in attribute table'.format(f))

    # verify path
    verify_path_exists(out_folder)

    with UpdateCursor(att_table, fields) as cursor:
        for row in cursor:

            # get the attachment file and create a filename
            attachment = row[0]
            filename = 'ATT_{2}_{1}'.format(*row)

            # write the output file and update the row's value to the file name
            open(join(out_folder, filename), 'wb').write(attachment.tobytes())
            row[3] = filename
            cursor.updateRow(row)

            # cleanup
            del row
            del filename
            del attachment
