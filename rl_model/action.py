import traci 

class PhaseModifier:

	def change_to_phase(junctionID,phase):
		traci.trafficlights.setPhase(str(junctionID), phase)
