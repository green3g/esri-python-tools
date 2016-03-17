#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      groemhildt
#
# Created:     17/03/2016
# Copyright:   (c) groemhildt 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from arcpy.mp import ArcGISProject
from arcpy.da import UpdateCursor
from arcpy import Parameter


def update_layer(layer, field, value, new_value):
    try:
        cursor = UpdateCursor(layer, field, '{} = \'{}\''.format(field, value))
    except(TypeError):
        return "Error loading table {}".format(layer)

    try:
        for row in cursor:
            row[0] = new_value
            cursor.updateRow(row);
    except(RuntimeError):
        del cursor
        return 'Error on field: {}, where {} = \'{}\''.format( field, field, value )

    return 'Layer Updated: {}'.format(layer)

def get_layer_names():
    doc = ArcGISProject('current')
    m = doc.listMaps('Map')[0]
    return [l.name for l in m.listLayers()]

def main():
    layers = get_layer_names()
    for layer in layers:
        print(update_layer(layer, 'Plan_ID', '1415', '1415TownSquareLn'))

if __name__ == '__main__':
    main()

class MultipleLayerUpdater(object):
    def __init__(self):
        self.label = 'Multiple Layer Updater'
        self.alias = 'Updates a field in multiple layers in the current map document with a value'
        self.canRunInBackground = False

    def getParameterInfo(self):
        return [Parameter(
            displayName='Field',
            name='field',
            datatype='GPString',
            parameterType='Required',
            direction='Input'
        ), Parameter(
            displayName='Old Value',
            name='old_value',
            datatype='GPString',
            parameterType='Required',
            direction='Input'
        ), Parameter(
            displayName='New Value',
            name='new_value',
            datatype='GPString',
            parameterType='Required',
            direction='Input'
        )]

    def execute(self, parameters, messages):
        layers= get_layer_names()
        for layer in layers:
            messages.addMessage(
            update_layer(layer, parameters[0].valueAsText, parameters[1].valueAsText, parameters[2].valueAsText))
