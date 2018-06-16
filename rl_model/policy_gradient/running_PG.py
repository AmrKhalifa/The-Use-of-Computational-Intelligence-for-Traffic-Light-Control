import matplotlib.pyplot as plt
import numpy as np
from SARS import RewardCollector
from SARS import StateObserver
from SARS import Actor
from action import PhaseModifier
from torch_network import PolicyNetwork
from reward import RewardCalculator
from simulation import Simulator
import traci

sumocfg1 = "..\\..\\test_environments\\single_intersection_random_trips\\newnet.sumocfg"
roads_list = [["-road1_0","road3_0"],["road2_0","road4_0"]]
lossings = []
policy_network = PolicyNetwork()

gamma = .99

def discount_and_norm_rewards(rewards):
    discounted_episode_rewards = np.zeros_like(rewards)
    cumulative = 0
    for t in reversed(range(len(rewards))):
        cumulative = cumulative * gamma + rewards[t]
        discounted_episode_rewards[t] = cumulative

    discounted_episode_rewards -= np.mean(discounted_episode_rewards)
    discounted_episode_rewards /= np.std(discounted_episode_rewards)
    return discounted_episode_rewards


def shift(seq, n):
    n = n % len(seq)
    return seq[n:] + seq[:n]

for i in range (1000):

    rc = RewardCalculator(alpha= 0)
    rewardCollector = RewardCollector(rc)

    sim = Simulator()
    observer = StateObserver(sim)
    sim.add_simulation_component(observer)
    actor = Actor(observer,policy_network)
    sim.add_tickable(actor)
    sim.add_tickable(rc)
    sim.add_tickable(rewardCollector)

    sim.run(sumocfg1, gui=False, time_steps= 2000)
    sim.results['rewards'] = rewardCollector.get_reward_log()
    sim.results['actions']= actor.get_actions_list()
    shifted_rewards = shift(sim.results['rewards'],1)

    discounted_normed_rewards = discount_and_norm_rewards(shifted_rewards)

    s = sim.results['states'][0]
    a = sim.results['actions']
    r = discounted_normed_rewards

    loss = policy_network.train(np.array(s),a,np.array(r))
    lossings.append(loss)

plt.plot(lossings)






