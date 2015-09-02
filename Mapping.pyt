import lib
from lib.Sitemap_Tool import SiteMapGenerator

class Toolbox(object):
    def __init__(self):
        self.label = 'Mapping Toolbox'
        self.alias = 'Mapping'
        self.tools = [SiteMapGenerator]