from simulation import SimulationComponent
import matplotlib.pyplot as plt
import traci
from utils.tripinfo import XMLDataExtractor

class OverallMeanJourneyTimeRecorder(SimulationComponent):
    def __init__(self):
       self.mean_journey_time =0

    def tick(self):
        pass
      
    def post_run(self):

        self.mean_journey_time = XMLDataExtractor("D:/My study/5th year/Graduation Project/traffic-optimization/rl_model/tripinfo.xml").get_data()
        print("*="*10)
        print("the mean Journey time is: ", self.mean_journey_time)
        pass
