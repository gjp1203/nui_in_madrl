from env.ApprenticeFiremen.tool import Tool
import env.ApprenticeFiremen.colors
class Fire_Exstinguisher(Tool):
    """ Fire exstinguisher tool """
    NAME = 'fire_exstinguisher'
    ID = 1
    def __init__(self, color):
        super(Fire_Exstinguisher, self).__init__(color)
