from env.ApprenticeFiremen.tool import Tool
import env.ApprenticeFiremen.colors
class Fire_Blanket(Tool):
    """ Fire blanket tool """
    NAME = 'fire_blanket'
    ID = 0
    def __init__(self, color): 
        super(Fire_Blanket, self).__init__(color)

	
