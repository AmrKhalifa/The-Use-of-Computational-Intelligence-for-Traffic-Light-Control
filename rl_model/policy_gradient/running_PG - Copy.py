import matplotlib.pyplot as plt
import numpy as np
from SARS import RewardCollector
from SARS import StateObserver
from SARS import Actor
from action import PhaseModifier
from torch_network import PolicyNetwork
from reward import RewardCalculator
from simulation import Simulator
from stats import SimulationOutputParser
import traci
import subprocess
import time
import os
import pandas as pd

sumocfg1 = "..\\..\\test_environments\\single_intersection_random_trips\\newnet.sumocfg"
roads_list = [["-road1_0","road3_0"],["road2_0","road4_0"]]
lossings = []
rewards = []

policy_network = PolicyNetwork()
policy_network.loadModel()

#################################
def define_data_frame():
    simulation_dataFrame = pd.DataFrame({'iteration': [0],
                                         'mean_speed': [0],
                                         'duration': [0],
                                         'waiting_time': [0],
                                         'time_loss': [0],
                                          'vssd':[0],
                                        'jtsd':[0]})
    simulation_dataFrame.set_index('iteration', inplace=True)
    return simulation_dataFrame


def generate_iteration_data_frame(iteration_no,mean_speed_result,duration_result,waiting_time,time_loss,vssd,jtsd):
    iteration_dataFrame = pd.DataFrame(({'iteration': [iteration_no],
                                         'mean_speed': [mean_speed_result],
                                         'duration': [duration_result],
                                         'waiting_time': [waiting_time],
                                         'time_loss': [time_loss],
                                        'vssd':[vssd],
                                        'jtsd':[jtsd]}))
    iteration_dataFrame.set_index('iteration',inplace= True)
    return iteration_dataFrame


def concat_frames(f1,f2):
    frames = [f1, f2]
    frame = pd.concat(frames)
    return frame

def save_dataframe2CSV(f1,file):
    f1.to_csv(file)
##########################################

simulation_dataFrame = define_data_frame()


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

iterations = 10
for i in range (iterations):

    rc = RewardCalculator(alpha= 0.5)
    rewardCollector = RewardCollector(rc)

    sim = Simulator()
    observer = StateObserver(sim)
    sim.add_simulation_component(observer)
    actor = Actor(observer,policy_network)
    sim.add_tickable(actor)
    sim.add_tickable(rc)
    sim.add_tickable(rewardCollector)

    sim.add_simulation_component(SimulationOutputParser(sim)) 
    sim.run(sumocfg1, gui=False,time_steps = 2000)
    sim.results['rewards'] = rewardCollector.get_reward_log()
    sim.results['actions']= actor.get_actions_list()

    mean_speed_result = (np.mean(sim.results['mean_speed']))
    duration_result = (np.mean(sim.results['duration']))
    waiting_time = (np.mean(sim.results['waiting_time']))
    time_loss = (np.mean(sim.results['time_loss']))
    vssd = sim.results['mean_speed'].var() ** .5
    jtsd = sim.results['duration'].var() ** .5

    iteration_dataFrame = generate_iteration_data_frame(i, mean_speed_result, duration_result, waiting_time, time_loss,vssd,jtsd)
    simulation_dataFrame = concat_frames(simulation_dataFrame, iteration_dataFrame)

#####################################################################

save_dataframe2CSV(simulation_dataFrame,"D:\My study\\5th year\Graduation Project\\traffic-optimization\\rl_model\policy_gradient\pg_results_ex_data.csv")

#policy_network.saveModel()
print(rewards)
plt.plot(rewards)
plt.show()
