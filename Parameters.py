import json
import os

# Path to your relations dict
rel_path = "DiseaseSpecific/processed_data/GNBR/relations_dict.json"

def load_relations(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.load(f)
        # Invert the dictionary: {0: "chemical-gene:...", 1: "..."}
        return {int(v): k for k, v in data.items()}
    else:
        print(f"Warning: Could not find {path}")
        return {}

# This is the variable attack.py is looking for
edge_id_to_type = load_relations(rel_path)

# Based on your entities_dict, we can also define types here
# chemical_..., gene_..., disease_...
node_types = ['chemical', 'gene', 'disease']

def load_entities(path):
    ent_path = "DiseaseSpecific/processed_data/GNBR/entities_dict.json"
    if os.path.exists(ent_path):
        with open(ent_path, 'r') as f:
            data = json.load(f)
        # Create a mapping of {ID: "type"} 
        # Example: {103: "chemical"}
        id_to_type = {}
        for key, val in data.items():
            node_type = key.split('_')[0]
            id_to_type[int(val)] = node_type
        return id_to_type
    return {}

entityid_to_nodetype = load_entities("DiseaseSpecific/processed_data/GNBR/entities_dict.json")