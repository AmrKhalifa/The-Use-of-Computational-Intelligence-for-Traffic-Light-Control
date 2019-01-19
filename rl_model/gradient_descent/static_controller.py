class StaticTrafficLightController:
    def __init__(self, controller, sequence, timings):
        self._controller = controller
        assert (len(sequence) == len(timings))
        self._n_phases = len(sequence)
        self._phase_sequence = sequence
        self._timings = timings
        self._time_elapsed = 0
        self._phase_number = 0

    def tick(self):
        self._time_elapsed += 1
        self._controller.set_phase(self._phase_sequence[self._phase_number])
        if self._time_elapsed == self._timings[self._phase_number]:
            self._phase_number += 1
            self._phase_number %= self._n_phases
            self._time_elapsed = 0

