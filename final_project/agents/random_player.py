from game.players import BasePokerPlayer
import random as rand


class RandomPlayer(BasePokerPlayer):
    def __init__(self):
        self.fold_ratio = self.call_ratio = raise_ratio = 1.0 / 3

    def set_action_ratio(self, fold_ratio, call_ratio, raise_ratio):
        ratio = [fold_ratio, call_ratio, raise_ratio]
        scaled_ratio = [1.0 * num / sum(ratio) for num in ratio]
        self.fold_ratio, self.call_ratio, self.raise_ratio = scaled_ratio

    def declare_action(self, valid_actions, hole_card, round_state):
        choice = self.__choice_action(valid_actions)
        action = choice["action"]
        amount = choice["amount"]
        if action == "raise":
            amount = rand.randrange(
                amount["min"], max(amount["min"], amount["max"]) + 1
            )
        return action, amount

    def __choice_action(self, valid_actions):
        r = rand.random()
        if r <= self.fold_ratio:
            return valid_actions[0]
        elif r <= self.call_ratio:
            return valid_actions[1]
        else:
            return valid_actions[2]


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
    return RandomPlayer()
