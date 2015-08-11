import lib
from lib.Geodatabase import Reproject

class Toolbox(object):
    def __init__(self):
        self.label = 'Geodatabase Management Toolbox'
        self.alias = 'Management'
        self.tools = [Reproject]