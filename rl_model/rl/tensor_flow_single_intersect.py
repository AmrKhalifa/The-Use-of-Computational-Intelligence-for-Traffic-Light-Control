from rl import RLAgent, StateGenerator, Controller, ActionRepresentation
from reward import RewardCalculator
from simulation import Simulator
from action import PhaseModifier
from stats import SimulationOutputParser
import tensorflow as tf
import numpy as np


N_ACTIONS = 3

class SingleIntersectQAgent (RLAgent):
    def __init__(self, reward_calc, state, controller, actions):
        super().__init__(reward_calc, state, controller, actions)
        self._build_model_graph()
        self._discount = .9
        self._explore_prob = 0.2

    def _select_action(self, state):
        if np.random.rand(1) < self._explore_prob:
            action = np.eye(N_ACTIONS)[np.random.randint(N_ACTIONS)]
            return action
        output = self._session.run(self._model_output, feed_dict={self._model_input: state})

        action_number = np.argmax(output)
        one_hot = np.eye(output.size)[action_number]
        return one_hot

    def set_explore_probability(self, explore_probability):
        self._explore_prob = explore_probability

    def _build_model_graph(self):
        self._model_input = tf.placeholder(dtype=tf.float64, shape=[1,120])
        layer1 = tf.layers.dense(inputs=self._model_input,units=100, activation=tf.nn.relu)
        layer2 = tf.layers.dense(inputs=layer1,units=100, activation=tf.nn.relu)
        layer3 = tf.layers.dense(inputs=layer2, units=3)
        self._model_output = layer3

        self._calculated_q = tf.placeholder(dtype=tf.float64, shape=(1, N_ACTIONS))
        self._loss = tf.reduce_sum(tf.square(self._calculated_q - self._model_output))
        self._optimizer = tf.train.AdamOptimizer().minimize(self._loss)

        g_initializer = tf.global_variables_initializer()
        l_initializer = tf.local_variables_initializer()

        self._session = tf.Session()
        self._saver = tf.train.Saver()
        self._session.run(g_initializer)
        self._session.run(l_initializer)


    def _update_model(self, state, action, reward, new_state):
        initial_q = self._session.run(self._model_output, feed_dict={self._model_input: state})
        next_q = self._session.run(self._model_output, feed_dict={self._model_input: new_state})
        max_next_q = np.max(next_q)

        action_index = np.argmax(action)
        calculated_q = initial_q
        calculated_q[0,action_index] = reward + self._discount*max_next_q
        self._session.run(self._optimizer, feed_dict={self._model_input: state, self._calculated_q: calculated_q})

    def save_model(self, save_path):
        self._saver.save(self._session, save_path)

    def restore_model(self, save_path):
        self._saver.restore(self._session, save_path)

if __name__ == "__main__":
    sumocfg = "..\\..\\test_environments\\single_intersection_random_trips\\newnet.sumocfg"
    rc = RewardCalculator(alpha=0)
    action_translator = ActionRepresentation([0, 3, 4])
    controller = Controller(PhaseModifier("node1"), action_translator)
    state_gen = StateGenerator()
    agent = SingleIntersectQAgent(rc, state_gen, controller, np.eye(3))
    explore_prob = .4
    avg_speed = []
    mean_dur = []
    for episode in range(500):
        controller.reset()
        rc.reset()
        agent.reset()

        explore_prob *= .99
        agent.set_explore_probability(explore_prob)

        sim = Simulator()
        sim.add_tickable(rc)
        sim.add_tickable(controller)
        sim.add_tickable(agent)
        sim.add_simulation_component(SimulationOutputParser)
        sim.run(sumocfg, time_steps=3000, gui=False)
        mean_speed = sim.results["mean_speed"].mean()
        mean_dur.append(sim.results["duration"].mean())
        print("Episode %i : avg speed %.3f, mean journey %.3f"%(episode, mean_speed, mean_dur[-1]))
        avg_speed.append(mean_speed)
        agent.save_model("./rl_models/2_layer_model_100_100")

    print(avg_speed)
    print(mean_dur)