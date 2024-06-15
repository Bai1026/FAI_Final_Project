# import pickle
# import numpy as np
# import random
# from collections import defaultdict

# class QLearning:
#     def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
#         self.alpha = alpha  # Learning rate
#         self.gamma = gamma  # Discount factor
#         self.epsilon = epsilon  # Exploration rate
#         self.q_table = defaultdict(lambda: defaultdict(float))

#     def choose_action(self, state, actions):
#         if random.uniform(0, 1) < self.epsilon:
#             return random.choice(actions)
#         else:
#             q_values = [self.q_table[state][action] for action in actions]
#             max_q = max(q_values)
#             max_q_actions = [actions[i] for i in range(len(actions)) if q_values[i] == max_q]
#             return random.choice(max_q_actions)

#     def update_q_value(self, state, action, reward, next_state, next_actions):
#         best_next_action = self.choose_action(next_state, next_actions)
#         td_target = reward + self.gamma * self.q_table[next_state][best_next_action]
#         td_error = td_target - self.q_table[state][action]
#         self.q_table[state][action] += self.alpha * td_error

#     def save_model(self, filename):
#         with open(filename, 'wb') as f:
#             pickle.dump(dict(self.q_table), f)

#     def load_model(self, filename):
#         with open(filename, 'rb') as f:
#             self.q_table = pickle.load(f)


# import os
# import pickle
# from game.players import BasePokerPlayer
# from collections import defaultdict

# class QLearningPlayer(BasePokerPlayer):
#     def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1, model_file=None):
#         super().__init__()
#         self.ql = QLearning(alpha, gamma, epsilon)
#         self.model_file = model_file

#         if model_file and os.path.exists(model_file):
#             print('Loading model...')
#             self.ql.load_model(model_file)
#         else:
#             print('Starting training from scratch.')

#     def declare_action(self, valid_actions, hole_card, round_state):
#         state = self.init_game_state(hole_card, round_state)
#         actions = [action['action'] for action in valid_actions]
#         action = self.ql.choose_action(state, actions)
#         amount = 0
#         # print(f"Hole Card: {hole_card}, Action: {action}, Amount: {amount}")

#         if action == 'raise':
#             amount = random.randint(valid_actions[2]['amount']['min'], valid_actions[2]['amount']['max'])
        
#         self.previous_state = state
#         self.previous_action = action
#         self.hole_card = hole_card

#         return action, amount

#     # def receive_round_result_message(self, winners, hand_info, round_state):
#     #     # update Q values based on the round result
#     #     pass

#     def receive_round_result_message(self, winners, hand_info, round_state):
#         state = self.init_game_state(self.hole_card, round_state)
#         next_state = "terminal"  # Use a special terminal state
#         actions = ['fold', 'call', 'raise']
        
#         reward = 0
#         for winner in winners:
#             if winner['uuid'] == self.uuid:
#                 reward = 1
#             else:
#                 reward = -1
        
#         self.ql.update_q_value(self.previous_state, self.previous_action, reward, next_state, actions)


#     def init_game_state(self, hole_card, round_state):
#         # Create a state representation based on the hole card and round state
#         print(f"{hole_card}|{round_state['community_card']}|{round_state['seats'][0]['stack']}|{round_state['seats'][1]['stack']}")
#         return f"{hole_card}|{round_state['community_card']}|{round_state['seats'][0]['stack']}|{round_state['seats'][1]['stack']}"
    
#     def save_model(self):
#         if self.model_file:
#             self.ql.save_model(self.model_file)


#     def receive_game_start_message(self, game_info):
#         pass

#     def receive_round_start_message(self, round_count, hole_card, seats):
#         pass

#     def receive_street_start_message(self, street, round_state):
#         pass

#     def receive_game_update_message(self, action, round_state):
#         pass

#     def receive_round_result_message(self, winners, hand_info, round_state):
#         pass





# import pickle
# import random
# from collections import defaultdict

# class QLearning:
#     def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
#         self.alpha = alpha  # Learning rate
#         self.gamma = gamma  # Discount factor
#         self.epsilon = epsilon  # Exploration rate
#         self.q_table = defaultdict(lambda: defaultdict(float))

#     def choose_action(self, state, actions):
#         if random.uniform(0, 1) < self.epsilon:
#             return random.choice(actions)
#         else:
#             q_values = [self.q_table[state][action] for action in actions]
#             max_q = max(q_values)
#             max_q_actions = [actions[i] for i in range(len(actions)) if q_values[i] == max_q]
#             return random.choice(max_q_actions)

