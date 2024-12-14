import numpy as np
import json

rng = np.random.default_rng()

with open('dades/tipus_grup.json') as f:
    grups_base = json.load(f)
grups_base = set(grups_base.values())

def generar(n):
    rng.choice()