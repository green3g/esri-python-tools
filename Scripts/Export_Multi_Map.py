from lib.esri.Extent import expand
from lib.util.String import get_safe_string

def export_layer_maps(helper, title, layer_key='Map:', title_element='Title', subtitle_element='Subtitle', output='C:/Temp/', file_suffix=''):
    """
    exports a set of maps by toggling a filtered set of layers
    By default, it searches for layers that start with 'Map:' and
    uses this list to generate a set of maps
        helper - A MapLayoutHelper
        title - The primary title of the map
        layer_key - (optional) the string to filter map layers on. The default is 'Map:'
        title_element - (optional) the string to search for a title text element. This item
            will be updated with the title text
        subtitle_element - (optional) the string to search for a subtitle text element.
            This item will be updated to the name of the layer, minus the layer_key text.
            If a layer's name is Map:Aerial, the subtitle will be set to "Aerial"
        output - (optional) The output folder path.
        file_suffix - (optional) The default filename will be the title_subtitle.pdf,
            adding this value will add an additional string to the end of the filepath.
    """

    # get a list of layers to use for "maps"
    # set them all to not visible for starters
    layers = [l for l in helper.map.map.listLayers() if layer_key in l.name]
    for l in layers:
        l.visible = False

    # get the text elements
    subtitle_element = helper.layout.listElements('TEXT_ELEMENT', subtitle_element)[0]
    title_element = helper.layout.listElements('TEXT_ELEMENT', title_element)[0]
    title_element.text = title

    # Go through each layer, set it to visible, and export a pdf
    for l in layers:
        l.visible = True
        name = l.name.split(':')[1]
        subtitle_element.text = name
        filename = get_safe_string('{}_{}_{}'.format(title, name, file_suffix))
        helper.layout.exportToPDF(output + filename)
        l.visible = False

class FeatureExtentIter:
    """
    A quick helper to iterate through a feature layer and set a map extent.
    This is similar to data driven pages in ArcMap. (Not tested with points!)
    Usage:
        helper = MapLayoutHelper('CURRENT')
        rows = FeatureExtentIter(helper, iter_layer='My Layer', expand_extent=50)
        for row in rows:
            helper.layout.exportToPDF('C:/Temp/' + row[3])
    Constructor:
        helper - the MapLayoutHelper
        iter_layer - The layer to iterate through
        expand_extent - The percent to expand each feature's extent
    """
    def __init__(self, helper, iter_layer='Industrial Development Sites', expand_extent=25):
        from arcpy.da import SearchCursor
        from arcpy import Describe
        layer = helper.map.map.listLayers(iter_layer)[0]
        fields = ['SHAPE@'] + [f.name for f in Describe(layer).fields]
        self.helper = helper
        self.cursor = SearchCursor(layer, fields)
        self.expand_extent = expand_extent

    def __iter__(self):
        return self

    def __next__(self):
        row = next(self.cursor)
        if not row:
            raise StopIteration
        self.helper.map.camera.setExtent(expand(row[0].extent, self.expand_extent))
        return row

class MapLayoutHelper(object):
    """
    A helper object to initialize a project, layout, and a map for easy access.
    Usage:
        MapLayoutHelper('CURRENT')
    Constructor:
        project - (optional) The path to the ArcGIS Pro project or the text "CURRENT"
            if you are using an open proejct. The default is 'CURRENT'.
        layout - (optional) The name of the layout to initialize. The default
            is 'Template'
        map - (optional) The name of the map element inside the layout provided.
            The default is 'Map'
    """
    def __init__(self, project='CURRENT', layout='Template', map='Map'):
        from arcpy.mp import ArcGISProject
        self.project = ArcGISProject(project)
        self.layout = self.project.listLayouts(layout)[0]
        self.map = self.layout.listElements('MAPFRAME_ELEMENT', map)[0]
