# import random
# import os
# import json
# from game.game import setup_config, start_poker
# from agents.mccfr_player import MCCFRPlayer
# from baseline0 import setup_ai as baseline0_ai
# from baseline1 import setup_ai as baseline1_ai
# from baseline2 import setup_ai as baseline2_ai
# from baseline3 import setup_ai as baseline3_ai
# from baseline4 import setup_ai as baseline4_ai
# from baseline5 import setup_ai as baseline5_ai
# from baseline6 import setup_ai as baseline6_ai
# from baseline7 import setup_ai as baseline7_ai

# # 基准玩家列表
# baseline_players = [
#     baseline0_ai, baseline1_ai, baseline2_ai, baseline3_ai,
#     baseline4_ai, baseline5_ai, baseline6_ai, baseline7_ai
# ]

# # MCCFR Player设置
# iterations = 100000
# model_file = "./agents/model/mccfr_model.pkl"
# mccfr_player = MCCFRPlayer(iterations=iterations, model_file=model_file)

# # 训练过程
# def train_mccfr_with_baselines(mccfr_player, baseline_players, training_rounds=500):
#     results = {f"baseline{i}": {'wins': 0, 'losses': 0, 'draws': 0} for i in range(len(baseline_players))}

#     for i in range(training_rounds):
#         # 随机选择一个基准玩家
#         baseline_index = random.randint(0, len(baseline_players) - 1)
#         baseline_ai = baseline_players[baseline_index]
#         baseline_name = f"baseline{baseline_index}"
        
#         # 设置游戏配置
#         config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
        
#         # 注册玩家
#         config.register_player(name="mccfr", algorithm=mccfr_player)
#         config.register_player(name="baseline", algorithm=baseline_ai())
        
#         # 运行游戏
#         game_result = start_poker(config, verbose=1)

#         # 记录胜负
#         for player in game_result["players"]:
#             if player["name"] == "mccfr":
#                 if player["stack"] > 1000:
#                     results[baseline_name]['wins'] += 1
#                 elif player["stack"] < 1000:
#                     results[baseline_name]['losses'] += 1
#                 else:
#                     results[baseline_name]['draws'] += 1
        
#         print(f"Training round {i+1}/{training_rounds} completed.")
    
#     # 保存训练后的模型
#     mccfr_player.save_model(model_file)
#     print("Training completed and model saved.")

#     result_file_path = './results/mccfr/mccfr_results.json'
#     i = 0
#     while os.path.exists(result_file_path):
#         i += 1
#         result_file_path = './results/mccfr/mccfr_results_' + str(i) + '.json'
#     with open(result_file_path, 'w') as f:
#         json.dump(results, f, indent=4)
#     print('Game result saved to', result_file_path)

# # 执行训练
# train_mccfr_with_baselines(mccfr_player, baseline_players)



import random
import os
import json
from tqdm import tqdm
from game.game import setup_config, start_poker
from agents.mccfr_player import MCCFRPlayer, visualize_regret
from baseline0 import setup_ai as baseline0_ai
from baseline1 import setup_ai as baseline1_ai
from baseline2 import setup_ai as baseline2_ai
from baseline3 import setup_ai as baseline3_ai
from baseline4 import setup_ai as baseline4_ai
from baseline5 import setup_ai as baseline5_ai
from baseline6 import setup_ai as baseline6_ai
from baseline7 import setup_ai as baseline7_ai

# def train_mccfr_with_baselines(mccfr_player, baseline_players, training_rounds=1000):
#     results = {f"baseline{i}": {'wins': 0, 'losses': 0, 'draws': 0, 'winning_rate': 0} for i in range(len(baseline_players))}
#     win_rates = {f"baseline{i}": [] for i in range(len(baseline_players))}

#     for i in tqdm(range(training_rounds)):
#         baseline_index = random.randint(0, len(baseline_players) - 1)
#         baseline_ai = baseline_players[baseline_index]
#         baseline_name = f"baseline{baseline_index}"
#         print('playing against:', baseline_name)
        
#         # 设置游戏配置
#         config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
        
#         # 注册玩家
#         config.register_player(name="mccfr", algorithm=mccfr_player)
#         config.register_player(name="baseline", algorithm=baseline_ai())
        
#         game_result = start_poker(config, verbose=1)

#         # 记录胜负
#         for player in game_result["players"]:
#             if player["name"] == "mccfr":
#                 if player["stack"] > 1000:
#                     results[baseline_name]['wins'] += 1
#                 elif player["stack"] < 1000:
#                     results[baseline_name]['losses'] += 1
#                 else:
#                     results[baseline_name]['draws'] += 1

#                 results[baseline_name]['winning_rate'] = results[baseline_name]['wins'] / (results[baseline_name]['wins'] + results[baseline_name]['losses'] + results[baseline_name]['draws'])

#         total_games = results[baseline_name]['wins'] + results[baseline_name]['losses'] + results[baseline_name]['draws']
#         # win_rate = results[baseline_name]['wins'] / total_games if total_games > 0 else 0
#         # win_rates[baseline_name].append(win_rate)
        
#         print(f"Training round {i+1}/{training_rounds} completed.")
#         print()
#         print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
#         print()
    
#     mccfr_player.save_model(model_file)
#     # visualize_regret(mccfr_player.mccfr)
#     print("Training completed and model saved.")

