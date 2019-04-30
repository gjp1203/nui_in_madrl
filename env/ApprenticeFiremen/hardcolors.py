import numpy as np
OBSTACLE = np.array((145, 145, 145)) 
EMPTY_TILE = np.array((0, 0, 0))
# Tool Colors
AGENT = np.array((.0, 200.0, .0)) #np.array((255.0, 255.0, 255.0))
FIRE_BLANKET       = np.array((200.0, 0.0,   200.0))
CHARGE             = np.array((0.0,   200.0, 200.0)) 
FIRE_EXSTINGUISHER = np.array((200.0,   200.0,   0.0))
AGENT_COLORS = {'fire_blanket'        : FIRE_BLANKET,
                'fire_exstinguisher'  : FIRE_EXSTINGUISHER,
                'charge'              : CHARGE,
                'itemless'            : AGENT}
FIRE = np.array((200.0, 0.0, 0.0))

