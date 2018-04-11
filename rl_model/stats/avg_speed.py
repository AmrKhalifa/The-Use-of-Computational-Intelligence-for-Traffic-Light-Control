from simulation import SimulationComponent
import matplotlib.pyplot as plt
import traci

class OverallAverageSpeedRecorder(SimulationComponent):
    def __init__(self):
        self._speeds = []

    def tick(self):
        avg = 0
        for veh_id in traci.simulation.getDepartedIDList():
            traci.vehicle.subscribe(veh_id, [traci.constants.VAR_SPEED])
        velocities = traci.vehicle.getSubscriptionResults()
        for i in velocities.values():
            avg += i[traci.constants.VAR_SPEED]
        avg/=traci.vehicle.getIDCount()
        self._speeds.append(avg)


    def post_run(self):
        plt.plot(self._speeds)
        #plt.show()