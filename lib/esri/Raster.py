#
# Thanks to FelixIP
# http://gis.stackexchange.com/questions/187322/extracting-values-to-points-without-arcgis-spatial-analyst

from arcpy.da import UpdateCursor, SearchCursor
from arcpy import Describe, RasterToNumPyArray, PointGeometry, Point, SetProgressor, SetProgressorPosition, ResetProgressor, MakeTableView_management, GetCount_management, AddMessage, CalculateField_management

def getElevationAtPoint(raster, point):
    """
    retrieves the elevation at a point
    """

    # project the point
    sr = Describe(raster).spatialReference
    projected_point = point.projectAs(sr).getPart(0)

    # Get the first cell that starts at the point
    result = RasterToNumPyArray(raster, projected_point, 1, 1, -999)
    return result[0][0]

def calculatePointElevationField(points, raster, field_name):

    #monitor progress by counting features
    view = MakeTableView_management(points, 'points')
    count = int(GetCount_management('points').getOutput(0))
    SetProgressor('step', 'Extracting point elevations', 0, count)
    AddMessage('{} features to process'.format(count))

    # Get the object id field
    oid = Describe(points).OIDFieldName

    # make an update cursor and update each row's elevation field
    cursor = UpdateCursor(points, [field_name, 'SHAPE@', oid])

    # make a temporary dict to store our elevation values we extract
    elevations = {}

    for row in cursor:
        row[0] = getElevationAtPoint(raster, row[1])
        cursor.updateRow(row)
        AddMessage('row updated to {}; oid: {}'.format(row[0], row[2]))
        SetProgressorPosition()

    # release the data
    del cursor

    #reset this progressor
    ResetProgressor()
