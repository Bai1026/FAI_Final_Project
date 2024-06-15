import random
import json
from collections import Counter
from itertools import combinations

def evaluate_hand(hand):
    """评估手牌的强度（简化版）"""
    ranks = '23456789TJQKA'
    values = {r: i for i, r in enumerate(ranks, 2)}
    hand_ranks = sorted([values[card[0]] for card in hand], reverse=True)
    return hand_ranks

def simulate_hand(hole_cards, community_cards, iterations=10000):
    deck = [r+s for r in '23456789TJQKA' for s in 'HDSC']
    deck = [card for card in deck if card not in hole_cards + community_cards]

    wins, losses, ties = 0, 0, 0

    for _ in range(iterations):
        random.shuffle(deck)
        opponent_hole = deck[:2]
        remaining_community = deck[2:5]

        final_community = community_cards + remaining_community
        my_hand = hole_cards + final_community
        opponent_hand = opponent_hole + final_community

        my_hand_rank = evaluate_hand(my_hand)
        opponent_hand_rank = evaluate_hand(opponent_hand)

        if my_hand_rank > opponent_hand_rank:
            wins += 1
        elif my_hand_rank < opponent_hand_rank:
            losses += 1
        else:
            ties += 1

    total = wins + losses + ties
    return {
        'win': wins / total * 100,
        'lose': losses / total * 100,
        'tie': ties / total * 100
    }

# 示例使用
hole_cards = ['AC', 'KD']
community_cards = ['H6', 'D9', 'ST']

result = simulate_hand(hole_cards, community_cards)
print(f"Win: {result['win']:.2f}%")
print(f"Lose: {result['lose']:.2f}%")
print(f"Tie: {result['tie']:.2f}%")

flop_table = []

# 示例手牌
hands = [
    (['AC', 'KD'], ['H6', 'D9', 'ST']),
    (['QH', 'QS'], ['H6', 'D9', 'ST']),
    # 添加更多手牌组合...
]

for hole_cards, community_cards in hands:
    result = simulate_hand(hole_cards, community_cards)
    # 判断是否为同花色
    if hole_cards[0][1] == hole_cards[1][1]:
        suited = 's'
    else:
        suited = 'u'
    hand_str = f"{hole_cards[0][0]}/{hole_cards[1][0]}/{suited}"
    flop_table.append({
        'hand': hand_str,
        'win': result['win'],
        'lose': result['lose'],
        'tie': result['tie'],
        'expected_value': result['win'] - result['lose'],
        'additional_chance': result['tie']
    })

with open('flop_odds.json', 'w') as f:
    json.dump({'flop_table': flop_table}, f, indent=4)