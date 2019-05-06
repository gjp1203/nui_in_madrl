class EnvConfigV3:

    ''' Env. V1 Parameters '''
    def __init__(self, civilians, accesspoints):

        """ Gridworld Dimensions """
        self.GRID_HEIGHT = 13
        self.GRID_WIDTH = 13
        self.CHANNELS = 3
        self.GH = self.GRID_HEIGHT
        self.GW = self.GRID_WIDTH
        self.HMP = int(self.GW/2) # HMP = Horizontal Mid Point
        self.VMP = int(self.GH/2) # VMP = Vertical Mid Point
        self.CP = 0 # Cell padding around the gridwolrd

        """ Color Codes """
        self.CHALLENGING_COLORS = False

        """ Agents """
        self.AGENTS_START_X = [1, self.GW-2]
        self.AGENTS_START_Y = [self.GH-2, self.GH-2]
        
        """ Civilians """
        self.CIVILIANS = civilians # Number of civilians
        # Boundary area within which the civilians must remain:
        self.Y_UPPER_BOUNDARY = self.VMP + 5
        self.Y_LOWER_BOUNDARY = self.VMP - 5
        self.X_UPPER_BOUNDARY = self.HMP + 5
        self.X_LOWER_BOUNDARY = self.HMP - 5
        self.CIVILIAN_SHIFT = 3

        # Fire coordinates
        self.FIRE_X = [self.HMP]
        self.FIRE_Y = [self.VMP]

        self.FIRE_X = lambda: self.HMP
        self.FIRE_Y = lambda: self.VMP
        if accesspoints == 1:
            self.OVERLAP_XY = (self.HMP,self.VMP+1)
   
        """ Obstacles """
        self.OBSTACLES_YX = []

        for i in range(self.GW):
            if i != self.HMP:
                self.OBSTACLES_YX.append((self.GH-3, i))
            if i!=self.HMP and i != self.HMP-2 and i != self.HMP+2:
                self.OBSTACLES_YX.append((1, i))
            self.OBSTACLES_YX.append((self.GH-1, i))
            self.OBSTACLES_YX.append((0, i))
 
        for i in range(self.GH):
            self.OBSTACLES_YX.append((i, 0))
            self.OBSTACLES_YX.append((i, self.GW-1))


        if accesspoints == 1:
            self.OBSTACLES_YX.append((self.VMP-1, self.HMP))
            self.OBSTACLES_YX.append((self.VMP, self.HMP-1))
            self.OBSTACLES_YX.append((self.VMP, self.HMP+1))
        elif accesspoints == 2:
            self.OBSTACLES_YX.append((self.VMP+1, self.HMP))
            self.OBSTACLES_YX.append((self.VMP-1, self.HMP))
        elif accesspoints == 3:
            self.OBSTACLES_YX.append((self.VMP-1, self.HMP))

        """ Tool Pickup Locations """
        self.PICKUP_LOCATIONS = [('charge', self.HMP+2,1),
                                 ('fire_blanket', self.HMP,1),
                                 ('fire_exstinguisher', self.HMP-2, 1)]



        """ Agent observation space """
        self.AHEAD_VIEW = 6
        self.SIDE_VIEW = 6
        self.DIM = [self.AHEAD_VIEW+self.AHEAD_VIEW+1,\
                    self.SIDE_VIEW+self.SIDE_VIEW+1]
        self.OFFSET = self.AHEAD_VIEW


