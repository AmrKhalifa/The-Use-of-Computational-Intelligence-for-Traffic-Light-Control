import numpy as np 
import traci 

class DTSE_Generator:


	def get_traffic_state(road,direction,state_size,cell_size):

		vehicles = traci.edge.getLastStepVehicleIDs(traci.lane.getEdgeID(road))
		vehicles_existence = np.zeros(state_size) 
		vehicles_speed = np.zeros(state_size)
		road_length = traci.lane.getLength(road) 
		
		for v in vehicles :
			if direction == "in":
				v_position = abs(road_length-int (traci.vehicle.getLanePosition(v)))
			else:
				v_position = abs(int (traci.vehicle.getLanePosition(v)))	
			v_speed = abs(int(traci.vehicle.getSpeed(v)))
			index = 0
			for i in range (0,cell_size*state_size,cell_size):
				if(v_position >=i and v_position<i+cell_size):
					vehicles_existence[index] =1
					vehicles_speed[index]=v_speed
				index+=1

		return vehicles_existence, vehicles_speed


	def get_traffic_lights_state(id):
		traffic_lights_state = traci.trafficlights.getRedYellowGreenState(id)
		phase = traci.trafficlights.getPhase(id)

		return traffic_lights_state , phase