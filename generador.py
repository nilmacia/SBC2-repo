import numpy as np
import json
import pandas as pd
from cas import Cas

rng = np.random.default_rng()

mides = ('individu', 'parella', 'grup', 'gran')
generacions = ('infant', 'adolescent', 'jove', 'adult', 'vell')

tipus_visitant = (
    0, # formiga
    1, # saltamartí
    2, # papallona
    3  # peix
)

with open('dades/domini.json') as f:
    domini = json.load(f)

artistes_pop = (
    "Rembrandt (Rembrandt van Rijn)",
    "Peter Paul Rubens",
    "Jean Honore Fragonard",
    "Goya (Francisco de Goya y Lucientes)",
    "Eugene Delacroix",
    "Jean-Francois Millet",
    "Claude Monet",
    "Vincent van Gogh",
    "Edgar Degas"
)

periodes_pop = (
    "Renaissance",
    "Impressionism"
)

df = pd.read_csv('dades/obres.csv')

t_obra = 5
t_trasllat = 2
n_sales = 10


def valorar(casos):    
    # temps
    temps_previst = np.array([c.temps for c in casos])

    coef = lambda n: np.linspace(np.sqrt(.5), np.sqrt(2), n)
    temps_visita = np.array([c.obres for c in casos]) * t_obra
    temps_visita *= coef(10)[df.Relevance]
    temps_visita *= coef(10)[df.Complexity]
    temps_visita *= coef(4)[[3 - c.tipus for c in casos]]

    temps_visita = temps_visita.sum(-1)
    temps_visita *= rng.normal(1, 0.2, temps_visita.shape).clip(0.4, 1.6)
    
    valoracio_temps = 

    # preferencies
    # estil

    valoracio = ...

    for c, v in zip(casos, valoracio):
        c.valoracio = v


def recomanar_random(casos):
    t = np.array([c.temps for c in casos])
    t -= t_trasllat * n_sales
    n_obres_aprox = t / t_obra
    p = n_obres_aprox / df.shape[0]
    recomanacio = rng.binomial(1, p, (len(casos), df.shape[0]))

    for c, r in zip(casos, recomanacio):
        c.obres = r


def generar_casos(n):
    # MIDA
    mida = rng.choice(mides, n)

    nombre = np.empty(n, int)
    nombre[mida == 'individu'] = 1
    nombre[mida == 'parella'] = 2
    nombre[mida == 'grup'] = 3 + rng.binomial(4, 0.25, np.sum(mida == 'grup'))
    nombre[mida == 'gran'] = rng.uniform(8, 16, np.sum(mida == 'gran')).astype(int)

    # EDAT
    generacio = rng.choice(generacions, n)

    mean = np.empty(n)
    std = np.empty(n)

    mean[generacio == 'infant'] = 8.
    std[generacio == 'infant'] = 1.

    mean[generacio == 'adolescent'] = 15.
    std[generacio == 'adolescent'] = 1.5

    mean[generacio == 'jove'] = 28.
    std[generacio == 'jove'] = 3.

    mean[generacio == 'adult'] = 50.
    std[generacio == 'adult'] = 5.

    mean[generacio == 'vell'] = 78.
    std[generacio == 'vell'] = 4.

    edat = rng.normal(mean, std).clip(5, 95).astype(int)

    # HORES
    hores = np.log(edat)
    hores = hores - np.log(5) + 1
    hores *= 7/np.log(95)
    hores += rng.binomial(3, 0.15, n)
    hores = hores.round().astype(int)

    # DIES
    m = np.empty(n, int)
    p = np.empty(n)

    m[generacio == 'infant'] = 0
    p[generacio == 'infant'] = 0.

    m[generacio == 'adolescent'] = 2
    p[generacio == 'adolescent'] = 0.05

    m[generacio == 'jove'] = 2
    p[generacio == 'jove'] = 0.1

    m[generacio == 'adult'] = 4
    p[generacio == 'adult'] = 0.1

    m[generacio == 'vell'] = 4
    p[generacio == 'vell'] = 0.2

    dies = 1 + rng.binomial(m, p)

    # TIPUS
    tipus = np.empty(n, int)

    i = generacio == 'infant'
    tipus[i] = rng.choice(tipus_visitant, tipus[i].shape, p=(0.1, 0.2, 0.4, 0.3))

    i = generacio == 'adolescent'
    tipus[i] = rng.choice(tipus_visitant, tipus[i].shape, p=(0.1, 0.2, 0.3, 0.4))

    i = generacio == 'jove'
    tipus[i] = rng.choice(tipus_visitant, tipus[i].shape, p=(0.2, 0.4, 0.3, 0.1))

    i = generacio == 'adult'
    tipus[i] = rng.choice(tipus_visitant, tipus[i].shape, p=(0.3, 0.4, 0.2, 0.1))

    i = generacio == 'vell'
    tipus[i] = rng.choice(tipus_visitant, tipus[i].shape, p=(0.4, 0.3, 0.2, 0.1))

    # ARTISTES
    noms = list(domini['artistes'])
    artistes = np.empty((n, len(noms)), int)

    i = np.isin(noms, artistes_pop)
    artistes[:, i] = rng.binomial(1, 1/len(artistes_pop), (n, i.sum()))

    i = ~np.isin(noms, artistes_pop)
    artistes[:, i] = rng.binomial(1, 1/len(noms), (n, i.sum()))

    # PERIODES
    noms = list(domini['periodes'])
    periodes = np.empty((n, len(noms)), int)

    i = np.isin(noms, periodes_pop)
    periodes[:, i] = rng.binomial(1, 1/len(periodes_pop), (n, i.sum()))

    i = ~np.isin(noms, periodes_pop)
    periodes[:, i] = rng.binomial(1, 1/len(noms), (n, i.sum()))


    return [Cas(*feats) for feats in zip(
        nombre,
        edat,
        hores,
        dies,
        tipus,
        artistes,
        periodes
    )]


# def generar_museu(n, sales):
#     if isinstance(n, int):
#         museu = df.sample(n).reset_index()
#     else:
#         museu = df.sample(frac=n).reset_index()
#     museu['Sala'] = rng.permutation(np.arange(museu.shape[0]) % sales + 1)
#     return museu
# 
# def guardar_museu(museu, nom):
#     museu.to_csv('dades/' + nom, index=False)
# 
# def carregar_museu(nom):
#     return pd.read_csv('dades/' + nom)