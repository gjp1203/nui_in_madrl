import random

class Rewards:
    """ Rewards for tool combos """
    def __init__(self,mode):
        '''
        :param string: Reward mode (deterministic, partially or fully stochastic)
        '''
        if mode == 'DET':
           self.__r = self.detRewards() 
        elif mode == 'PS':
           self.__r = self.psRewards() 
        elif mode == 'FS':
           self.__r = self.fsRewards() 

    @property
    def r(self):
        return self.__r

    def detRewards(self):
        '''
        Returns deterministic rewards dict
        '''
        return {'ce_ce': lambda: 0.8, 
                'c_nfb': lambda: -1.0,
                'ce_fb': lambda: 0.0,
	        'fe_fe': lambda: 0.6,
	        'fe_fb': lambda: 0.5,
	        'fb_fb': lambda: 0.4,
	        'fb_fe': lambda: 0.0} 

    def psRewards(self):
        '''
        Returns partially stochastic rewards dict
        '''
        return {'ce_ce': lambda: 0.8, 
                'c_nfb': lambda: -1.0,
                'ce_fb': lambda: 0.0,
	        'fe_fe': lambda: 0.0 if random.uniform(0, 1) < 0.4 else 1.0,
	        'fe_fb': lambda: 0.5,
	        'fb_fb': lambda: 0.4,
	        'fb_fe': lambda: 0.0} 

    def fsRewards(self):
        '''
        Returns fully stochastic rewards dict
        '''
        return {'ce_ce': lambda: 0.7   if random.uniform(0, 1) < 0.5 else 0.9, 
                'c_nfb': lambda: 0.2   if random.uniform(0, 1) < 0.5 else -1.0,
                'ce_fb': lambda: -0.6  if random.uniform(0, 1) < 0.5 else 0.6,
	        'fe_fe': lambda: 0.0   if random.uniform(0, 1) < 0.4 else 1.0,
	        'fe_fb': lambda: 0.1   if random.uniform(0, 1) < 0.5 else 0.9,
	        'fb_fb': lambda: 0.0   if random.uniform(0, 1) < 0.5 else 0.8,
	        'fb_fe': lambda: -0.4  if random.uniform(0, 1) < 0.5 else 0.4}


