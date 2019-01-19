from simulation import SimulationComponent
from xml.dom import minidom
import numpy as np

class SimulationOutputParser (SimulationComponent):
    def __init__(self, simulation):
        self.mean_journey_time =0
        self._simulation = simulation

    def tick(self):
        pass
      
    def post_run(self):
        results = {"mean_speed":[], "duration":[], "waiting_time":[], "time_loss":[]}
        xmldoc = minidom.parse(self._simulation.output_file)
        tripinfo_list = xmldoc.getElementsByTagName("tripinfo")
        for entry in tripinfo_list:
            duration = float(entry.getAttribute("duration"))
            mean_speed = float(entry.getAttribute("routeLength"))/duration
            results["mean_speed"].append(mean_speed)
            results["duration"].append(duration)
            results["waiting_time"].append(float(entry.getAttribute("waitSteps")))
            results["time_loss"].append(float(entry.getAttribute("timeLoss")))

        for category, values in results.items():
            self._simulation.results [category] = np.array(values)
