import time
import gym
import gym_cap
import numpy as np

# the modules that you can use to generate the policy.
import policy.patrol 
import policy.random

# my stupid roomba policy
from policy.roomba import gen_action

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
        
        #env.render(mode="fast")
        #print(f'Observation:\n {observation.T}')
        # for agent in env.team_blue:
        #     print(f'loc: {agent.get_loc()}')

        actions = gen_action(env.team_blue, observation)
        #print(f'action:\n {actions_h(actions)}')
        
        observation, reward, done, info = env.step(actions)  # feedback from environment
        
        #time.sleep(0.5)
        
        t += 1
        if t == 100000:
            break
        
    total_score += reward
    env.reset()
    done = False
    print("Total time: %s s, score: %s" % ((time.time() - start_time),total_score))

