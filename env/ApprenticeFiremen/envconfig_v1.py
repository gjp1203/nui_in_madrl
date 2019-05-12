import random
class EnvConfigV1:

    ''' Env. V1 Parameters '''
    def __init__(self, civilians):

        """ Gridworld Dimensions """
        self.GRID_HEIGHT = 16
        self.GRID_WIDTH = 15
        self.CHANNELS = 3
        self.GH = self.GRID_HEIGHT
        self.GW = self.GRID_WIDTH
        self.HMP = int(self.GW/2) # HMP = Horizontal Mid Point
        self.VMP = int(self.GH/2) # VMP = Vertical Mid Point
        self.CP = 1 # Cell padding around the gridwolrd

        """ Color Codes """
        self.CHALLENGING_COLORS = False

        """ Agents """
        self.AGENTS_START_X = [2, self.GW-3]
        self.AGENTS_START_Y = [self.GH-2, self.GH-2]
        
        """ Civilians """
        self.CIVILIANS = civilians # Number of civilians
        # Boundary area within which the civilians must remain:
        self.Y_UPPER_BOUNDARY = self.VMP + 3
        self.Y_LOWER_BOUNDARY = self.VMP - 5
        self.X_UPPER_BOUNDARY = self.HMP + 5
        self.X_LOWER_BOUNDARY = self.HMP - 5
        self.CIVILIAN_SHIFT = 2

        # Fire coordinates
        self.FIRE_X = lambda: random.randrange(self.HMP-4, self.HMP+4, 2)
        self.FIRE_Y = lambda: random.randrange(self.VMP-5, self.VMP+3, 2)

        """ Obstacles """
        self.OBSTACLES_YX = []

        for i in range(self.GW):
            if i != self.HMP:
                self.OBSTACLES_YX.append((self.GH-3, i))
            if i!=self.HMP and i != self.HMP-2 and i != self.HMP+2:
                self.OBSTACLES_YX.append((1, i))
            self.OBSTACLES_YX.append((self.GH-1, i))
            self.OBSTACLES_YX.append((0, i))
 
            if i%2 == 1:
                self.OBSTACLES_YX.append((self.VMP-1, i))
                self.OBSTACLES_YX.append((self.VMP-3, i))
                self.OBSTACLES_YX.append((self.VMP-5, i))
                self.OBSTACLES_YX.append((self.VMP+1, i))
                self.OBSTACLES_YX.append((self.VMP+3, i))

        for i in range(self.GH):
            self.OBSTACLES_YX.append((i, 0))
            self.OBSTACLES_YX.append((i, 1))
            self.OBSTACLES_YX.append((i, self.GW-1))
            self.OBSTACLES_YX.append((i, self.GW-2))

        """ Tool Pickup Locations """
        self.PICKUP_LOCATIONS = [('charge', self.HMP+2,1),
                                 ('fire_blanket', self.HMP,1),
                                 ('fire_exstinguisher', self.HMP-2, 1)]



        """ Agent observation space """
        self.AHEAD_VIEW = 6
        self.SIDE_VIEW = 6
        self.DIM = [self.AHEAD_VIEW+self.AHEAD_VIEW+1,\
                    self.SIDE_VIEW+self.SIDE_VIEW+1,
                    self.CHANNELS]
        self.OFFSET = self.AHEAD_VIEW


