def crb(new_case, root_node, d_weights, layer_thresholds, books_db, user_cases_db):
    """
    Implementació del sistema CRB amb les quatre fases:
    Retrieve, Reuse, Revise, Retain.

    :param new_case: Diccionari o llista amb les característiques del nou cas.
    :param root_node: L'arrel de l'arbre de decisions (Node).
    :param d_weights: Pesos per a les característiques dels casos (numpy array).
    :param layer_thresholds: Llindars utilitzats per a la divisió en nodes interns.
    :param books_db: Base de dades dels llibres disponibles.
    :param user_cases_db: Base de dades dels casos ja processats (usuaris i llibres).
    :return: Casos recuperats, solucions reusades, llibre adaptat, nou cas.
    """
    # 1. Retrieve: Cerca de casos similars
    def retrieve(new_case, root_node, d_weights):
        """
        Cerca els casos més similars al nou cas a partir de l'arbre.
        """
        retrieved_case = root_node.feed(new_case)
        return retrieved_case

    # 2. Reuse: Reutilització de la solució del cas més similar
    def reuse(retrieved_case):
        """
        Reutilitza la solució del cas recuperat.
        """
        # Assumim que el cas recuperat inclou informació del llibre recomanat
        solution = retrieved_case[-1]  # Última columna: Solució (id del llibre)
        return solution

    # 3. Revise: Revisa la solució recomanada per assegurar que compleix les restriccions
    def revise(solution, new_case, books_db):
        """
        Revisa i, si cal, adapta la solució perquè compleixi les restriccions del cas nou.
        """
        # Extraiem informació del cas i comprovem les restriccions
        book_row = books_db[books_db['id_llibre'] == solution]

        oblig = [False, False, False, False]

        # 1. Gènere
        genres_case = {genre for genre in new_case['genres']}
        intersection = book_row.iloc[0]['pertany_a'].intersection(genres_case)
        if len(intersection) > 0:
            oblig[0] = True

        # 2. Edat mínima
        if book_row.iloc[0]['edat_minima'] <= new_case['user_age']:
            oblig[1] = True

        # 3. Idioma
        if len(book_row.iloc[0]['traduccions'].intersection(new_case['languages'])) > 0:
            oblig[2] = True

        # 4. Llibre no recomanat abans
        if len(user_cases_db[(user_cases_db['id_usuari'] == new_case['user_id']) & 
                             (user_cases_db['id_llibre'] == solution)]) == 0:
            oblig[3] = True

        # Si no es compleixen totes les restriccions, buscar un altre llibre
        if False in oblig:
            # Filtratge dels llibres que compleixen les restriccions obligatòries
            filtered_books = books_db.copy()
            filtered_books = filtered_books[filtered_books['edat_minima'] <= new_case['user_age']]
            filtered_books = filtered_books[filtered_books['id_llibre'] != solution]
            filtered_books = filtered_books[filtered_books['pertany_a'].apply(lambda x: len(x.intersection(genres_case)) > 0)]
            filtered_books = filtered_books[filtered_books['traduccions'].apply(lambda x: len(x.intersection(new_case['languages'])) > 0)]

            # Selecció del llibre més semblant segons la mètrica de similitud
            books_sim = []
            for _, fila in filtered_books.iterrows():
                vector_llibre = np.array([1 if genre in fila['pertany_a'] else 0 for genre in genres_case])
                vector_llibre += [fila['any_publicacio'], fila['best_seller'], fila['saga'],
                                  fila['adaptacio_a_pelicula'], fila['edat_minima'], fila['num_pagines']]
                books_sim.append((fila['id_llibre'], np.dot(d_weights, vector_llibre)))
            
            books_sim_sorted = sorted(books_sim, key=lambda x: x[1], reverse=True)
            new_solution = books_sim_sorted[0][0]  # Retornem l'id del llibre més semblant
            return new_solution
        else:
            return solution

    # 4. Retain: Afegir el nou cas a la base de dades
    def retain(new_case, adapted_solution, user_cases_db, books_db):
        """
        Guarda el nou cas a la base de dades.
        """
        new_case['id_llibre'] = adapted_solution
        user_cases_db = user_cases_db.append(new_case, ignore_index=True)
        return user_cases_db

    # Execució de les quatre R
    retrieved = retrieve(new_case, root_node, d_weights)
    reused = reuse(retrieved)
    revised = revise(reused, new_case, books_db)
    retained_db = retain(new_case, revised, user_cases_db, books_db)

    return retrieved, reused, revised, retained_db