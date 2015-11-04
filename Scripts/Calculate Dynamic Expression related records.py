# Calculates the dynamic expression for a layer and can be used
# to dynamically display related records text for data driven pages
# or feature labels

# Change the FindLabel parameter to the id field of the main table
# This id should be related to each of the related tables
# Also change the first line of FindLabel. Set parameter equal to the FindLabel parameter
def FindLabel ( [PARCELID] ):
    return get_lookup_text([PARCELID])

# create formatter functions to return what you want displayed
# for each row. These should return plain text for each row.

# returns a string with the parcel zone
def get_parcel(row):
    return row["ZONE"]

# change the lookup tables and assign their appropriate formatter function
# Properties of each lookup item:
# table: the name of the table in the mxd
# row_formatter: the function that will format each row's properties and return
# the text string
# id_field: the name of the field in the table that is related to the
# id passed in to FindLabel
# fields: list of fields by name (optiononal) default '*'
lookup_tables = [{
    "table": "Related_Zones",
    "row_formatter": get_parcel,
    "id_field": "PARCELID",
    "fields": ['PARCELID', 'ZONE'],
    "header": 'Parcel Zones:',
},
#other lookup tables...
]


def get_lookup_text(id):
    # init the return value
    text = ''
    if id is not None:
        for table in lookup_tables:
            if table.has_key('header'):
                text += "{} \n".format(table['header'])
            if type(id) is str or type(id) is unicode:
                query = "{} = '{}'".format(table["id_field"], id)
            else:
                query = "{} = {}".format(table["id_field"], id)
            fields = table['fields'] if table.has_key('fields') else '*'
            with arcpy.da.SearchCursor(table["table"], fields, where_clause=query) as rows:
                for row in rows:
                    dictionary = dict()
                    for idx, val in enumerate(rows.fields):
                        dictionary[val] = row[idx]
                    text += "{} \n".format(table["row_formatter"](dictionary))
    return text
