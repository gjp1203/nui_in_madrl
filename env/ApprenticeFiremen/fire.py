from rewards import Rewards
class Fire:
    """ Can be used to create fire instance at a specified x, y coordinate """

    def __init__(self,x,y, rewardMode, color):
        '''
        :param int x: x coordinate
        :param int y: y coordinate
        :param string: reward mode (deterministic, partially or fully stochastic)
        :param vector: RGB color code for fire
        '''
        self.x = x
	self.y = y
	self.ignite()
        self.rewards = Rewards(rewardMode)
        self.color = color

    def ignite(self):
        '''
        Sets temperature to max value
        '''
	self.temperature = 1.0

    def getXY(self):
        '''
        :return int self.x: x coordinate
        :return int self.y: y coordinate
        '''
        return self.x, self.y

    def reset(self):
        '''
        Used to reset fire temperatures
        '''
	self.temperature = 1.0

    def getTemperature(self):
        '''
        :return float: Fire temperature
        '''
	return self.temperature

    def getStatus(self):
        '''
        :return float indicating if fire is on or off
        '''
	return 1.0 if self.temperature == 1.0 else 0.0

    def coolDown(self, tools):
        '''
        Regulated temperature cooling
        :param float effectiveness: determines cooling speed
        :return float: reward for actions taken
        :return bool: Indicates uncontrolled explosion
        '''
        c = tools.count("charge")
        fb = tools.count("fire_blanket")
        fe = tools.count("fire_exstinguisher")
        self.temperature = 0.0
        if c == 2:
            print(str(len(tools)) + " charge")
            return self.rewards.r['ce_ce']()
        elif c > 0 and c + fb != 2:          
            print("Charge plus non-fb")
            return self.rewards.r['c_nfb']()
        elif c > 0 and c + fb == 2:
            print("charge plus fb")
            return self.rewards.r['ce_fb']()
        elif fe == 2:
            print(str(len(tools)) + " fe")
            return self.rewards.r['fe_fe']()
        elif tools[0] == 'fire_exstinguisher' and fb > 0:
            print("fe and fb")
            return self.rewards.r['fe_fb']()
        elif fb == 2:
            print(str(len(tools)) + " fb")
            return self.rewards.r['fb_fb']()
        else:
            return self.rewards.r['fb_fe']()

    def getColor(self):
        '''
        :return list int: rgb values based on fire status
        '''
        return self.color
