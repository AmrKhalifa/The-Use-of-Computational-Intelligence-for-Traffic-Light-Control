import traci
EPS = 0.1

class RewardCalculator:
    def __init__(self, alpha=0.5, log=True):
        self.vehicles = {}
        self._alpha = alpha
        self._is_logging = log
        self._log = []

    def tick(self):
        if self._alpha > 0:
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
        avg_speed = 0
        n_cars = 0
        for vehID in traci.vehicle.getIDList():
            avg_speed += traci.vehicle.getSpeed(vehID)
            n_cars += 1
        if n_cars == 0:
            avg_speed = 0
        else:
            avg_speed /= n_cars

        if abs(self._alpha ) < .000001:
            r = avg_speed
        else:
            if n_cars != 0:
                delay_penalty = float(sum(self.vehicles.values()))/n_cars
            else:
                delay_penalty = 0
            r =  avg_speed - self._alpha*delay_penalty

        if self._is_logging:
            self._log.append(r)
        return r

    def get_log(self):
        if not self._is_logging:
            raise Exception("Loggging is not turned on")
        return self._log

    def reset(self):
        self._log = []
        self._vehicles = {}