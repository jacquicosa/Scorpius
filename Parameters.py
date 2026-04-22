import json
import os

# The absolute root of your project
BASE_PATH = "/homes/iws/jacqub3/Scorpius"

# The specific directory for raw data
# Added trailing slash because attack.py does: GNBRfile + 'entity_raw_name'
GNBRfile = os.path.join(BASE_PATH, "GNBRdata") + "/"

# Paths for the KG dictionaries in the DiseaseSpecific folder
kg_data_path = os.path.join(BASE_PATH, "DiseaseSpecific/processed_data/GNBR/")
rel_path = os.path.join(kg_data_path, "relations_dict.json")
ent_path = os.path.join(kg_data_path, "entities_dict.json")

def load_relations(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.load(f)
        return {int(v): k for k, v in data.items()}
    return {}

def load_entities(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.load(f)
        id_to_type = {}
        for key, val in data.items():
            # Standardizes 'chemical_mesh:c05' -> 'chemical'
            node_type = key.split('_')[0]
            id_to_type[int(val)] = node_type
        return id_to_type
    return {}

# These are the specific attributes the Tracebacks showed were missing
edge_id_to_type = load_relations(rel_path)
entityid_to_nodetype = load_entities(ent_path)