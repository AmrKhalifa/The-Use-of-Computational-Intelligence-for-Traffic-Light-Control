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
        for lane,direction in zip(("-road1_0", "road2_0", "road3_0", "road4_0"), ("in", "in", "in", "in")):
            a, b = dtse.DTSE_Generator.get_traffic_state(lane, direction, 15, 7.5)
            a, b = np.asarray(a), np.asarray(b)
            state = np.hstack((state, a.ravel(), b.ravel()))
        phase = dtse.DTSE_Generator.get_traffic_light_phase()

        state = np.hstack((state))
        return state

class Controller:
    def __init__(self, phase_modifier):
        self._phase_modifier = phase_modifier
        self._ticks_since_changed = 0

    def do_action(self, action):
        self._phase_modifier
        self._phase_modifier.set_phase(action)

    def tick(self):
        self._ticks_since_changed += 1


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
    class X:
        def __init__(self,s):
            self.x = 0
            self.s = s

        def tick(self):
            s.get_state()

    sim = Simulator()
    rc = RewardCalculator()
    sim.add_tickable(rc)
    c = Controller(PhaseModifier("node1"))
    s = StateGenerator()
    agent = RLAgent(rc,s,c,[0,3,4])
    sim.add_tickable(X(s))
    sumocfg = "..\\..\\test_environments\\single_intersection_map\\newnet.sumocfg"
    sim.run(sumocfg, time_steps=1000, gui=True)

