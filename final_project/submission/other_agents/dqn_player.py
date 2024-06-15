import os
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque, defaultdict

from game.game import BasePokerPlayer

import logging

# 定義DQN模型
class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_size, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, action_size)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

class ReplayBuffer:
    def __init__(self, buffer_size, batch_size):
        self.memory = deque(maxlen=buffer_size)
        self.batch_size = batch_size
    
    def add(self, experience):
        self.memory.append(experience)
    
    def sample(self):
        experiences = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*experiences)
        states = np.vstack(states)
        next_states = np.vstack(next_states)
        return states, actions, rewards, next_states, dones
    
    def __len__(self):
        return len(self.memory)

class DQNAgent:
    def __init__(self, state_size, action_size, buffer_size=10000, batch_size=64, gamma=0.99, alpha=0.001, epsilon=0.1, epsilon_decay=0.995, epsilon_min=0.01):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = ReplayBuffer(buffer_size, batch_size)
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.batch_size = batch_size
        self.model = DQN(state_size, action_size)
        self.target_model = DQN(state_size, action_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=alpha)
        self.update_target_model()

    def update_target_model(self):
        self.target_model.load_state_dict(self.model.state_dict())
    
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        state = torch.FloatTensor(state).unsqueeze(0)
        act_values = self.model(state)
        return torch.argmax(act_values, dim=1).item()
    
    def replay(self):
        if len(self.memory) < self.batch_size:
            return
        
        states, actions, rewards, next_states, dones = self.memory.sample()
        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(next_states)
        dones = torch.FloatTensor(dones)
        
        target = rewards + (1 - dones) * self.gamma * torch.max(self.target_model(next_states), dim=1)[0]
        target_f = self.model(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        
        loss = nn.MSELoss()(target_f, target.detach())
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save(self, filename):
        torch.save(self.model.state_dict(), filename)
    
    def load(self, filename):
        self.model.load_state_dict(torch.load(filename))
        self.update_target_model()


class DQNPlayer(BasePokerPlayer):
    def __init__(self, state_size, action_size, model_file=None):
        super().__init__()
        self.state_size = state_size
        self.action_size = action_size
        self.agent = DQNAgent(state_size, action_size)
        self.previous_state = None
        self.previous_action = None
        self.hole_card = None
        self.model_file = model_file

        if model_file and os.path.exists(model_file):
            print('Loading model...')
            self.agent.load(model_file)
        else:
            print('Starting training from scratch.')

    def declare_action(self, valid_actions, hole_card, round_state):
        state = self.init_game_state(hole_card, round_state)
        action_idx = self.agent.act(state)

        action = valid_actions[action_idx]['action']
        amount = 0

        if action == 'raise':
            min_raise = valid_actions[action_idx]['amount']['min']
            max_raise = valid_actions[action_idx]['amount']['max']
            amount = random.randint(min_raise, max_raise)
        elif action == 'call':
            if valid_actions[action_idx]['amount']['min'] > 0:
                amount = valid_actions[action_idx]['amount']['min']
            else:
                amount = 0
        elif action == 'fold':
            amount = 0

        self.previous_state = state
        self.previous_action = action_idx
        self.hole_card = hole_card

        logging.info(f"Declare action: state={state}, action={action}, amount={amount}")

        return action, amount

    def receive_round_result_message(self, winners, hand_info, round_state):
        if self.previous_state is None or self.previous_action is None:
            logging.warning("Missing previous state or action for DQN update, skipping.")
            return

        state = self.init_game_state(self.hole_card, round_state)
        next_state = np.zeros_like(state)  # Use a special terminal state
        
        reward = 0
        for winner in winners:
            if winner['uuid'] == self.uuid:
                reward = 1
            else:
                reward = -1

        self.agent.memory.add((self.previous_state, self.previous_action, reward, next_state, 1))
        self.agent.replay()
        self.agent.update_target_model()

        logging.info(f"Round result: winners={winners}, reward={reward}, state={state}, next_state={next_state}")

        self.previous_state = None
        self.previous_action = None

    def init_game_state(self, hole_card, round_state):
        def card_to_value(card):
            card_value_map = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
            return card_value_map.get(card[1], 0)

        def card_to_suit(card):
            suit_map = {'S': 0, 'H': 1, 'D': 2, 'C': 3}
            return suit_map.get(card[0], 0)

        hole_card_values = [card_to_value(card) for card in hole_card]
        hole_card_suits = [card_to_suit(card) for card in hole_card]

        community_cards = round_state['community_card'] if round_state['community_card'] else []
        community_card_values = [card_to_value(card) for card in community_cards]
        community_card_suits = [card_to_suit(card) for card in community_cards]

        player_stacks = [player['stack'] for player in round_state['seats']]
        pot_size = round_state['pot']['main']['amount']

        state = hole_card_values + hole_card_suits + community_card_values + community_card_suits + player_stacks + [pot_size]
        state = np.pad(state, (0, self.state_size - len(state)), 'constant', constant_values=0)
        state = np.array(state, dtype=np.float32)
        
        logging.info(f"init_game_state: {state}")
        return state.flatten()
    
    def save_model(self):
        if self.model_file:
            self.agent.save(self.model_file)

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

def setup_ai():
    state_size = 20  # Ensure this matches the fixed state length
    action_size = 3  # fold, call, raise
    return DQNPlayer(state_size, action_size, model_file="dqn_model.pth")