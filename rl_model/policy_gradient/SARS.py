from xml.dom import minidom

import numpy as np
import reward
from action import PhaseModifier
from dtse import DTSE_Generator
from policy_network import PolicyNetwork
from simulation import SimulationComponent


class StateAction(SimulationComponent):

    def __init__(self, simulation):

        self._simulation = simulation
        self._roads_list = [["-road1_0", "road3_0"], ["road2_0", "road4_0"]]
        self._node = "node1"
        self._states = []
        self._current_state = 0
        self._actions = []
        self._modifier = PhaseModifier(self._node)

    def tick(self):

        state = self.get_state()
        self._states.append(state)
        self.act()
        pass

    def post_run(self):
        results = {"states": [], "actions": [], "rewards": []}
        results["states"].append(self._states)
        results["actions"].append(self._actions)
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

    def act(self):

        output,output_softmax = PolicyNetwork.get_output(self._current_state.reshape(1,120))

        action = np.random.choice(range(len(output_softmax.ravel())), p=output_softmax.ravel())

        if(action == 0):
            self._modifier.set_phase(0)
        else:
            self._modifier.set_phase(4)

        one_hot_action = np.zeros(2)
        one_hot_action[action] = 1
        self._actions.append(one_hot_action)
        pass

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

