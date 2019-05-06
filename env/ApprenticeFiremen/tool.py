class Tool(object):
    """ Used to create tool object """   
    def __init__(self, color):
        self.COLOR = color
        pass


    def getColor(self):
        '''
        :return list int: RGB color code
        '''
        return self.COLOR

