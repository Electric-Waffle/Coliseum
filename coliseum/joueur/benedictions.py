"""Bénédictions et malédictions en cours, lues dans la sauvegarde permanente."""

from coliseum import services


def RecupereMaledictionEnCours(type_of_demand="base"):
    liste_malediction = [
        "Apyre",
        "Infrigérable",
        "Isolant",
        "Arénacé",
        "Anoxique",
        "Exsangue",
        "Impotent",
        "Chronophage",
        "Sparifique",
        "Ascétique",
        "Pur",
        "Ordinaire",
    ]
    if type_of_demand != "base": 
        return liste_malediction
    else:
        liste_tags =  services.Sove.ModifieTagsDansSove("Donne",None)
        for tag in liste_tags:
            if tag in liste_malediction:
                return tag
        return "Aucun"


def RegardeSiBenedictionDisponible(benediction):
    if  services.Sove.ModifieTagsDansSove("Checke", "Debloque Incandescent") and benediction == "Incandescent":
        return True
    elif  services.Sove.ModifieTagsDansSove("Checke", "Debloque Glaciaire") and benediction == "Glaciaire":
        return True
    elif  services.Sove.ModifieTagsDansSove("Checke", "Debloque Conducteur") and benediction == "Conducteur":
        return True
    elif  services.Sove.ModifieTagsDansSove("Checke", "Debloque Rocailleux") and benediction == "Rocailleux":
        return True
    elif  services.Sove.ModifieTagsDansSove("Checke", "Debloque Musclé") and benediction == "Musclé":
        return True
    elif  services.Sove.ModifieTagsDansSove("Checke", "Debloque Sain") and benediction == "Sain":
        return True
    elif  services.Sove.ModifieTagsDansSove("Checke", "Debloque Omnipotent") and benediction == "Omnipotent":
        return True
    elif  services.Sove.ModifieTagsDansSove("Checke", "Debloque Accumulateur de Tachyon") and benediction == "Accumulateur de Tachyon":
        return True
    elif  services.Sove.ModifieTagsDansSove("Checke", "Debloque Polyvalent") and benediction == "Polyvalent":
        return True
    elif  services.Sove.ModifieTagsDansSove("Checke", "Debloque Materiel") and benediction == "Materiel":
        return True
    elif  services.Sove.ModifieTagsDansSove("Checke", "Debloque Augmenté") and benediction == "Augmenté":
        return True
    elif  services.Sove.ModifieTagsDansSove("Checke", "Debloque Extraordinaire") and benediction == "Extraordinaire":
        return True
    else:
        return False


def RecupereBenedictionEnCours(type_of_demand="base"):
    liste_benediction = [
        "Incandescent",
        "Glaciaire",
        "Conducteur",
        "Rocailleux",
        "Musclé",
        "Sain",
        "Omnipotent",
        "Accumulateur de Tachyon",
        "Polyvalent",
        "Materiel",
        "Augmenté",
        "Extraordinaire",
    ]
    if type_of_demand != "base": 
        return liste_benediction
    else:
        liste_tags = services.Sove.ModifieTagsDansSove("Donne",None)
        for tag in liste_tags:
            if tag in liste_benediction:
                return tag
        return "Aucun"
