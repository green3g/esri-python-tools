#directory operation functions
from os.path import split, join, isfile, exists
from os import makedirs
import errno
from PyPDF2 import PdfFileWriter, PdfFileReader
from shutil import copyfile
from arcpy.da import SearchCursor

def verify_path_exists(path):
    try:
        makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def get_page_filename(filename, page):
    """
    formats a filename
    """
    return "Page_{}.pdf".format(page + 1)

def copy_file(input_folder, destination_folder, filename):
    """
    copy a file from a path into a new directory, creating new directories where necessary
    duplicating the directory structure
        input_folder - The input file folder
        destination_folder - The destination file folder
        filename - the name of the file to copy
    """

    filepath = join(input_folder, filename)
    #make sure the file exists
    if not isfile(filepath):
        print('{} is not a file'.format(filepath))
        return False

    # make sure the output folder exists
    verify_path_exists(destination_folder)

    #copy the file
    new_filepath = join(destination_folder, filename)
    if not isfile(new_filepath):
        copyfile(filepath, new_filepath)
        print('Created file: {}'.format(new_filepath))
    return True

def extract_page(input_file, number, output_path, filename_formatter=get_page_filename):
    """
    extracts a page from a pdf and saves it to a file
        input_file - the input file pdf path
        number - the page number to extract
        format_string - the string formatter that recieves the original filename and page number
    """

    if not isfile(input_file):
        print ('{} is not a file'.format(input_file))
        return False

    #get a file name
    file_parts = split(input_file)
    file_name = file_parts[1].split('.pdf')[0]

    #check if file exists and skip if it does
    if not output_path:
        output_path = file_parts[0]
    output_file = join(output_path, filename_formatter(file_name, number).strip('/'))
    verify_path_exists(split(output_file)[0])
    if exists(output_file):
        return True

    #initialize the pdf reader/writer
    input_pdf = PdfFileReader(open(input_file, 'rb'))
    output_pdf = PdfFileWriter()

    #extract the page
    page = None
    try:
        page = input_pdf.getPage(number)
    except:
        print('error extracting page from {}'.format(input_file))
        return False

    #add the page to the output writer
    output_pdf.addPage(page)

    print('writing output - {}'.format(output_file))
    with open(output_file, 'wb') as output:
        try:
            output_pdf.write(output)
        except:
            print('error while writing output to {}'.format(output_file))
            return False
    return True

def copy_layer_filepath(layer, output_base, fields, log_file=None):
    """
    copies files in a path to a new path and splits the required pages into
    separate files for quicker loading
        layer:          the path to the layer or layer name in workspace
        output_base:    the base path to the output file
        fields:         A list of field names to use. Order should be like this:
                        [path, name, doc_id, page_num]
        log_file:       an open file or class with a `write` method
    """
    cursor = SearchCursor(layer, fields)
    print('Scanning layer - {}'.format(layer))
    if log_file:
        print ('Writing logfile - {}'.format(log_file))
        log_file.write('Problem,Layer,Plan,Page\n')

    # a dict to keep track of which files/pages to copy
    # each key references a file, and the value is a list of pages to copy
    file_list = {}
    for row in cursor:
        folder = row[0]
        name = row[1]
        doc_id = row[2]
        page_num = row[3]

        plan = join(folder, name)

        #make sure the plan isn't already in the dict
        if not doc_id in file_list:
            file_list[doc_id] = {
                'pages': [],
                'folder': folder,
                'filename': name
            }

        #add the page index to the list
        #page numbers are one more than the page index so we
        #subtract 1 because the index is one less than the page number
        try:
            page_num = int(page_num) - 1
            if page_num < 0:
                page_num = 0
        except:
            #handle invalid values (null)
            page_num = 0
        if not page_num in file_list[doc_id]['pages']:
            file_list[doc_id]['pages'].append(page_num)

    for plan, props in file_list.iteritems():
        input_folder = props['folder']
        pages = props['pages']
        filename = props['filename']
        input_file = join(input_folder, filename)
        output_folder = join(output_base, filename)

        #copy the entire file
        #log errors
        if not copy_file(input_folder, output_folder, filename) and log_file:
            log_file.write('Copy file failed,{},{},{} \n'.format(layer, plan, -99))
        for page in pages:
            # and split the pages
            #log errors for future purposes
            #functions return false if error occurs
            if not extract_page(input_file, page, output_folder) and log_file:
                 log_file.write('Extract page failed,{},{},{} \n'.format(layer, plan, page))
    print('----Done-----!\n\n')
