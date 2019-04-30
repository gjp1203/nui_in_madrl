from collections import deque
import random as random
import numpy as np

class FIFO(object):
    '''Episodic fifo stores whole episodes innside a 
       first-in first-out queue data structure.'''

    def __init__(self, c):
        '''
        Class is instantiated with a queue data
        structure for storing the episodes, and
        a list for storing the transitions of 
        the current episode. 
        :param config: Replay Memory Hyperparameters
        '''
        self.c = c
        self._transitions = deque([], c.erm.size)
        self._batch_size = c.erm.batch_size
        self._size = c.erm.size
        self._num_transitions_stored = 0
        self._learning_threshold = c.erm.threshold
        
    def getSize(self):
        ''' 
        Returns the number of transitions currently
        stored inside the list. 
        '''
        return len(self._transitions)

    def add_experience(self, transition, meta_strategy=None):
        ''' 
        Method used to add state transitions to the replay memory. 
        :param transition: Tuple containing state transition tuple
        '''
        # Add transition to list:
        self._transitions.append(transition)

    def isFull(self):
        '''
        :return bool: True if RM is full, false otherwise
        '''
        return True if len(self._transitions) == self._size else False
            

    def get_mini_batch(self):
        '''
        Method returns a mini-batch of sample traces.
        :return list traces: List of traces
        '''
        return random.sample(self._transitions, self._batch_size)	

    def getUnzippedSamples(self):
        '''
        :return unzipped samples
        '''
        # Samples are obtained from the replay memory and unzipped
        samples = self.get_mini_batch()
        return zip(*samples)
