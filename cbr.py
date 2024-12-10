class CRBSystem:
    def __init__(self, root):
        self.root = root  # Arrel de l'arbre jeràrquic de nodes

    def retrieve(self, case):
        """
        Busca el cas més proper en el sistema de casos.
        """
        print("=== Retrieve ===")
        closest_case = self.root.feed(case)
        if closest_case is None:
            print("  -> No s'ha trobat cap cas similar (nou cas).")
        else:
            print(f"  -> Cas recuperat: {closest_case}")
        return closest_case

    def reuse(self, closest_case, case):
        """
        Adapta la informació del cas recuperat per crear una solució inicial pel nou cas.
        """
        print("\n=== Reuse ===")
        if closest_case is None:
            print("  -> No hi ha cap cas per reutilitzar, es crea una nova solució des de zero.")
            solution = {"adapted_solution": "default_solution"}  # Solució base per nous casos
        else:
            print(f"  -> Reutilitzant el cas recuperat {closest_case} per adaptar-lo al nou cas.")
            solution = {"adapted_solution": f"adapted_from_{closest_case}"}
        print(f"  -> Solució inicial: {solution}")
        return solution

    def revise(self, solution):
        """
        Revisa la solució proposada. Aquí se simula una revisió manual o automàtica.
        """
        print("\n=== Revise ===")
        # Simulem una revisió manual o automàtica
        revised_solution = solution.copy()
        revised_solution["revised"] = True  # Marquem la solució com revisada
        print(f"  -> Solució revisada: {revised_solution}")
        return revised_solution

    def retain(self, case, solution):
        """
        Emmagatzema el nou cas i la seva solució al sistema de casos.
        """
        print("\n=== Retain ===")
        print(f"  -> Emmagatzemant el cas {case} amb la solució {solution}.")
        self.root.feed(case)  # El nou cas es guarda al sistema de nodes

    def crb(self, case):
        """
        Implementa tot el cicle CRB per un cas donat.
        """
        # 1. Retrieve
        closest_case = self.retrieve(case)

        # 2. Reuse
        solution = self.reuse(closest_case, case)

        # 3. Revise
        revised_solution = self.revise(solution)

        # 4. Retain
        self.retain(case, revised_solution)

        print("\n=== CRB Finalitzat ===")
        return revised_solution


# Inicialitzem el sistema CRB amb l'arrel de l'arbre
crb_system = CRBSystem(root)

# Provem amb un cas nou
new_case = np.array([6, 28, 2, 0, 1, 0, 0, 1, 1])
crb_result = crb_system.crb(new_case)
crb_result