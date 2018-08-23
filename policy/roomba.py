import numpy as np

class PolicyGen:

    def __init__(self):
        self.prev_actions = np.random.choice([2, 4], 4).tolist()
        self.cnt = 59

    def gen_action(self, agent_list, observation):
        self.cnt -= 1
        if self.cnt == 0:
            self.cnt = 59
            return np.random.randint(0, 5, 4).tolist()
        
        actions = []

        num_trials_until_give_up = 10
        for agent_idx in range(len(agent_list)):
            agent_loc = agent_list[agent_idx].get_loc()

            action = self.prev_actions[agent_idx]
            if action == 3:
                action = np.random.choice([2, 4])
            next_x, next_y = self.next_position(agent_loc[0], agent_loc[1], action)
            if self.is_obstacle(next_x, next_y, observation) and (action == 2 or action == 4):
                action = 3
                next_xx, next_yy = self.next_position(agent_loc[0], agent_loc[1], action)
                if self.is_obstacle(next_xx, next_yy, observation):
                    action = np.random.choice([0, 1])

            next_pos = self.next_position(agent_loc[0], agent_loc[1], action)
            for _ in range(num_trials_until_give_up-1):
                if not self.is_dangerous(agent_list[agent_idx], next_pos[0], next_pos[1], observation):
                    break
                else:
                    action = np.random.choice([0, 1, 2, 3, 4], p=[0.1, 0.2, 0.15, 0.4, 0.15])
                    next_pos = self.next_position(agent_loc[0], agent_loc[1], action)
            
            actions.append(action)

        # update the previous actions
        self.prev_actions = actions
        return actions

    def next_position(self, x, y, action):
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

    def is_obstacle(self, next_x, next_y, observation):
        # the next position is out of bound
        if next_x < 0 or next_x >= len(observation) or next_y < 0 or next_y >= len(observation[0]):
            #print('the next position is out of bound')
            return True

        # the next position is obstacle
        if observation[next_x][next_y] == 8:
            #print('next position is obstacle')
            return True

        # the next position is member of the same team (dont shoot your ally)
        if observation[next_x][next_y] == 2:
            return True

        return False

    def is_dangerous(self, agent, next_x, next_y, observation):
        if self.is_obstacle(next_x, next_y, observation):
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
                        return True
        return False

    @staticmethod
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