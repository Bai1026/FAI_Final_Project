import json

def read_json_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def merge_baselines(data_list):
    merged_data = {}

    for data in data_list:
        for baseline in data.keys():
            if baseline not in merged_data:
                merged_data[baseline] = {
                    'wins': 0,
                    'losses': 0,
                    'draws': 0
                }
            
            merged_data[baseline]['wins'] += data[baseline].get('wins', 0)
            merged_data[baseline]['losses'] += data[baseline].get('losses', 0)
            merged_data[baseline]['draws'] += data[baseline].get('draws', 0)

    for baseline in merged_data:
        total_wins = merged_data[baseline]['wins']
        total_losses = merged_data[baseline]['losses']
        total_draws = merged_data[baseline]['draws']
        total_games = total_wins + total_losses + total_draws

        winning_rate = total_wins / total_games if total_games > 0 else 0
        merged_data[baseline]['winning_rate'] = winning_rate

    return merged_data

def save_json_file(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


data4 = read_json_file('./no_switch/mccfr_results.json')
data1 = read_json_file('./no_switch/mccfr_results_1.json')
data2 = read_json_file('./no_switch/mccfr_results_2.json')
data3 = read_json_file('./no_switch/mccfr_results_3.json')
data4 = read_json_file('./no_switch/mccfr_results_4.json')

data_list = [data1, data2, data3, data4]
merged_data = merge_baselines(data_list)

save_json_file(merged_data, './no_switch/mccfr_results_merged.json')

print("Merged data has been saved to './no_switch/mccfr_results_merged.json'")
