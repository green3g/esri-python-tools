from arcpy import Parameter

#parameter indexes
_attach_table = 0
_out_folder = 1

class ExtractAttachments(object):
    def __init__(self):
        self.label = 'Extract table attachments'
        self.description = 'Extract table attachments and add a file name field'
        self.canRunInBackground = True

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
        )]
        return params

    def execute(self, params, messages):
        """
        gets the parameters and passes them to process
        """

        attach_table = params[_attach_table].valueAsText
        out_folder = params[_out_folder].valueAsText
        self.process(attach_table, out_folder)

    def process(self, attach_table, out_folder):
        """
        creates a new field on the attachments table and uses
        extract attachments function to move the attachments to
        the output path.
        """

        from arcpy import AddField_management
        from .esri.Attachments import extract_attachments
        
        # add a file name field
        AddField_management(attach_table, 'file_name', "TEXT", field_length=50)

        # run the task
        extract_attachments(attach_table, out_folder)
