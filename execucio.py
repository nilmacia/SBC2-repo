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
casos_entrenament = generar_casos(1000)
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

avg_test = sum(valoracions_test) / len(valoracions_test)
print(f"\nMitjana de Valoracions dels jocs de prova: {avg_test:.4f}")

valoracions_entrenament = np.array(valoracions_entrenament).reshape(-1, 10).mean(-1)

plt.plot(valoracions_entrenament)
plt.title("Valoracions entrenament")
plt.savefig('dades/corva_entrenament')
plt.show()


def crear_cas():
    # Preguntes a l'usuari
    nombre = int(input("Quantes persones feu la visita? "))  # Assegura que sigui un enter
    edat = int(input("Quina és l'edat més representativa del grup? "))
    t_dia = float(input("Quant temps tens per fer la visita (per dia i en minuts)? "))
    dies = int(input("Quants dies durarà la teva visita? "))

    # Preguntes per artistes i periodes
    artistes_input = input("Quins artistes vols incloure? (Separats per comes) ")
    periodes_input = input("Quins períodes vols incloure? (Separats per comes) ")

    # Convertir les respostes a llistes
    artistes = artistes_input.split(",") if artistes_input else []
    periodes = periodes_input.split(",") if periodes_input else []

    # Comprovar si els artistes i periodes són correctes dins del domini
    artistes_valids = ["Vincent van Gogh", "Claude Monet", "Leonardo da Vinci", "Anthony van Dyck", "Rembrandt (Rembrandt van Rijn)", "Frans Hals"]
    periodes_valids = ["Renaissance", "Baroque", "Realism", "Impressionism"]

    artistes = [art.strip() for art in artistes if art.strip() in artistes_valids]
    periodes = [per.strip() for per in periodes if per.strip() in periodes_valids]

    # Crear la instància de la classe Cas
    cas = Cas(nombre, edat, t_dia, dies, artistes, periodes)

    # Debug per verificar les dades
    print("Dades del cas creat:", cas.__dict__)

    return cas

cas1 = crear_cas()

# Executar el retrieve per obtenir els casos més semblants
top_casos = cbr.retrieve(cas1)

# Reutilitzar els casos i obtenir les obres seleccionades
obres_visitar = cbr.reuse(top_casos, cas1)

# Mostrar les obres seleccionades per visitar
print("\nObres seleccionades per visitar en el cas:")
for obra in cas1.noms_obres:
    print(f"- {obra}")

# Preguntar a l'usuari per introduir una valoració numèrica
valoracio = float(input("\nIntrodueix una valoració per aquesta proposta (ex: 1-10): "))

# Assignar la valoració al cas
cas1.valoracio = valoracio

# Fer el retain per afegir el cas amb la seva valoració i obres al sistema
cbr.retain(cas1)

print("\nEl cas s'ha guardat correctament al sistema amb la nova valoració i obres seleccionades.")