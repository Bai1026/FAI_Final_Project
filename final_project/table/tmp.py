import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from treys import Evaluator, Card

# 初始化評估器
evaluator = Evaluator()

# 創建一個13x13的矩陣來存儲勝率
win_rates = np.zeros((13, 13))

# 所有的牌值和花色
values = '23456789TJQKA'
suits = 'shdc'

# 對每個起手牌組合進行計算
for i, v1 in enumerate(values):
    for j, v2 in enumerate(values):
        if i < j:  # 同花
            hand = [Card.new(v1 + suits[0]), Card.new(v2 + suits[0])]
        elif i > j:  # 不同花
            hand = [Card.new(v1 + suits[0]), Card.new(v2 + suits[1])]
        else:
            win_rates[i, j] = np.nan
            continue

        # 模擬多次對局來計算平均勝率
        wins = 0
        trials = 1000
        for _ in range(trials):
            board = [Card.new(v + suits[0]) for v in np.random.choice(values, 5)]
            opponent_hand = [Card.new(v + suits[1]) for v in np.random.choice(values, 2)]
            if evaluator.evaluate(board, hand) < evaluator.evaluate(board, opponent_hand):
                wins += 1

        win_rates[i, j] = wins / trials

# 繪製熱圖
fig, ax = plt.subplots(figsize=(10, 10))
sns.heatmap(win_rates, annot=True, fmt=".2f", cmap="RdYlGn", xticklabels=values, yticklabels=values, ax=ax)
plt.title('Preflop Win Rates')
plt.xlabel('Card 1')
plt.ylabel('Card 2')
# plt.show()
plt.savefig('win_rates.png')
