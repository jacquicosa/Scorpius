import json
import random
import os
import pickle
from collections import Counter

# This connects to the 'Parameters' file
import sys
sys.path.append("..")
import Parameters

def main():
    # --- FIX 1: DYNAMIC PATHING ---
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Build the path to the training data relative to this script
    train_path = os.path.join(script_dir, "processed_data", "GNBR", "train.txt")
    
    chemical_counts = Counter()
    
    print(f"Reading library at: {train_path}")
    if not os.path.exists(train_path):
        print(f"Error: Could not find train.txt at {train_path}")
        return

    with open(train_path, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 3: continue
            s, o = int(parts[0]), int(parts[2])
            
            if Parameters.entityid_to_nodetype.get(s) == 'chemical':
                chemical_counts[s] += 1
            if Parameters.entityid_to_nodetype.get(o) == 'chemical':
                chemical_counts[o] += 1

    # Get the Top 80 most popular drugs
    top_80_drugs = [str(drug_id) for drug_id, count in chemical_counts.most_common(80)]

    # --- FIX 2: ALIGNING WITH ATTACK.PY ---
    # According to attack.py: 'for i, target in enumerate(target_data):'
    # and: 'target_trip.append([target, str(10), disease])'
    # We only need to save the list of Drug IDs.
    
    output_path = os.path.join(script_dir, 'target_data.pkl')
    with open(output_path, 'wb') as f:
        pickle.dump(top_80_drugs, f)
        
    print(f"Success! Created a target drug list with {len(top_80_drugs)} drugs at {output_path}.")

if __name__ == "__main__":
    main()