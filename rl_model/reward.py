import traci
EPS = 0.1

class RewardCalculator:
    def __init__(self):
        self.vehicles = {}

    def tick(self):
        current_vehicle_ids = traci.vehicle.getIDList()
        old_vehicle = list(self.vehicles.keys())
        for vehID in old_vehicle:
            if vehID not in current_vehicle_ids:
                # vehile has departed simulation, remove entry from vehicle dictionary
                self.vehicles.pop(vehID)
        for vehID in current_vehicle_ids:
            if vehID not in self.vehicles.keys():
                self.vehicles[vehID] = 0
        for vehID in traci.simulation.getDepartedIDList():
            traci.vehicle.subscribe(vehID, [traci.constants.VAR_SPEED])
        subscription_results = traci.vehicle.getSubscriptionResults()
        for vehID in current_vehicle_ids:
            speed = subscription_results[vehID][traci.constants.VAR_SPEED]
            if speed < EPS:
                self.vehicles[vehID] += 1
            else:
                self.vehicles[vehID] = 0

    def get_reward(self):
        alpha = 0.5
        avg_speed = 0
        n_cars = 0
        for vehID in traci.vehicle.getIDList():
            avg_speed += traci.vehicle.getSpeed(vehID)
            n_cars += 1
        avg_speed /= n_cars
        delay_penalty = float(sum(self.vehicles.values()))/n_cars
        return avg_speed - alpha*delay_penalty