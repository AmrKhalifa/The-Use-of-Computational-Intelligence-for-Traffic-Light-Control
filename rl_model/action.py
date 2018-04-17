import traci 


class PhaseModifier:
    def __init__(self, junctionID):
        self._junction_id = junctionID

    def set_phase(self,phase):
        traci.trafficlights.setPhase(self._junction_id, phase)
