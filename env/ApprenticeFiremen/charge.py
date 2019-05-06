from env.ApprenticeFiremen.tool import Tool
class Charge(Tool):
    """ Charge charge tool """
    NAME = 'charge'
    ID = 2
    def __init__(self, color): 
        super(Charge, self).__init__(color)

