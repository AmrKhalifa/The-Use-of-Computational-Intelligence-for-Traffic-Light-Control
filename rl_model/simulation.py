import traci


class Simulator:
    def __init__(self):
        self._tickables = []
        self._post_run_funcs = []
        self._sim_components = []
        self._tick_freq = {}
        self._sim_step = 0

    def tick(self):
        traci.simulationStep()
        for tickable in self._tickables:
            if self._sim_step % self._tick_freq[tickable] == 0:
                tickable.tick()
        for component in self._sim_components:
            if self._sim_step % self._tick_freq[component]:
                component.tick()
        self._sim_step += 1

    def run(self, path_to_cfg, time_steps ,gui=False):
        if gui:
            sumoBinary = "sumo-gui"
        else:
            sumoBinary = "sumo"
        sumoCmd = [sumoBinary, "-c"]
        sumoCmd.append(path_to_cfg)
        traci.start(sumoCmd)
        while self._sim_step < time_steps:
            self.tick()
        for func in self._post_run_funcs:
            func()
        for component in self._sim_components:
            component.post_run()
        traci.close()

    def add_tickable(self, tickable, freq=1):
        self._tickables.append(tickable)
        self._tick_freq[tickable] = freq

    def add_postrun(self, func):
        self._post_run_funcs.append(func)

    def add_simulation_component(self, Component, freq=1, *args, **kwargs):
        component = Component(*args, **kwargs)
        self._sim_components.append(component)
        self._tick_freq[component] = freq