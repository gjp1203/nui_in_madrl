import sys
from .tool import Tool
from .fire_blanket import Fire_Blanket
from .fire_exstinguisher import Fire_Exstinguisher
from .charge import Charge
import random

class Fireman:
    """Implementation of a Fireman agent."""

    def __init__(self, fireman_id, x, y, c, colors):
        '''
        :param int fireman_id: Each agent receives a unique id
        :param int x: initial x coordinate
        :param int y: initial y coordinate
        :param object c: environment config
        :param vector: rgb color code
        '''
        self.c = c
        # List used to inidcate the tools available to the agent
        self.tools = ['fire_blanket', 'fire_exstinguisher', 'charge']
        # Dict to indicate how profficient the fireman
        # is witch each item 
        self._last_tool_id = None
        self._facingFire = False
        self.done = False
        self.fire_id = None
        self.reward = 0
        self.x = x # x coordinate is set
        self.y = y # y coordinate is set
        self.initial_x = x # Used for reset
        self.initial_y = y # Used for reset
        self.fireman_id = fireman_id # Fireman id is set
        self.minReward = None
        self.initToolSteps() # Tool step counters are initialised
        self.agent_colors = colors.AGENT_COLORS # Agents colors are set
        self._active = False # Indicates agent participation in putting out fires
        self._charge = Charge(colors.CHARGE)
        self._fb = Fire_Blanket(colors.FIRE_BLANKET)
        self._fe = Fire_Exstinguisher(colors.FIRE_EXSTINGUISHER)
        self._toolList = [self._charge, self._fb, self._fe]
        self._tooldicts = {'charge':self._charge,
                           'fire_exstinguisher':self._fe,
                           'fire_blanket':self._fb}

    def setFacingFire(self):
        '''
        Set _facingFire to true.
        '''
        self._facingFire = True

    def isFacingFire(self):
        '''
        Returns true if the agent is facing the fire.
        '''
        return self._facingFire

    def updateUseCount(self):
        '''
        Updates the number of times current tool has been used.
        '''
        self.tool_steps[self.getToolName()] += 1
   
    def undoXY(self):
        '''
        Used to undo last step. 
        '''
        self.x = self._reset_x 
        self.y = self._reset_y

    def move(self, action, cN, cS, cE, cW):
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
        # Execute action
        if action == 0 and cN == False: 
            self.moveNorth() 
        elif action == 1 and cS == False:
            self.moveSouth() 
        elif action == 2 and cE == False:
            self.moveEast() 
        elif action == 3 and cW == False:
            self.moveWest() 
        elif action == 4: # No-op
            return

    def getActive(self):
        '''
	Getter method to find out whether agent is/was active participant
        in putting out a fire.
        '''
        return self._active

    def resetActive(self):
        '''
        Default setting for self._active is False
        '''
        self._active = False


    def setActive(self):
        '''
        Switch self._active to True
        '''
        self._active = True


    def initToolSteps(self):
        '''
        Method used to initialise tool step counter
        '''
        self.tool_steps = {'itemless':0}
        for item in self.tools:
            self.tool_steps.update({item:0})
     
    def getEXSteps(self):
        '''
        :return int: number of steps taken with charges
        '''
        return self.tool_steps['charge']

    def getFESteps(self):
        '''
        :return int: number of steps taken with charges
        '''
        return self.tool_steps['fire_exstinguisher']
  
    def getFBSteps(self):
        '''
        :return int: number of steps taken with charges
        '''
        return self.tool_steps['fire_blanket']

    def getID(self):
        '''
        :return int: agent's id
        '''
        return self.fireman_id

    def getToolSteps(self):
        ''' 
        Method returns list with number of steps
        each available tool has been carried.
        :return list of integers
        '''
        return self.tool_steps

    def resetXY(self):
        ''' 
	Method used to reset agents x and y coordinates.
	'''
        self.x = self.initial_x
        self.y = self.initial_y

    def putDownTool(self):
        '''
        Method used to delete tool held by the agent
        '''
        if self.holdingTool():
            del self.tool

    def releaseItem(self):
        '''
        Method used to release tool:
        :return tool: Tool being released by the agent
        '''
        tmpTool = self.tool
        del self.tool
        return tmpTool

    def holdingTool(self):
        '''
        Method to check if agent is holding a tool 
        :return bool: true if agent is holding tool
        '''
        return hasattr(self, 'tool')

    def getColor(self):
        '''
        Method returns the color of the fireman based upon
        which tool is currently being used 
        return: list with three integers representing RGB
        '''
        if self.holdingTool():
            return self.agent_colors[self.tool.NAME]
        else:
            return self.agent_colors['itemless']

    def moveNorth(self):
        '''
        Moves agent 1 step towards the north
        '''
        if self._facingFire == False:
            self.y = (self.y + 1)%self.c.GRID_HEIGHT

    def moveSouth(self):
        '''
        Moves agent 1 step towards the south
        '''
        if self._facingFire == False:
            self.y = (self.y - 1)%self.c.GRID_HEIGHT

    def moveEast(self):
        '''
        Moves agent 1 step towards the east
        '''
        if self._facingFire == False:
            self.x = (self.x + 1)%self.c.GRID_WIDTH

    def moveWest(self):
        '''
        Moves agent 1 step towards the west
        '''
        if self._facingFire == False:
            self.x  = (self.x - 1)%self.c.GRID_WIDTH

    def getXY(self):
        '''
        :return self.x: x coordiantes of the agent
        :return self.y: y coordiantes of the agent
        '''
        return self.x, self.y

    def useTool(self, toolname):
        '''
        Agent switches to toolname.
        :param string toolname: name of tool that the agent should use.
        '''
        self.tool =self._tooldicts[toolname]
        self._last_tool_id = self.tool.ID
        #self.toolPickupQ = self.drl.getCurrentQ()
        self.updateUseCount()

    def pickupTool(self, tool):
        '''
        Method to pickup tool object 
        :param tool tool: tool object to be picked up
        '''
        print("Agent " + self.getID() + " picked up " + tool.NAME)
        self.tool = tool
        self._last_tool_id = self.tool.ID

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

    def getToolName(self):
        '''
        Method to get the name of the current tool 
        :return string: Name of tool held by the agent
        '''
        if self.holdingTool():
            return self.tool.NAME
        else:
            return 'itemless'

    def getLastToolID(self):
        '''
        Method to get the id of the current tool 
        :return string: Name of tool held by the agent
        '''
        return self._last_tool_id

    def resetTool(self):
        '''
        Resets tool.
        '''
        if self.holdingTool():
            del self.tool

    def reset(self):
        '''
        Method called upon to reset agent state
        '''
        self._facingFire = False
        self.done = False
        self.resetXY()
        self.initToolSteps()
        self.resetTool()
        self.fire_id = None
        self.reward = 0

