from reward import RewardCalculator
from simulation import Simulator
from action import PhaseModifier
import numpy as np
import dtse

class ActionRepresentation:
    def __init__(self, actions):
        self._eye = np.eye(len(actions))
        self._indices = dict(zip(actions, range(len(actions))))
        self._action_numbers = actions

    def get_one_hot(self, action_number):
        return self._eye[self._indices[action_number]]

    def get_phase_number(self, one_hot_vec):
        hot = np.argmax(one_hot_vec)
        return self._action_numbers[hot]

    def get_phases(self):
        return self._action_numbers

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
        state = np.hstack((state))
        return state

class Controller:
    def __init__(self, phase_modifier, action_reprentation_handler):
        self._phase_modifier = phase_modifier
        self._ticks_since_changed = 0
        self._action_representation = action_reprentation_handler
        self._current_phase = action_reprentation_handler.get_phases()[0]

    def do_action(self, action):
        self._current_phase = self._action_representation.get_phase_number(action)
        self._phase_modifier.set_phase(self._current_phase)

    def tick(self):
        self._phase_modifier.set_phase(self._current_phase)
        self._ticks_since_changed += 1

    def reset(self):
        self._current_phase = self._action_representation.get_phases()[0]
        self._ticks_since_changed = 0

class RLAgent:
    def __init__(self, reward_calc, state, controller, actions):
        self._reward_calc = reward_calc
        self._state_calc = state
        self._controller = controller
        self._actions = actions
        self._previous_state = None
        self._previous_action = None

    def tick(self):
        state = self._state_calc.get_state()[np.newaxis, :]
        reward = self._reward_calc.get_reward()
        if self._previous_state is not None:
            self._update_model(self._previous_state, self._previous_action, reward, state)
        action = self._select_action(state)
        self._controller.do_action(action)
        self._previous_action = action
        self._previous_state = state

    def reset(self):
        self._previous_state = None
        self._previous_action = None

    def _select_action(self, state):
        pass
    
    def _update_model(self, state, action, reward, new_state):
        pass


if __name__ == "__main__":

    sim = Simulator()
    rc = RewardCalculator()
    sim.add_tickable(rc)

    action_translator = ActionRepresentation([0,3,4])
    controller = Controller(PhaseModifier("node1"), action_translator)
    sim.add_tickable(controller)
    state_gen = StateGenerator()
    agent = RLAgent(rc,state_gen,controller,[0,3,4])
    sumocfg = "..\\..\\test_environments\\single_intersection_map\\newnet.sumocfg"
    sim.run(sumocfg, time_steps=3000, gui=False)

