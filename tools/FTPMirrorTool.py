#
# Download an ftp directory to a local folder as a scriptable
# and model builder friendly arcpy tool
# http://stackoverflow.com/questions/5230966/python-ftp-download-all-files-in-directory
#

from arcpy import Parameter, AddMessage, AddWarning
from os.path import join
from lib.util.File_Operations import verify_path_exists
from ftplib import FTP

#paramter indexes
_output_folder = 0
_ftp_folder = 1
_ftp_server = 2
_ftp_username = 3
_ftp_password = 4

def is_file(ftp, filename):
    try: 
        ftp.cwd(filename)
    except Exception as e:
        return True 
    return False

def retrieve_directory_recursive(ftp, output_folder, directory, pattern=None):
    """
    recursively retrieves files from an ftp directory
    """

    verify_path_exists(output_folder)
    AddMessage('Navigating to {}'.format(directory))

    if is_file(ftp, directory):
        AddMessage('Processing file: {}'.format(directory))
        local_filename = join(output_folder, directory)

        if pattern is not None and pattern not in directory:
            return
        try:
            f = open(local_filename, 'wb')
            ftp.retrbinary('RETR '+ directory, f.write)
            f.close()
        except Exception as e:
            AddWarning('Could not access file {}'.format(directory))
    else:
        output_folder = join(output_folder, directory)
        filenames = ftp.nlst() # get filenames within the directory

         #navigate sub directories
        for d in filenames:
            retrieve_directory_recursive(ftp, output_folder, d)
        

class FTPMirror(object):
    def __init__(self):
        """
        Define the tool (tool name is the name of the class).
        """
        self.label = "Mirror FTP Directory"
        self.description = 'Downloads an ftp directory to a local drive'
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
        self.mirror(output_folder, ftp_folder, ftp_server, ftp_username, ftp_password)

    def mirror(self, output_folder, ftp_folder, ftp_server, ftp_username=None, ftp_password=None, pattern=None):
        """
        connects to an ftp server and downloads a directory
            output_folder - The local path to the download directory
            ftp_folder - The path on the server to download or mirror
            ftp_server - The server url to the ftp server
            ftp_username - The username to use to connect to the ftp server. The default is None
            ftp_password - The usernames password to connect to the ftp server. The default is None
            AddMessage - A logging function. The default is print
        """

        ftp = FTP(ftp_server)

        AddMessage('Logging in.')
        ftp.login(ftp_username, ftp_password)
        retrieve_directory_recursive(ftp, output_folder, ftp_folder, pattern=pattern)

        ftp.quit() # This is the polite way to close a connection
