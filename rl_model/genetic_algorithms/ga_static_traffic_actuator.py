import traci
import rl_model.action as ac
import numpy as np

class StaticTrafficLightAcuator:
    def __init__(self,chromosome,simulation_time):

        self._chromosome = chromosome
        self._simulation_time = simulation_time
        self._counter =0
        self._current_phase =0
        self._phases_list = chromosome._phases_steps
        self._phase_array= np.cumsum(np.array(self._phases_list))

        pass

    def tick(self):
        #print("This Chromosome info are : ")
   
        phase = traci.trafficlights.getPhase("node1")
        #print("the current phase is : ",phase)
        #print("the phases list is : ", self._phase_array)
        mylist = self._phases_list
        modifier = ac.PhaseModifier("node1")

        if(self._counter >= 0 and self._counter<self._phase_array[0]):
           modifier.set_phase(0)
           #print("the counter count is :", self._counter)
        elif (self._counter >= self._phase_array[0] and self._counter < self._phase_array[1]):
            modifier.set_phase(1)
            #print("the counter count is :", self._counter)
        elif (self._counter >= self._phase_array[1] and self._counter < self._phase_array[2]):
            modifier.set_phase(2)
            #print("the counter count is :", self._counter)
        elif (self._counter >= self._phase_array[2] and self._counter < self._phase_array[3]):
            modifier.set_phase(3)
            #print("the counter count is :", self._counter)
        elif (self._counter >= self._phase_array[3] and self._counter < self._phase_array[4]):
            modifier.set_phase(4)
            #print("the counter count is :", self._counter)
        elif (self._counter >= self._phase_array[4] and self._counter < self._phase_array[5]):
            modifier.set_phase(5)
            #print("the counter count is :", self._counter)
        elif (self._counter >= self._phase_array[5] and self._counter < self._phase_array[6]):
            modifier.set_phase(6)
            #print("the counter count is :", self._counter)
        elif (self._counter >= self._phase_array[6] and self._counter < self._phase_array[7]):
            modifier.set_phase(7)
            #print("the counter count is :", self._counter)
        else:
            self._counter =0
            #print("the counter count now is ",self._counter)
            #print("the cycle has successfully completed ...")

        #print("*="*15)

        self._counter +=1
        pass

