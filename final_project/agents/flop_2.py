import subprocess
import os
import re
import json
from game.players import BasePokerPlayer
from .evaluator import card_to_tuple, RANKS, SUITS, hand_strength, compare_hands, evaluate_hand_with_possible_outcomes, evaluate_flop, evaluate_turn, evaluate_river, parallel_evaluator
# from .evaluator import hand_strength, compare_hands, evaluate_hand_with_possible_outcomes, evaluate_flop, evaluate_turn, evaluate_river, parallel_evaluator

# current working directory is "FAI_Final_Project/final_project"
# print(f"Current working directory: {os.getcwd()}")  # 打印当前工作目录
# file_path = os.path.expanduser('~/bai/FAI_Final_Project/final_project/table/poker_odds.json')
file_path = "./table/poker_odds.json"
with open(file_path, 'r') as file:
    winning_table = json.load(file)['winning_table']
    # print(winning_table)
    

def get_hand_strength_from_python(hole_cards, community_cards):
    hole_cards_tuple = [card_to_tuple(card) for card in hole_cards]
    community_cards_tuple = [card_to_tuple(card) for card in community_cards]
    # print(hole_cards_tuple)
    # print(community_cards_tuple)

    print("Hole Cards:", hole_cards)
    print("Community Cards:", community_cards)

    if len(community_cards) == 3:
        print('FLOP')
        win_rate = parallel_evaluator(evaluate_flop, hole_cards_tuple, community_cards_tuple)
    elif len(community_cards) == 4:
        print('TURN')
        win_rate = parallel_evaluator(evaluate_turn, hole_cards_tuple, community_cards_tuple)
    elif len(community_cards) == 5:
        print('RIVER')
        win_rate = parallel_evaluator(evaluate_river, hole_cards_tuple, community_cards_tuple)
    else:
        raise ValueError("Invalid number of community cards")

    # print(f"Calculated Win Rate: {win_rate}%")
    return win_rate


def calculate_remaining(round_state):
    blind_remaining = 0
    round_count = int(round_state['round_count'])
    round_remaining = 5 - round_count
    # print(round_remaining)

    blind_remaining += ((round_remaining // 2) + 1) * 5
    blind_remaining += (((round_remaining - 1) // 2) + 1) * 10
    print(blind_remaining)

    return blind_remaining


class CallPlayer(BasePokerPlayer):
    def declare_action(self, valid_actions, hole_card, round_state): # valid_actions format => [fold_action_info, call_action_info, raise_action_info]
        community_cards = round_state['community_card']

        print(round_state)
        print()

        # choose to flop till the game over or not
        blind_remaining = calculate_remaining(round_state)
        if round_state['seats'][1]['stack'] - blind_remaining >= round_state['seats'][1]['stack'] + blind_remaining:
            print("Fold")
            print(round_state['seats'][1]['stack'], round_state['seat'][0]['stack'], blind_remaining)

            fold_action_info = valid_actions[0]
            action, amount = fold_action_info["action"], fold_action_info["amount"]
            return action, amount
        
        # ====================================================== PREFLOP ======================================================
        if len(community_cards) == 0:
            print("Preflop")
            card1, card2 = hole_card
            rank1, suit1 = card1[1], card1[0]
            rank2, suit2 = card2[1], card2[0]
            
            suited = 's' if suit1 == suit2 else 'u'
            rank_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
            hole_card_str = f"{rank1}/{rank2}/{suited}" if rank_order[rank1] < rank_order[rank2] else f"{rank2}/{rank1}/{suited}"

            print(f"Hole card string: {hole_card_str}")
            hand_data = next((item for item in winning_table if item["hand"] == hole_card_str), None)

            if hand_data:
                print(f"Preflop winning rate: {hand_data['win']}%")
            else:
                print("No hand data found for the given hole cards")

            if hand_data and hand_data["win"] > 90.0:
                raise_action_info = valid_actions[2]
                action, amount = raise_action_info["action"], raise_action_info["amount"]["max"]
            elif hand_data and hand_data["win"] > 75.0:
                raise_amount = 20
                raise_action_info = valid_actions[2]
                if raise_action_info["amount"]["min"] > raise_amount:
                    call_action_info = valid_actions[1]
                    action, amount = call_action_info["action"], call_action_info["amount"]
                else:
                    action, amount = raise_action_info["action"], min(raise_amount, raise_action_info["amount"]["max"])
            elif hand_data and hand_data["win"] > 40.0:
                call_action_info = valid_actions[1]
                action, amount = call_action_info["action"], call_action_info["amount"]
            else:
                fold_action_info = valid_actions[0]
                action, amount = fold_action_info["action"], fold_action_info["amount"]


        # ====================================================== FLOP ======================================================
        elif len(community_cards) == 3:
            print(valid_actions[2])
            print("Flop")

            hole_cards_str = [f"{card[1]}{card[0]}" for card in hole_card]
            # print(f"Hole cards string: {hole_cards_str}")
            # print(f"Community cards: {community_cards}")

            print('Getting winning rate...')
            winning_rate = get_hand_strength_from_python(hole_cards_str, community_cards)
            print(f"Winning Rate: {winning_rate}%")
            print()

            call_action_info = valid_actions[1]
            action, amount = call_action_info["action"], call_action_info["amount"]


        # ====================================================== TURN ======================================================
        elif len(community_cards) == 4:
            # print("Turn")
            call_action_info = valid_actions[1]
            action, amount = call_action_info["action"], call_action_info["amount"]


        # ====================================================== RIVER ======================================================
        else:
            print("River")
            # raise_action_info = valid_actions[2]
            # action, amount = raise_action_info["action"], raise_action_info["amount"]["max"]
            call_action_info = valid_actions[1]
            action, amount = call_action_info["action"], call_action_info["amount"]


        print(f"Action: {action}, Amount: {amount}")
        return action, amount





    # def receive_game_start_message(self, game_info):
    #     self.game_info = game_info
    #     self.current_round = 0
    #     # print("Game started:", game_info)
    #     print("Game started!!")
    #     # print()
    #     # pass

    # def receive_round_start_message(self, round_count, hole_card, seats):
    #     self.current_round = round_count
    #     self.hole_card = hole_card
    #     self.seats = seats
    #     # print(f"Round {round_count} started with hole cards: {hole_card} and seats: {seats}")
    #     print(f"Round {round_count} started with hole cards: {hole_card}")
    #     print()
    #     # pass

    # def receive_street_start_message(self, street, round_state):
    #     self.current_street = street
    #     self.round_state = round_state
    #     print(f"Street {street} started with round state: {round_state}")
    #     print()
    #     # pass

    # def receive_game_update_message(self, action, round_state):
    #     self.last_action = action
    #     self.round_state = round_state
    #     print(f"Game updated with action: {action} and round state: {round_state}")
    #     print()
    #     # pass

    # def receive_round_result_message(self, winners, hand_info, round_state):
    #     self.winners = winners
    #     self.hand_info = hand_info
    #     self.round_state = round_state
    #     print(f"Round ended. Winners: {winners}, Hand info: {hand_info}, Round state: {round_state}")
    #     # print(f"Round {self.current_round} ended. Winners: {winners}")
    #     print()
    #     # pass


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
    return CallPlayer()
