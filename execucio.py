from generador import generar_casos, recomanar_random, valorar
from arbre import Arbre
from cbr import CBR
from cas import Cas

casos_inicials = generar_casos(1000)
recomanar_random(casos_inicials)
for cas in casos_inicials: valorar(cas)

arbre = Arbre()
for cas in casos_inicials: arbre.feed(cas)

cbr = CBR(arbre)

casos_entrenament = generar_casos(1000)
for cas in casos_entrenament:
    top_casos = cbr.retrieve(cas)
    cbr.reuse(top_casos, cas)
    cbr.retain(cas)

# Pas 3: Definir jocs de prova per validar diferents escenaris
print("\n=== Pas 3: Proves del Sistema ===")
jocs_test = [
    [4, 20, 300, 1, ["Vincent van Gogh"], []],  # Cas de prova: Artista conegut, sense període
    [2, 40, 600, 2, ["Pablo Picasso"], ["Cubisme"]],  # Artista i període coneguts
    [8, 25, 120, 1, ["Leonardo da Vinci"], []],  # Artista conegut amb pressupost de temps petit
    [5, 30, 1800, 3, [], ["Renaixament"]],  # Període conegut, sense artista
    [10, 50, 240, 2, [], []],  # Cas completament aleatori (sense artista ni període)
    [3, 18, 180, 1, ["Claude Monet"], ["Impressionisme"]],  # Cas equilibrat
    [6, 22, 360, 2, ["Frida Kahlo"], ["Modernisme"]],  # Artista i període modern
    [7, 28, 900, 3, ["Edvard Munch"], []],  # Artista conegut amb temps ample
    [9, 35, 1500, 3, [], ["Barroc"]],  # Període conegut amb temps més llarg
    [1, 15, 120, 1, ["Salvador Dalí"], ["Surrealisme"]],  # Artista surrealisme amb temps petit
]

valoracions = []
for i, joc in enumerate(jocs_test, 1):
    print(f"\n--- Joc de Prova {i}: ---")
    cas = Cas(*joc)  # Crear un cas de prova
    top_casos = cbr.retrieve(cas)  # Recuperar casos similars
    solution = cbr.reuse(top_casos, cas)  # Generar una recomanació
    valorar(cas)  # Avaluar la solució
    valoracions.append(cas.valoracio)  # Guardar l'avaluació
    print(f"Obres Recomanades: {cas.noms_obres}")

# Pas 4: Resumir resultats
print("\n=== Pas 4: Resum dels Resultats ===")
print("Avaluacions dels Jocs de Prova:")
for i, valor in enumerate(valoracions, 1):
    print(f"Joc de Prova {i}: Valoració = {valor:.4f}")

avg_valoracio = sum(valoracions) / len(valoracions)
print(f"\nMitjana de Valoracions: {avg_valoracio:.4f}")


