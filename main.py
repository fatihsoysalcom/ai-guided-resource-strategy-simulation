import random

# --- Configuration ---
NUM_HUMANS = 6
INITIAL_RESOURCE_POOL = 500
NUM_ROUNDS = 10

# --- Stratagems (Tactics) ---
# Each stratagem is a function that takes (agent_id, current_pool, agent_score)
# and returns the amount to attempt to take.
def stratagem_greedy(agent_id, current_pool, agent_score):
    """Attempts to take a fixed large amount, prioritizing individual gain."""
    return min(current_pool, 30) # Take up to 30 units, or whatever is left

def stratagem_cautious(agent_id, current_pool, agent_score):
    """Attempts to take a fixed small amount, conserving resources."""
    return min(current_pool, 5) # Take up to 5 units, or whatever is left

def stratagem_proportional(agent_id, current_pool, agent_score):
    """Attempts to take a percentage of the remaining pool, adapting to availability."""
    return min(current_pool, int(current_pool * 0.15)) # Take 15% of remaining, or whatever is left

def ai_decision_maker(agent_id, current_pool, agent_score, all_stratagems):
    """
    A simple 'AI' that suggests the best stratagem based on current state.
    This simulates an AI-powered strategy, adapting to the 'rabbit hole' of changing conditions.
    """
    # Simple heuristic AI logic:
    if current_pool < 50: # If resources are very low
        # Suggest a cautious approach to prolong the game or ensure minimal gain.
        print(f"  AI for Human {agent_id}: Pool low ({current_pool}), suggesting Cautious.")
        return all_stratagems['cautious']
    elif agent_score < 100 and current_pool > 200: # If agent is behind and resources are abundant
        # Suggest a greedy approach to catch up.
        print(f"  AI for Human {agent_id}: Score low ({agent_score}), Pool high, suggesting Greedy.")
        return all_stratagems['greedy']
    else:
        # Otherwise, take a balanced, proportional approach.
        print(f"  AI for Human {agent_id}: Defaulting to Proportional.")
        return all_stratagems['proportional']

# Map of stratagem names to their functions
ALL_STRATAGEMS = {
    'greedy': stratagem_greedy,
    'cautious': stratagem_cautious,
    'proportional': stratagem_proportional,
}

# --- Simulation Setup ---
humans = [{'id': i, 'score': 0, 'chosen_stratagem_name': None} for i in range(NUM_HUMANS)]
resource_pool = INITIAL_RESOURCE_POOL

# Assign initial stratagems to humans.
# For demonstration, a mix of fixed strategies and one AI-powered agent.
humans[0]['chosen_stratagem_name'] = 'greedy'
humans[1]['chosen_stratagem_name'] = 'cautious'
humans[2]['chosen_stratagem_name'] = 'proportional'
humans[3]['chosen_stratagem_name'] = 'greedy'
humans[4]['chosen_stratagem_name'] = 'cautious'
humans[5]['chosen_stratagem_name'] = 'ai_powered' # This human uses the AI to pick their stratagem

print("--- Simulation Start ---")
print(f"Initial Resource Pool: {resource_pool}")
for i, human in enumerate(humans):
    print(f"Human {human['id']} starts with score {human['score']} and uses stratagem: {human['chosen_stratagem_name']}")
print("-" * 30)

# --- Simulation Loop ---
for round_num in range(1, NUM_ROUNDS + 1):
    print(f"\n--- Round {round_num} ---")
    print(f"Resource Pool at start of round: {resource_pool}")

    # Randomize turn order for fairness
    turn_order = list(range(NUM_HUMANS))
    random.shuffle(turn_order)

    for human_idx in turn_order:
        human = humans[human_idx]
        stratagem_name = human['chosen_stratagem_name']
        
        # Determine the actual stratagem function to use
        actual_stratagem_func = None
        if stratagem_name == 'ai_powered':
            # If the human uses the AI-powered strategy, the AI decides which base stratagem to use.
            # This is where the 'AI-powered' aspect comes in, adapting to the current state.
            actual_stratagem_func = ai_decision_maker(human['id'], resource_pool, human['score'], ALL_STRATAGEMS)
            print(f"Human {human['id']} (AI-Powered) decision process:")
        else:
            actual_stratagem_func = ALL_STRATAGEMS[stratagem_name]

        # Calculate amount to take based on the chosen (or AI-suggested) stratagem
        amount_to_take = actual_stratagem_func(human['id'], resource_pool, human['score'])
        
        # Ensure not to take more than available
        actual_taken = min(amount_to_take, resource_pool)
        
        resource_pool -= actual_taken
        human['score'] += actual_taken
        
        print(f"Human {human['id']} ({stratagem_name}{' via AI' if stratagem_name == 'ai_powered' else ''}) tried to take {amount_to_take}, took {actual_taken}. Pool remaining: {resource_pool}")
        
        if resource_pool <= 0:
            print("Resource pool depleted!")
            break
    
    if resource_pool <= 0:
        break

print("\n--- Simulation End ---")
print(f"Final Resource Pool: {resource_pool}")
print("Final Scores:")
for human in humans:
    print(f"Human {human['id']}: Score = {human['score']}")

# --- Analysis ---
print("\n--- Analysis of Strategies ---")
scores_by_strategy = {}
for human in humans:
    strat_name = human['chosen_stratagem_name']
    if strat_name not in scores_by_strategy:
        scores_by_strategy[strat_name] = []
    scores_by_strategy[strat_name].append(human['score'])

for strat_name, scores in scores_by_strategy.items():
    avg_score = sum(scores) / len(scores)
    print(f"Strategy '{strat_name}': Average Score = {avg_score:.2f}, Individual Scores = {scores}")
