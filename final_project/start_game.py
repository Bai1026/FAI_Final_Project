import os
import json
from game.game import setup_config, start_poker
from agents.call_player import setup_ai as call_ai
from agents.call_player import setup_ai_allin as call_ai_allin
from agents.random_player import setup_ai as random_ai
from agents.console_player import setup_ai as console_ai

from baseline0 import setup_ai as baseline0_ai
from baseline1 import setup_ai as baseline1_ai
from baseline2 import setup_ai as baseline2_ai
from baseline3 import setup_ai as baseline3_ai
from baseline4 import setup_ai as baseline4_ai
from baseline5 import setup_ai as baseline5_ai
from baseline6 import setup_ai as baseline6_ai
from baseline7 import setup_ai as baseline7_ai

config = setup_config(max_round=20, initial_stack=1000, small_blind_amount=5)

# baseline players
# config.register_player(name="p1", algorithm=baseline0_ai())
config.register_player(name="p1", algorithm=baseline1_ai())

# our players
# config.register_player(name="p2", algorithm=random_ai())
config.register_player(name="p2", algorithm=call_ai())
# config.register_player(name="p2", algorithm=call_ai_allin())

## Play in interactive mode if uncomment
#config.register_player(name="me", algorithm=console_ai())
game_result = start_poker(config, verbose=1)

print(json.dumps(game_result, indent=4))

file_path = './results/game_result.json'
i = 0
while os.path.exists(file_path):
    i += 1
    file_path = './results/game_result_' + str(i) + '.json'
with open(file_path, 'w') as f:
    json.dump(game_result, f, indent=4)
print('Game result saved to', file_path)
