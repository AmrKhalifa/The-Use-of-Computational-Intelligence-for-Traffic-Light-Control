from rl import RLAgent, StateGenerator, Controller
from reward import RewardCalculator
from simulation import Simulator
from action import PhaseModifier


class SingleIntersectQAgent (RLAgent):
    def __init__(self, reward_calc, state, controller, actions):
        super().__init__(reward_calc, state, controller, actions)
        import itertools
        self._phases = itertools.cycle([0]*30 + [4]*30)

    def _select_action(self, state):
        return next(self._phases)

if __name__ == "__main__":
    class X:
        def __init__(self,s):
            self.x = 0
            self.s = s

        def tick(self):
            x = int(input("Enter a phase :"))
            self.s.do_action(x)

    sim = Simulator()
    rc = RewardCalculator()
    sim.add_tickable(rc)
    c = Controller(PhaseModifier("node1"))
    s = StateGenerator()
    agent = SingleIntersectQAgent(rc,s,c,[0,3,4])
    sim.add_tickable(agent)
    sim.add_tickable(X(c))
    sumocfg = "..\\..\\test_environments\\single_intersection_map\\newnet.sumocfg"
    sim.run(sumocfg, time_steps=1000, gui=True)

