# import os
# import json
# from game.game import setup_config, start_poker

# from agents.call_player import setup_ai as call_ai
# from agents.random_player import setup_ai as random_ai
# from agents.console_player import setup_ai as console_ai
# from agents.allin_player import setup_ai as allin_ai
# from agents.raise_100_player import setup_ai as raise_100_ai
# from agents.raise_250_player import setup_ai as raise_250_ai
# from agents.preflop_call_player import setup_ai as preflop_call_ai
# from agents.preflop_allin_player import setup_ai as preflop_allin_ai

# # from agents.flop import setup_ai as flop_ai
# from agents.flop_2 import setup_ai as flop_ai

# from baseline0 import setup_ai as baseline0_ai
# from baseline1 import setup_ai as baseline1_ai
# from baseline2 import setup_ai as baseline2_ai
# from baseline3 import setup_ai as baseline3_ai
# from baseline4 import setup_ai as baseline4_ai
# from baseline5 import setup_ai as baseline5_ai
# from baseline6 import setup_ai as baseline6_ai
# from baseline7 import setup_ai as baseline7_ai

# # config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
# config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)

# # player order: 2, 1, 2, 1, 2, 1...

# # ============ Baseline players ============
# config.register_player(name="p1", algorithm=baseline3_ai())

# # ============ Our players ============
# # config.register_player(name="p2", algorithm=random_ai())
# # config.register_player(name="p2", algorithm=call_ai())
# # config.register_player(name="p2", algorithm=allin_ai())
# # config.register_player(name="p2", algorithm=preflop_call_ai())
# config.register_player(name="p2", algorithm=preflop_allin_ai())
# # config.register_player(name="p2", algorithm=raise_100_ai())
# # config.register_player(name="p2", algorithm=raise_250_ai())

# # config.register_player(name="p2", algorithm=flop_ai())

# ## ============ Play in interactive mode if uncomment ============
# # config.register_player(name="me", algorithm=console_ai())

# game_result = start_poker(config, verbose=1)

# print(json.dumps(game_result, indent=4))

# # file_path = './results/game_result.json'
# # i = 0
# # while os.path.exists(file_path):
# #     i += 1
# #     file_path = './results/game_result_' + str(i) + '.json'
# # with open(file_path, 'w') as f:
# #     json.dump(game_result, f, indent=4)
# # print('Game result saved to', file_path)



import os
import json
import random
from tqdm import tqdm
from game.game import setup_config, start_poker

# from agents.call_player import setup_ai as call_ai
# from agents.random_player import setup_ai as random_ai
# from agents.console_player import setup_ai as console_ai
# from agents.allin_player import setup_ai as allin_ai
# from agents.raise_100_player import setup_ai as raise_100_ai
# from agents.raise_250_player import setup_ai as raise_250_ai
# from agents.preflop_call_player import setup_ai as preflop_call_ai
# from agents.preflop_allin_player import setup_ai as preflop_allin_ai
# from agents.flop_2 import setup_ai as flop_ai

from src.agent import setup_ai as preflop_allin_ai

from baseline0 import setup_ai as baseline0_ai
from baseline1 import setup_ai as baseline1_ai
from baseline2 import setup_ai as baseline2_ai
from baseline3 import setup_ai as baseline3_ai
from baseline4 import setup_ai as baseline4_ai
from baseline5 import setup_ai as baseline5_ai
from baseline6 import setup_ai as baseline6_ai
from baseline7 import setup_ai as baseline7_ai


def train_call_player_with_baselines(thresholds, baseline_players, training_rounds=1):
    results = {f"baseline{i}": {threshold: {'wins': 0, 'losses': 0, 'draws': 0, 'winning_rate': 0} for threshold in thresholds} for i in range(len(baseline_players))}

    for threshold in thresholds:
        print(f"Testing threshold: {threshold}")
        call_player = preflop_allin_ai()
        
        for baseline_index in tqdm(range(len(baseline_players))):
            for i in range(training_rounds):
                baseline_ai = baseline_players[baseline_index]
                baseline_name = f"baseline{baseline_index}"
                print('Playing against:', baseline_name)

                config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)

                if i % 2 == 0:
                    config.register_player(name="baseline", algorithm=baseline_ai())
                    config.register_player(name="call_player", algorithm=call_player)
                else:
                    config.register_player(name="call_player", algorithm=call_player)
                    config.register_player(name="baseline", algorithm=baseline_ai())

                game_result = start_poker(config, verbose=0)

                for player in game_result["players"]:
                    if player["name"] == "call_player":
                        if player["stack"] > 1000:
                            results[baseline_name][threshold]['wins'] += 1
                        elif player["stack"] < 1000:
                            results[baseline_name][threshold]['losses'] += 1
                        else:
                            results[baseline_name][threshold]['draws'] += 1

                        total_games = results[baseline_name][threshold]['wins'] + results[baseline_name][threshold]['losses'] + results[baseline_name][threshold]['draws']
                        if total_games > 0:
                            results[baseline_name][threshold]['winning_rate'] = results[baseline_name][threshold]['wins'] / total_games

            print(f"Testing against {baseline_name} with threshold {threshold} completed.")

    result_file = "./results/call_player_results.json"
    i = 0
    while os.path.exists(result_file):
        i += 1
        result_file = f'./results/call_player_results_{i}.json'
    with open(result_file, 'w') as f:
        json.dump(results, f, indent=4)
    print('Game result saved to', result_file)


# baseline_players = [
#     baseline0_ai, baseline1_ai, baseline2_ai, baseline3_ai,
#     baseline4_ai, baseline5_ai, baseline6_ai, baseline7_ai
# ]

baseline_players = [
    baseline3_ai
]


# 执行训练
# thresholds = range(40, 71)
# thresholds = [53, 49, 45, 44, 42]
thresholds = [45]
train_call_player_with_baselines(thresholds, baseline_players, training_rounds=1)
