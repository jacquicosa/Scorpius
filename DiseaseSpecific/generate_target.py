import json
import random
import os
import pickle
import argparse
from collections import Counter

# This connects to the 'Parameters' file to load the entity and relation mappings
import sys
sys.path.append("..")
import Parameters

def main():
    # Path to training data
    # This is the 'Library' we are looking through
    train_path = "processed_data/GNBR/train.txt"
    
    chemical_counts = Counter()
    
    # Count how often each drug (chemical) appears
    print("Reading library to find the most popular drugs...")
    with open(train_path, 'r') as f:
        for line in f:
            # Each line is: SubjectID, RelationID, ObjectID
            parts = line.strip().split('\t')
            s, o = int(parts[0]), int(parts[2])
            
            # If it's a chemical, count it
            if Parameters.entityid_to_nodetype.get(s) == 'chemical':
                chemical_counts[s] += 1
            if Parameters.entityid_to_nodetype.get(o) == 'chemical':
                chemical_counts[o] += 1

    # Get the Top 80 most popular drugs
    top_80_drugs = [drug_id for drug_id, count in chemical_counts.most_common(80)]

    # Find all possible diseases to pick from
    all_diseases = [ent_id for ent_id, n_type in Parameters.entityid_to_nodetype.items() 
                    if n_type == 'disease']

    # Create the "Hit List" (Target Triples)
    # Relation ID 10 = "treatment/therapy" found in relations_dict.json. Essentially we are creating triples of the form (Drug, "treatment/therapy", Disease)
    TARGET_RELATION = 10
    hit_list = []
    
    print(f"Picking 5 random diseases for each of the top 80 drugs...")
    for drug in top_80_drugs:
        target_diseases = random.sample(all_diseases, 5)
        for disease in target_diseases:
            # Format: (Drug, Relation 10, Disease)
            hit_list.append((drug, TARGET_RELATION, disease))

    # Save the list so 'attack.py' can find it
    # The original code looks for 'target_data.pkl'
    with open('target_data.pkl', 'wb') as f:
        pickle.dump(hit_list, f)
        
    print(f"Success! Created a hit list with {len(hit_list)} targets.")

if __name__ == "__main__":
    main()