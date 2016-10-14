import sys
import os
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)
from tools.DataUpdater import MultipleLayerUpdater
from tools.ClipTool import Clip
from tools.ReprojectTool import Reproject
from tools.PolygonCentroidTool import PolygonCentroidToPoint
from tools.LineEndpointTool import LineEndPoints
from tools.PointElevationTool import PointElevations
from tools.ExtractAttachmentsTool import ExtractAttachments
from tools.FTPMirrorTool import FTPMirror

class Toolbox(object):
    def __init__(self):
        self.label = 'Utilities'
        self.alias = 'Utilities'
        self.tools = [
          Clip,
          Reproject,
          MultipleLayerUpdater,
          PolygonCentroidToPoint,
          LineEndPoints,
          PointElevations,
          ExtractAttachments,
          FTPMirror,
        ]