#     def update_q_value(self, state, action, reward, next_state, next_actions):
#         if state not in self.q_table:
#             self.q_table[state] = {action: 0.0 for action in next_actions}
#         if next_state not in self.q_table:
#             self.q_table[next_state] = {action: 0.0 for action in next_actions}
            
#         best_next_action = max(self.q_table[next_state], key=self.q_table[next_state].get)
#         td_target = reward + self.gamma * self.q_table[next_state][best_next_action]
#         td_error = td_target - self.q_table[state][action]
#         self.q_table[state][action] += self.alpha * td_error

#     def save_model(self, filename):
#         with open(filename, 'wb') as f:
#             pickle.dump(dict(self.q_table), f)

#     def load_model(self, filename):
#         with open(filename, 'rb') as f:
#             self.q_table = pickle.load(f)

# import os
# import random
# from game.players import BasePokerPlayer

# class QLearningPlayer(BasePokerPlayer):
#     def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1, model_file=None):
#         super().__init__()
#         self.ql = QLearning(alpha, gamma, epsilon)
#         self.model_file = model_file
#         self.hole_card = None  # Initialize hole_card
#         self.previous_state = None
#         self.previous_action = None

#         if model_file and os.path.exists(model_file):
#             print('Loading model...')
#             self.ql.load_model(model_file)
#         else:
#             print('Starting training from scratch.')

#     def declare_action(self, valid_actions, hole_card, round_state):
#         self.hole_card = hole_card  # Ensure hole_card is set
#         state = self.init_game_state(hole_card, round_state)
#         actions = [action['action'] for action in valid_actions]
#         action = self.ql.choose_action(state, actions)
#         amount = 0

#         if action == 'raise':
#             amount = random.randint(valid_actions[2]['amount']['min'], valid_actions[2]['amount']['max'])
        
#         self.previous_state = state
#         self.previous_action = action

#         return action, amount

#     def receive_round_result_message(self, winners, hand_info, round_state):
#         if self.hole_card is None or self.previous_state is None or self.previous_action is None:
#             print("Warning: missing information for Q-learning update, skipping.")
#             return
        
#         state = self.init_game_state(self.hole_card, round_state)
#         next_state = "terminal"  # Use a special terminal state
#         actions = ['fold', 'call', 'raise']
        
#         reward = 0
#         for winner in winners:
#             if winner['uuid'] == self.uuid:
#                 reward = 1
#             else:
#                 reward = -1
        
#         # Ensure Q-value initialization
#         if next_state not in self.ql.q_table:
#             self.ql.q_table[next_state] = {action: 0.0 for action in actions}

#         self.ql.update_q_value(self.previous_state, self.previous_action, reward, next_state, actions)

#     def init_game_state(self, hole_card, round_state):
#         return f"{hole_card}|{round_state['community_card']}|{round_state['seats'][0]['stack']}|{round_state['seats'][1]['stack']}"
    
#     def save_model(self):
#         if self.model_file:
#             self.ql.save_model(self.model_file)

#     def receive_game_start_message(self, game_info):
#         pass


#     def receive_round_start_message(self, round_count, hole_card, seats):
#         self.hole_card = hole_card  # Set hole_card at the start of the round
#         self.previous_state = None
#         self.previous_action = None

#     def receive_street_start_message(self, street, round_state):
#         pass

#     def receive_game_update_message(self, action, round_state):
#         pass



import os
import pickle
import numpy as np
import random
from collections import defaultdict
import logging

class QLearning:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.q_table = defaultdict(lambda: defaultdict(float))

    def choose_action(self, state, actions):
        self.ensure_state_actions_initialized(state, actions)
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(actions)
        else:
            q_values = [self.q_table[state][action] for action in actions]
            max_q = max(q_values)
            max_q_actions = [actions[i] for i in range(len(actions)) if q_values[i] == max_q]
            return random.choice(max_q_actions)

    def update_q_value(self, state, action, reward, next_state, next_actions):
        self.ensure_state_action_initialized(state, action)
        self.ensure_state_actions_initialized(next_state, next_actions)

        best_next_action = self.choose_action(next_state, next_actions)
        td_target = reward + self.gamma * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.alpha * td_error

        logging.info(f"Updated Q-value for state: {state}, action: {action}, reward: {reward}, next state: {next_state}")
        logging.info(f"TD Target: {td_target}, TD Error: {td_error}, Updated Q-value: {self.q_table[state][action]}")

    def ensure_state_action_initialized(self, state, action):
        if action not in self.q_table[state]:
            self.q_table[state][action] = 0.0

    def ensure_state_actions_initialized(self, state, actions):
        print('Entering ensure_state_actions_initialized')
        if state not in self.q_table:
            print(f'Initializing state: {state}')
            self.q_table[state] = defaultdict(float)
        # print('table')
        # print(self.q_table[state])

        for action in actions:
            if action not in self.q_table[state]:
                # print('occur')
                self.q_table[state][action] = 0.0
        
            # print(action)

    def save_model(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(dict(self.q_table), f)

    def load_model(self, filename):
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)


