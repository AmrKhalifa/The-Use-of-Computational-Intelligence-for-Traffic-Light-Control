from xml.dom import minidom

import numpy as np
import reward
from action import PhaseModifier
from dtse import DTSE_Generator
from simulation import SimulationComponent


class StateObserver(SimulationComponent):

    def __init__(self, simulation):

        self._simulation = simulation
        self._roads_list = [["-road1_0", "road3_0"], ["road2_0", "road4_0"]]
        self._node = "node1"
        self._states = []
        self._current_state = 0
        self._modifier = PhaseModifier(self._node)

    def tick(self):
        print("state has been observed, and the state is: ")
        state = self.get_state()
        print(self._current_state)
        print("...")
        self._states.append(state)
        pass

    def post_run(self):
        results = {"states": [], "actions": [], "rewards": []}
        results["states"].append(self._states)
        self._simulation.results = results
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

        state = np.concatenate([exist_1,exist_2,exist_3,exist_4,speed_1,speed_2,speed_3,speed_4])
        self._current_state = state
        return state


class RewardCollector:
    def __init__(self,reward_calculator):
        self._reward_calculator = reward_calculator
        self._reward_log = []
        pass

    def tick(self):
        self._reward_log.append(self._reward_calculator.get_reward())
        pass

    def get_reward_log(self):
        return self._reward_log 

class Actor:
    def __init__(self,StateObserver,network):
        self._network = network
        self._actions_list = []
        self._StateObserver = StateObserver

        pass

    def tick(self):
        # act
        #network.get_action(self._StateObserver._current_state)
        print("<<< am acting >>>")
        print("the state is: ")
        print(self._StateObserver._current_state)
        print("done")
        # save to the list
        pass

    def get_actions_list(self):
        return self._actions_list
        pass