import os
import pickle
import sys
from collections import Counter
import random

# 1. PORTABLE PATH ANCHORING
# Get the directory where THIS script is saved
base_dir = os.path.dirname(os.path.abspath(__file__))

# Build the path relative to the script's location
# This works whether you are on your local machine or a server
data_file = os.path.join(base_dir, "processed_data", "GNBR", "edge_nghbrs.pickle")

# Add the parent directory to sys.path so we can import Parameters.py
sys.path.append(os.path.dirname(base_dir))
import Parameters

def main():
    print(f"--- Target Generation Started ---")
    print(f"Searching for Library at: {data_file}")
    
    # 2. Check if the file exists
    if not os.path.exists(data_file):
        print(f"ERROR: Could not find the data file at {data_file}")
        print("Ensure the 'processed_data' folder is in the same directory as this script.")
        return

    # 3. Load the binary dictionary {node_id: [neighbors]}
    try:
        with open(data_file, 'rb') as f:
            edge_data = pickle.load(f)
    except Exception as e:
        print(f"ERROR: Failed to load pickle file. {e}")
        return

    chemical_counts = Counter()
    
    print("Scanning the Knowledge Graph for the most active chemicals...")
    
    # 4. Count appearances of chemicals (drugs)
    for node, neighbors in edge_data.items():
        node_str = str(node)
        node_type = Parameters.entityid_to_nodetype.get(node_str)
        
        if node_type == 'chemical':
            chemical_counts[node_str] += len(neighbors)

    # 5. Extract the Top 80 most connected drugs
    top_80_drugs = [drug_id for drug_id, count in chemical_counts.most_common(80)]
    
    if not top_80_drugs:
        print("CRITICAL ERROR: No chemicals found in the data!")
        return

    # 6. Save 'target_data.pkl' in the same folder as the script
    output_path = os.path.join(base_dir, 'target_data.pkl')
    
    try:
        with open(output_path, 'wb') as f:
            pickle.dump(top_80_drugs, f)
        print(f"--- Success! ---")
        print(f"Created 'target_data.pkl' with {len(top_80_drugs)} target drugs.")
    except Exception as e:
        print(f"ERROR: Could not save the target list. {e}")

if __name__ == "__main__":
    main()