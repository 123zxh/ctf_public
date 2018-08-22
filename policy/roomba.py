import numpy as np 

def gen_action(agent_list, observation):
    num_trials_until_give_up = 25
    
    actions = []

    for agent_idx in range(len(agent_list)):
        agent_loc = agent_list[agent_idx].get_loc()
        action = np.random.randint(0, 5)
        next_pos = next_position(agent_loc[0], agent_loc[1], action)
        #print(agent_idx, agent_list[agent_idx].isAlive)
        for _ in range(num_trials_until_give_up-1):
            if not is_dangerous(agent_list[agent_idx], next_pos[0], next_pos[1], observation):
                break
            else:
                action = np.random.randint(0, 5)
                next_pos = next_position(agent_loc[0], agent_loc[1], action)
        
        actions.append(action)
    return actions

def next_position(x, y, action):
    if action == 0:   # noop
        return x, y
    elif action == 1: # north ⬆️
        return x, y - 1
    elif action == 2: # east ➡️
        return x + 1, y
    elif action == 3: # south ⬇️
        return x, y + 1
    else:             # west ⬅️
        return x - 1, y

def is_dangerous(agent, next_x, next_y, observation):
    # the next position is out of bound
    if next_x < 0 or next_x >= len(observation) or next_y < 0 or next_y >= len(observation[0]):
        #print('the next position is out of bound')
        return True
    
    # the next position is obstacle
    if observation[next_x][next_y] == 8:
        #print('next position is obstacle')
        return True

    # the next position is my territory
    if observation[next_x][next_y] == 0:
        #print('next position is my territory')
        return False
    
    # the next position is within my opponent's attack
    for x in range(-2 * agent.a_range, 2 * agent.a_range + 1):
        for y in range(-2 * agent.a_range, 2 * agent.a_range + 1):
            locx, locy = next_x + x, next_y + y
            if (x ** 2 + y ** 2 <= (agent.a_range*2) ** 2 and
                (not (locx < 0 or locy < 0 or locx >= len(observation) or locy >= len(observation[0])))):
                if observation[locx][locy] == 4:
                    #print('next position is within my opponent\'s attack')
                    return True
    return False

def actions_h(actions):
    """Human readable actions"""
    res = []
    for action in actions:
        if action == 0:
            res.append('X')
        elif action == 1:
            res.append('N')
        elif action == 2:
            res.append('E')
        elif action == 3:
            res.append('S')
        else:
            res.append('W')
    return res