def train_mccfr_with_baselines(mccfr_player, baseline_players, rounds_per_baseline=10):
    results = {f"baseline{i}": {'wins': 0, 'losses': 0, 'draws': 0, 'winning_rate': 0} for i in range(len(baseline_players))}
    win_rates = {f"baseline{i}": [] for i in range(len(baseline_players))}

    for baseline_index, baseline_ai in enumerate(baseline_players):
        baseline_name = f"baseline{baseline_index}"
        print(f'Training against: {baseline_name}')

        for i in tqdm(range(rounds_per_baseline)):
            config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
            
            if i % 2 == 0:
                config.register_player(name="mccfr", algorithm=mccfr_player)
                config.register_player(name="baseline", algorithm=baseline_ai())
            else:
                config.register_player(name="baseline", algorithm=baseline_ai())
                config.register_player(name="mccfr", algorithm=mccfr_player)
            
            game_result = start_poker(config, verbose=1)

            for player in game_result["players"]:
                if player["name"] == "mccfr":
                    if player["stack"] > 1000:
                        results[baseline_name]['wins'] += 1
                    elif player["stack"] < 1000:
                        results[baseline_name]['losses'] += 1
                    else:
                        results[baseline_name]['draws'] += 1

                    results[baseline_name]['winning_rate'] = results[baseline_name]['wins'] / (results[baseline_name]['wins'] + results[baseline_name]['losses'] + results[baseline_name]['draws'])

            total_games = results[baseline_name]['wins'] + results[baseline_name]['losses'] + results[baseline_name]['draws']
            win_rate = results[baseline_name]['wins'] / total_games if total_games > 0 else 0
            win_rates[baseline_name].append(win_rate)
            
            print(f"Training round {i+1}/{rounds_per_baseline} against {baseline_name} completed.")
            print()
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print()
    
    mccfr_player.save_model(model_file)
    visualize_regret(mccfr_player.mccfr)
    print("Training completed and model saved.")

    result_file = "./results/mccfr/mccfr_results.json"
    i = 0
    while os.path.exists(result_file):
        i += 1
        result_file = 'results/mccfr/mccfr_results_' + str(i) + '.json'
    with open(result_file, 'w') as f:
        json.dump(results, f, indent=4)
    print('Game result saved to', result_file)


# 基准玩家列表
baseline_players = [
    baseline0_ai, baseline1_ai, baseline2_ai, baseline3_ai,
    baseline4_ai, baseline5_ai, baseline6_ai, baseline7_ai
]

# MCCFR Player设置
iterations = 10000
# model_file = "mccfr_model.pkl"
model_file = "./agents/model/mccfr_model.pkl"
mccfr_player = MCCFRPlayer(iterations=iterations, model_file=model_file)



train_mccfr_with_baselines(mccfr_player, baseline_players, rounds_per_baseline=100)
# train_mccfr_with_baselines(mccfr_player, baseline_players)

# ================================================================================================================
# ======================================== The above is the original code ========================================
# ================================================================================================================



# import random
# import os
# import json
# from tqdm import tqdm
# from game.game import setup_config, start_poker
# from agents.mccfr_player import MCCFRPlayer, visualize_regret
# from baseline0 import setup_ai as baseline0_ai
# from baseline1 import setup_ai as baseline1_ai
# from baseline2 import setup_ai as baseline2_ai
# from baseline3 import setup_ai as baseline3_ai
# from baseline4 import setup_ai as baseline4_ai
# from baseline5 import setup_ai as baseline5_ai
# from baseline6 import setup_ai as baseline6_ai
# from baseline7 import setup_ai as baseline7_ai

# # 基准玩家列表
# baseline_players = [
#     baseline0_ai, baseline1_ai, baseline2_ai, baseline3_ai,
#     baseline4_ai, baseline5_ai, baseline6_ai, baseline7_ai
# ]

# # MCCFR Player设置
# iterations = 10000
# model_file = "./mccfr_model-2.pkl"
# mccfr_player = MCCFRPlayer(iterations=iterations, model_file=model_file)

# # 训练过程
# def train_mccfr_with_baselines(mccfr_player, baseline_players, training_rounds=2):
#     results = {f"baseline{i}": {'wins': 0, 'losses': 0, 'draws': 0, 'winning_rate': 0} for i in range(len(baseline_players))}
#     win_rates = {f"baseline{i}": [] for i in range(len(baseline_players))}

#     for i in tqdm(range(training_rounds)):
#         baseline_index = random.randint(0, len(baseline_players) - 1)
#         baseline_ai = baseline_players[baseline_index]
#         baseline_name = f"baseline{baseline_index}"
#         print('playing against:', baseline_name)
        
#         # 设置游戏配置
#         config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
        
#         # 注册玩家
#         config.register_player(name="mccfr", algorithm=mccfr_player)
#         config.register_player(name="baseline", algorithm=baseline_ai())
        
#         game_result = start_poker(config, verbose=1)

#         # 记录胜负
#         for player in game_result["players"]:
#             if player["name"] == "mccfr":
#                 if player["stack"] > 1000:
#                     results[baseline_name]['wins'] += 1
#                 elif player["stack"] < 1000:
#                     results[baseline_name]['losses'] += 1
#                 else:
#                     results[baseline_name]['draws'] += 1

#                 results[baseline_name]['winning_rate'] = results[baseline_name]['wins'] / (results[baseline_name]['wins'] + results[baseline_name]['losses'] + results[baseline_name]['draws'])

#         total_games = results[baseline_name]['wins'] + results[baseline_name]['losses'] + results[baseline_name]['draws']
#         win_rate = results[baseline_name]['wins'] / total_games if total_games > 0 else 0
#         win_rates[baseline_name].append(win_rate)
        
#         print(f"Training round {i+1}/{training_rounds} completed.")
#         print()
#         print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
#         print()
    
#     mccfr_player.save_model(model_file)
#     visualize_regret(mccfr_player.mccfr)
#     print("Training completed and model saved.")

# # 执行训练
# train_mccfr_with_baselines(mccfr_player, baseline_players)
