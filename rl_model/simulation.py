import traci
import time
import pickle
import abc

class Simulator:
    def __init__(self):
        self._tickables = []
        self._post_run_funcs = []
        self._sim_components = []
        self._tick_freq = {}
        self._sim_step = 0
        self.results = {}
        self.output_file = "tripinfo.xml"
    def tick(self):
        traci.simulationStep()
        for tickable in self._tickables:
            if self._sim_step % self._tick_freq[tickable] == 0:
                tickable.tick()
        for component in self._sim_components:
            if self._sim_step % self._tick_freq[component] == 0:
                component.tick()
        self._sim_step += 1

    def run(self, path_to_cfg, time_steps="run_to_completion" ,gui=False):
        start_time = time.time()
        if gui:
            sumoBinary = "sumo-gui"
        else:
            sumoBinary = "sumo"
        sumoCmd = [sumoBinary, "-c"]
        sumoCmd.append(path_to_cfg)
        sumoCmd.append("--tripinfo-output")
        sumoCmd.append(self.output_file)


        traci.start(sumoCmd)
        if time_steps == "run_to_completion":
            while traci.simulation.getMinExpectedNumber() > 0 :
                self.tick()
        else:
            while self._sim_step < time_steps and traci.simulation.getMinExpectedNumber() > 0:
                self.tick()
        traci.close()
        for func in self._post_run_funcs:
            func()
        for component in self._sim_components:
            component.post_run()
        print("Runtime: %.3f"%(time.time()-start_time))


    def add_tickable(self, tickable, freq=1):
        self._tickables.append(tickable)
        self._tick_freq[tickable] = freq

    def add_postrun(self, func):
        self._post_run_funcs.append(func)

    def add_simulation_component(self, Component, freq=1, *args, **kwargs):
        component = Component(self, *args, **kwargs)
        self._sim_components.append(component)
        self._tick_freq[component] = freq

    def save_results(self, filename):
        file_io = open(filename + ".pkl", 'wb')
        results = pickle.dump(self.results, file_io)
        file_io.close()

class Tickable:
    @abc.abstractmethod
    def tick(self):
        pass


class SimulationComponent(Tickable):
    @abc.abstractmethod
    def post_run(self):
        pass