def calculate_remaining(round_state):
    blind_remaining = 0
    round_count = int(round_state['round_count'])
    round_remaining = 20 - round_count

    blind_remaining += ((round_remaining // 2) + 1) * 5
    blind_remaining += (((round_remaining - 1) // 2) + 1) * 10
    print(blind_remaining)

    return blind_remaining


import os
from game.players import BasePokerPlayer
import logging

class QLearningPlayer(BasePokerPlayer):
    def __init__(self, threshold, alpha=0.1, gamma=0.9, epsilon=0.1, model_file=None):
        super().__init__()
        self.ql = QLearning(alpha, gamma, epsilon)
        self.model_file = model_file
        self.previous_state = None
        self.previous_action = None
        self.hole_card = None

        if model_file and os.path.exists(model_file):
            print('Loading model...')
            self.ql.load_model(model_file)
        else:
            print('Starting training from scratch.')

    def declare_action(self, valid_actions, hole_card, round_state):
        state = self.init_game_state(hole_card, round_state)
        actions = [action['action'] for action in valid_actions]
        action = self.ql.choose_action(state, actions)
        amount = 0

        blind_remaining = calculate_remaining(round_state)
        print(round_state['seats'][0])
        print('player 1: ', round_state['seats'][0]['stack'] + blind_remaining)
        print('player 2: ', round_state['seats'][1]['stack'] - blind_remaining)

        if round_state['seats'][0]['stack'] - blind_remaining >= round_state['seats'][1]['stack'] + blind_remaining:
            # print("Fold with enough blind remaining")
            # print(round_state['seats'][0]['stack'], round_state['seat'][1]['stack'], blind_remaining)
            logging.info(f"Fold with enough blind remaining")
            logging.info(f"Player 1: {round_state['seats'][0]['stack']}, Player 2: {round_state['seats'][1]['stack']}, Blind Remaining: {blind_remaining}")

            fold_action_info = valid_actions[0]
            action, amount = fold_action_info["action"], fold_action_info["amount"]
            return action, amount
        

        if action == 'raise':
            amount = random.randint(valid_actions[2]['amount']['min'], valid_actions[2]['amount']['max'])

        # print(state)
        self.previous_state = state
        self.previous_action = action
        self.hole_card = hole_card

        logging.info(f"Declare action: state={state}, action={action}, amount={amount}")

        return action, amount

    def receive_round_result_message(self, winners, hand_info, round_state):
        if self.previous_state is None or self.previous_action is None:
            logging.warning("Missing previous state or action for Q-learning update, skipping.")
            return

        state = self.init_game_state(self.hole_card, round_state)
        # print(f'state: {state}')
        next_state = "terminal"  # Use a special terminal state
        actions = ['fold', 'call', 'raise']
        
        reward = 0
        for winner in winners:
            if winner['uuid'] == self.uuid:
                reward = 1
            else:
                reward = -1
        
        self.ql.update_q_value(self.previous_state, self.previous_action, reward, next_state, actions)
        
        logging.info(f"Round result: winners={winners}, reward={reward}, state={state}, next_state={next_state}")

        # Reset previous state and action
        self.previous_state = None
        self.previous_action = None

    def init_game_state(self, hole_card, round_state):
        community_cards = round_state['community_card'] if round_state['community_card'] else []
        state = f"{hole_card}|{community_cards}|{round_state['seats'][0]['stack']}|{round_state['seats'][1]['stack']}"
        # print(f'init_game_state: {state}')
        return state
    
    def save_model(self):
        if self.model_file:
            self.ql.save_model(self.model_file)

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

def setup_ai(threshold):
    return QLearningPlayer(threshold, alpha=0.1, gamma=0.9, epsilon=0.1, model_file="q_learning_model.pkl")
