import subprocess
import os
import re
import json
from game.players import BasePokerPlayer

# current working directory is "FAI_Final_Project/final_project"
# print(f"Current working directory: {os.getcwd()}")  # 打印当前工作目录
# file_path = os.path.expanduser('~/bai/FAI_Final_Project/final_project/table/poker_odds.json')
file_path = "./table/poker_odds.json"
with open(file_path, 'r') as file:
    winning_table = json.load(file)['winning_table']
    # print(winning_table)

# def get_hand_strength_from_cpp(hole_cards, community_cards):
#     # evaluator_path = os.path.expanduser('~/bai/FAI_Final_Project/final_project/agents/evaluator')
#     evaluator_path = "./agents/evaluator"
#     command = [evaluator_path] + hole_cards + community_cards
#     # print(f"Running command: {' '.join(command)}")

#     try:
#         result = subprocess.run(command, capture_output=True, text=True, check=True)
#         # print(f"Results: {result.stdout.strip()}")
#     except subprocess.CalledProcessError as e:
#         print(f"Subprocess failed with error: {e}")
#         raise

#     match = re.search(r'Win rate: (\d+\.\d+)%', result.stdout)
#     if match:
#         win_rate = float(match.group(1))
#         # print(f"Extracted win rate: {win_rate}")
#         return win_rate
#     else:
#         raise ValueError("Failed to extract win rate from output")

#     # return float(result.stdout.strip())
#     return win_rate

def get_hand_strength_from_cpp(hole_cards, community_cards):
    evaluator_path = os.path.expanduser('~/bai/FAI_Final_Project/final_project/agents/C++/')
    
    # Determine which evaluator to use based on the number of community cards
    if len(community_cards) == 3:
        evaluator = os.path.join(evaluator_path, 'evaluator_flop')
    elif len(community_cards) == 4:
        evaluator = os.path.join(evaluator_path, 'evaluator_turn')
    elif len(community_cards) == 5:
        evaluator = os.path.join(evaluator_path, 'evaluator_river')
    else:
        raise ValueError("Invalid number of community cards")
    
    print(f"Using evaluator: {evaluator}")

    command = [evaluator] + hole_cards + community_cards
    print(f"Running command: {' '.join(command)}")

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"Results: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"Subprocess failed with error: {e}")
        raise

    match = re.search(r'Win rate: (\d+\.\d+)%', result.stdout)
    if match:
        win_rate = float(match.group(1))
        print(f"Extracted win rate: {win_rate}")
        return win_rate
    else:
        raise ValueError("Failed to extract win rate from output")

    return win_rate

