import json

class Cas:
    def __init__(self, nombre: int, edat: int, hores: int, dies: int,
                 autors: list[str] = [], estils: list[str] = []):
        """
        - nombre: int[1,  15]
        - edat (mitjana): int[0, 100]
        - hores: int[1,  12]
        - dies: int[1,   5]
        - autors: list[str]
        - estils: list[str]
        
        Els atributs de "autors", "estils" i "obres" seran llistes d'strings
        però es transformaran a vectors binaris amb el mètode "array".
        Per determinar la llargada dels vectors s'utilitzarà el fitxer
        "data/domini.json".
        Si s'introdueixen valors no vistos abans s'inclouran al
        fitxer però aleshores hem de tenir en compte que els vectors retornats
        ja no seran compatibles amb els generats anteriorment.
        Procurem utilitzar els valors ja inclosos mentre sigui posible.
        """

        self.nombre = nombre
        self.edat = edat
        self.hores = hores
        self.dies = dies
        self.autors = autors
        self.estils = estils
        self.obres = None

        with open("data/domini.json") as f:
            domini = json.load(f)
        
        autors = set(autors)
        autorsD = set(domini["autors"])
        if not autors <= autorsD:
            domini["autors"].extend([a for a in autors if a not in autorsD])

        estils = set(estils)
        estilsD = set(domini["estils"])
        if not estils <= estilsD:
            domini["estils"].extend([e for e in estils if e not in estilsD])