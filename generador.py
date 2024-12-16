import numpy as np
import json
import pandas as pd
from cas import Cas, noms

rng = np.random.default_rng()

with open('dades/domini.json') as f:
    domini = json.load(f)


df = pd.read_csv('dades/obres.csv')

t_trasllat = 2
n_sales = 10


def valorar(cas):
    def bell(x, a, b):
        return np.exp(-(x - b)**2/(2*((b - a)*0.35)**2))
    
    def rescale(x, a, b, c, d):
        return (x-a) * (d-c) / (b-a) +c

    def coef(x, a, b, c):
        x = bell(x, a, b)
        return rescale(x, 0, 1, 1-c, 1+c)

    noms_artistes = np.array(list(domini['artistes']))[cas.artistes]
    noms_periodes = np.array(list(domini['periodes']))[cas.periodes]

    # temps
    temps_obres = df.Temps * cas.obres
    temps_obres[df.Artista.isin(noms_artistes) | df.Periode.isin(noms_periodes)] *= 1.1
    temps_obres = temps_obres.sum()
    temps_obres *= coef(cas.edat, 5, 95, 0.2)

    temps_trasllats = n_sales * t_trasllat
    temps_trasllats *= coef(np.abs(50 - cas.edat), 0, 45, 0.2)

    temps_visita = temps_obres + temps_trasllats
    temps_visita *= coef(cas.nombre, 1, 15, 0.2)
    temps_visita *= rng.normal(1, 0.1, temps_visita.shape).clip(0.7, 1.3)
    
    diff = temps_visita/cas.temps
    diff = np.minimum(diff, 1/diff)
    valoracio_temps = bell(diff, 0, 1)

    # preferencies
    obres = df[cas.obres]
    preferencies = set(domini['periodes'][p] for p in noms_periodes)
    periode_artistes = set(domini['artistes'][a] for a in noms_artistes)
    preferencies.union(domini['periodes'][p] for p in periode_artistes)
    if preferencies:
        preferencies = np.array(list(preferencies))
        recomanacio = np.array([domini['periodes'][p] for p in obres.Period])
        dist = np.abs(recomanacio[:, None] - preferencies).min(-1)
        dist[obres.Artist.isin(noms_artistes)] -= 1
        dist = dist.mean()
    else:
        dist = 0

    valoracio_preferencies = bell(dist, 7, -1)

    cas.valoracio = valoracio_temps * valoracio_preferencies


def recomanar_random(casos):
    t = np.array([c.temps for c in casos])
    t -= t_trasllat * n_sales
    n_obres_aprox = t / df.Temps.mean()
    p = n_obres_aprox / df.shape[0]
    recomanacio = rng.binomial(1, p, (len(casos), df.shape[0])).astype(bool)

    for c, r in zip(casos, recomanacio):
        c.obres = r


def generar_casos(n):
    # MIDA
    mida = rng.choice(('individu', 'parella', 'grup', 'gran'), n)

    nombre = np.empty(n, int)
    nombre[mida == 'individu'] = 1
    nombre[mida == 'parella'] = 2
    nombre[mida == 'grup'] = 3 + rng.binomial(4, 0.25, np.sum(mida == 'grup'))
    nombre[mida == 'gran'] = rng.uniform(8, 16, np.sum(mida == 'gran')).astype(int)

    # EDAT
    generacio = rng.choice(('infant', 'adolescent', 'jove', 'adult', 'vell'), n)

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

    # T_DIA
    hores = np.log(edat)
    hores = (hores - np.log(5)) * (7 - 1) / (np.log(95) - np.log(5)) + 1
    hores += rng.binomial(3, 0.15, n)
    t_dia = (hores * 60).round().astype(int)

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

    # ARTISTES
    artistes = rng.binomial(1, 1/len(noms['artistes']), (n, len(noms['artistes'])))

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
    artistes[:, np.isin(noms['artistes'], artistes_pop)] = \
        rng.binomial(1, 1/len(artistes_pop), (n, len(artistes_pop)))

    artistes = artistes.astype(bool)

    # PERIODES
    periodes = rng.binomial(1, 1/len(noms['periodes']), (n, len(noms['periodes'])))

    periodes_pop = (
        "Renaissance",
        "Impressionism"
    )
    periodes[:, np.isin(noms['periodes'], periodes_pop)] = \
        rng.binomial(1, 1/len(periodes_pop), (n, len(periodes_pop)))

    periodes = periodes.astype(bool)

    return [Cas(*feats) for feats in zip(
        nombre,
        edat,
        t_dia,
        dies,
        artistes,
        periodes
    )]