# ========================================== not precise yet ==========================================
import itertools
import multiprocessing
from collections import Counter
from functools import partial

RANKS = "23456789TJQKA"
SUITS = "HDCS"

# def card_to_tuple(card):
#     return (RANKS.index(card[0]), SUITS.index(card[1]))

def detect_card_order(card):
    # Detect if card is in 'S3' or '3S' format
    if card[0] in SUITS:
        return 'SUIT_FIRST'
    else:
        return 'RANK_FIRST'

def card_to_tuple(card):
    order = detect_card_order(card)
    if order == 'SUIT_FIRST':
        return (RANKS.index(card[1]), SUITS.index(card[0]))
    else:
        return (RANKS.index(card[0]), SUITS.index(card[1]))

def hand_strength(hand):
    ranks = [card[0] for card in hand]
    suits = [card[1] for card in hand]
    rank_counter = Counter(ranks)
    suit_counter = Counter(suits)
    is_flush = max(suit_counter.values()) >= 5
    is_straight = False
    rank_set = set(ranks)
    for i in range(len(RANKS) - 4):
        if all(rank in rank_set for rank in range(i, i + 5)):
            is_straight = True
            break

    if is_flush and is_straight:
        return 8  # Straight flush
    if 4 in rank_counter.values():
        return 7  # Four of a kind
    if 3 in rank_counter.values() and 2 in rank_counter.values():
        return 6  # Full house
    if is_flush:
        return 5  # Flush
    if is_straight:
        return 4  # Straight
    if 3 in rank_counter.values():
        return 3  # Three of a kind
    if list(rank_counter.values()).count(2) == 2:
        return 2  # Two pair
    if 2 in rank_counter.values():
        return 1  # One pair
    return 0  # High card

def compare_hands(hand1, hand2):
    strength1 = hand_strength(hand1)
    strength2 = hand_strength(hand2)
    if strength1 > strength2:
        return 1
    elif strength1 < strength2:
        return -1
    return 0

def evaluate_hand_with_possible_outcomes(hole_cards, community_cards, possible_outcomes):
    deck = [card_to_tuple(rank + suit) for rank in RANKS for suit in SUITS]
    excluded = set(hole_cards + community_cards)
    remaining_deck = [card for card in deck if card not in excluded]

    if not possible_outcomes:
        possible_outcomes = [()]

    win_count = 0
    total_count = 0

    possible_outcome_list = list(possible_outcomes)
    opponent_hand_combinations = list(itertools.combinations(remaining_deck, 2))

    # print(f"Number of possible outcomes: {len(possible_outcome_list)}")
    # print(f"Number of opponent hand combinations: {len(opponent_hand_combinations)}")

    for outcome in possible_outcome_list:
        full_community = community_cards + list(outcome)
        for opponent_hand in opponent_hand_combinations:
            my_hand = hole_cards + full_community
            opp_hand = list(opponent_hand) + full_community
            result = compare_hands(my_hand, opp_hand)
            if result == 1:
                win_count += 1
            elif result == 0:
                win_count += 0.5
            total_count += 1
 
    if total_count == 0:
        return 0

    return (win_count / total_count) * 100

def evaluate_flop(hole_cards, community_cards):
    possible_turns = itertools.combinations([card_to_tuple(rank + suit) for rank in RANKS for suit in SUITS if card_to_tuple(rank + suit) not in set(hole_cards + community_cards)], 1)
    return evaluate_hand_with_possible_outcomes(hole_cards, community_cards, possible_turns)

def evaluate_turn(hole_cards, community_cards):
    possible_rivers = itertools.combinations([card_to_tuple(rank + suit) for rank in RANKS for suit in SUITS if card_to_tuple(rank + suit) not in set(hole_cards + community_cards)], 1)
    return evaluate_hand_with_possible_outcomes(hole_cards, community_cards, possible_rivers)

def evaluate_river(hole_cards, community_cards):
    return evaluate_hand_with_possible_outcomes(hole_cards, community_cards, [])

def parallel_evaluator(evaluate_func, hole_cards, community_cards):
    with multiprocessing.Pool() as pool:
        results = pool.starmap(evaluate_func, [(hole_cards, community_cards)])
    return sum(results) / len(results)

if __name__ == "__main__":
    hole_cards = [card_to_tuple('AC'), card_to_tuple('AS')]
    community_cards_flop = [card_to_tuple('AD'), card_to_tuple('TH'), card_to_tuple('KC')]
    community_cards_turn = community_cards_flop + [card_to_tuple('7D')]
    community_cards_river = community_cards_turn + [card_to_tuple('7S')]

    print("Flop Win Rate:", parallel_evaluator(evaluate_flop, hole_cards, community_cards_flop))
    print("Turn Win Rate:", parallel_evaluator(evaluate_turn, hole_cards, community_cards_turn))
    print("River Win Rate:", parallel_evaluator(evaluate_river, hole_cards, community_cards_river))



