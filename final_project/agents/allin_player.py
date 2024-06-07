from game.players import BasePokerPlayer


class AllInPlayer(BasePokerPlayer):
    def declare_action(self, valid_actions, hole_card, round_state):
        # valid_actions format => [fold_action_info, call_action_info, raise_action_info]
        raise_action_info = valid_actions[2]
        action, amount = raise_action_info["action"], raise_action_info["amount"]["max"]
        # print('jsklfjklsdjfkldfj')
        print(action, amount)
        print()
        return action, amount  # always go all-in

    def receive_game_start_message(self, game_info):
        # pass
        print(game_info)

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass

def setup_ai():
    # receive_game_start_message()
    return AllInPlayer()