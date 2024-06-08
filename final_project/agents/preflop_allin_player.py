import os
import json
from game.players import BasePokerPlayer


file_path = os.path.expanduser('~/bai/FAI_Final_Project/final_project/table/poker_odds.json')
with open(file_path, 'r') as file:
    winning_table = json.load(file)
    winning_table = winning_table['winning_table']
    # print(winning_table['winning_table'])

# print(winning_table)

class CallPlayer(BasePokerPlayer):
    def declare_action(self, valid_actions, hole_card, round_state):
        # valid_actions format => [fold_action_info, call_action_info, raise_action_info]
        # print(hole_card)
        card1, card2 = hole_card
        rank1, suit1 = card1[1], card1[0]
        rank2, suit2 = card2[1], card2[0]
        
        if suit1 == suit2:
            suited = 's'
        else:
            suited = 'u'
        

        hole_card_str = f"{rank1}/{rank2}/{suited}" if rank1 < rank2 else f"{rank2}/{rank1}/{suited}"
        print(hole_card_str)

        hand_data = next((item for item in winning_table if item["hand"] == hole_card_str), None)
        # print('hand_data', hand_data, hand_data["win"])
        print(f"winning_rate: {hand_data['win']}%")
        print()

        # if hand_data["win"] > 50.0, we allin
        if hand_data and hand_data["win"] > 50.0:
            raise_action_info = valid_actions[2]
            action, amount = raise_action_info["action"], raise_action_info["amount"]["max"]

        # if hand_data["win"] < 50.0, we fold
        else:
            print("Fold")
            fold_action_info = valid_actions[0]
            action, amount = fold_action_info["action"], fold_action_info["amount"]
        
        print()
        return action, amount


    def receive_game_start_message(self, game_info):
        self.game_info = game_info
        self.current_round = 0
        # print("Game started:", game_info)
        print("Game started!!")
        # print()
        # pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        self.current_round = round_count
        self.hole_card = hole_card
        self.seats = seats
        # print(f"Round {round_count} started with hole cards: {hole_card} and seats: {seats}")
        print(f"Round {round_count} started with hole cards: {hole_card}")
        print()
        # pass

    def receive_street_start_message(self, street, round_state):
        self.current_street = street
        self.round_state = round_state
        print(f"Street {street} started with round state: {round_state}")
        print()
        # pass

    def receive_game_update_message(self, action, round_state):
        self.last_action = action
        self.round_state = round_state
        print(f"Game updated with action: {action} and round state: {round_state}")
        print()
        # pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        self.winners = winners
        self.hand_info = hand_info
        self.round_state = round_state
        print(f"Round ended. Winners: {winners}, Hand info: {hand_info}, Round state: {round_state}")
        print(f"Round {self.current_round} ended. Winners: {winners}")
        print()
        # pass

def setup_ai():
    return CallPlayer()