# ========================================== 1081 x 1081 version ==========================================
# import itertools
# import multiprocessing
# from collections import Counter
# from functools import partial

# RANKS = "23456789TJQKA"
# SUITS = "HDCS"

# def card_to_tuple(card):
#     return (RANKS.index(card[0]), SUITS.index(card[1]))

# def hand_strength(hand):
#     ranks = [card[0] for card in hand]
#     suits = [card[1] for card in hand]
#     rank_counter = Counter(ranks)
#     suit_counter = Counter(suits)
#     is_flush = max(suit_counter.values()) >= 5
#     is_straight = False
#     rank_set = set(ranks)
#     for i in range(len(RANKS) - 4):
#         if all(rank in rank_set for rank in range(i, i + 5)):
#             is_straight = True
#             break

#     if is_flush and is_straight:
#         return 8  # Straight flush
#     if 4 in rank_counter.values():
#         return 7  # Four of a kind
#     if 3 in rank_counter.values() and 2 in rank_counter.values():
#         return 6  # Full house
#     if is_flush:
#         return 5  # Flush
#     if is_straight:
#         return 4  # Straight
#     if 3 in rank_counter.values():
#         return 3  # Three of a kind
#     if list(rank_counter.values()).count(2) == 2:
#         return 2  # Two pair
#     if 2 in rank_counter.values():
#         return 1  # One pair
#     return 0  # High card

# def compare_hands(hand1, hand2):
#     strength1 = hand_strength(hand1)
#     strength2 = hand_strength(hand2)
#     if strength1 > strength2:
#         return 1
#     elif strength1 < strength2:
#         return -1
#     return 0

# def evaluate_hand_with_possible_outcomes(hole_cards, community_cards, possible_outcomes):
#     deck = [card_to_tuple(rank + suit) for rank in RANKS for suit in SUITS]
#     excluded = set(hole_cards + community_cards)
#     remaining_deck = [card for card in deck if card not in excluded]

#     if not possible_outcomes:
#         possible_outcomes = [()]

#     win_count = 0
#     total_count = 0

#     possible_outcome_list = list(possible_outcomes)
#     opponent_hand_combinations = list(itertools.combinations(remaining_deck, 2))

#     print(f"Number of possible outcomes: {len(possible_outcome_list)}")
#     print(f"Number of opponent hand combinations: {len(opponent_hand_combinations)}")

#     for outcome in possible_outcome_list:
#         full_community = community_cards + list(outcome)
#         for opponent_hand in opponent_hand_combinations:
#             my_hand = hole_cards + full_community
#             opp_hand = list(opponent_hand) + full_community
#             result = compare_hands(my_hand, opp_hand)
#             if result == 1:
#                 win_count += 1
#             elif result == 0:
#                 win_count += 0.5
#             total_count += 1

#     if total_count == 0:
#         return 0

#     return (win_count / total_count) * 100

# def evaluate_flop(hole_cards, community_cards):
#     possible_turn_river_combinations = itertools.combinations([card_to_tuple(rank + suit) for rank in RANKS for suit in SUITS if card_to_tuple(rank + suit) not in set(hole_cards + community_cards)], 2)
#     return evaluate_hand_with_possible_outcomes(hole_cards, community_cards, possible_turn_river_combinations)

# def evaluate_turn(hole_cards, community_cards):
#     possible_rivers = itertools.combinations([card_to_tuple(rank + suit) for rank in RANKS for suit in SUITS if card_to_tuple(rank + suit) not in set(hole_cards + community_cards)], 1)
#     return evaluate_hand_with_possible_outcomes(hole_cards, community_cards, possible_rivers)

# def evaluate_river(hole_cards, community_cards):
#     return evaluate_hand_with_possible_outcomes(hole_cards, community_cards, [])

# def parallel_evaluator(evaluate_func, hole_cards, community_cards):
#     with multiprocessing.Pool() as pool:
#         results = pool.starmap(evaluate_func, [(hole_cards, community_cards)])
#     return sum(results) / len(results)

# if __name__ == "__main__":
#     hole_cards = [card_to_tuple('AC'), card_to_tuple('5S')]
#     community_cards_flop = [card_to_tuple('AD'), card_to_tuple('TH'), card_to_tuple('KC')]
#     community_cards_turn = community_cards_flop + [card_to_tuple('7D')]
#     community_cards_river = community_cards_turn + [card_to_tuple('7S')]

#     print("Flop Win Rate:", parallel_evaluator(evaluate_flop, hole_cards, community_cards_flop))
#     print("Turn Win Rate:", parallel_evaluator(evaluate_turn, hole_cards, community_cards_turn))
#     print("River Win Rate:", parallel_evaluator(evaluate_river, hole_cards, community_cards_river))
