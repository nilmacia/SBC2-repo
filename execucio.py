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

jocs_test = [
    [4, 20, 300, 1, ["Vincent van Gogh"], []],]

valoracions = []
for i, joc in enumerate(jocs_test, 1):
    cas = Cas(*joc)
    top_casos = cbr.retrieve(cas)
    cbr.reuse(cas)
    valorar(cas)
    valoracions.append(cas.valoracio)
    print('Recomanació', i, cas.noms_obres)

print('Resultats:', valoracions)
print('Avg:', sum(valoracions)/len(valoracions))

