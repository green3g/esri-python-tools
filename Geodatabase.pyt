from lib.Clip_Tool import Clip
from lib.Reproject_Tool import Reproject

class Toolbox(object):
    def __init__(self):
        self.label = 'Geodatabase Management Toolbox'
        self.alias = 'gdb'
        self.tools = [Reproject, Clip]
