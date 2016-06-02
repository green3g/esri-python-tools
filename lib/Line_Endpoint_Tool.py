from arcpy import Parameter, CreateFeatureclass_management, Describe, AddMessage
from os.path import split as Split_Path
from .esri.Geometry import line_to_endpoints

#paramter indexes
_input_fc = 0
_use_template = 1
_output_fc = 2

class LineEndPoints(object):
    def __init__(self):
        """
        Define the tool (tool name is the name of the class).
        """
        self.label = "Extract Polyline Endpoints"
        self.description = 'Converts a polyline geometry into start and endpoints'
        self.canRunInBackground = True

    def getParameterInfo(self):
        """
        Define parameter definitions
        """
        params = [Parameter(
            displayName='Input Polyline Layer',
            name='input_fc',
            datatype='DEFeatureClass',
            parameterType='Required',
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
            parameterType='Required',
            direction='Output'
        )]

        params[_use_template].value = False
        return params

    def execute(self, params, messages):
        """
        The source code of the tool
        """
        input_fc = params[_input_fc].valueAsText
        output_fc = params[_output_fc].valueAsText
        use_template = params[_use_template].valueAsText
        self.process(input_fc, output_fc, use_template)

    def process(self, input_fc, output_fc, use_template='false'):
        template = None
        if use_template == 'true':
            template = input_fc

        #get the directory, filename, and spatial reference
        sp_ref = Describe(input_fc).spatialReference
        directory, filename = Split_Path(output_fc)

        #create a new feature class
        AddMessage('Creating feature class {}'.format(output_fc))
        CreateFeatureclass_management(directory, filename, 'POINT', template, 'DISABLED', 'DISABLED', sp_ref)

        #copy the geometry centroid
        AddMessage('Extracting endpoints...')
        line_to_endpoints(input_fc, output_fc)
