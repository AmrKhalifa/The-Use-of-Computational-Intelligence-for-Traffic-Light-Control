import matplotlib.pyplot as plt
import numpy as np
from SARS import RewardCollector
from SARS import StateAction
from action import PhaseModifier
from policy_network import PolicyNetwork
from reward import RewardCalculator
from simulation import Simulator

sumocfg1 = "..\\..\\test_environments\\single_intersection_random_trips\\newnet.sumocfg"
roads_list = [["-road1_0","road3_0"],["road2_0","road4_0"]]

rc = RewardCalculator(alpha= 0)
rewardCollector = RewardCollector(rc)

sim = Simulator()
sim.add_simulation_component(StateAction)
sim.add_tickable(rc)
sim.add_tickable(rewardCollector)

PolicyNetwork.initialize_variables()

sim.run(sumocfg1, gui=False, time_steps= 1500)
sim.results['rewards'] = rewardCollector.get_reward_log()

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

discounted_normed_rewards = discount_and_norm_rewards(sim.results['rewards'])

loss = []
loss_sum = 0
counter = 0
for i in range (len(sim.results['states'][0])):

    s = sim.results['states'][0][i]
    a = sim.results['actions'][0][i]
    r = sim.results['rewards'][0]

    # fix the reward shit
    loss.append(PolicyNetwork.train(s,a,r))
    counter +=1
    print(counter)


for element in loss:
    print(element)



