from ..esri.Geometry import line_to_endpoints
import arcpy

arcpy.AddToolbox('../Utilities.pyt')

related_layers = [{
    'layer': 'storm_pipe',
    'related': 'storm_struc',
    'from_foreign_key': 'from_struc_id',
    'to_foreign_key': 'to_struc_id',
    'reference_key': 'cid'
}]

for layer in related_layers:
    print('processing layer {}...'.format(layer['layer']))

    # create the points layer
    foreign_key = 'related_oid'
    points = 'in_memory/end_point'
    points = arcpy.Utilities.LineEndPoints(layer['layer'], 'false', points).getOutput(0)
    print('points layer created: {}'.format(points))

    # spatially join to the related point layer
    joined_points = 'in_memory/joined_points'
    joined_points = arcpy.SpatialJoin_analysis(points, layer['related'], joined_points).getOutput(0)
    print('spatial join completed: {}'.format(joined_points))

    # add a join on the line layer
    line_layer = arcpy.MakeFeatureLayer_management(layer['layer'], 'line_layer').getOutput(0)
    oid_field = arcpy.Describe(line_layer).OIDFieldName
    arcpy.AddJoin_management(joined_points, foreign_key, line_layer, oid_field)
    print('join added: {}'.format(joined_points))

    # create two feature layers one for each related field
    start_points = arcpy.MakeFeatureLayer_management(joined_points, 'start_points', where_clause='point_type="START"').getOutput(0)
    end_points = arcpy.MakeFeatureLayer_management(joined_points, 'end_points', where_clause='point_type="END"').getOutput(0)
    print('layers created: {}, {}'.format(start_points, end_points))

    # calculate the fields new values 
    arcpy.CalculateField_management(start_points, layer['from_foreign_key'], layer['reference_key'])
    arcpy.CalculateField_management(end_points, layer['to_foreign_key'], layer['reference_key'])
