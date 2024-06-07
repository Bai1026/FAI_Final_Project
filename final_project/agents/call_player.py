from game.players import BasePokerPlayer


class CallPlayer(
    BasePokerPlayer
):  # Do not forget to make parent class as "BasePokerPlayer"

    #  we define the logic to make an action through this method. (so this method would be the core of your AI)
    def declare_action(self, valid_actions, hole_card, round_state):
        # valid_actions format => [fold_action_info, call_action_info, raise_action_info]
        call_action_info = valid_actions[1]
        action, amount = call_action_info["action"], call_action_info["amount"]
        return action, amount  # action returned here is sent to the poker engine

# what should I do if I do not want to pass the functions below?
    #  we receive the game information in this method.
    #  the game information contains "rule", "seats", "button" and "self_uuid".
    #  "rule" is a dictionary containing "name" and "small_blind_amount"
    #  "seats" is an array containing players' information.
    #  "button" is the player UUID who is the dealer.
    #  "self_uuid" is your UUID.
    def receive_game_start_message(self, game_info):
        # print(game_info)
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        # print(round_count, hole_card, seats)
        pass

    def receive_street_start_message(self, street, round_state):
        # print(street, round_state)
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass


def setup_ai():
    return CallPlayer()