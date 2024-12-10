from cbr import CRB
from case_base import Node

import numpy as np

def generate_synthetic_cases(num_cases):
    """
    Genera una base de casos sintètics seguint el format especificat.
    :param num_cases: Nombre de casos sintètics a generar.
    :return: Llista de casos sintètics.
    """
    synthetic_cases = []
    for i in range(num_cases):
        nombre = i + 1  # Identificador únic
        edat = np.random.randint(5, 91)  # Edat entre 5 i 90 anys
        hores = np.random.randint(1, 9)  # Hores entre 1 i 8
        dies = np.random.randint(1, 8)  # Dies entre 1 i 7
        preferències = np.random.randint(0, 2, size=5)  # 5 valors booleans (0 o 1)
        case = np.array([nombre, edat, hores, dies, *preferències])
        synthetic_cases.append(case)
    return synthetic_cases


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
crb_system = CRB(root)

# Generem 10 casos sintètics
synthetic_cases = generate_synthetic_cases(50)

# Introduïm els casos al sistema
introduce_synthetic_cases(crb_system, synthetic_cases)

# Provem amb un cas nou
new_case = np.array([6, 28, 2, 0, 1, 0, 0, 1, 1])
crb_result = crb_system.crb(new_case)
crb_result