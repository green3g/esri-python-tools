import arcpy
from lib.SiteMap import SiteMapGenerator

reload(SiteMap)

class Toolbox(object):
    def __init__(self):
        self.label = 'Mapping Toolbox'
        self.alias = 'Mapping'
        self.tools = [SiteMapGenerator]


