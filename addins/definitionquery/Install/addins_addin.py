import arcpy
import pythonaddins


def get_layer(layer):

    # we might be passed a layer object already
    if not isinstance(layer, basestring):
        return layer

    # always use current
    doc = arcpy.mapping.MapDocument('current')
    try:
        layer = [l for l in arcpy.mapping.ListLayers(doc) if l.name == layer][0]
        return layer
    except IndexError as e:
        raise Exception('Layer not found::{layer}'.format(layer=layer))
        return

def create(layer):
    # layer = get_layer(layer)

    # check selection set
    ids = [str(id) for id in layer.getSelectionSet()]
    if not len(ids):
        print('No selections on current layer')
        return

    id_field = arcpy.Describe(layer).OIDFieldName

    # set definition query
    layer.definitionQuery = '{field} IN ({ids})'.format(field=id_field, ids=','.join(ids))
    arcpy.RefreshActiveView()

def clear(layer):
    # layer = get_layer(layer)
    layer.definitionQuery = ''
    arcpy.RefreshActiveView()


class applyDefButton(object):
    """Implementation for addins_addin.defButton (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        layer = pythonaddins.GetSelectedTOCLayerOrDataFrame()
        print(layer)
        create(layer)

class clearDefinitions(object):
    """Implementation for addins_addin.clearDefs (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        layer = pythonaddins.GetSelectedTOCLayerOrDataFrame()
        print(layer)
        clear(layer)
