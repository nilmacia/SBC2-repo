from generador import *
from cas import *
from cbr import *
from arbre import *

casos_inicials = generar_casos(1000)
recomanar_random(casos_inicials)
for cas in casos_inicials: valorar(cas)

arbre = Arbre()
for cas in casos_inicials: arbre.feed(cas)

cbr = CBR()