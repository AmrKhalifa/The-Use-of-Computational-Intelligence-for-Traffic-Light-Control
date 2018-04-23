from reward import RewardCalculator
from simulation import Simulator
from action import PhaseModifier
import numpy as np
import dtse

class StateGenerator:
    def __init__(self):
        pass

    def get_state(self):
        # TODO add traffic light phase to state
        state = np.array(())
        for lane in ("-road1_0", "road2_0", "road3_0", "road4_0"):
            a, b = dtse.DTSE_Generator.get_traffic_state("-road4_0", "out", 15, 5)
            a, b = np.asarray(a), np.asarray(b)
            state = np.hstack((state, a.ravel(), b.ravel()))
        return state

class Controller:
    def __init__(self, phase_modifier):
        self._phase_modifier = phase_modifier

    def do_action(self, action):
        self._phase_modifier.set_phase(action)

class RLAgent:
    def __init__(self, reward_calc, state, controller, actions):
        self._reward_calc = reward_calc
        self._state_calc = state
        self._controller = controller
        self._actions = actions
        self._previous_state = None
        self._previous_action = None

    def tick(self):
        state = self._state_calc.get_state()
        reward = self._reward_calc.get_reward()
        if self._previous_state is not None:
            self._update_model(self._previous_state, self._previous_action, reward)
        action = self._select_action(state)
        self._controller.do_action(action)
        self._previous_action = action
        self._previous_state = state

    def _select_action(self, state):
        pass
    
    def _update_model(self, state, action, reward):
        pass


if __name__ == "__main__":
    sim = Simulator()
    rc = RewardCalculator()
    sim.add_tickable(rc)
    c = Controller(PhaseModifier("node1"))
    s = StateGenerator()
    agent = RLAgent(rc,s,c,[0,3,4])
    sim.add_tickable(agent)
    sumocfg = "..\\..\\test_environments\\single_intersection_map\\newnet.sumocfg"
    sim.run(sumocfg, time_steps=100, gui=True)

