import random
import json
import os
import logging
from tqdm import tqdm
from game.game import setup_config, start_poker
# from agents.dqn_player import QLearningPlayer
from agents.dqn_player import setup_ai as dqn_ai

from agents.dqn_player import setup_ai as dqn_ai

from baseline0 import setup_ai as baseline0_ai
from baseline1 import setup_ai as baseline1_ai
from baseline2 import setup_ai as baseline2_ai
from baseline3 import setup_ai as baseline3_ai
from baseline4 import setup_ai as baseline4_ai
from baseline5 import setup_ai as baseline5_ai
from baseline6 import setup_ai as baseline6_ai
from baseline7 import setup_ai as baseline7_ai


def train_dqn_learning_with_baselines(dqn_ai, baseline_players, rounds_per_baseline=2):
    results = {f"baseline{i}": {'wins': 0, 'losses': 0, 'draws': 0, 'winning_rate': 0} for i in range(len(baseline_players))}
    logger = logging.getLogger(__name__)

    for baseline_index, baseline_ai in enumerate(baseline_players):
        baseline_name = f"baseline{baseline_index}"
        print(f'Training against: {baseline_name}')

        for i in tqdm(range(rounds_per_baseline)):
            
            config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)
            config.register_player(name="dqn", algorithm=dqn_ai)
            config.register_player(name="baseline", algorithm=baseline_ai())
            
            game_result = start_poker(config, verbose=1)

            for player in game_result["players"]:
                if player["name"] == "dqn":
                    if player["stack"] > 1000:
                        results[baseline_name]['wins'] += 1
                    elif player["stack"] < 1000:
                        results[baseline_name]['losses'] += 1
                    else:
                        results[baseline_name]['draws'] += 1
                    results[baseline_name]['winning_rate'] = results[baseline_name]['wins'] / (results[baseline_name]['wins'] + results[baseline_name]['losses'] + results[baseline_name]['draws'])

            # print(f"Training round {i+1}/{training_rounds} completed.")
            # logger.info(f"Round {i+1}/{rounds_per_baseline} against {baseline_name}: Results - {results}")
            print(f"Training round {i+1}/{rounds_per_baseline} against {baseline_name} completed.")
            print()
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print()
    
    dqn_player.save_model()
    print("Training completed and model saved.")
    logger.info("Training completed and model saved.")

    result_file = "./results/dqn/dqn_results.json"
    i = 0
    while os.path.exists(result_file):
        i += 1
        result_file = 'results/dqn/dqn_results_' + str(i) + '.json'
    with open(result_file, 'w') as f:
        json.dump(results, f, indent=4)
    print('Game result saved to', result_file)

import logging

# Set up logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("./results/dqn/dqn_training.log"),  # Output to file
                        logging.StreamHandler()  # Output to console
                    ])


model_file = "./agents/model/dqn_model.pkl"
rounds_per_baseline = 50
# Ensure this part is correct in your main script

baseline_players = [
    baseline0_ai, baseline1_ai, baseline2_ai, baseline3_ai,
    baseline4_ai, baseline5_ai, baseline6_ai, baseline7_ai
]

# baseline_players = [
#     baseline0_ai, baseline1_ai
# ]


if __name__ == "__main__":
    dqn_player = dqn_ai()
    train_dqn_learning_with_baselines(dqn_player, baseline_players, rounds_per_baseline=rounds_per_baseline)
    print('end')

