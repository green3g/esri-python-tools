from lib.Sitemap_Tool import SiteMapGenerator
from lib.Data_Updater import MultipleLayerUpdater
from lib.Clip_Tool import Clip
from lib.Reproject_Tool import Reproject
from lib.Polygon_Centroid_Tool import PolygonCentroidToPoint

class Toolbox(object):
    def __init__(self):
        self.label = 'Utilities'
        self.alias = 'Utilities'
        self.tools = [
          Clip,
          Reproject,
          SiteMapGenerator,
          MultipleLayerUpdater,
          PolygonCentroidToPoint,
        ]
