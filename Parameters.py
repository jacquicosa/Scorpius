import json
import os

# Get the absolute path to the project root
# This ensures it works no matter where you run the script from
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# 1. The missing variable the error asked for:
# This points to the folder containing 'entity_raw_name'
GNBRfile = os.path.join(BASE_PATH, "DiseaseSpecific/processed_data/GNBR/")

# 2. Paths for the dict files
rel_path = os.path.join(GNBRfile, "relations_dict.json")
ent_path = os.path.join(GNBRfile, "entities_dict.json")

def load_relations(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.load(f)
        return {int(v): k for k, v in data.items()}
    else:
        print(f"Warning: Could not find {path}")
        return {}

def load_entities(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.load(f)
        id_to_type = {}
        for key, val in data.items():
            node_type = key.split('_')[0]
            id_to_type[int(val)] = node_type
        return id_to_type
    return {}

# Variables expected by attack.py
edge_id_to_type = load_relations(rel_path)
entityid_to_nodetype = load_entities(ent_path)