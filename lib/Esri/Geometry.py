from arcpy.da import SearchCursor, InsertCursor
from arcpy import Describe, AddField_management

def polygon_to_point(input_fc, output_fc):
    """
    copies the centroid of polygon geometry to
    a point feature class
    """

    oid_field = Describe(input_fc).OIDFieldName
    new_field = 'Rel_OID'

    AddField_management(output_fc, new_field, 'Long')

    search_cursor = SearchCursor(input_fc, ['SHAPE@', oid_field])
    insert_cursor = InsertCursor(output_fc, ["SHAPE@", new_field])
    spatial_reference = Describe(output_fc).spatialReference

    for row in search_cursor:
        point = row[0].projectAs(spatial_reference).centroid
        oid = row[1]
        insert_cursor.insertRow([point, oid])

    del search_cursor, insert_cursor, spatial_reference
