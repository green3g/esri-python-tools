#directory operation functions
from os.path import split, join, isfile, exists
from os import makedirs
import errno
from PyPDF2 import PdfFileWriter, PdfFileReader
from shutil import copyfile

def make_sure_path_exists(path):
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
        print ('{} is not a file'.format(filepath))
        return False

    # make sure the output folder exists
    make_sure_path_exists(destination_folder)

    #copy the file
    new_filepath = join(destination_folder, filename)
    if not isfile(new_filepath):
        copyfile(filepath, new_filepath)
        print ('Created file: {}'.format(new_filepath))
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
    make_sure_path_exists(split(output_file)[0])
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
        'error extracting page from {}'.format(input_file)
        return False

    #add the page to the output writer
    output_pdf.addPage(page)

    print('writing output - {}'.format(output_file))
    with open(output_file, 'wb') as output:
        try:
            output_pdf.write(output)
        except:
            'error while writing output to {}'.format(output_file)
            return False
    return True
