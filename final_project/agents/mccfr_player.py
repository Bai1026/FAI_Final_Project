import os
import pickle
from game.players import BasePokerPlayer
from collections import defaultdict
import random  # Don't forget to import the random module

def default_float_dict():
    return defaultdict(float)

class MCCFR:
    def __init__(self, iterations=10000):
        self.iterations = iterations
        self.regret_sum = defaultdict(default_float_dict)
        self.strategy_sum = defaultdict(default_float_dict)
        self.strategy = defaultdict(default_float_dict)

        self.regret_history = []

    def get_strategy(self, info_set, actions):
        strategy = self.strategy[info_set]
        normalizing_sum = sum(strategy.values())
        if normalizing_sum > 0:
            return {a: p / normalizing_sum for a, p in strategy.items()}
        else:
            return {a: 1.0 / len(actions) for a in actions}

    def update_strategy(self, info_set, actions, regret):
        for action in regret:
            self.regret_sum[info_set][action] += regret[action]
            self.strategy[info_set][action] = max(self.regret_sum[info_set][action], 0.0)
    
    def mccfr(self, state, player, pi):
        if self.is_terminal(state):
            return self.get_terminal_utility(state, player)

        info_set = self.get_info_set(state, player)
        actions = self.get_possible_actions(state)
        strategy = self.get_strategy(info_set, actions)

        action_utilities = {}
        node_util = 0
        for action in actions:
            new_state, reward = self.play_action(state.copy(), action)
            action_util = reward + self.mccfr(new_state, 1 - player, pi * strategy[action])
            action_utilities[action] = action_util
            node_util += strategy[action] * action_util

        for action in actions:
            regret = {action: action_utilities[action] - node_util}
            self.update_strategy(info_set, actions, regret)

        return node_util

    def train(self, game, initial_hands, initial_round_state):
        for i in range(self.iterations):
            state = self.init_game_state(initial_hands, initial_round_state)
            print(state)
            self.mccfr(state, player=0, pi=1.0)

            if (i + 1) % 100 == 0:
                total_regret = sum([sum(regrets.values()) for regrets in self.regret_sum.values()])
                self.regret_history.append(total_regret)
                print(f"Iteration {i + 1}/{self.iterations}, Total Regret: {total_regret}")


    def get_info_set(self, state, player):
        hand = ''.join(sorted(state['player_hands'][player]))
        community = ''.join(sorted(state['community_cards']))
        return hand + '|' + community

    def get_action(self, state, player):
        info_set = self.get_info_set(state, player)
        actions = self.get_possible_actions(state)
        strategy = self.get_strategy(info_set, actions)
        return random.choices(list(strategy.keys()), weights=strategy.values(), k=1)[0]

    def is_terminal(self, state):
        return any(chips <= 0 for chips in state['player_chips'])

    def get_terminal_utility(self, state, player):
        if state['player_chips'][player] > state['player_chips'][1 - player]:
            return 1
        elif state['player_chips'][player] < state['player_chips'][1 - player]:
            return -1
        else:
            return 0

    def get_possible_actions(self, state):
        actions = ['fold', 'call']
        if state['player_chips'][state['current_player']] > state['current_bet']:
            actions.append('raise')
        return actions

    def play_action(self, state, action):
        current_player = state['current_player']
        if action == 'fold':
            state['player_chips'][1 - current_player] += state['pot']
            state['pot'] = 0
            state['player_chips'][current_player] = 0  # 当前玩家输了
            return state, -1
        elif action == 'call':
            state['player_chips'][current_player] -= state['current_bet']
            state['pot'] += state['current_bet']
        elif action == 'raise':
            raise_amount = min(100, state['player_chips'][current_player])
            state['player_chips'][current_player] -= raise_amount
            state['pot'] += raise_amount
            state['current_bet'] = raise_amount

        state['current_player'] = 1 - current_player  # 轮到另一个玩家
        return state, 0


