import sys
import os
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)

from tools.SitemapTool import SiteMapGenerator
from tools.ClipTool import Clip
from tools.ReprojectTool import Reproject
from tools.PolygonCentroidTool import PolygonCentroidToPoint
from tools.LineEndpointTool import LineEndPoints
from tools.PointElevationTool import PointElevations
from tools.ExtractAttachmentsTool import ExtractAttachments
from tools.FTPMirrorTool import FTPMirror

class Toolbox(object):
    def __init__(self):
        self.label = 'ArcMapUtilities'
        self.alias = 'ArcMapUtilities'
        self.tools = [
          Clip,
          Reproject,
          SiteMapGenerator,
          PolygonCentroidToPoint,
          LineEndPoints,
          PointElevations,
          ExtractAttachments,
          FTPMirror,
        ]
