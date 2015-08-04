import arcpy

__author__ = "groemhildt"

def expand(extent, percent):
    '''expands an arcpy.Extent by a given percentage'''
    multiplier = percent / float(100)
    x_dif = (extent.XMax - extent.XMin) * multiplier
    y_dif = (extent.YMax - extent.YMin) * multiplier
    return arcpy.Extent(extent.XMin - x_dif, extent.YMin - y_dif,
                        extent.XMax + x_dif, extent.YMax + y_dif)