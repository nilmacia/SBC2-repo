from cbr import CBR
from base_casos import Node

import numpy as np

synthetic_cases = [[2, 30, 3, 1, 3, 0, 0, 0, 1, 0],
    [2, 25, 6, 1, 4, 0, 0, 0, 0, 1],
    [4, 25, 2, 1, 2, 1, 0, 0, 0, 0],
    [4, 35, 8, 1, 2, 0, 0, 0, 0, 1],
    [1, 50, 6, 2, 1, 0, 1, 0, 1, 0],
    [2, 50, 6, 2, 1, 0, 1, 0, 1, 0],
    [10, 12, 4, 1, 2, 0, 1, 0, 0, 0],
    [10, 15, 6, 1, 4, 0, 1, 0, 0, 0]]


def introduce_synthetic_cases(crb_system, cases):
    """
    Introdueix una llista de casos sintètics al sistema CRB.
    :param crb_system: Sistema CRB.
    :param cases: Llista de casos sintètics.
    """
    for case in cases:
        print(f"Introduint el cas: {case}")
        crb_system.crb(case)  # Introduïm el cas al sistema

d_weights = np.array([1,1,1,1,1,1,1,1,1])
layer_thresholds = [4, 30, 4, 2, 1, 1, 1, 1, 1]

nodes = [Node() for _ in range(2**len(d_weights))]

for i in reversed(range(len(d_weights))):
    for _ in range(int(2**(i-1))):
        node = Node(layer_thresholds[i], nodes[:2])
        nodes.append(node)
        del nodes[:2]

root = nodes[0]

# Inicialitzem el sistema CRB amb l'arrel de l'arbre
crb_system = CBR(root)

# Introduïm els casos al sistema
introduce_synthetic_cases(crb_system, synthetic_cases)

# Provem amb un cas nou
new_case = np.array([6, 28, 2, 0, 1, 0, 0, 1, 1])
crb_result = crb_system.crb(new_case)
crb_result
