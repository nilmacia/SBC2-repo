from __future__ import annotations

# PODEM AFEGIR I TREURE CLASSES I FUNCIONS, AIXÒ ÉS ORIENTATIU DE LES OPERACIONS
# I OBJECTES QUE NECESSITEM
# Per exemple la visita potser no necessita una classe i pot ser una llista i ja

with open('keywords.dat') as f:
    keywords = [w.strip() for w in f.readlines()]

with open('distance_weights.dat') as f:
    distance_weights = [float(w) for w in f.readlines()]

with open('max_base_size.dat') as f:
    # Això si mantenim la base per mida màxima enlloc de per nombre d'iteracions
    max_base_size = float(f.read())


class CaseBase: # Una matriu (n_casos, dim_cas)
    """
    Potser podria ser classe node enlloc de base i que cada node tingui fills i
    guardem el primer node, però molaria també tenir tots els casos guardats en
    alguna mena de matriu si volem calcular la distància espacialment per poder
    fer la resta i ponderació per un vector de manera eficient
    """
    def save(self, path: str) -> None:
        pass

    @staticmethod
    def load(path: str) -> CaseBase:
        pass


class Museum:
    """
    Representar el museu com un graf, com conjunts ordenats d'obres...
    """
    def save(self, path: str) -> None:
        pass

    @staticmethod
    def load(path: str) -> Museum:
        pass

class Case:
    """
    Hem d'associar d'alguna manera les característiques del cas amb la visita
    recomanada i la valoració
    """
    pass

class Visit:
    """
    Representació de la visita
    """
    pass


def retain(case: Case, base: CaseBase) -> None:
    """
    Decidir si guardem el cas i com ho fem
    Es crida per cada cas avaluat (online)
    """
    if len(base) > max_base_size:
        maintain(base)

def maintain(base: CaseBase) -> None:
    """
    Agrupem o oblidem casos
    Cada cert nombre d'iteracions o quan la base sigui molt gran (offline)
    """
    pass

def get_new_case() -> Case:
    """
    Obtenir les característiques d'entrada pel nou cas
    Aquest "Case" encara no tindria una visita ni una valoració associades
    """
    pass

def get_closest(case: Case, base: CaseBase, n: int = 1) -> list[Case]:
    """
    Trobar el cas o casos més semblants de la base
    """
    pass

def adapt(closest: list[Case], museum: Museum) -> Visit:
    """
    A partir de les característiques dels casos més semblants, les seves
    valoracions i recomanacions associades i el museu actual, adaptar la nova
    recomanació
    """
    pass

def suggest(visit: Visit) -> int:
    """
    Mostrar/proposar la visita calculada i guardar-ne la valoració
    """
    pass


if __name__ == "__main__":
    base_path = 'case_base.dat'
    museum_path = 'museumX.dat'

    base = CaseBase.load(base_path)
    museum = Museum.load(museum_path)

    from sys import argv

    for _ in range(int(argv[1])):
        case = get_new_case()
        closest = get_closest(case, base)
        case.visit = adapt(closest, museum)
        case.ranking = suggest(case.visit)
        retain(case)
        if base.size == max_base_size:
            maintain(base)
    
    base.save(base_path)
    museum.save(museum_path)