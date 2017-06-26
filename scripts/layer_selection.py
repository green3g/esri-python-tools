#
#
# A better way to create selection set layers
# This method uses object id's to create a definition expression
# rather than a weird layer that we can't modify later like
# arcmap's builtin method
#
#

import arcpy

# always use current
doc = arcpy.mapping.MapDocument('current')

def get_layer(layer):
    try:
        layer = [l for l in arcpy.mapping.ListLayers(doc) if l.name == layer][0]
        return layer
    except IndexError as e:
        raise Exception('Layer not found::{layer}'.format(layer=layer))
        return

def create(layer):
    layer = get_layer(layer)

    # check selection set
    ids = [str(id) for id in layer.getSelectionSet()]
    if not len(ids):
        print('No selections on current layer')
        return

    id_field = arcpy.Describe(layer).OIDFieldName

    # set definition query
    layer.definitionQuery = '{field} IN ({ids})'.format(field=id_field, ids=','.join(ids))

def clear(layer):
    layer = get_layer(layer)
    layer.definitionQuery = ''
