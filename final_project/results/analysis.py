import json

def find_thresholds_above_rate(results, rate):
    # Initialize a set with all possible thresholds from the first baseline
    common_thresholds = set(results[next(iter(results))].keys())

    # Iterate over each baseline
    for baseline in results.values():
        # Find thresholds for the current baseline with a winning rate above the specified rate
        high_rate_thresholds = {threshold for threshold, data in baseline.items() if data['winning_rate'] > rate}
        # Keep only common thresholds across all baselines
        common_thresholds.intersection_update(high_rate_thresholds)
    
    return common_thresholds


# 53, 49, 45, 44, 42
def print_threshold_rates(results):
    # Iterate over each threshold
    for threshold in results[next(iter(results))].keys():
        print(f"Threshold: {threshold}")
        # Iterate over each baseline
        for baseline_name, baseline in results.items():
            if threshold in baseline:
                win_rate = baseline[threshold]['winning_rate']
                print(f"  {baseline_name}: {win_rate:.2f}")
        print()



# Load the results JSON file
file_path = './call_player_results_1.json'
with open(file_path, 'r') as file:
    results = json.load(file)

print_threshold_rates(results)

# # Define the rate threshold
# rate_threshold = 0.3

# # Find thresholds where the winning rate is above the specified rate for all baselines
# valid_thresholds = find_thresholds_above_rate(results, rate_threshold)

# print(f"Thresholds with winning rate > {rate_threshold} for all baselines: {sorted(valid_thresholds)}")
