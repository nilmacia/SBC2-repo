import matplotlib.pyplot as plt
import numpy as np

from generador import generar_casos, recomanar_random, valorar
from arbre import Arbre
from cbr import CBR
from cas import Cas

print('=== Inicialització ===')

print(' - Generació')
casos_inicials = generar_casos(1000)

print(' - Recomanació')
recomanar_random(casos_inicials)

print(' - Valoració')
for cas in casos_inicials: valorar(cas)

print(' - Retenció')
arbre = Arbre()
for cas in casos_inicials: arbre.feed(cas)

cbr = CBR(arbre)

print('\n=== Entrenament ===')
casos_entrenament = generar_casos(10000)
valoracions_entrenament = []
for i, cas in enumerate(casos_entrenament, 1):
    cbr(cas)
    if i % 100 == 0:
        arbre.mantenir()
    valoracions_entrenament.append(cas.valoracio)
    print('\r', i, '/', len(casos_entrenament), end='')
print()


# Pas 3: Definir jocs de prova per validar diferents escenaris
print("\n=== Proves del Sistema ===")
jocs_test = [
    [4, 20, 300, 1, ["Vincent van Gogh"], []],  # Cas de prova: Artista conegut, sense període
    [2, 40, 300, 2, ["Gustave Courbet"], ["Realism"]],  # Artista i període coneguts
    [6, 25, 120, 1, ["Leonardo da Vinci"], []],  # Artista conegut amb pressupost de temps petit
    [5, 30, 400, 3, [], ["Renaissance"]],  # Període conegut, sense artista
    [1, 50, 120, 2, [], []],  # Cas completament aleatori (sense artista ni període)
    [3, 18, 180, 1, ["Claude Monet"], ["Impressionism"]],  # Cas equilibrat
    [10, 22, 180, 2, ["Anthony van Dyck"], ["Expressionism"]],  # Artista i període modern
    [3, 28, 300, 3, ["Rembrandt (Rembrandt van Rijn)"], []],  # Artista conegut amb temps ample
    [2, 35, 500, 3, [], ["Baroque"]],  # Període conegut amb temps més llarg
    [1, 15, 120, 1, ["Frans Hals"], ["Baroque"]],  # Artista barroc amb temps petit
]

valoracions_test = []
verbose = False
for i, joc in enumerate(jocs_test, 1):
    if verbose:
        print(f"\n--- Joc de Prova {i}: ---")
    cas = Cas(*joc)  # Crear un cas de prova
    cbr(cas)
    valoracions_test.append(cas.valoracio)  # Guardar l'avaluació
    if verbose:
        print("Obres Recomanades:", end='')
        print('', *cas.noms_obres, sep='\n - ')

# Pas 4: Resumir resultats
print("\n=== Resum dels Resultats ===")
print("Avaluacions dels Jocs de Prova:")
for i, valor in enumerate(valoracions_test, 1):
    print(f"Valoració {i} = {valor:.4f}")

avg_train_ini = sum(valoracions_entrenament[:100])/100
avg_test = sum(valoracions_test) / len(valoracions_test)
print(f"\nMitjana de Valoracions dels jocs de prova: {avg_test:.4f}")
print(f"Baseline: {avg_train_ini:.4f}\n")

valoracions_entrenament = np.array(valoracions_entrenament).reshape(-1, 100).mean(-1)

plt.plot(valoracions_entrenament)
plt.title("Valoracions entrenament")
plt.savefig('dades/corva_entrenament')
plt.show()