def calculate_remaining(round_state):
    blind_remaining = 0
    round_count = int(round_state['round_count'])
    round_remaining = 20 - round_count
    # print(round_remaining)

    blind_remaining += ((round_remaining // 2) + 1) * 5
    blind_remaining += (((round_remaining - 1) // 2) + 1) * 10
    print(blind_remaining)

    return blind_remaining


import matplotlib.pyplot as plt
def visualize_regret(mccfr):
    plt.plot(mccfr.regret_history)
    plt.xlabel('Iteration (x100)')
    plt.ylabel('Total Regret')
    plt.title('Total Regret Over Time')
    # plt.show()
    plt.savefig('./results/mccfr/regret_history.png')


import json
class MCCFRPlayer(BasePokerPlayer):
    def __init__(self, iterations=100000, model_file=None):
        super().__init__()
        self.iterations = iterations
        self.model_file = model_file
        self.mccfr = MCCFR(iterations)
        self.tracked_info_sets = ['C2CA', 'D3DA', 'H4HK', 'S5SJ', 'C6CQ']  # 你想监控的特定信息集
        self.regret_tracking = {info_set: [] for info_set in self.tracked_info_sets}

        if model_file and os.path.exists(model_file):
            try:
                print('Loading model...')
                self.load_model(model_file)
            except (EOFError, pickle.UnpicklingError):
                print("Model file is empty or corrupted, retraining...")
                self.train_model()
                if model_file:
                    self.save_model(model_file)
        else:
            print('Training model...')
            self.train_model()
            if model_file:
                self.save_model(model_file)

    def train_model(self):
        for i in range(self.iterations):
            state = self.init_game_state()
            self.mccfr.mccfr(state, player=0, pi=1.0)

            if (i + 1) % 100 == 0:  # 每100次迭代记录一次遗憾值
                for info_set in self.tracked_info_sets:
                    if info_set in self.mccfr.regret_sum:
                        self.regret_tracking[info_set].append(self.mccfr.regret_sum[info_set].copy())

        with open('regret_tracking.json', 'w') as f:
            json.dump(self.regret_tracking, f)
            print('Output regret_tracking.json')

    def declare_action(self, valid_actions, hole_card, round_state):
        state = self.init_game_state(hole_card, round_state)
        
        # 训练模型
        self.mccfr.mccfr(state, player=0, pi=1.0)
        
        # 打印当前遗憾值
        # print(f"Current regret_sum: {self.mccfr.regret_sum}")
        limited_regret_sum = {k: self.mccfr.regret_sum[k] for k in list(self.mccfr.regret_sum)[:2]}
        print(f"Current limited regret_sum: {limited_regret_sum}")
        print()

        blind_remaining = calculate_remaining(round_state)

        # print(round_state['seats'][0])
        # print('player 1: ', round_state['seats'][0]['stack'] + blind_remaining)
        # print('player 2: ', round_state['seats'][1]['stack'] - blind_remaining)


        # if round_state['seats'][0]['stack'] - blind_remaining >= round_state['seats'][1]['stack'] + blind_remaining:
        #     print("Fold with enough blind remaining")
        #     print(round_state['seats'][0]['stack'], round_state['seat'][1]['stack'], blind_remaining)

        #     fold_action_info = valid_actions[0]
        #     action, amount = fold_action_info["action"], fold_action_info["amount"]
        #     return action, amount
        
        player_uuid = self.uuid
        my_seat = next(seat for seat in round_state['seats'] if seat['uuid'] == player_uuid)
        opponent_seat = next(seat for seat in round_state['seats'] if seat['uuid'] != player_uuid)
        blind_remaining = calculate_remaining(round_state)
        
        print('player: ', my_seat['stack'] + blind_remaining)
        print('opponent: ', opponent_seat['stack'] - blind_remaining)

        if my_seat['stack'] - blind_remaining >= opponent_seat['stack'] + blind_remaining:
            print("Fold with enough blind remaining")
            print(opponent_seat['stack'], my_seat['stack'], blind_remaining)

            fold_action_info = valid_actions[0]
            action, amount = fold_action_info["action"], fold_action_info["amount"]
            return action, amount
        
        action = self.mccfr.get_action(state, state['current_player'])
        print(f"Action chosen: {action}")


        for valid_action in valid_actions:
            if valid_action['action'] == action:
                if action == 'raise':
                    min_amount = valid_action['amount']['min']
                    max_amount = valid_action['amount']['max']
                    amount = random.randint(min_amount, max_amount)
                    return action, amount
                elif action == 'call' and valid_action['amount'] == 0:
                    return 'call', 0
                else:
                    return action, valid_action['amount']
        return 'fold', 0

    # def load_model(self, filename):
    #     with open(filename, 'rb') as f:
    #         self.mccfr.regret_sum, self.mccfr.strategy_sum, self.mccfr.strategy = pickle.load(f)

    # def save_model(self, filename):
    #     with open(filename, 'wb') as f:
    #         pickle.dump((self.mccfr.regret_sum, self.mccfr.strategy_sum, self.mccfr.strategy), f)

    def init_game_state(self, hole_card=None, round_state=None):
        if hole_card is not None and round_state is not None:
            print("init successfully!!")
            # print(f"Init game state called with hole_card: {hole_card}, round_state: {round_state}")
            return {
                'player_hands': [hole_card, ['XX', 'XX']],
                'community_cards': round_state['community_card'],
                'current_bet': round_state['pot']['main']['amount'],
                'current_player': round_state['next_player'],
                'player_chips': [player['stack'] for player in round_state['seats']],
                'pot': round_state['pot']['main']['amount'],
                'actions': round_state['action_histories']
            }
        else:
            return {
                'player_hands': [['2H', '3D'], ['4S', '5C']],
                'community_cards': [],
                'current_bet': 0,
                'current_player': 0,
                'player_chips': [1000, 1000],
                'pot': 0,
                'actions': []
            }


    def load_model(self, filename):
        with open(filename, 'rb') as f:
            self.mccfr.regret_sum, self.mccfr.strategy_sum, self.mccfr.strategy = pickle.load(f)

    def save_model(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump((self.mccfr.regret_sum, self.mccfr.strategy_sum, self.mccfr.strategy), f)

    def receive_game_start_message(self, game_info):
        # print(f"Game start message: {game_info}")
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        # print(f"Round start message - Round count: {round_count}, Hole card: {hole_card}, Seats: {seats}")
        pass

    def receive_street_start_message(self, street, round_state):
        # print(f"Street start message - Street: {street}, Round state: {round_state}")
        pass

    def receive_game_update_message(self, action, round_state):
        # print(f"Game update message - Action: {action}, Round state: {round_state}")
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        # print(f"Round result message - Winners: {winners}, Hand info: {hand_info}, Round state: {round_state}")
        pass

def setup_ai():
    return MCCFRPlayer(model_file="mccfr_model.pkl")


# ================================================================================================================
# ======================================== The above is the original code ========================================
# ================================================================================================================



# import os
# import pickle
# from game.players import BasePokerPlayer
# from collections import defaultdict
# import random
# import matplotlib.pyplot as plt

# def default_float_dict():
#     return defaultdict(float)

# class MCCFR:
#     def __init__(self, iterations=10000):
#         self.iterations = iterations
#         self.regret_sum = defaultdict(default_float_dict)
#         self.strategy_sum = defaultdict(default_float_dict)
#         self.strategy = defaultdict(default_float_dict)
#         self.regret_history = []

#     def get_strategy(self, info_set, actions):
#         strategy = self.strategy[info_set]
#         normalizing_sum = sum(strategy.values())
#         if normalizing_sum > 0:
#             return {a: p / normalizing_sum for a, p in strategy.items()}
#         else:
#             return {a: 1.0 / len(actions) for a in actions}

#     def update_strategy(self, info_set, actions, regret):
#         for action in regret:
#             self.regret_sum[info_set][action] += regret[action]
#             self.strategy[info_set][action] = max(self.regret_sum[info_set][action], 0.0)

#     def mccfr(self, state, player, pi):
#         if self.is_terminal(state):
#             return self.get_terminal_utility(state, player)

#         info_set = self.get_info_set(state, player)
#         actions = self.get_possible_actions(state)
#         strategy = self.get_strategy(info_set, actions)

#         action_utilities = {}
#         node_util = 0
#         for action in actions:
#             new_state, reward = self.play_action(state.copy(), action)
#             action_util = reward + self.mccfr(new_state, 1 - player, pi * strategy[action])
#             action_utilities[action] = action_util
#             node_util += strategy[action] * action_util

#         for action in actions:
#             regret = {action: action_utilities[action] - node_util}
#             self.update_strategy(info_set, actions, regret)

#         return node_util

#     def get_info_set(self, state, player):
#         hand = ''.join(sorted(state['player_hands'][player]))
#         community = ''.join(sorted(state['community_cards']))
#         return hand + '|' + community

#     def get_action(self, state, player):
#         info_set = self.get_info_set(state, player)
#         actions = self.get_possible_actions(state)
#         strategy = self.get_strategy(info_set, actions)
#         return random.choices(list(strategy.keys()), weights=strategy.values(), k=1)[0]

#     def is_terminal(self, state):
#         return any(chips <= 0 for chips in state['player_chips'])

#     def get_terminal_utility(self, state, player):
#         if state['player_chips'][player] > state['player_chips'][1 - player]:
#             return 1
#         elif state['player_chips'][player] < state['player_chips'][1 - player]:
#             return -1
#         else:
#             return 0

#     def get_possible_actions(self, state):
#         actions = ['fold', 'call']
#         if state['player_chips'][state['current_player']] > state['current_bet']:
#             actions.append('raise')
#         return actions

#     def play_action(self, state, action):
#         current_player = state['current_player']
#         if action == 'fold':
#             state['player_chips'][1 - current_player] += state['pot']
#             state['pot'] = 0
#             state['player_chips'][current_player] = 0
#             return state, -1
#         elif action == 'call':
#             state['player_chips'][current_player] -= state['current_bet']
#             state['pot'] += state['current_bet']
#         elif action == 'raise':
#             raise_amount = min(100, state['player_chips'][current_player])
#             state['player_chips'][current_player] -= raise_amount
#             state['pot'] += raise_amount
#             state['current_bet'] = raise_amount

#         state['current_player'] = 1 - current_player
#         return state, 0

# def calculate_remaining(round_state):
#     blind_remaining = 0
#     round_count = int(round_state['round_count'])
#     round_remaining = 20 - round_count

#     blind_remaining += ((round_remaining // 2) + 1) * 5
#     blind_remaining += (((round_remaining - 1) // 2) + 1) * 10
#     print(blind_remaining)

#     return blind_remaining

# def visualize_regret(mccfr):
#     plt.plot(mccfr.regret_history)
#     plt.xlabel('Iteration (x100)')
#     plt.ylabel('Total Regret')
#     plt.title('Total Regret Over Time')
#     plt.savefig('./results/mccfr/regret_history.png')
#     plt.show()

# class MCCFRPlayer(BasePokerPlayer):
#     def __init__(self, iterations=100000, model_file=None):
#         super().__init__()
#         self.iterations = iterations
#         self.model_file = model_file
#         self.mccfr = MCCFR(iterations)
#         self.tracked_info_sets = ['C2CA', 'D3DA', 'H4HK', 'S5SJ', 'C6CQ']
#         self.regret_tracking = {info_set: [] for info_set in self.tracked_info_sets}

#         if model_file and os.path.exists(model_file):
#             try:
#                 print('Loading model...')
#                 self.load_model(model_file)
#             except (EOFError, pickle.UnpicklingError):
#                 print("Model file is empty or corrupted, retraining...")
#                 self.train_model()
#                 if model_file:
#                     self.save_model(model_file)
#         else:
#             print('Training model...')
#             self.train_model()
#             if model_file:
#                 self.save_model(model_file)

#     def train_model(self):
#         pass

#     def declare_action(self, valid_actions, hole_card, round_state):
#         state = self.init_game_state(hole_card, round_state)
        
#         # 训练模型
#         for _ in range(self.iterations):
#             self.mccfr.mccfr(state, player=0, pi=1.0)
#             if (len(self.mccfr.regret_history) + 1) % 100 == 0:
#                 total_regret = sum([sum(regrets.values()) for regrets in self.mccfr.regret_sum.values()])
#                 self.mccfr.regret_history.append(total_regret)
        
#         # 打印当前遗憾值
#         limited_regret_sum = {k: self.mccfr.regret_sum[k] for k in list(self.mccfr.regret_sum)[:2]}
#         print(f"Current limited regret_sum: {limited_regret_sum}")
#         print()

#         blind_remaining = calculate_remaining(round_state)
#         print(round_state['seats'][0])
#         print('player 1: ', round_state['seats'][0]['stack'] + blind_remaining)
#         print('player 2: ', round_state['seats'][1]['stack'] - blind_remaining)

#         if round_state['seats'][0]['stack'] - blind_remaining >= round_state['seats'][1]['stack'] + blind_remaining:
#             print("Fold with enough blind remaining")
#             print(round_state['seats'][0]['stack'], round_state['seat'][1]['stack'], blind_remaining)

#             fold_action_info = valid_actions[0]
#             action, amount = fold_action_info["action"], fold_action_info["amount"]
#             return action, amount

#         action = self.mccfr.get_action(state, state['current_player'])
#         print(f"Action chosen: {action}")

#         for valid_action in valid_actions:
#             if valid_action['action'] == action:
#                 if action == 'raise':
#                     min_amount = valid_action['amount']['min']
#                     max_amount = valid_action['amount']['max']
#                     amount = random.randint(min_amount, max_amount)
#                     return action, amount
#                 elif action == 'call' and valid_action['amount'] == 0:
#                     return 'call', 0
#                 else:
#                     return action, valid_action['amount']
#         return 'fold', 0

#     def init_game_state(self, hole_card=None, round_state=None):
#         if hole_card is not None and round_state is not None:
#             print("init successfully!!")
#             return {
#                 'player_hands': [hole_card, ['XX', 'XX']],
#                 'community_cards': round_state['community_card'],
#                 'current_bet': round_state['pot']['main']['amount'],
#                 'current_player': round_state['next_player'],
#                 'player_chips': [player['stack'] for player in round_state['seats']],
#                 'pot': round_state['pot']['main']['amount'],
#                 'actions': round_state['action_histories']
#             }
#         else:
#             return {
#                 'player_hands': [['2H', '3D'], ['4S', '5C']],
#                 'community_cards': [],
#                 'current_bet': 0,
#                 'current_player': 0,
#                 'player_chips': [1000, 1000],
#                 'pot': 0,
#                 'actions': []
#             }

#     def load_model(self, filename):
#         with open(filename, 'rb') as f:
#             self.mccfr.regret_sum, self.mccfr.strategy_sum, self.mccfr.strategy = pickle.load(f)

#     def save_model(self, filename):
#         with open(filename, 'wb') as f:
#             pickle.dump((self.mccfr.regret_sum, self.mccfr.strategy_sum, self.mccfr.strategy), f)

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

# def setup_ai():
#     return MCCFRPlayer(model_file="mccfr_model.pkl")



# import os
# import pickle
# from game.players import BasePokerPlayer
# from collections import defaultdict
# import random

# def default_float_dict():
#     return defaultdict(float)

# class MCCFR:
#     def __init__(self, iterations=10000):
#         self.iterations = iterations
#         self.regret_sum = defaultdict(default_float_dict)
#         self.strategy_sum = defaultdict(default_float_dict)
#         self.strategy = defaultdict(default_float_dict)
#         self.regret_history = []

#     def get_strategy(self, info_set, actions):
#         strategy = self.strategy[info_set]
#         normalizing_sum = sum(strategy.values())
#         if normalizing_sum > 0:
#             return {a: p / normalizing_sum for a, p in strategy.items()}
#         else:
#             return {a: 1.0 / len(actions) for a in actions}

#     def update_strategy(self, info_set, actions, regret):
#         for action in regret:
#             self.regret_sum[info_set][action] += regret[action]
#             self.strategy[info_set][action] = max(self.regret_sum[info_set][action], 0.0)

#     def mccfr(self, state, player, pi):
#         if self.is_terminal(state):
#             return self.get_terminal_utility(state, player)

#         info_set = self.get_info_set(state, player)
#         actions = self.get_possible_actions(state)
#         strategy = self.get_strategy(info_set, actions)

#         action_utilities = {}
#         node_util = 0
#         for action in actions:
#             new_state, reward = self.play_action(state.copy(), action)
#             action_util = reward + self.mccfr(new_state, 1 - player, pi * strategy[action])
#             action_utilities[action] = action_util
#             node_util += strategy[action] * action_util

#         for action in actions:
#             regret = {action: action_utilities[action] - node_util}
#             self.update_strategy(info_set, actions, regret)

#         if (len(self.regret_history) + 1) % 100 == 0:
#             total_regret = sum([sum(regrets.values()) for regrets in self.regret_sum.values()])
#             self.regret_history.append(total_regret)

#         return node_util

#     def get_info_set(self, state, player):
#         hand = ''.join(sorted(state['player_hands'][player]))
#         community = ''.join(sorted(state['community_cards']))
#         return hand + '|' + community

#     def get_action(self, state, player):
#         info_set = self.get_info_set(state, player)
#         actions = self.get_possible_actions(state)
#         strategy = self.get_strategy(info_set, actions)
#         return random.choices(list(strategy.keys()), weights=strategy.values(), k=1)[0]

#     def is_terminal(self, state):
#         return any(chips <= 0 for chips in state['player_chips'])

#     def get_terminal_utility(self, state, player):
#         if state['player_chips'][player] > state['player_chips'][1 - player]:
#             return 1
#         elif state['player_chips'][player] < state['player_chips'][1 - player]:
#             return -1
#         else:
#             return 0

#     def get_possible_actions(self, state):
#         actions = ['fold', 'call']
#         if state['player_chips'][state['current_player']] > state['current_bet']:
#             actions.append('raise')
#         return actions

#     def play_action(self, state, action):
#         current_player = state['current_player']
#         if action == 'fold':
#             state['player_chips'][1 - current_player] += state['pot']
#             state['pot'] = 0
#             state['player_chips'][current_player] = 0  # 当前玩家输了
#             return state, -1
#         elif action == 'call':
#             state['player_chips'][current_player] -= state['current_bet']
#             state['pot'] += state['current_bet']
#         elif action == 'raise':
#             raise_amount = min(100, state['player_chips'][current_player])
#             state['player_chips'][current_player] -= raise_amount
#             state['pot'] += raise_amount
#             state['current_bet'] = raise_amount

#         state['current_player'] = 1 - current_player  # 轮到另一个玩家
#         return state, 0


# import matplotlib.pyplot as plt
# def visualize_regret(mccfr):
#     plt.plot(mccfr.regret_history)
#     plt.xlabel('Iteration (x100)')
#     plt.ylabel('Total Regret')
#     plt.title('Total Regret Over Time')
#     plt.savefig('./results/mccfr/regret_history.png')
#     print('figure saved as ./results/mccfr/regret_history.png')
#     plt.show()


# class MCCFRPlayer(BasePokerPlayer):
#     def __init__(self, iterations=100000, model_file=None):
#         super().__init__()
#         self.iterations = iterations
#         self.model_file = model_file
#         self.mccfr = MCCFR(iterations)
#         self.tracked_info_sets = ['C2CA', 'D3DA', 'H4HK', 'S5SJ', 'C6CQ']  # 你想监控的特定信息集
#         self.regret_tracking = {info_set: [] for info_set in self.tracked_info_sets}

#         if model_file and os.path.exists(model_file):
#             try:
#                 print('Loading model...')
#                 self.load_model(model_file)
#             except (EOFError, pickle.UnpicklingError):
#                 print("Model file is empty or corrupted, retraining...")
#                 self.train_model()
#                 if model_file:
#                     self.save_model(model_file)
#         else:
#             print('Training model...')
#             self.train_model()
#             if model_file:
#                 self.save_model(model_file)

#     def train_model(self):
#         pass

#     def declare_action(self, valid_actions, hole_card, round_state):
#         state = self.init_game_state(hole_card, round_state)
        
#         # 训练模型
#         self.mccfr.mccfr(state, player=0, pi=1.0)
        
#         # 打印当前遗憾值
#         limited_regret_sum = {k: self.mccfr.regret_sum[k] for k in list(self.mccfr.regret_sum)[:2]}
#         print(f"Current limited regret_sum: {limited_regret_sum}")
#         print()

#         blind_remaining = calculate_remaining(round_state)
#         print(round_state['seats'][0])
#         print('player 1: ', round_state['seats'][0]['stack'] + blind_remaining)
#         print('player 2: ', round_state['seats'][1]['stack'] - blind_remaining)


#         if round_state['seats'][0]['stack'] - blind_remaining >= round_state['seats'][1]['stack'] + blind_remaining:
#             print("Fold with enough blind remaining")
#             print(round_state['seats'][0]['stack'], round_state['seat'][1]['stack'], blind_remaining)

#             fold_action_info = valid_actions[0]
#             action, amount = fold_action_info["action"], fold_action_info["amount"]
#             return action, amount

#         action = self.mccfr.get_action(state, state['current_player'])
#         print(f"Action chosen: {action}")

#         for valid_action in valid_actions:
#             if valid_action['action'] == action:
#                 if action == 'raise':
#                     min_amount = valid_action['amount']['min']
#                     max_amount = valid_action['amount']['max']
#                     amount = random.randint(min_amount, max_amount)
#                     return action, amount
#                 elif action == 'call' and valid_action['amount'] == 0:
#                     return 'call', 0
#                 else:
#                     return action, valid_action['amount']
#         return 'fold', 0

#     def init_game_state(self, hole_card=None, round_state=None):
#         if hole_card is not None and round_state is not None:
#             print("init successfully!!")
#             return {
#                 'player_hands': [hole_card, ['XX', 'XX']],
#                 'community_cards': round_state['community_card'],
#                 'current_bet': round_state['pot']['main']['amount'],
#                 'current_player': round_state['next_player'],
#                 'player_chips': [player['stack'] for player in round_state['seats']],
#                 'pot': round_state['pot']['main']['amount'],
#                 'actions': round_state['action_histories']
#             }
#         else:
#             return {
#                 'player_hands': [['2H', '3D'], ['4S', '5C']],
#                 'community_cards': [],
#                 'current_bet': 0,
#                 'current_player': 0,
#                 'player_chips': [1000, 1000],
#                 'pot': 0,
#                 'actions': []
#             }

#     def load_model(self, filename):
#         with open(filename, 'rb') as f:
#             self.mccfr.regret_sum, self.mccfr.strategy_sum, self.mccfr.strategy = pickle.load(f)

#     def save_model(self, filename):
#         with open(filename, 'wb') as f:
#             pickle.dump((self.mccfr.regret_sum, self.mccfr.strategy_sum, self.mccfr.strategy), f)

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

# def setup_ai():
#     return MCCFRPlayer(model_file="mccfr_model.pkl")


# ================================================================================================================
# ======================================== The above is the modified code ========================================
# ================================================================================================================









# class MCCFRPlayer(BasePokerPlayer):
#     def __init__(self, iterations=100000, model_file=None):  # 这里设置迭代次数
#         super().__init__()
#         self.iterations = iterations
#         self.model_file = model_file
#         self.mccfr = MCCFR(iterations)
        
#         if model_file and os.path.exists(model_file):
#             try:
#                 print('loading model!!!!!!!!')
#                 self.load_model(model_file)
#                 # self.train_model()
#             except (EOFError, pickle.UnpicklingError):
#                 print("Model file is empty or corrupted, retraining...")
#                 self.train_model()
#                 if model_file:
#                     self.save_model(model_file)
#         else:
#             print('training model!')
#             self.train_model()
#             if model_file:
#                 self.save_model(model_file)

#     def declare_action(self, valid_actions, hole_card, round_state):
#         # print(f"Declare action called with valid_actions: {valid_actions}, hole_card: {hole_card}, round_state: {round_state}")
#         state = self.create_state(hole_card, round_state)
#         action = self.mccfr.get_action(state, state['current_player'])
#         # print(f"Action chosen: {action}")

#         for valid_action in valid_actions:
#             if valid_action['action'] == action:
#                 if action == 'raise':
#                     min_amount = valid_action['amount']['min']
#                     max_amount = valid_action['amount']['max']
#                     amount = random.randint(min_amount, max_amount)  # 选择一个合法的数值
#                     return action, amount
#                 else:
#                     return action, valid_action['amount']
#         return 'fold', 0


#     def create_state(self, hole_card, round_state):
#         player_hands = []
#         for seat in round_state['seats']:
#             if seat['uuid'] == self.uuid:
#                 player_hands.append(hole_card)
#             else:
#                 player_hands.append(['XX', 'XX'])  # 隐藏其他玩家的手牌

#         state = {
#             'player_hands': player_hands,
#             'community_cards': round_state['community_card'],
#             'current_bet': round_state['pot']['main']['amount'],
#             'current_player': round_state['next_player'],
#             'player_chips': [seat['stack'] for seat in round_state['seats']],
#             'pot': round_state['pot']['main']['amount'],
#             'actions': round_state['action_histories']
#         }
#         # print(f"Created state: {state}")
#         return state

#     def train_model(self):
#         # regrets_over_time = []
#         # for i in range(self.mccfr.iterations):
#         #     state = self.init_game_state()
#         #     self.mccfr.mccfr(state, player=0, pi=1.0)
#         #     if (i + 1) % 100 == 0:  # 每100次迭代记录一次遗憾值
#         #         regrets_over_time.append(self.mccfr.regret_sum.copy())
#         #         print(f"Iteration {i + 1}: regret_sum = {self.mccfr.regret_sum}")

#         initial_hands = [['2H', '3D'], ['4S', '5C']]
#         initial_round_state = {
#             'street': 'preflop',
#             'pot': {'main': {'amount': 0}, 'side': []},
#             'community_card': [],
#             'dealer_btn': 0,
#             'next_player': 0,
#             'small_blind_pos': 0,
#             'big_blind_pos': 1,
#             'round_count': 0,
#             'small_blind_amount': 5,
#             'seats': [
#                 {'name': 'mccfr', 'uuid': 'player1', 'stack': 1000, 'state': 'participating'},
#                 {'name': 'baseline', 'uuid': 'player2', 'stack': 1000, 'state': 'participating'}
#             ],
#             'action_histories': {'preflop': []}
#         }
#         self.mccfr.train(self, initial_hands, initial_round_state)

#     def init_game_state(self, initial_hands, initial_round_state):
#         return {
#             'player_hands': initial_hands,
#             'community_cards': initial_round_state['community_card'],
#             'current_bet': 0,
#             'current_player': 0,
#             'player_chips': [seat['stack'] for seat in initial_round_state['seats']],
#             'pot': 0,
#             'actions': initial_round_state['action_histories']
#         }

#     def load_model(self, filename):
#         with open(filename, 'rb') as f:
#             self.mccfr.regret_sum, self.mccfr.strategy_sum, self.mccfr.strategy = pickle.load(f)

#     def save_model(self, filename):
#         with open(filename, 'wb') as f:
#             pickle.dump((self.mccfr.regret_sum, self.mccfr.strategy_sum, self.mccfr.strategy), f)

#     # def receive_game_start_message(self, game_info):
#     #     print(f"Game started with info: {game_info}")

#     # def receive_round_start_message(self, round_count, hole_card, seats):
#     #     print(f"Round {round_count} started with hole_card: {hole_card}, seats: {seats}")

#     # def receive_street_start_message(self, street, round_state):
#     #     print(f"Street {street} started with round_state: {round_state}")

#     # def receive_game_update_message(self, action, round_state):
#     #     print(f"Game updated with action: {action}, round_state: {round_state}")

#     # def receive_round_result_message(self, winners, hand_info, round_state):
#     #     print(f"Round ended. Winners: {winners}, hand_info: {hand_info}, round_state: {round_state}")

    # def receive_game_start_message(self, game_info):
    #     # print(f"Game start message: {game_info}")
    #     pass

    # def receive_round_start_message(self, round_count, hole_card, seats):
    #     # print(f"Round start message - Round count: {round_count}, Hole card: {hole_card}, Seats: {seats}")
    #     pass

    # def receive_street_start_message(self, street, round_state):
    #     # print(f"Street start message - Street: {street}, Round state: {round_state}")
    #     pass

    # def receive_game_update_message(self, action, round_state):
    #     # print(f"Game update message - Action: {action}, Round state: {round_state}")
    #     pass

    # def receive_round_result_message(self, winners, hand_info, round_state):
    #     # print(f"Round result message - Winners: {winners}, Hand info: {hand_info}, Round state: {round_state}")
    #     pass

# def setup_ai():
#     return MCCFRPlayer(model_file="mccfr_model.pkl")





# class MCCFRPlayer(BasePokerPlayer):
#     def __init__(self, iterations=100000, model_file=None):  # 增加迭代次数
#         super().__init__()
#         self.iterations = iterations
#         self.model_file = model_file
#         self.mccfr = MCCFR(iterations)
        
#         if model_file and os.path.exists(model_file):
#             try:
#                 print('Loading Model!!!!!')
#                 self.load_model(model_file)
#             except (EOFError, pickle.UnpicklingError):
#                 print("Model file is empty or corrupted, retraining...")
#                 self.train_model()
#                 if model_file:
#                     self.save_model(model_file)
#         else:
#             self.train_model()
#             if model_file:
#                 self.save_model(model_file)

#     def declare_action(self, valid_actions, hole_card, round_state):
#         # print(f"Declare action called with valid_actions: {valid_actions}, hole_card: {hole_card}, round_state: {round_state}")
#         state = self.create_state(hole_card, round_state)
#         action = self.mccfr.get_action(state, state['current_player'])
#         # print(f"Action chosen: {action}")
#         for valid_action in valid_actions:
#             if valid_action['action'] == action:
#                 return action, valid_action['amount']
#         return 'fold', 0

#     def create_state(self, hole_card, round_state):
#         player_hands = []
#         for seat in round_state['seats']:
#             if seat['uuid'] == self.uuid:
#                 player_hands.append(hole_card)
#             else:
#                 player_hands.append(['XX', 'XX'])  # 隐藏其他玩家的手牌

#         state = {
#             'player_hands': player_hands,
#             'community_cards': round_state['community_card'],
#             'current_bet': round_state['pot']['main']['amount'],
#             'current_player': round_state['next_player'],
#             'player_chips': [seat['stack'] for seat in round_state['seats']],
#             'pot': round_state['pot']['main']['amount'],
#             'actions': round_state['action_histories']
#         }
#         # print(f"Created state: {state}")
#         return state

#     def train_model(self):
#         for _ in range(self.iterations):
#             state = self.init_game_state()
#             self.mccfr.mccfr(state, player=0, pi=1.0)

#     def init_game_state(self):
#         return {
#             'player_hands': [['2H', '3D'], ['4S', '5C']],
#             'community_cards': [],
#             'current_bet': 0,
#             'current_player': 0,
#             'player_chips': [1000, 1000],
#             'pot': 0,
#             'actions': []
#         }

#     def train_model(self):
#         for _ in range(self.iterations):
#             state = self.init_game_state()
#             self.mccfr.mccfr(state, player=0, pi=1.0)

#     def init_game_state(self):
#         return {
#             'player_hands': [['2H', '3D'], ['4S', '5C']],
#             'community_cards': [],
#             'current_bet': 0,
#             'current_player': 0,
#             'player_chips': [1000, 1000],
#             'pot': 0,
#             'actions': []
#         }

#     def load_model(self, filename):
#         with open(filename, 'rb') as f:
#             self.mccfr.regret_sum, self.mccfr.strategy_sum, self.mccfr.strategy = pickle.load(f)

#     def save_model(self, filename):
#         with open(filename, 'wb') as f:
#             pickle.dump((self.mccfr.regret_sum, self.mccfr.strategy_sum, self.mccfr.strategy), f)

#     # def receive_game_start_message(self, game_info):
#     #     print(f"Game started with info: {game_info}")
#     #     print()

#     # def receive_round_start_message(self, round_count, hole_card, seats):
#     #     print(f"Round {round_count} started with hole_card: {hole_card}, seats: {seats}")
#     #     print()

#     # def receive_street_start_message(self, street, round_state):
#     #     print(f"Street {street} started with round_state: {round_state}")
#     #     print()

#     # def receive_game_update_message(self, action, round_state):
#     #     print(f"Game updated with action: {action}, round_state: {round_state}")
#     #     print()

#     # def receive_round_result_message(self, winners, hand_info, round_state):
#     #     print(f"Round ended. Winners: {winners}, hand_info: {hand_info}, round_state: {round_state}")
#     #     print()

#     def receive_game_start_message(self, game_info):
#         # print(f"Game start message: {game_info}")
#         pass

#     def receive_round_start_message(self, round_count, hole_card, seats):
#         # print(f"Round start message - Round count: {round_count}, Hole card: {hole_card}, Seats: {seats}")
#         pass

#     def receive_street_start_message(self, street, round_state):
#         # print(f"Street start message - Street: {street}, Round state: {round_state}")
#         pass

#     def receive_game_update_message(self, action, round_state):
#         # print(f"Game update message - Action: {action}, Round state: {round_state}")
#         pass

#     def receive_round_result_message(self, winners, hand_info, round_state):
#         # print(f"Round result message - Winners: {winners}, Hand info: {hand_info}, Round state: {round_state}")
#         pass

# def setup_ai():
#     return MCCFRPlayer(model_file="mccfr_model.pkl")



# import os
# import pickle
# from game.players import BasePokerPlayer
# from collections import defaultdict
# import random  # Don't forget to import the random module

# def default_float_dict():
#     return defaultdict(float)

# class MCCFR:
#     def __init__(self, iterations=10000):  # 默认值为10000，你可以传入更大的值
#         self.iterations = iterations
#         self.regret_sum = defaultdict(default_float_dict)
#         self.strategy_sum = defaultdict(default_float_dict)
#         self.strategy = defaultdict(default_float_dict)

#     # def __init__(self, iterations=10000):
#     #     self.iterations = iterations
#     #     self.regret_sum = {}
#     #     self.strategy_sum = {}
#     #     self.strategy = {}

#     def get_strategy(self, info_set, actions):
#         strategy = self.strategy[info_set]
#         normalizing_sum = sum(strategy.values())
#         if normalizing_sum > 0:
#             return {a: p / normalizing_sum for a, p in strategy.items()}
#         else:
#             return {a: 1.0 / len(actions) for a in actions}

#     def update_strategy(self, info_set, actions, regret):
#         for action in regret:
#             self.regret_sum[info_set][action] += regret[action]
#             self.strategy[info_set][action] = max(self.regret_sum[info_set][action], 0.0)

#     # def mccfr(self, state, player, pi):
#     #     if self.is_terminal(state):
#     #         return self.get_terminal_utility(state, player)

#     #     info_set = self.get_info_set(state, player)
#     #     actions = self.get_possible_actions(state)
#     #     strategy = self.get_strategy(info_set, actions)

#     #     action_utilities = {}
#     #     node_util = 0
#     #     for action in actions:
#     #         new_state, reward = self.play_action(state.copy(), action)
#     #         action_util = reward + self.mccfr(new_state, 1 - player, pi * strategy[action])
#     #         action_utilities[action] = action_util
#     #         node_util += strategy[action] * action_util

#     #     for action in actions:
#     #         regret = action_utilities[action] - node_util
#     #         self.update_strategy(info_set, actions, {action: regret})

#     #     return node_util
    
#     def mccfr(self, state, player, pi):
#         if self.is_terminal(state):
#             return self.get_terminal_utility(state, player)

#         info_set = self.get_info_set(state, player)
#         actions = self.get_possible_actions(state)
#         strategy = self.get_strategy(info_set, actions)

#         action_utilities = {}
#         node_util = 0
#         for action in actions:
#             new_state, reward = self.play_action(state.copy(), action)
#             action_util = reward + self.mccfr(new_state, 1 - player, pi * strategy[action])
#             action_utilities[action] = action_util
#             node_util += strategy[action] * action_util

#         for action in actions:
#             regret = {action: action_utilities[action] - node_util}
#             self.update_strategy(info_set, actions, regret)

#         return node_util

#     def train(self, game, initial_hands, initial_round_state):
#         for _ in range(self.iterations):
#             state = self.init_game_state(initial_hands, initial_round_state)
#             print(state)
#             self.mccfr(state, player=0, pi=1.0)

#     def get_info_set(self, state, player):
#         hand = ''.join(sorted(state['player_hands'][player]))
#         community = ''.join(sorted(state['community_cards']))
#         return hand + '|' + community

#     def get_action(self, state, player):
#         info_set = self.get_info_set(state, player)
#         actions = self.get_possible_actions(state)
#         strategy = self.get_strategy(info_set, actions)
#         return random.choices(list(strategy.keys()), weights=strategy.values(), k=1)[0]

#     def is_terminal(self, state):
#         return any(chips <= 0 for chips in state['player_chips'])

#     def get_terminal_utility(self, state, player):
#         if state['player_chips'][player] > state['player_chips'][1 - player]:
#             return 1
#         elif state['player_chips'][player] < state['player_chips'][1 - player]:
#             return -1
#         else:
#             return 0

#     def get_possible_actions(self, state):
#         actions = ['fold', 'call']
#         if state['player_chips'][state['current_player']] > state['current_bet']:
#             actions.append('raise')
#         return actions

#     def play_action(self, state, action):
#         current_player = state['current_player']
#         if action == 'fold':
#             state['player_chips'][1 - current_player] += state['pot']
#             state['pot'] = 0
#             state['player_chips'][current_player] = 0  # 当前玩家输了
#             return state, -1
#         elif action == 'call':
#             state['player_chips'][current_player] -= state['current_bet']
#             state['pot'] += state['current_bet']
#         elif action == 'raise':
#             raise_amount = min(100, state['player_chips'][current_player])
#             state['player_chips'][current_player] -= raise_amount
#             state['pot'] += raise_amount
#             state['current_bet'] = raise_amount

#         state['current_player'] = 1 - current_player  # 轮到另一个玩家
#         return state, 0


# # def calculate_remaining(round_state):
# #     blind_remaining = 0
# #     round_count = int(round_state['round_count'])
# #     round_remaining = 20 - round_count
# #     # print(round_remaining)

# #     blind_remaining += ((round_remaining // 2) + 1) * 5
# #     blind_remaining += (((round_remaining - 1) // 2) + 1) * 10
# #     print(blind_remaining)

# #     return blind_remaining


# import json
# class MCCFRPlayer(BasePokerPlayer):
#     def __init__(self, iterations=100000, model_file=None):
#         super().__init__()
#         self.iterations = iterations
#         self.model_file = model_file
#         self.mccfr = MCCFR(iterations)
#         self.tracked_info_sets = ['C2CA', 'D3DA', 'H4HK', 'S5SJ', 'C6CQ']  # 你想监控的特定信息集
#         self.regret_tracking = {info_set: [] for info_set in self.tracked_info_sets}

#         if model_file and os.path.exists(model_file):
#             try:
#                 print('Loading model...')
#                 self.load_model(model_file)
#             except (EOFError, pickle.UnpicklingError):
#                 print("Model file is empty or corrupted, retraining...")
#                 self.train_model()
#                 if model_file:
#                     self.save_model(model_file)
#         else:
#             print('Training model...')
#             self.train_model()
#             if model_file:
#                 self.save_model(model_file)

#     def train_model(self):
#         for i in range(self.iterations):
#             state = self.init_game_state()
#             self.mccfr.mccfr(state, player=0, pi=1.0)

#             if (i + 1) % 100 == 0:  # 每100次迭代记录一次遗憾值
#                 for info_set in self.tracked_info_sets:
#                     if info_set in self.mccfr.regret_sum:
#                         self.regret_tracking[info_set].append(self.mccfr.regret_sum[info_set].copy())

#         with open('regret_tracking.json', 'w') as f:
#             json.dump(self.regret_tracking, f)
#             print('Output regret_tracking.json')

#     def declare_action(self, valid_actions, hole_card, round_state):
#         state = self.init_game_state(hole_card, round_state)
        
#         # 训练模型
#         self.mccfr.mccfr(state, player=0, pi=1.0)
        
#         # # 打印当前遗憾值
#         # print(f"Current regret_sum: {self.mccfr.regret_sum}")

#         limited_regret_sum = {k: self.mccfr.regret_sum[k] for k in list(self.mccfr.regret_sum)[:3]}
#         print(f"Current limited regret_sum: {limited_regret_sum}")
#         print()

#         # with open('regret_tracking.json', 'r') as f:
#         #     json.dump(limited_regret_sum, f)
#         #     print('Output regret_tracking.json')

#         # blind_remaining = calculate_remaining(round_state)

#         # print(round_state['seats'][1])
#         # print('player 1: ', round_state['seats'][0]['stack'] + blind_remaining)
#         # print('player 2: ', round_state['seats'][1]['stack'] - blind_remaining)

#         # if round_state['seats'][1]['stack'] - blind_remaining >= round_state['seats'][0]['stack'] + blind_remaining:
#         #     print("Fold with enough blind remaining")
#         #     print(round_state['seats'][1]['stack'], round_state['seat'][0]['stack'], blind_remaining)

#         #     fold_action_info = valid_actions[0]
#         #     action, amount = fold_action_info["action"], fold_action_info["amount"]
#         #     return action, amount

#         action = self.mccfr.get_action(state, state['current_player'])
#         # print(f"Action chosen: {action}")

#         for valid_action in valid_actions:
#             if valid_action['action'] == action:
#                 if action == 'raise':
#                     min_amount = valid_action['amount']['min']
#                     max_amount = valid_action['amount']['max']
#                     amount = random.randint(min_amount, max_amount)
#                     return action, amount
#                 elif action == 'call' and valid_action['amount'] == 0:
#                     return 'call', 0
#                 else:
#                     return action, valid_action['amount']
#         return 'fold', 0

#     # def load_model(self, filename):
#     #     with open(filename, 'rb') as f:
#     #         self.mccfr.regret_sum, self.mccfr.strategy_sum, self.mccfr.strategy = pickle.load(f)

#     # def save_model(self, filename):
#     #     with open(filename, 'wb') as f:
#     #         pickle.dump((self.mccfr.regret_sum, self.mccfr.strategy_sum, self.mccfr.strategy), f)

#     def init_game_state(self, hole_card=None, round_state=None):
#         if hole_card is not None and round_state is not None:
#             print("init successfully!!")
#             # print(f"Init game state called with hole_card: {hole_card}, round_state: {round_state}")
#             return {
#                 'player_hands': [hole_card, ['XX', 'XX']],
#                 'community_cards': round_state['community_card'],
#                 'current_bet': round_state['pot']['main']['amount'],
#                 'current_player': round_state['next_player'],
#                 'player_chips': [player['stack'] for player in round_state['seats']],
#                 'pot': round_state['pot']['main']['amount'],
#                 'actions': round_state['action_histories']
#             }
#         else:
#             return {
#                 'player_hands': [['2H', '3D'], ['4S', '5C']],
#                 'community_cards': [],
#                 'current_bet': 0,
#                 'current_player': 0,
#                 'player_chips': [1000, 1000],
#                 'pot': 0,
#                 'actions': []
#             }


#     def load_model(self, filename):
#         with open(filename, 'rb') as f:
#             self.mccfr.regret_sum, self.mccfr.strategy_sum, self.mccfr.strategy = pickle.load(f)

#     def save_model(self, filename):
#         with open(filename, 'wb') as f:
#             pickle.dump((self.mccfr.regret_sum, self.mccfr.strategy_sum, self.mccfr.strategy), f)

#     def receive_game_start_message(self, game_info):
#         # print(f"Game start message: {game_info}")
#         pass

#     def receive_round_start_message(self, round_count, hole_card, seats):
#         # print(f"Round start message - Round count: {round_count}, Hole card: {hole_card}, Seats: {seats}")
#         pass

#     def receive_street_start_message(self, street, round_state):
#         # print(f"Street start message - Street: {street}, Round state: {round_state}")
#         pass

#     def receive_game_update_message(self, action, round_state):
#         # print(f"Game update message - Action: {action}, Round state: {round_state}")
#         pass

#     def receive_round_result_message(self, winners, hand_info, round_state):
#         # print(f"Round result message - Winners: {winners}, Hand info: {hand_info}, Round state: {round_state}")
#         pass

# def setup_ai():
#     return MCCFRPlayer(model_file="mccfr_model.pkl")

