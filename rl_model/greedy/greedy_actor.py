from stats import SimulationOutputParser
from dtse import DTSE_Generator
from simulation import Tickable
import numpy as np
from action import PhaseModifier
import random

class LongestQueueFirst(Tickable):
    def __init__(self,node,roads_list):
        self._roads_list = roads_list
        self._node = node
        pass


    def get_state(self):

        phase_1 = self._roads_list[0]
        phase_2 = self._roads_list[1]

        exist_1 = []
        exist_2 = []
        exist_3 = []
        exist_4 = []

        exist_1, speed_1 = DTSE_Generator.get_traffic_state(phase_1[0], direction="in", state_size=15, cell_size=7)
        exist_2, speed_2 = DTSE_Generator.get_traffic_state(phase_1[1], direction="in", state_size=15, cell_size=7)

        for road in phase_2:

            exist_3,speed_3 = DTSE_Generator.get_traffic_state(phase_2 [0], direction="in",state_size=15,cell_size =7)
            exist_4, speed_4 = DTSE_Generator.get_traffic_state(phase_2[1], direction="in", state_size=15, cell_size=7)

        #queue_1 = np.count_nonzero(exist_1) + np.count_nonzero(exist_2)
        #queue_2 = np.count_nonzero(exist_3) + np.count_nonzero(exist_4)

        queue_1 = self.count_queue_length(exist_1, exist_2)
        queue_2 = self.count_queue_length(exist_3, exist_4)


        return queue_1,queue_2
        pass


    def act(self):
        pass

    def tick(self):
        # call get state
        q_1,q_2 = self.get_state()
        modifier = PhaseModifier(self._node)
        if(q_1>q_2):
            modifier.set_phase(4)
        elif(q_1<q_2):
            modifier.set_phase(0)
        else:
            if(bool(random.randint(0,1))):
                modifier.set_phase(0)
            else:
                modifier.set_phase(4)
        # call act upon the result
        pass

    def post_run(self):
        pass

    def count_queue_length(self,road_1,road_2):
        counter =0
        for i in range (len(road_1)):
            if road_1[i]==1:
                counter +=1
            else:
                break

        for i in range (len(road_2)):
            if road_1[i]==2:
                counter +=1

        return counter