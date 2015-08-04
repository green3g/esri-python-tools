
__author__ = "groemhildt"
__date__ = "$Aug 4, 2015 8:45:26 AM$"

def expand(extent, percent):
    '''expands an arcpy.Extent by a given percentage'''
    multiplier = percent / float(100)
    x_dif = (extent.XMax - extent.XMin) * multiplier
    y_dif = (extent.YMax - extent.YMin) * multiplier
    return arcpy.Extent(extent.XMin - x_dif, extent.YMin - y_dif,
                        extent.XMax + x_dif, extent.YMax + y_dif)