class CallPlayer(BasePokerPlayer):
    def declare_action(self, valid_actions, hole_card, round_state):

        community_cards = round_state['community_card']
        print(f"Community cards: {community_cards}")
        
        # =========================== Preflop ===========================
        if len(community_cards) == 0:
            print("Preflop")
            card1, card2 = hole_card
            rank1, suit1 = card1[1], card1[0]
            rank2, suit2 = card2[1], card2[0]
            
            if suit1 == suit2:
                suited = 's'
            else:
                suited = 'u'
            
            # hole_card_str = f"{rank1}/{rank2}/{suited}" if rank1 < rank2 else f"{rank2}/{rank1}/{suited}"
            rank_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
            hole_card_str = f"{rank1}/{rank2}/{suited}" if rank_order[rank1] < rank_order[rank2] else f"{rank2}/{rank1}/{suited}"

            print(f"Hole card string: {hole_card_str}")
            hand_data = next((item for item in winning_table if item["hand"] == hole_card_str), None)

            # print(f"Hand data: {hand_data}")
            print(f"Preflop winning rate: {hand_data['win']}%")
            print()

            if hand_data and hand_data["win"] > 80.0:
                raise_action_info = valid_actions[2]
                action, amount = raise_action_info["action"], raise_action_info["amount"]["max"]
                # call_action_info = valid_actions[1]
                # action, amount = call_action_info["action"], call_action_info["amount"]
            
            elif hand_data and hand_data["win"] > 60.0:
                raise_action_info = valid_actions[2]
                action, amount = raise_action_info["action"], min(100, raise_action_info["amount"]["max"])

            elif hand_data and hand_data["win"] > 50.0:
                call_action_info = valid_actions[1]
                action, amount = call_action_info["action"], call_action_info["amount"]

            else:
                # call_action_info = valid_actions[1]
                # action, amount = call_action_info["action"], call_action_info["amount"]
                fold_action_info = valid_actions[0]
                action, amount = fold_action_info["action"], fold_action_info["amount"]


        # =========================== Postflop ===========================
        elif len(community_cards) == 3:
            print("Flop")
            hole_cards_str = [f"{card[1]}{card[0]}" for card in hole_card]
            print(f"Hole cards string: {hole_cards_str}")
            print(f"Community cards: {community_cards}")

            # getting the hand winning_rate after flop
            winning_rate = get_hand_strength_from_cpp(hole_cards_str, community_cards)
            print(f"Hand strength after flop: {winning_rate}%")
            print()

            # if winning_rate > 50.0:
            #     # raise_action_info = valid_actions[2]
            #     # action, amount = raise_action_info["action"], raise_action_info["amount"]["max"]
            #     call_action_info = valid_actions[1]
            #     action, amount = call_action_info["action"], call_action_info["amount"]
            # else:
            #     fold_action_info = valid_actions[0]
            #     action, amount = fold_action_info["action"], fold_action_info["amount"]

            if hand_data and hand_data["win"] > 80.0:
                raise_action_info = valid_actions[2]
                action, amount = raise_action_info["action"], raise_action_info["amount"]["max"]
                # call_action_info = valid_actions[1]
                # action, amount = call_action_info["action"], call_action_info["amount"]
            
            elif hand_data and hand_data["win"] > 60.0:
                raise_action_info = valid_actions[2]
                action, amount = raise_action_info["action"], min(100, raise_action_info["amount"]["max"])

            elif hand_data and hand_data["win"] > 50.0:
                call_action_info = valid_actions[1]
                action, amount = call_action_info["action"], call_action_info["amount"]

            else:
                # call_action_info = valid_actions[1]
                # action, amount = call_action_info["action"], call_action_info["amount"]
                fold_action_info = valid_actions[0]
                action, amount = fold_action_info["action"], fold_action_info["amount"]


        elif len(community_cards) == 4:
            print("Turn")
            hole_cards_str = [f"{card[1]}{card[0]}" for card in hole_card]
            print(f"Hole cards string: {hole_cards_str}")
            print(f"Community cards: {community_cards}")

            # getting the hand winning_rate after flop
            winning_rate = get_hand_strength_from_cpp(hole_cards_str, community_cards)
            print(f"Hand strength after flop: {winning_rate}%")
            print()

            # if winning_rate > 50.0:
            #     # raise_action_info = valid_actions[2]
            #     # action, amount = raise_action_info["action"], raise_action_info["amount"]["max"]
            #     call_action_info = valid_actions[1]
            #     action, amount = call_action_info["action"], call_action_info["amount"]
            # else:
            #     fold_action_info = valid_actions[0]
            #     action, amount = fold_action_info["action"], fold_action_info["amount"]

            if hand_data and hand_data["win"] > 80.0:
                raise_action_info = valid_actions[2]
                action, amount = raise_action_info["action"], raise_action_info["amount"]["max"]
                # call_action_info = valid_actions[1]
                # action, amount = call_action_info["action"], call_action_info["amount"]
            
            elif hand_data and hand_data["win"] > 60.0:
                raise_action_info = valid_actions[2]
                action, amount = raise_action_info["action"], min(100, raise_action_info["amount"]["max"])

            elif hand_data and hand_data["win"] > 50.0:
                call_action_info = valid_actions[1]
                action, amount = call_action_info["action"], call_action_info["amount"]

            else:
                call_action_info = valid_actions[1]
                action, amount = call_action_info["action"], call_action_info["amount"]
                # fold_action_info = valid_actions[0]
                # action, amount = fold_action_info["action"], fold_action_info["amount"]
        
        elif len(community_cards) == 5:
            print("River")
            hole_cards_str = [f"{card[1]}{card[0]}" for card in hole_card]
            print(f"Hole cards string: {hole_cards_str}")
            print(f"Community cards: {community_cards}")

            # getting the hand winning_rate after flop
            winning_rate = get_hand_strength_from_cpp(hole_cards_str, community_cards)
            print(f"Hand strength after flop: {winning_rate}%")
            print()

            # if winning_rate > 50.0:
            #     raise_action_info = valid_actions[2]
            #     action, amount = raise_action_info["action"], raise_action_info["amount"]["max"]
            # else:
            #     fold_action_info = valid_actions[0]
            #     action, amount = fold_action_info["action"], fold_action_info["amount"]
            if hand_data and hand_data["win"] > 80.0:
                raise_action_info = valid_actions[2]
                action, amount = raise_action_info["action"], raise_action_info["amount"]["max"]
                # call_action_info = valid_actions[1]
                # action, amount = call_action_info["action"], call_action_info["amount"]
            
            elif hand_data and hand_data["win"] > 60.0:
                raise_action_info = valid_actions[2]
                action, amount = raise_action_info["action"], min(100, raise_action_info["amount"]["max"])

            elif hand_data and hand_data["win"] > 50.0:
                call_action_info = valid_actions[1]
                action, amount = call_action_info["action"], call_action_info["amount"]

            else:
                call_action_info = valid_actions[1]
                action, amount = call_action_info["action"], call_action_info["amount"]
                # fold_action_info = valid_actions[0]
                # action, amount = fold_action_info["action"], fold_action_info["amount"]


        print(f"Action: {action}, Amount: {amount}")
        return action, amount


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
