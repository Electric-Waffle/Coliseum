"""Questions posées au plan d'un étage."""

def RegardeSiEtageCompletementObserve(blueprint):
    for numero_de_salle in blueprint:
        salle_a_checker = blueprint[numero_de_salle]
        if salle_a_checker["type"] in ["ENTREE"]:
            continue
        elif salle_a_checker["marqué sur la carte"] == False:
            return False
    return True
