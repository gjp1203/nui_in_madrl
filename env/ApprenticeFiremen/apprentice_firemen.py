from env.ApprenticeFiremen.fire_exstinguisher import Fire_Exstinguisher
from env.ApprenticeFiremen.fire_blanket import Fire_Blanket
from matplotlib import pyplot as plt
from env.ApprenticeFiremen.pickuparea import Pickuparea
from env.ApprenticeFiremen.civilian import Civilian
from scipy.misc import imsave 
from env.ApprenticeFiremen.fireman import Fireman
from config import Config
from env.ApprenticeFiremen.charge import Charge
from env.ApprenticeFiremen.fire import Fire
import numpy as np
import os.path
import random
import time
import csv
import cv2

class ApprenticeFiremen(object):
    """ Gridworld Apprentice Firemen Environment """
    def __init__(self, flags, version, civilians, rewardMode, accesspoints):
        '''
        :param tf.flags: Settings
        '''
        if version == 1:
            from envconfig_v1 import EnvConfigV1
            self.c = EnvConfigV1(civilians)
        if version == 2:
            from envconfig_v2 import EnvConfigV2
            self.c = EnvConfigV2(civilians)
        if version == 3:
            from envconfig_v3 import EnvConfigV3
            self.c = EnvConfigV3(civilians, accesspoints)
        if self.c.CHALLENGING_COLORS:
            import hardcolors
            self.colors = hardcolors
        else:
            import colors
            self.colors = colors
        self.accesspoints = accesspoints
        self.eval = 0
        self.episode_count = 0 
        self.civilians = [Civilian(self.c) for i in range(self.c.CIVILIANS)]
        self.rewardMode = rewardMode
        if flags.agents > len(self.c.AGENTS_START_X):
            raise ValueError('Agent limmit ' + str(len(self.c.AGENTS_START_X)) + ' exceeded.')
        if flags.agents != 2 and flags.agents != 4:
            raise ValueError('ApprenticeFiremen requires either 2 or 4 agents.')

        self.firemen = [Fireman("A" + str(i), 
		        self.c.AGENTS_START_X[i], 
	                self.c.AGENTS_START_Y[i],
			self.c,
                        self.colors)\
                        for i in range(flags.agents)]
        
        # Dict can be called upon to create new tools
        self.createTool = {'charge' : self.newCharge,
                           'fire_blanket' : self.newFireBlanket,
                           'fire_exstinguisher' : self.newFireExstinguisher}
   
        # Set fieldnames used for stats
        self.fieldnames = ['Episode',
                           'Eval',
                           'Steps', 
                           'Total_Reward']
        for i in range(flags.agents):
            self.fieldnames.append('A'+str(i)+'fes')
            self.fieldnames.append('A'+str(i)+'fbs')
            self.fieldnames.append('A'+str(i)+'exs')
            self.fieldnames.append('A'+str(i)+'_reward')
            self.fieldnames.append('A'+str(i)+'_fire_id')

        self.__dim = self.c.DIM
        self.__out = 5 # No-op, turn left/right, or move up, down, left, righ

    @property
    def dim(self):
        return self.__dim

    @property
    def out(self):
        return self.__out

    def getEpStatsFieldnames(self):
        fieldnames = []
        fieldnames.append('eval')
        for i in range(len(self.firemen)):
            fieldnames.append('A'+str(i)+'_saliency')
            fieldnames.append('A'+str(i)+'_x')
            fieldnames.append('A'+str(i)+'_y')
            fieldnames.append('A'+str(i)+'_fes')
            fieldnames.append('A'+str(i)+'_fbs')
            fieldnames.append('A'+str(i)+'_exs')
            fieldnames.append('A'+str(i)+'_fire_id')
        for i in range(self.c.CIVILIANS):
            fieldnames.append('C'+str(i)+'_xy_saliency')
            fieldnames.append('C'+str(i)+'_x')
            fieldnames.append('C'+str(i)+'_y')
        for tool, x, y in self.c.PICKUP_LOCATIONS:
            fieldnames.append(str(tool) + '_' + str(x) + '_' + str(y) + '_saliency')
        for _, fire in self.fires.items():
            x, y = fire.getXY()
            fieldnames.append('fire_' + str(x) + '_' + str(y) + '_saliency')
        return fieldnames

    def getAgentCoordinates(self):
        coordinates = []
        for f in self.firemen:
            coordinates.append(f.getXY())
        return coordinates

    def getSaliencyCoordinates(self):
        coordinates = []
        for i in range(len(self.firemen)):
            coordinates.append(self.firemen[i].getXY())
        for i in range(self.c.CIVILIANS):
            coordinates.append(self.civilians[i].getXY())
        for tool, x, y in self.c.PICKUP_LOCATIONS: 
            coordinates.append((x,y))
        for _, fire in self.fires.items():
            coordinates.append(fire.getXY())
        return coordinates

    def getHW(self):
        return (self.c.GH, self.c.GW)

    def processSaliencyCoordinates(self, saliency, runFolder):
        for f, s in zip(self.firemen, saliency):
            folder = runFolder + str(self.episode_count)+ "_"+str(f.fireman_id)
            statscsv = folder + '/ep_stats.csv'
            if not os.path.exists(folder):
                 os.mkdir(folder)
                 with open(statscsv, 'w') as csvfile:
                     writer = csv.DictWriter(csvfile, fieldnames=self.getEpStatsFieldnames())
                     writer.writeheader()
            with open(statscsv, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.getEpStatsFieldnames())
                writer.writerow(self.setStepStatsUsingVector(s))

    def processSaliency(self, saliency, runFolder):
        for f, s in zip(self.firemen, saliency):
            x, y = f.getXY()
            tmp = np.copy(self.global_observation)
            h = len(self.global_observation[0]) 
            w = len(self.global_observation[1]) 
            x_start=x-self.c.AHEAD_VIEW
            y_start=y-self.c.AHEAD_VIEW
            x_end = x_start+s.shape[1]
            y_end = y_start+s.shape[0]
            for i in range(y_start, y_start+s.shape[0]):
                for j in range(x_start, x_start+s.shape[1]):
                    tmp[i%h][j%w] = s[i-y_start][j-x_start] 
            r=16
            ep = self.episode_count
            diff = abs(tmp-self.global_observation)
            folder = runFolder + str(ep)+ "_"+str(f.fireman_id)
            statscsv = folder + '/ep_stats.csv'
            if not os.path.exists(folder):
                 os.mkdir(folder)
                 with open(statscsv, 'w') as csvfile:
                     writer = csv.DictWriter(csvfile, fieldnames=self.getEpStatsFieldnames())
                     writer.writeheader()
            if self.eval == 0:
                imsave(folder + "/" + str(self.steps) + ".png", np.repeat(np.repeat(self.global_observation+(diff*50), r, axis=0), r, axis=1).astype(np.uint8))
                #imsave(folder + "/diff" + str(self.steps) + ".png", np.repeat(np.repeat(diff, r, axis=0), r, axis=1).astype(np.uint8))
            with open(statscsv, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.getEpStatsFieldnames())
                writer.writerow(self.setStepStats(diff))

    def setStepStatsUsingVector(self, v):
        d = {}
        d.update({'eval':self.eval})
        vCount = 0 
        for i in range(len(self.firemen)):
            x, y = self.firemen[i].getXY()
            d.update({'A'+str(i)+'_saliency':v[vCount]})
            d.update({'A'+str(i)+'_x':x})
            d.update({'A'+str(i)+'_y':y})
            d.update({'A'+str(i)+'_fes':self.firemen[i].getFESteps()})
            d.update({'A'+str(i)+'_fbs':self.firemen[i].getFBSteps()})
            d.update({'A'+str(i)+'_exs':self.firemen[i].getEXSteps()})
            d.update({'A'+str(i)+'_fire_id':self.firemen[i].fire_id})
            vCount += 1
        for i in range(self.c.CIVILIANS):
            x, y = self.civilians[i].getXY()
            d.update({'C'+str(i)+'_xy_saliency':v[vCount]})
            d.update({'C'+str(i)+'_x':x})
            d.update({'C'+str(i)+'_y':y})
            vCount += 1
        for tool, x, y in self.c.PICKUP_LOCATIONS:
            d.update({str(tool) + '_' + str(x) + '_' + str(y) + '_saliency':v[vCount]})
            vCount += 1
        for _, fire in self.fires.items():
            x, y = fire.getXY()
            d.update({'fire_' + str(x) + '_' + str(y) + '_saliency':v[vCount]})
            vCount += 1
        return d

    def setStepStats(self, diff):
        d = {}
        d.update({'eval':self.eval})
        for i in range(len(self.firemen)):
            x, y = self.firemen[i].getXY()
            d.update({'A'+str(i)+'_saliency':diff[y][x][0]})
            d.update({'A'+str(i)+'_x':x})
            d.update({'A'+str(i)+'_y':y})
            d.update({'A'+str(i)+'_fes':self.firemen[i].getFESteps()})
            d.update({'A'+str(i)+'_fbs':self.firemen[i].getFBSteps()})
            d.update({'A'+str(i)+'_exs':self.firemen[i].getEXSteps()})
            d.update({'A'+str(i)+'_fire_id':self.firemen[i].fire_id})
        for i in range(self.c.CIVILIANS):
            x, y = self.civilians[i].getXY()
            d.update({'C'+str(i)+'_xy_saliency':diff[y][x][0]})
            d.update({'C'+str(i)+'_x':x})
            d.update({'C'+str(i)+'_y':y})
        for tool, x, y in self.c.PICKUP_LOCATIONS:
            d.update({str(tool) + '_' + str(x) + '_' + str(y) + '_saliency':diff[y][x][0]})
        for _, fire in self.fires.items():
            x, y = fire.getXY()
            d.update({'fire_' + str(x) + '_' + str(y) + '_saliency':diff[y][x][0]})
        return d


    def initFires(self):
        '''
        Creates a dict, to which fires are added.
        '''
        self.fires = {}
        xlist = []
        ylist = []
        for i in range(len(self.firemen)/2):
            if self.c.FIRE_X == None and self.c.FIRE_Y == None:
                while True:
                    x = random.randrange(self.c.HMP-4, self.c.HMP+4, 2)
                    y = random.randrange(self.c.VMP-4, self.c.VMP+4, 2)
                    key = str(x)+"_"+str(y) 
                    if (len(xlist) == 0) or (abs(xlist[0]-x) > 2 and y not in ylist):
                        xlist.append(x)
                        ylist.append(y)
                        break
            else:
                x = self.c.FIRE_X() 
                y = self.c.FIRE_Y()
                key = str(x)+"_"+str(y) 
            self.fires.update({key:Fire(x,y,self.rewardMode, self.colors.FIRE)})
             
    def initAgents(self):
        '''
        Method for initialising the required number of firemen and 
        positionsing them on designated positions within the grid 
        '''
        map(lambda fireman: fireman.reset(), self.firemen) 

    def initCivilians(self):
        '''
        Method for initialising the required number of civilians and 
        positionsing them on designated positions within the grid 
        '''
        map(lambda civilians: civilians.reset(), self.civilians) 

    def initPickupLocations(self):
        '''
        Method for initialising the pickup locations
        '''  
        self.plocations = []
        for tool, x, y in self.c.PICKUP_LOCATIONS:
            self.plocations.append(Pickuparea(self.createTool[tool](), x, y))

    def newCharge(self):
        '''
        :return tool: new charge object
        '''
        return Charge(self.colors.CHARGE)

    def newFireBlanket(self):
        '''
        :return tool: new fire blanket object
        '''
        return Fire_Blanket(self.colors.FIRE_BLANKET)

    def newFireExstinguisher(self):
        '''
        :return tool: new fire blanket object
        '''
        return Fire_Exstinguisher(self.colors.FIRE_EXSTINGUISHER)

    def setObstacles(self):
        '''
        Method used to initiate the obstacles within the environment 
        '''
        self.s_t = np.zeros((self.c.GH, self.c.GW, self.c.CHANNELS), dtype=np.float32)
        self.s_t_reduced = np.zeros((self.c.GH, self.c.GW, self.c.CHANNELS), dtype=np.float32)
        for y, x in self.c.OBSTACLES_YX:
            self.s_t[y][x] = self.colors.OBSTACLE

    def evalReset(self, evalType):
        '''
        Eval Reset. 
        :param int: typer of eval to take place
        '''
        self.reset()
        self.eval = evalType
        if evalType == 1:
            self.firemen[0].x = self.c.GW-2
            self.firemen[1].x = 1
        elif evalType == 2:
            self.firemen[0].useTool('charge')
        elif evalType == 3:
            self.firemen[0].useTool('fire_exstinguisher')
        elif evalType == 4:
            self.firemen[0].useTool('fire_blanket')
        elif evalType == 5:
            self.firemen[1].useTool('charge')
        elif evalType == 6:
            self.firemen[1].useTool('fire_exstinguisher')
        elif evalType == 7:
            self.firemen[1].useTool('fire_blanket')
        elif evalType == 8:
            self.firemen[0].x = self.c.HMP-2
            self.firemen[0].y = 3
        elif evalType == 9:
            self.firemen[1].x = self.c.HMP-2
            self.firemen[1].y = 3

        # Method is called to render the state,
        # which is subsequently passed to the agents.
        # Can also be viewed for debugging.
        self.renderState()
        return self.getObservations()

    def reset(self):
        '''
        Reset everything. 
        '''
        # Obstacles, agents and goods are initialised:
        self.setObstacles()
        self.initPickupLocations()
        self.initAgents()
        self.initCivilians()
        self.initFires()
        self.episode_count += 1
        self.eval = 0
        # Used to keep track of the reward total acheived throughout 
        # the episode:
        self.reward_total = 0.0
        self.terminal_rewards = {} 

        # For statistical purposes:
        # Step counter for the episode is initialised
        self.steps = 0 

        # Method is called to render the state,
        # which is subsequently passed to the agents.
        # Can also be viewed for debugging.
        self.renderState()
        
        for f in self.firemen:
            f.resetTool()

        return self.getObservations()

    def terminal(self):
        '''
        Find out if terminal conditions have been reached.
        '''
        return not self.getRoomTemperature() > 0.0

    def step(self, actions):

        # Civilians change location:
        self.moveCivilians()
            
        # Agents move according to actions selected
        self.moveAgents(actions)

        # New state is rendered
        self.renderState()
             
        # Observations are loaded for each agent
        observations, reduced_observations = self.getObservations()

        # Fires are updated based on agent locations
        rewards = self.updateFires()
        for f, r in zip(self.firemen, rewards):
            f.reward += r
        self.reward_total += sum(rewards)    

        # Tool pickup checks to see if the agents have
        # reached a position where they can grasp the tool.                    
        self.toolPickup()

        # Counters are incremented:
        self.steps += 1 
         
        strategies = []
        for f in self.firemen:
            strategies.append(f.getLastToolID())
        return observations, rewards, self.terminal(), strategies, reduced_observations

    def stats(self):
        stats = { 'Episode': str(self.episode_count), 
                  'Steps':str(self.steps),
                  'Eval':str(self.eval),
                  'Total_Reward': str(self.reward_total) }

        for f in self.firemen:
            stats.update({str(f.getID())+'fes':f.getFESteps()})
            stats.update({str(f.getID())+'fbs':f.getFBSteps()})
            stats.update({str(f.getID())+'exs':f.getEXSteps()})
            stats.update({str(f.getID())+'_reward':f.reward})
            stats.update({str(f.getID())+'_fire_id':f.fire_id})
        return stats
   
    def getObservation(self, x, y, currentColor, final=0, reduced=False):
        '''
	Method extracts centered observation 
        from the state space s_t, which is in 
        hwc format. 
        :param int x: agent's x coordinate
        :param int y: agent's y coordinate
        :param int h: agent's heading
	:return: local observation of s_t
	:rtype: numpy array
	'''
	# Offset is added after making the state space
	# s_t toroidal
        o = self.c.OFFSET
        os_x = x + o # offset_x
        os_y = y + o # offset_y
        x1 = os_x - o
        x2 = os_x + o+1
        y1 = os_y - o
        y2 = os_y + o+1
        if reduced:
            return np.copy(self.reduced_toroidal_s_t[y1:y2, x1:x2])
        else:
            return np.copy(self.toroidal_s_t[y1:y2, x1:x2])

    def saveStateImage(self, img, name='outfile.jpg', r=8):
        '''
        Method can be used to save a np array as a padded image.
        :param np.array img: contains image to be saved
        :param string name: name of file to be saved
        :param padding: number of times pixels are to be repeated
        '''
        imsave(name, np.repeat(np.repeat(img, r, axis=0), r, axis=1))

    def render(self):
        '''
        Used to render the env.
        '''
        r = 16
        try:
            img = np.repeat(np.repeat(self.global_observation, r, axis=0), r, axis=1).astype(np.uint8)
            cv2.imshow('image', img)
            k = cv2.waitKey(1)
            if k == 27:         # If escape was pressed exit
                cv2.destroyAllWindows()
        except AttributeError:
            pass

    def renderState(self):
        '''
        Method is used to render the current state.
        The end product is an upated representation,
        which is stored in self.toroidal_s_t.
        '''
        # List used to keep track of x, y coordinates 
        # that have been modified. The list can 
        # sub-sequencly be used to set the respective
        # coordinates back to 0 for the next time step.
        yx_list = [] 
        # Render fires
        for _, fire in self.fires.items():
            x, y = fire.getXY()
            yx_list.append((y, x))
            self.s_t[y][x] = fire.getColor()
            self.s_t_reduced[y][x] = fire.getColor()
        # Render pickup locations
        for p in self.plocations:
            x, y = p.getXY()
            yx_list.append((y, x))
            self.s_t[y][x] = p.getColor()
        # Render civilians
        for c in self.civilians:
            x, y = c.getXY()
            yx_list.append((y, x))
            self.s_t[y][x] = c.getColor() 
        # Render agents
        for f in self.firemen:
            x, y = f.getXY()
            yx_list.append((y, x))
            if self.s_t[y][x].sum() > 0.0:
                self.s_t[y][x] += f.getColor() 
                self.s_t[y][x] = self.s_t[y][x] / 2
                self.s_t_reduced[y][x] += f.getColor()
                self.s_t_reduced[y][x] = self.s_t_reduced[y][x] / 2
            else:
                self.s_t[y][x] = f.getColor() 
                self.s_t_reduced[y][x] = f.getColor()

        # If debug is true, or if display scren time step
        # has occured:
        #if envconfig.DEBUG == True or self.episode_count%envconfig.OUTPUT_STEPS == 0:
        #self.saveStateImage(self.s_t, name='outfile.jpg') #+ str(self.steps) + '.jpg')
 
        # For when agents use global observations:
        self.global_observation = np.copy(self.s_t)

	# The agent observations are toroidal:
        #self.toroidal_s_t = np.pad(self.s_t, ((self.c.OFFSET, self.c.OFFSET), 
	#	           (self.c.OFFSET, self.c.OFFSET)), mode='wrap')
        #self.reduced_toroidal_s_t = np.pad(self.s_t_reduced, ((self.c.OFFSET, self.c.OFFSET), 
	#	           (self.c.OFFSET, self.c.OFFSET)), mode='wrap')

        # self.s_t is reset for next iteration
        #for i in range(len(yx_list)):
        #    self.s_t[yx_list[i][0]][yx_list[i][1]] = 0.0
        #    self.s_t_reduced[yx_list[i][0]][yx_list[i][1]] = 0.0

        # The agent observations are toroidal:
        self.toroidal_s_t = np.pad(self.s_t, ((self.c.OFFSET, self.c.OFFSET), 
		           (self.c.OFFSET, self.c.OFFSET),
			   (0,0)), mode='wrap')
        self.reduced_toroidal_s_t = np.pad(self.s_t_reduced, ((self.c.OFFSET, self.c.OFFSET), 
		           (self.c.OFFSET, self.c.OFFSET),
			   (0,0)), mode='wrap')

        # self.s_t is reset for next iteration
        for i in range(len(yx_list)):
            self.s_t[yx_list[i][0]][yx_list[i][1]] = [0.0, 0.0, 0.0]
            self.s_t_reduced[yx_list[i][0]][yx_list[i][1]] = [0.0, 0.0, 0.0]

    def moveCivilians(self):
        '''
        Each agent is allowed to perform one move.
        '''
        for c in self.civilians:
            x, y = c.getXY() # Get agents x, y coordinates
            cN = self.isOccupied(x, y+1) # Is occupied north 
            cS = self.isOccupied(x, y-1) # Is occupied south 
            cE = self.isOccupied(x+1, y) # Is occupied east 
            cW = self.isOccupied(x-1, y) # Is occupied west 
            c.move(cN, cS, cE, cW)

    def moveAgents(self, actions):
        '''
        Each agent is allowed to perform one move.
        '''
        for f, a in zip(self.firemen, actions):
            if f.done == False:
                x, y = f.getXY() # Get agents x, y coordinates
                cN = self.isOccupied(x, y+1) # Is occupied north 
                cS = self.isOccupied(x, y-1) # Is occupied south 
                cE = self.isOccupied(x+1, y) # Is occupied east 
                cW = self.isOccupied(x-1, y) # Is occupied west 
                f.move(a, cN, cS, cE, cW)

    def getObservations(self):
        '''
        Returns centered observation for each agent
        '''
        observations = []
        reduced_observations = []
        for f in self.firemen:
            x, y = f.getXY() # Get agents x, y coordinates
            observations.append(self.getObservation(x, y, f.getColor()))
            reduced_observations.append(self.getObservation(x, y, f.getColor(), reduced=True))

        return observations, reduced_observations

    def isOccupied(self, x, y):
        '''
        Method verifies is grid coordinate is obstacle free
        :return bool: True if obstacle is at grid location
        '''
        if self.accesspoints == 1 and (x, y) == self.c.OVERLAP_XY:
            return False
        key = str(x)+"_"+str(y) 
        for c in self.civilians:
            if (x, y) == c.getXY(): 
                return True
        for f in self.firemen:
            if (x, y) == f.getXY(): 
                return True
        if key in self.fires \
           and self.fires[key].getTemperature() > 0.0: # Check if fire is at location
            return True
        else:
            return np.array_equal(self.s_t[y%self.c.GH][x%self.c.GW], self.colors.OBSTACLE)

    def toolPickup(self):
        '''
        Method for picking up a tool, if the agent
        find themselves in positions adjecent to a tool. 
        '''
        for f in self.firemen:
            if f.holdingTool() == False:
                location = f.getXY()
                for p in self.plocations:
                    if location == p.getXY(): # If agent is at pickup location
                        f.useTool(p.getToolName())

    def getRoomTemperature(self):
        '''
        :return float: Room temperature based on fires
        '''
        temperature = 0.0
        for _, fire in self.fires.items():
            temperature += fire.getStatus()
        return temperature 

    def updateFires(self):
        '''
        Fire manager
        '''
        plusX = [0, 1, 0, -1]
        plusY = [1, 0, -1, 0]
        feedback = []
        # Find out if two (or more) agents are facing 
        # towards identical coordinates
        facingDict = {} # Stores number of agents facing coordinates
        for i in range(len(self.firemen)):
            feedback.append(0.0)
            x, y = self.firemen[i].getXY()
            
            # Find out which cell the agent is facing:
            if self.firemen[i].holdingTool() == True:
                for j in range(4):
                    key = str(x+plusX[j])+"_"+str(y+plusY[j])
                    if key in facingDict:
                        facingDict[key].append(i)
                    else:
                        facingDict.update({key:[i]})

        for key, agentIDs in facingDict.iteritems():
            if key in self.fires and self.fires[key].getTemperature() > 0.0:
                for i in agentIDs[:2]:
                    self.firemen[i].setFacingFire()
                if len(agentIDs) == 2:
                    for i in agentIDs:
                        print(self.firemen[i].getXY())
                    tools = []
                    for i in agentIDs[:2]:
                        tools.append(self.firemen[i].getToolName())
                    r = self.fires[key].coolDown(tools)
                    for i in agentIDs:
                        feedback[i] = r
                        self.firemen[i].fire_id = key
        return feedback     

