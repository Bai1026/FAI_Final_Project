# import os
# import json
# from game.players import BasePokerPlayer


# file_path = os.path.expanduser('~/bai/FAI_Final_Project/final_project/table/poker_odds.json')
# with open(file_path, 'r') as file:
#     winning_table = json.load(file)
#     winning_table = winning_table['winning_table']
#     # print(winning_table['winning_table'])

# # print(winning_table)

# # if the remaining blind is enough, fold till the game is over
# def calculate_remaining(round_state):
#     blind_remaining = 0
#     round_count = int(round_state['round_count'])
#     round_remaining = 20 - round_count
#     # print(round_remaining)

#     blind_remaining += ((round_remaining // 2) + 1) * 5
#     blind_remaining += (((round_remaining - 1) // 2) + 1) * 10
#     print(blind_remaining)

#     return blind_remaining


# class CallPlayer(BasePokerPlayer):
#     # valid_actions format => [fold_action_info, call_action_info, raise_action_info]
#     def declare_action(self, valid_actions, hole_card, round_state):
#         print(hole_card)
#         card1, card2 = hole_card
#         rank1, suit1 = card1[1], card1[0]
#         rank2, suit2 = card2[1], card2[0]
        
#         if suit1 == suit2:
#             suited = 's'
#         else:
#             suited = 'u'
        

#         hole_card_str = f"{rank1}/{rank2}/{suited}" if rank1 < rank2 else f"{rank2}/{rank1}/{suited}"
#         # print(f"hole card: {hole_card_str}")

#         hand_data = next((item for item in winning_table if item["hand"] == hole_card_str), None)
#         # print('hand_data', hand_data, hand_data["win"])
#         print(f"winning_rate: {hand_data['win']}%")
#         print()


#         blind_remaining = calculate_remaining(round_state)
#         print(round_state['seats'][1])
#         print('player 1: ', round_state['seats'][0]['stack'] + blind_remaining)
#         print('player 2: ', round_state['seats'][1]['stack'] - blind_remaining)

#         if round_state['seats'][1]['stack'] - blind_remaining >= round_state['seats'][0]['stack'] + blind_remaining:
#             print("Fold with enough blind remaining")
#             print(round_state['seats'][1]['stack'], round_state['seat'][0]['stack'], blind_remaining)

#             fold_action_info = valid_actions[0]
#             action, amount = fold_action_info["action"], fold_action_info["amount"]
#             return action, amount
        

#         # if hand_data["win"] > 50.0, we allin -> 75/169 cases -> 44.38%
#         if hand_data and hand_data["win"] > 45.0:
#             print('ALL INNNNNNNN!!!')
#             raise_action_info = valid_actions[2]
#             action, amount = raise_action_info["action"], raise_action_info["amount"]["max"]

#         # if hand_data["win"] < 50.0, we fold
#         else:
#             print("Fold")
#             fold_action_info = valid_actions[0]
#             action, amount = fold_action_info["action"], fold_action_info["amount"]
        
#         print()
#         return action, amount


#     # def receive_game_start_message(self, game_info):
#     #     self.game_info = game_info
#     #     self.current_round = 0
#     #     # print("Game started:", game_info)
#     #     print("Game started!!")
#     #     # print()
#     #     # pass

#     # def receive_round_start_message(self, round_count, hole_card, seats):
#     #     self.current_round = round_count
#     #     self.hole_card = hole_card
#     #     self.seats = seats
#     #     # print(f"Round {round_count} started with hole cards: {hole_card} and seats: {seats}")
#     #     print(f"Round {round_count} started with hole cards: {hole_card}")
#     #     print()
#     #     # pass

#     # def receive_street_start_message(self, street, round_state):
#     #     self.current_street = street
#     #     self.round_state = round_state
#     #     print(f"Street {street} started with round state: {round_state}")
#     #     print()
#     #     # pass

#     # def receive_game_update_message(self, action, round_state):
#     #     self.last_action = action
#     #     self.round_state = round_state
#     #     print(f"Game updated with action: {action} and round state: {round_state}")
#     #     print()
#     #     # pass

#     # def receive_round_result_message(self, winners, hand_info, round_state):
#     #     self.winners = winners
#     #     self.hand_info = hand_info
#     #     self.round_state = round_state
#     #     print(f"Round ended. Winners: {winners}, Hand info: {hand_info}, Round state: {round_state}")
#     #     print(f"Round {self.current_round} ended. Winners: {winners}")
#     #     print()
#     #     # pass

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
#     return CallPlayer()



import os
import json
from game.players import BasePokerPlayer

file_path = os.path.expanduser('~/bai/FAI_Final_Project/final_project/table/poker_odds.json')
with open(file_path, 'r') as file:
    winning_table = json.load(file)
    winning_table = winning_table['winning_table']

def calculate_remaining(round_state):
    blind_remaining = 0
    round_count = int(round_state['round_count'])
    round_remaining = 20 - round_count

    blind_remaining += ((round_remaining // 2) + 1) * 5
    blind_remaining += (((round_remaining - 1) // 2) + 1) * 10
    print(blind_remaining)

    return blind_remaining

class CallPlayer(BasePokerPlayer):
    def __init__(self, threshold=None):
        self.threshold = threshold

    def declare_action(self, valid_actions, hole_card, round_state):
        print(hole_card)
        # print(self.uuid)
        # # print(round_state)
        # print(round_state['seats'])
        # print(f"my_seat: {my_seat}")
        # print(f"opponent_seat: {opponent_seat}")


        card1, card2 = hole_card
        rank1, suit1 = card1[1], card1[0]
        rank2, suit2 = card2[1], card2[0]

        if suit1 == suit2:
            suited = 's'
        else:
            suited = 'u'

        hole_card_str = f"{rank1}/{rank2}/{suited}" if rank1 < rank2 else f"{rank2}/{rank1}/{suited}"
        print(f"hole card: {hole_card_str}")

        hand_data = next((item for item in winning_table if item["hand"] == hole_card_str), None)
        print(f"winning_rate: {hand_data['win']}%")


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

        if hand_data and hand_data["win"] > self.threshold:
            print('ALL INNNNNNNN!!!')
            raise_action_info = valid_actions[2]
            action, amount = raise_action_info["action"], raise_action_info["amount"]["max"]
        else:
            print("Fold")
            fold_action_info = valid_actions[0]
            action, amount = fold_action_info["action"], fold_action_info["amount"]

        return action, amount

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass
        # print(f"Round ended. Winners: {winners['name']} with stack: {winners['stack']}, Hand info: {hand_info}, Round state: {round_state}")

def setup_ai(threshold):
    return CallPlayer(threshold)
