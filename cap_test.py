import time
import gym
import gym_cap
import numpy as np

# the modules that you can use to generate the policy.
import policy.patrol 
import policy.random

# import the roomba policy
from policy.roomba import PolicyGen
roomba_policy = PolicyGen()

start_time = time.time()
env = gym.make("cap-v0") # initialize the environment

done = False
t = 0
total_score = 0

# reset the environment and select the policies for each of the team
observation = env.reset(map_size=20,
                        render_mode="env",
                        policy_blue=policy.patrol.PolicyGen(env.get_map, env.get_team_blue),
                        policy_red=policy.random.PolicyGen(env.get_map, env.get_team_red))


while True:
    while not done:
        
        env.render(mode="fast")
        #print(observation.T)
        actions = roomba_policy.gen_action(env.team_blue, observation)
        #print('\n')
        
        observation, reward, done, info = env.step(actions)  # feedback from environment
        
        
        #time.sleep(2)
        
        t += 1
        if t == 100000:
            break
        
    total_score += reward
    env.reset()
    done = False
    print("Total time: %s s, score: %s" % ((time.time() - start_time),total_score))

