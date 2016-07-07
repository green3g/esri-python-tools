#
# Thanks to FelixIP
# http://gis.stackexchange.com/questions/187322/extracting-values-to-points-without-arcgis-spatial-analyst

from arcpy.da import UpdateCursor, SearchCursor
from arcpy import Describe, RasterToNumPyArray, PointGeometry, Point, SetProgressor, SetProgressorPosition, ResetProgressor, MakeTableView_management, GetCount_management, AddMessage

def getElevationAtPoint(raster, point):
    """
    retrieves the elevation at a point
    """

    # project the point
    sr = Describe(raster).spatialReference
    projected_point = point.projectAs(sr).getPart(0)

    # Get the first cell that starts at the point
    result = RasterToNumPyArray(raster, projected_point)
    return result[0][0]

def calculatePointElevationField(points, raster, field_name):

    #monitor progress by counting features
    view = MakeTableView_management(points, 'points')
    count = int(GetCount_management('points').getOutput(0))
    SetProgressor('step', 'Calculating point elevations', 0, 100)
    AddMessage('{} features to process'.format(count))


    # make an update cursor and update each row's elevation field
    cursor = UpdateCursor(points, ['SHAPE@', field_name])

    for row in cursor:
        row[1] = getElevationAtPoint(raster, row[0])
        cursor.updateRow(row)
        SetProgressorPosition()

    #reset this progressor
    ResetProgressor()
