import lib
from lib.Geodatabase import Reproject, Clip
reload(lib)
reload(lib.Geodatabase)

class Toolbox(object):
    def __init__(self):
        self.label = 'Geodatabase Management Toolbox'
        self.alias = 'Management'
        self.tools = [Reproject, Clip]