import numpy as np
OBSTACLE = np.array((145, 145, 145)) 
EMPTY_TILE = np.array((0, 0, 0))
# Tool Colors
AGENT = np.array((255.0, 255.0, 255.0))
FIRE_BLANKET       = np.array((255.0, 0.0,   0.0))
CHARGE             = np.array((0.0,   255.0, 0.0)) 
FIRE_EXSTINGUISHER = np.array((0.0,   0.0,   255.0))
AGENT_COLORS = {'fire_blanket'        : FIRE_BLANKET,
                'fire_exstinguisher'  : FIRE_EXSTINGUISHER,
                'charge'              : CHARGE,
                'itemless'            : AGENT}
FIRE = np.array((255.0, 100.0, 100.0))

"""import numpy as np
OBSTACLE = 40.0 #np.array((145, 145, 145)) 
EMPTY_TILE = 0.0 #np.array((0, 0, 0))
# Tool Colors
AGENT = 80.0 #np.array((255.0, 255.0, 255.0))
FIRE_BLANKET       = 120.0 #np.array((255.0, 0.0,   0.0))
CHARGE             = 160.0 #np.array((0.0,   255.0, 0.0)) 
FIRE_EXSTINGUISHER = 200.0 #np.array((0.0,   0.0,   255.0))
AGENT_COLORS = {'fire_blanket'        : FIRE_BLANKET,
                'fire_exstinguisher'  : FIRE_EXSTINGUISHER,
                'charge'              : CHARGE,
                'itemless'            : AGENT}
FIRE = 240.0 #np.array((255.0, 100.0, 100.0))
"""
