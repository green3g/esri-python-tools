from arcpy import Parameter
from arcpy import AddField_management
from lib.esri.Raster import calculatePointElevationField

#parameter indexes
_input_raster = 0
_input_points = 1
_field_name = 2

class PointElevations(object):
    def __init__(self):
        self.label = 'Calculate Point Elevations'
        self.description = 'Adds an elevation field value from a raster dem'
        self.canRunInBackground = True

    def getParameterInfo(self):
        """
        defines the parameters
        """
        params = [Parameter(
            displayName='Input Raster DEM',
            name='input_raster',
            datatype=['DERasterDataset', 'DERasterCatalog'],
            parameterType='Required',
            direction='Input'
        ), Parameter(
            displayName='Input Points Layer',
            name='input_points',
            datatype=['DEFeatureClass', 'GPFeatureLayer'],
            parameterType='Required',
            direction='Input'
        ), Parameter(
            displayName='New Elevation Field Name',
            name='title',
            direction='Input',
            datatype='GPString',
            parameterType='Required',
        )]
        params[_field_name].value = 'point_elevation'
        return params

    def execute(self, params, messages):
        """
        gets the parameters and passes them to process
        """

        input_raster = params[_input_raster].valueAsText
        input_points = params[_input_points].valueAsText
        field_name = params[_field_name].valueAsText
        self.process(input_raster, input_points, field_name)

    def process(self, input_raster, input_points, field_name):
        """
        creates a new field called point_elevation on the feature class
        and populates it with values from the raster at the intersection
        """
        AddField_management(input_points, field_name, "FLOAT")
        calculatePointElevationField(input_points, input_raster, field_name)
