import json
import numpy as np

# Format: [nombre, edat, hores, dies, preferències x5]

def load():
    with open("data/casos_sintetics.json") as f:
        casos = json.load(f)
    return np.array(casos)