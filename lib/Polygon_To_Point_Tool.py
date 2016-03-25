from arcpy import Parameter, CreateFeatureclass_management, Describe
from os.path import dirname
from .Esri.Geometry import polygon_to_point

#paramter indexes
input_fc = 0
output_fc = 1
use_template = 2

class PolygonCentroidToPoint(object):
    def __init__(self):
        """
        Define the tool (tool name is the name of the class).
        """
        self.label = "Polygon Centroid To Point"
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = [
            Parameter(
                displayName='Input Polygon Layer',
                name='input_fc',
                datatype='DEFeatureClass',
                paramterType='Required',
                direction='Input'
            ),
            Parameter(
                displayName='Use input as template',
                name='use_template',
                datatype='GPBoolean',
                direction='Input'
            ),
            Parameter(
                displayName='Output Points Layer',
                name='output_fc',
                datatype='DEFeatureClass',
                paramterType='Derived',
                direction='Output'
            )
        ]

        params[use_template].value = False
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        input_fc = parameters[input_fc].valueAsText
        output_fc = parameters[output_fc].valueAsText
        output_projection = parameters[output_projection].valueAsText
        use_template = parameters[use_template].valueAsText
        template = None
        if use_template == 'true':
            template = input_fc

        #get the directory, filename, and spatial reference
        sp_ref = Describe(input_fc).spatialReference
        directory, filename = split(output_fc)

        #create a new feature class
        messages.AddMessage('Creating feature class {}'.format(output_fc))
        CreateFeatureclass_management(directory, filename, 'Point', template, 'No', 'No', sp_ref)

        #copy the geometry centroid
        messages.AddMessage('Copying polygon centroids...')
        polygon_to_point(input_fc, output_fc)
