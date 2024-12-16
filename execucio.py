from generador import generar_casos, recomanar_random, valorar
from arbre import Arbre
from cbr import CBR

casos_inicials = generar_casos(1000)
recomanar_random(casos_inicials)
for cas in casos_inicials: valorar(cas)

arbre = Arbre()
for cas in casos_inicials: arbre.feed(cas)

cbr = CBR(arbre)