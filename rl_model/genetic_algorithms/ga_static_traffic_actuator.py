import action as ac
import numpy as np


class StaticTrafficLightActuator:
    def __init__(self,chromosome):

        self._chromosome = chromosome
        self._counter =0
        self._current_phase =0
        self._phases_list = chromosome._phases_steps
        self._phase_array= np.cumsum(np.array(self._phases_list))
        pass

    def tick(self):
        modifier = ac.PhaseModifier("node1")

        if(self._counter >= 0 and self._counter<self._phase_array[0]):
           modifier.set_phase(0)

        elif (self._counter >= self._phase_array[0] and self._counter < self._phase_array[1]):
            modifier.set_phase(1)

        elif (self._counter >= self._phase_array[1] and self._counter < self._phase_array[2]):
            modifier.set_phase(2)

        elif (self._counter >= self._phase_array[2] and self._counter < self._phase_array[3]):
            modifier.set_phase(3)

        elif (self._counter >= self._phase_array[3] and self._counter < self._phase_array[4]):
            modifier.set_phase(4)

        elif (self._counter >= self._phase_array[4] and self._counter < self._phase_array[5]):
            modifier.set_phase(5)

        elif (self._counter >= self._phase_array[5] and self._counter < self._phase_array[6]):
            modifier.set_phase(6)

        elif (self._counter >= self._phase_array[6] and self._counter < self._phase_array[7]):
            modifier.set_phase(7)

        else:
            self._counter =0

        self._counter +=1
        pass

