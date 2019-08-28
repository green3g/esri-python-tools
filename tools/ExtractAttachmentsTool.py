from arcpy import Parameter, AddField_management, AddMessage, ListFields
from lib.esri.Attachments import extract_attachments

#parameter indexes
_attach_table = 0
_out_folder = 1
_group_by_field = 2

class ExtractAttachments(object):
    def __init__(self):
        self.label = 'Extract table attachments'
        self.description = 'Extract table attachments and add a file name field'
        self.canRunInBackground = True
		
    def initializeParameters(self):
	    self.parameters[_group_by_field].parameterDependencies = [_attach_table]
		
    def updateParameters(self, parameters):
        if parameters[_attach_table]:
            layer = parameters[_attach_table].valueAsText
            parameters[_group_by_field].filter.list = [f.name for f in ListFields(layer)]

    def getParameterInfo(self):
        """
        defines the parameters
        """
        params = [Parameter(
            displayName='Input attachment table',
            name='attach_table',
            datatype=['Table', 'GPTableView'],
            parameterType='Required',
            direction='Input'
        ), Parameter(
            displayName='Output attachments folder',
            name='out_folder',
            datatype=['DEFolder'],
            parameterType='Required',
            direction='Input'
        ), Parameter(
            displayName='Group By Field (place images in subfolders)',
            name='group_by_field',
            datatype='GPString',
            parameterType='Optional',
            direction='Input'
        )]
        return params

    def execute(self, params, messages):
        """
        gets the parameters and passes them to process
        """

        attach_table = params[_attach_table].valueAsText
        out_folder = params[_out_folder].valueAsText
        group_by_field = params[_group_by_field].valueAsText

        # run the task
        extract_attachments(attach_table, out_folder, group_by_field)

