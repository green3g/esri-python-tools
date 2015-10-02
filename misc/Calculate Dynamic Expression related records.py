# Calculates the dynamic expression for a layer and can be used
# to dynamically display related records text for data driven pages
# or feature labels
#
# Instructions:
# Change the FindLabel parameter to the id field of the main table
# This id should be related to each of the related tables
# Also change the first line of FindLabel. Set id equal to the FindLabel parameter
# Change the formatter functions to match up with what you want displayed
# for each row. These should return plain text for each row.
# change the lookup tables and assign their appropriate formatter function
#
# Properties of each lookup item:
# table: the name of the table in the mxd
# row_formatter: the function that will format each row's properties and return
# the text string
# id_field: the name of the field in the table that is related to the
# id passed in to FindLabel
import arcpy
def get_block(row):
    return "<BOL>Block {} ({}):\n {} Buildings</BOL>".format(row.Block, row.Reference, row.Number_of_Buildings)
def get_condition(row):
    return "- {} Units in {} Condition".format(row.Units, row.Condition)
def get_type(row):
    return "- {} Units of {} Type".format(row.Units, row.Type)
lookup_tables = [{
        "table": "Blocks",
        "row_formatter": get_block,
        "id_field": "Block"
    },{
        "table": "Conditions",
        "row_formatter": get_condition,
        "id_field": "Block_Number"
    }, {
        "table": "Types",
        "row_formatter": get_type,
        "id_field": "Block_Number"
    }
]
def FindLabel ( [Downtown_Parcels_wBlock2.Block_Number] ):
    id = [Downtown_Parcels_wBlock2.Block_Number]
    if id:
        mxd = arcpy.mapping.MapDocument("CURRENT")
        text = ""
        for value in lookup_tables:
            query = "{} = {}".format(id, value["id_field"])
            rows = arcpy.SearchCursor(value["table"], query)
            for row in rows:
                text ="{}{} \n".format(text, value["row_formatter"](row))
    return text
