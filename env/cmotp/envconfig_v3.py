import random
class EnvConfigV3:

    ''' Env. V3 Parameters '''
    def __init__(self):
        """ Gridworld Dimensions """
        self.GRID_HEIGHT = 16
        self.GRID_WIDTH = 16
        self.MID = self.GRID_WIDTH // 2
        self.GH = self.GRID_HEIGHT
        self.GW = self.GRID_WIDTH
        self.DIM = [self.GH, self.GW]
        self.HMP = int(self.GW//2) # HMP = Horizontal Mid Point
        self.VMP = int(self.GH//2) # VMP = Vertical Mid Point
        self.ACTIONS = 5 # No-op, move up, down, left, righ

        """ Wind (slippery surface) """
        self.WIND = 0.0
       
        """ Agents """
        self.NUMBER_OF_AGENTS = 2
        self.AGENTS_X =[1, self.GW-1] 
        self.AGENTS_Y = [self.GH-1, self.GH-1]

        """ Goods """
        self.GOODS_X = self.MID # Pickup X Coordinate
        self.GOODS_Y = 11       # Pickup y Coordinate
      
        """ DZONE (X, Y, Reward) """
        self.DZONES = [(self.MID-2,0, lambda: 1.0 if random.uniform(0, 1) > 0.4 else 0.4),
                       (self.MID+2,0, lambda: 0.8)] 
 
        """ Colors """
        self.AGENTS = [240.0, 200.0] # Colors [Agent1, Agent2]
        self.GOODS = 150.0
        self.OBSTACLE = 100.0

        # Noise related parameters.
        # Used to turn CMOTP into continous environment
        self.NOISE = 0
        self.MU = 1.0
        self.SIGMA = 0.0

        """ Obstacles """
        self.OBSTACLES_YX = []

        # Left column is made unavaialble:
        for i in range(self.GH):
            self.OBSTACLES_YX.append((i, 0))

        # Wall is initialised to seperate agents from the main room: 
        for i in range(0, self.GW):
            if i != self.MID:
                self.OBSTACLES_YX.append((self.GH-2, i))

        # Bottleneck Layers:
        #for i in range(0, self.MID-1):
        #    self.OBSTACLES_YX.append((3, i))

        #for i in range(self.MID+2, self.GW):
        #    self.OBSTACLES_YX.append((3, i))

        #for i in range(5, self.GW-4):
        #    self.OBSTACLES_YX.append((5, i))

        for i in range(0, 6):
            self.OBSTACLES_YX.append((8, i))

        for i in range(self.GW-5, self.GW):
            self.OBSTACLES_YX.append((8, i))

        # Platform above the goods
        for i in range(5, self.GW-4):
            self.OBSTACLES_YX.append((10, i))

        # Touchdown area 
        for i in range(0, self.MID - 3):
            self.OBSTACLES_YX.append((0, i))
        self.OBSTACLES_YX.append((0,self.MID))
        for i in range(self.MID + 4, self.GW):
            self.OBSTACLES_YX.append((0,i))

