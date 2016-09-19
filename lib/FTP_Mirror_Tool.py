#
# Download an ftp directory to a local folder as a scriptable
# and model builder friendly arcpy tool
# http://stackoverflow.com/questions/5230966/python-ftp-download-all-files-in-directory
#

from arcpy import Parameter

#paramter indexes
_output_folder = 0
_ftp_folder = 1
_ftp_server = 2
_ftp_username = 3
_ftp_password = 4

class FTPMirror(object):
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
            displayName='Output Folder',
            name='output_folder',
            datatype='DEFolder',
            parameterType='Required',
            direction='Output'
        ), Parameter(
            displayName='FTP Folder',
            name='ftp_folder',
            parameterType='Optional',
            direction='Input'
        ), Parameter(
            displayName='FTP Server',
            name='ftp_server',
            parameterType='Required',
            direction='Input'
        ), Parameter(
            displayName='FTP Username',
            name='ftp_username',
            parameterType='Optional',
            direction='Input'
        ), Parameter(
            displayName='FTP Password',
            name='ftp_password',
            parameterType='Optional',
            direction='Input'
        )]
        return params

    def execute(self, params, messages):
        """
        The source code of the tool
        """
        output_folder = params[_output_folder].valueAsText
        ftp_folder = params[_ftp_folder].valueAsText
        ftp_server = params[_ftp_server].valueAsText
        ftp_username = params[_ftp_username].valueAsText
        ftp_password = params[_ftp_password].valueAsText
        from arcpy import AddMessage
        self.process(output_folder, ftp_folder, ftp_server, ftp_username, ftp_password, AddMessage)

    def process(self, output_folder, ftp_folder, ftp_server, ftp_username=None, ftp_password=None, AddMessage):
        """
        connects to an ftp server and downloads a directory
            output_folder - The local path to the download directory
            ftp_folder - The path on the server to download or mirror
            ftp_server - The server url to the ftp server
            ftp_username - The username to use to connect to the ftp server. The default is None
            ftp_password - The usernames password to connect to the ftp server. The default is None
            AddMessage - A logging function. The default is print
        """

        from ftplib import FTP
        from os.path import join

        ftp = FTP(ftp_server)

        AddMessage('Logging in.')
        ftp.login(ftp_username, ftp_password)

        AddMessage('Navigating to {}'.format(ftp_folder))
        ftp.cwd(ftp_folder)
        ftp.retrlines('LIST')

        AddMessage('Accessing files')
        filenames = ftp.nlst() # get filenames within the directory
        AddMessage(filenames)

        for filename in filenames:
            local_filename = join(output_folder, filename)
            file = open(local_filename, 'wb')
            ftp.retrbinary('RETR '+ filename, file.write)

            file.close()

        ftp.quit() # This is the “polite” way to close a connection
