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

sumocfg1 = "..\\..\\test_environments\\single_intersection_no_traffic\\newnet.sumocfg"
roads_list = [["-road1_0","road3_0"],["road2_0","road4_0"]]
lossings = []
rewards = []
policy_network = PolicyNetwork()

#################################
def define_data_frame():
    simulation_dataFrame = pd.DataFrame({'iteration': [0],
                                         'mean_speed': [0],
                                         'duration': [0],
                                         'waiting_time': [0],
                                         'time_loss': [0],
                                          'vssd':[0],
                                        'jtsd':[0],
                                         'reward':[0]})
    simulation_dataFrame.set_index('iteration', inplace=True)
    return simulation_dataFrame


def generate_iteration_data_frame(iteration_no,mean_speed_result,duration_result,waiting_time,time_loss,vssd,jtsd,reward):
    iteration_dataFrame = pd.DataFrame(({'iteration': [iteration_no],
                                         'mean_speed': [mean_speed_result],
                                         'duration': [duration_result],
                                         'waiting_time': [waiting_time],
                                         'time_loss': [time_loss],
                                        'vssd':[vssd],
                                        'jtsd':[jtsd],
                                         'reward':[reward]}))
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


gamma = .90
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

def randomize_traffic():
    os.chdir(
        r"D:\My study\5th year\Graduation Project\traffic-optimization\test_environments\single_intersection_no_traffic")
    p = subprocess.Popen(["python", r'C:\Program Files (x86)\DLR\Sumo\tools\randomTrips.py', '-n', 'newnet.net.xml',
                          '-e', '800', '-p', '1.2', '-r', 'newnet.rou.xml'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    time.sleep(.1)


iterations = 1500
for i in range (iterations):

    rc = RewardCalculator(alpha= 0.5)
    rewardCollector = RewardCollector(rc)

    sim = Simulator()
    randomize_traffic()
    observer = StateObserver(sim)
    sim.add_simulation_component(observer)
    actor = Actor(observer,policy_network)
    sim.add_tickable(actor)
    sim.add_tickable(rc)
    sim.add_tickable(rewardCollector)

    parser = SimulationOutputParser(sim)
    sim.add_tickable(parser)
    sim.add_postrun(parser.post_run) 
    sim.run(sumocfg1, gui=False,time_steps = 2000)
    sim.results['rewards'] = rewardCollector.get_reward_log()
    sim.results['actions']= actor.get_actions_list()

    mean_speed_result = (np.mean(sim.results['mean_speed']))
    duration_result = (np.mean(sim.results['duration']))
    waiting_time = (np.mean(sim.results['waiting_time']))
    time_loss = (np.mean(sim.results['time_loss']))
    vssd = sim.results['mean_speed'].var() ** .5
    jtsd = sim.results['duration'].var() ** .5
    reward = np.mean(sim.results['rewards'])

    iteration_dataFrame = generate_iteration_data_frame(i, mean_speed_result, duration_result, waiting_time, time_loss,vssd,jtsd,reward)
    simulation_dataFrame = concat_frames(simulation_dataFrame, iteration_dataFrame)

    shifted_rewards = shift(sim.results['rewards'],1)

    discounted_normed_rewards = discount_and_norm_rewards(shifted_rewards)

    s = sim.results['states'][0]
    a = sim.results['actions']
    r = discounted_normed_rewards

    loss, reward= policy_network.train(np.array(s),a,np.array(r),i)
    lossings.append(loss)
    rewards.append(reward)


#####################################################################

rc = RewardCalculator(alpha= 0.5)
rewardCollector = RewardCollector(rc)

sim = Simulator()
randomize_traffic()
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

iteration_dataFrame = generate_iteration_data_frame(55555, mean_speed_result, duration_result, waiting_time, time_loss,vssd,jtsd,reward)
simulation_dataFrame = concat_frames(simulation_dataFrame, iteration_dataFrame)

shifted_rewards = shift(sim.results['rewards'],1)

discounted_normed_rewards = discount_and_norm_rewards(shifted_rewards)

s = sim.results['states'][0]
a = sim.results['actions']
r = discounted_normed_rewards

loss, reward= policy_network.train(np.array(s),a,np.array(r),55555)
lossings.append(loss)
rewards.append(reward)

#############################################################    

save_dataframe2CSV(simulation_dataFrame,"D:\My study\\5th year\Graduation Project\\traffic-optimization\\rl_model\policy_gradient\pg_results_alpha_05.csv")

policy_network.saveModel()
print(rewards)

