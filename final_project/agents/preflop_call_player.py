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
        print()

        # 查找手牌胜率
        hand_data = next((item for item in winning_table if item["hand"] == hole_card_str), None)
        print('hand_data', hand_data, hand_data["win"])
        if hand_data:
            # print(hand_data["win"])
            print("Found")
        else:
            print("Not found!!!!!!!!!!!!!!!!!")

        if hand_data and hand_data["win"] < 50.0:
            # 如果胜率小于50%，在preflop阶段弃牌
            print("Fold")
            fold_action_info = valid_actions[0]
            action, amount = fold_action_info["action"], fold_action_info["amount"]
        else:
            call_action_info = valid_actions[1]
            action, amount = call_action_info["action"], call_action_info["amount"]
        
        print()
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

def setup_ai():
    return CallPlayer()
