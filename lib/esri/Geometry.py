from arcpy.da import SearchCursor, InsertCursor
from arcpy import Describe, AddField_management, AddMessage

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

def line_to_endpoints(input_fc, output_fc, id_field=None):
    """
    copies the endpoints of a feature class into a point
    feature class
    """

    # id field can either be provided or obtained automagically
    oid_field = id_field if id_field else Describe(input_fc).OIDFieldName

    # we add two custom fields to track the related id and the type of end point
    related_field = 'related_oid'
    type_field = 'point_type'
    AddField_management(output_fc, related_field, 'LONG')
    AddField_management(output_fc, type_field, 'TEXT', field_length=10)


    fields = [f.name for f in Describe(input_fc).fields if f.name not in ['SHAPE@', 'Shape', 'Shape_Length']]
    output_fields = fields + ['SHAPE@', related_field, type_field]

    #shape will be the last column selected
    search_cursor = SearchCursor(input_fc, fields + ['SHAPE@'])

    #our insert cursor
    insert_cursor = InsertCursor(output_fc, output_fields)

    #identify the spatial reference for projecting the geometry
    spatial_reference = Describe(output_fc).spatialReference

    for row in search_cursor:
        # project and store the geometry
        geom = row[len(row) - 1].projectAs(spatial_reference)

        # get the row id
        oid = row[fields.index(oid_field)]
        
        # insert two entries but with our new custom geometry
        insert_cursor.insertRow(row[:-1] + (geom.firstPoint, oid, 'START'))
        insert_cursor.insertRow(row[:-1] + (geom.lastPoint, oid, 'END'))

    del search_cursor, insert_cursor, spatial_reference
