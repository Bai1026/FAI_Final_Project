import random
import multiprocessing
from functools import reduce
from itertools import groupby
from functools import partial

from game.engine.hand_evaluator import HandEvaluator
from game.engine.game_evaluator import GameEvaluator

class Card:
    rank_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                  'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def rank_value(self):
        return self.rank_order[self.rank]

    def __repr__(self):
        return f"{self.rank}{self.suit}"

def card_to_tuple(card):
    rank = card[0]
    suit = card[1]
    return Card(rank, suit)

def convert_to_rank_value(cards):
    return [Card(card.rank_value(), card.suit) for card in cards]

def game_evaluator(hole_cards, community_cards, opponent_hand):
    # Combine hole cards and community cards with opponent hand
    my_full_hand = hole_cards + community_cards
    opponent_full_hand = opponent_hand + community_cards

    # Evaluate both hands
    my_full_hand_converted = convert_to_rank_value(my_full_hand)
    opponent_full_hand_converted = convert_to_rank_value(opponent_full_hand)

    my_score = HandEvaluator.eval_hand(hole_cards, community_cards)
    opponent_score = HandEvaluator.eval_hand(opponent_hand, community_cards)

    # Determine win (1 for win, 0.5 for tie, 0 for loss)
    if my_score > opponent_score:
        return 1
    elif my_score == opponent_score:
        return 0.5
    else:
        return 0

def monte_carlo_simulation(evaluation_function, hole_cards, community_cards, num_simulations, total_community_cards):
    deck = [Card(rank, suit) for rank in '23456789TJQKA' for suit in 'CDHS']
    remaining_deck = [card for card in deck if card not in hole_cards and card not in community_cards]
    
    results = []
    for _ in range(num_simulations):
        sampled_deck = random.sample(remaining_deck, total_community_cards + 2)  # 2 opponent cards + remaining community cards
        opponent_hand = sampled_deck[:2]
        new_community_cards = community_cards + sampled_deck[2:]
        
        result = evaluation_function(hole_cards, new_community_cards, opponent_hand)
        results.append(result)
    
    win_rate = sum(results) / len(results)
    return win_rate, len(results)

if __name__ == "__main__":
    hole_cards = [card_to_tuple('AC'), card_to_tuple('5S')]
    community_cards_flop = [card_to_tuple('AD'), card_to_tuple('TH'), card_to_tuple('KC')]
    community_cards_turn = community_cards_flop + [card_to_tuple('7D')]
    community_cards_river = community_cards_turn + [card_to_tuple('7S')]

    num_simulations = 10000  # Number of Monte Carlo simulations

    flop_win_rate, flop_simulations = monte_carlo_simulation(game_evaluator, hole_cards, community_cards_flop, num_simulations, 5)
    turn_win_rate, turn_simulations = monte_carlo_simulation(game_evaluator, hole_cards, community_cards_turn, num_simulations, 6)
    river_win_rate, river_simulations = monte_carlo_simulation(game_evaluator, hole_cards, community_cards_river, num_simulations, 7)

    print(f"Flop Simulations: {flop_simulations}, Win Rate: {flop_win_rate}")
    print(f"Turn Simulations: {turn_simulations}, Win Rate: {turn_win_rate}")
    print(f"River Simulations: {river_simulations}, Win Rate: {river_win_rate}")
