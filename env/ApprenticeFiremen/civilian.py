from random import randint
import random as random
import colors
import sys

class Civilian:
    """Implementation of a civilian."""

    def __init__(self, c):
        '''
        :param object: config
        '''
	self.c = c
        self.agent_colors = colors.AGENT_COLORS # Agents colors are set
        self.resetXY()
 
    def undoXY(self):
	'''
        Used to undo last step. 
	'''
        self.x = self._reset_x 
        self.y = self._reset_y

    def move(self, cN, cS, cE, cW):
        '''
        Method obtains action via agent object:
        :param np.array s_t: current state
        :param bool cN: Is north cell obstacle free
        :param bool cS: Is south cell obstacle free
        :param bool cE: Is east cell obstacle free
        :param bool cW: Is west cell obstacle free
        '''
        self._reset_x = self.x 
        self._reset_y = self.y 
        action = random.randrange(5) 
        # Execute action
        if action == 0 and cN == False and self.y < self.c.Y_UPPER_BOUNDARY: 
            self.moveNorth() 
        elif action == 1 and cS == False and self.y > self.c.Y_LOWER_BOUNDARY:
            self.moveSouth() 
        elif action == 2 and cE == False and self.x < self.c.X_UPPER_BOUNDARY:
            self.moveEast() 
        elif action == 3 and cW == False and self.x > self.c.X_LOWER_BOUNDARY:
            self.moveWest() 
        elif action == 4: # No-op
            return

    def resetXY(self):
        ''' 
	Method used to reset agents x and y coordinates.
	'''
        r = random.randrange(2)
        if r == 0:
            self.y = self.c.VMP-self.c.CIVILIAN_SHIFT # y coordinate is set
        else:
            self.y = self.c.VMP+self.c.CIVILIAN_SHIFT # y coordinate is set
        self.x = self.c.HMP # x coordinate is set


    def getColor(self):
        '''
        Method returns the color of the agent based upon
        which tool is currently being used 
        return: list with three integers representing RGB
        '''
        return self.agent_colors['itemless']

    def moveNorth(self):
        '''
        Moves agent 1 step towards the north
        '''
        self.y = (self.y + 1)%self.c.GRID_HEIGHT

    def moveSouth(self):
        '''
        Moves agent 1 step towards the south
        '''
        self.y = (self.y - 1)%self.c.GRID_HEIGHT

    def moveEast(self):
        '''
        Moves agent 1 step towards the east
        '''
        self.x = (self.x + 1)%self.c.GRID_WIDTH

    def moveWest(self):
        '''
        Moves agent 1 step towards the west
        '''
        self.x  = (self.x - 1)%self.c.GRID_WIDTH

    def getXY(self):
        '''
        :return self.x: x coordiantes of the agent
        :return self.y: y coordiantes of the agent
        '''
        return self.x, self.y

    def getXYH(self):
        '''
        :return self.x: x coordiantes of the agent
	:return self.y: y coordiantes of the agent
        :return self.heading: direction that the agent is facing
        '''
	return self.x, self.y, self.heading

    def updateXY(self, x, y):
        '''
        Method to update the x and y coordinates.
        :param int x: new x coordinate
        :param int y: new y coordinate
        '''
        self.x = x
        self.y = y

    def nextNorth(self):
        '''
        :return x and y coordinate to the north of the agent
        '''
        return self.x, (self.y + 1)%self.c.GRID_HEIGHT

    def nextSouth(self):
        '''
        :return x and y coordinate to the south of the agent
        '''
        return self.x, (self.y - 1)%self.c.GRID_HEIGHT

    def nextEast(self):
        '''
        :return x and y coordinate to the east of the agent
        '''
        return (self.x + 1)%self.c.GRID_WIDTH, self.y

    def nextWest(self):
        '''
        :return x and y coordinate to the west of the agent
        '''
        return (self.x - 1)%self.c.GRID_WIDTH, self.y

    def reset(self):
        '''
        Method called upon to reset agent state
        '''
        self.resetXY()
