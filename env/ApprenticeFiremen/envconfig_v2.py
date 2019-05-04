class EnvConfigV2:

    ''' Env. V2 Parameters '''
    def __init__(self, civilians):

        """ Gridworld Dimensions """
        self.GRID_HEIGHT = 43
        self.GRID_WIDTH = 43
        self.CHANNELS = 3
        self.GH = self.GRID_HEIGHT
        self.GW = self.GRID_WIDTH
        self.HMP = int(self.GW/2) # HMP = Horizontal Mid Point
        self.VMP = int(self.GH/2) # VMP = Vertical Mid Point
        self.CP = 5 # Cell padding around the gridwolrd

        """ Color Codes """
        self.CHALLENGING_COLORS = False

        """ Agents """
        self.AGENTS_START_X = [self.HMP, self.HMP, self.CP+1, self.GW-self.CP-2]
        self.AGENTS_START_Y = [self.CP+1, self.GW-self.CP-2, self.VMP, self.VMP]

        """ Civilians """
        self.CIVILIANS = civilians # Number of civilians
        # Boundary area within which the civilians must remain:
        self.Y_UPPER_BOUNDARY = self.VMP + 5
        self.Y_LOWER_BOUNDARY = self.VMP - 5
        self.X_UPPER_BOUNDARY = self.HMP + 5
        self.X_LOWER_BOUNDARY = self.HMP - 5
        self.CIVILIAN_SHIFT = 3

        # Fire coordinates
	self.FIRE_X = None
	self.FIRE_Y = None

        """ Obstacles """
        self.OBSTACLES_YX = []
        for i in range(self.GH):
            self.OBSTACLES_YX.append((i, 0))
            self.OBSTACLES_YX.append((i, self.GW-1))
            if (i < self.CP+11 and i > self.CP+5) or (i > self.GH-self.CP-12 and i < self.GH-self.CP-6):
                for j in range(self.GW):
                    if j != self.HMP:
                        self.OBSTACLES_YX.append((i, j))
            if (i < self.CP+11) or (i > self.GH-self.CP-7):
                for j in range(self.GW):
                    if j < self.HMP-2 or j > self.HMP+2: 
                        self.OBSTACLES_YX.append((i, j))
                for j in range(self.CP):
                    self.OBSTACLES_YX.append((i, j))
                    self.OBSTACLES_YX.append((i, self.GW-1-j))
            if i!=self.VMP and i != self.VMP-2 and i != self.VMP+2: 
                self.OBSTACLES_YX.append((i, self.CP+3))
                self.OBSTACLES_YX.append((i, self.GW-self.CP-4))

        for i in range(self.GW):
            if (i < self.CP+11 and i > self.CP+5) or (i > self.GW-self.CP-12 and i < self.GW-self.CP-6):
                for j in range(self.GH):
                    if j != self.VMP:
                        self.OBSTACLES_YX.append((j, i))
            if (i < self.CP+11) or (i > self.GW-self.CP-12):
                for j in range(self.GH):
                    self.OBSTACLES_YX.append((j, i))
            if i%2 == 1 and i > self.CP+11 and i < self.GW-self.CP-12:
                self.OBSTACLES_YX.append((self.VMP, i))
                self.OBSTACLES_YX.append((self.VMP-2, i))
                self.OBSTACLES_YX.append((self.VMP-4, i))
                self.OBSTACLES_YX.append((self.VMP+2, i))
                self.OBSTACLES_YX.append((self.VMP+4, i))

            if i!=self.HMP and i != self.HMP-2 and i != self.HMP+2: 
                self.OBSTACLES_YX.append((self.CP+3, i))
                self.OBSTACLES_YX.append((self.GH-self.CP-4, i))

            for j in range(self.CP):
                self.OBSTACLES_YX.append((j, i))
                self.OBSTACLES_YX.append((self.GH-1-j, i))

        """ Tool Pickup Locations """
        self.PICKUP_LOCATIONS = [('charge', self.HMP+2,self.GW-self.CP-4),
                            ('fire_blanket', self.HMP,self.GW-self.CP-4),
	                    ('fire_exstinguisher',self.HMP-2, self.GW-self.CP-4),
                            ('charge', self.HMP+2, self.CP+3),
                            ('fire_blanket', self.HMP, self.CP+3),
	                    ('fire_exstinguisher',self.HMP-2, self.CP+3)]

        """ Agent observation space """
        self.AHEAD_VIEW = 6
        self.SIDE_VIEW = 6
        self.DIM = [self.AHEAD_VIEW+self.AHEAD_VIEW+1,\
                    self.SIDE_VIEW+self.SIDE_VIEW+1,
                    self.CHANNELS]
        self.OFFSET = self.AHEAD_VIEW


