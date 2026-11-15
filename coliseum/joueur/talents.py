"""Dépense des redcoins et fusion des talents."""

from coliseum import services
from coliseum.console import ClearConsole
from coliseum.donnees.personnages import ANNUAIREDECHOIXPOURREDCOIN


def DoRedcoin():
    while True:
        while True:
            try:
                print(
                    "     -={ RedCoin }=-   /925435351305251SERVICEDERECUPERATIONDEDONNEES7117764"
                )
                print(
                    "                      /7420952721321625369856321569852156AOUVRIRVIALEMENU556"
                )
                print(
                    "1 - Retour           /981265161565513513513165050742315698522685256PRINCIPAL"
                )
                print(
                    " ____/1233232311579764382419683214618568246856824565546532854663243615463745"
                )
                print(
                    " \95363541653155641654135641459565415631612952955265653959562413153556163153"
                )
                print(
                    "Code -       Nom       -    Prix    /128243165325615323235106506863236550325"
                )
                print(
                    "1257 - Affinité de Feu - 1 Redcoin /52565265163512ERRORERRORERRORERORERROR98"
                )
                print(
                    "5675 - Affinité de Foudre - 1 Red/487965651268416535498165319651965ERRORROOR"
                )
                print(
                    "9731 - Affinité de Sang - 1 Redc/789ERREUR:DONNESMANQUANTES96515866519651988"
                )
                print(
                    "7563 - Af/7845123553213506516896652565167841961561653163165ERRORERRORERROR58"
                )
                print(
                    "8240 - A/7845621365265216532561517VEUILLEZCONTACTERLESERVICEINFORMATIQUE9465"
                )
                print(
                    "6______/789OUUTILISEZNOTRESERVICE65235216513351DERECUPERATIONDEDONNEES313135"
                )
                print(
                    "/5698994524527/==================================\9AU5NUMERO5612353105151588"
                )
                print(
                    "1569899452452/Talent à débloquer avec le nombre corresponda\_35168SUIVANT:24"
                )
                choix = int(input("                              "))
                ClearConsole()
                if choix in ANNUAIREDECHOIXPOURREDCOIN or choix == 1:
                    break
            except ValueError:
                ClearConsole()
        if choix == 1:
            break
        caracteristique_du_talent = ANNUAIREDECHOIXPOURREDCOIN[choix]
        talent = caracteristique_du_talent[0]
        cout_du_talent = caracteristique_du_talent[1]
        talent_necessaire_pour_obtention = caracteristique_du_talent[2]
        if (
            (services.Player.nombre_de_red_coin >= cout_du_talent)
            and (talent_necessaire_pour_obtention == "None")
            and (talent not in services.Player.talents_possedes)
            or (services.Player.nombre_de_red_coin >= cout_du_talent)
            and (talent_necessaire_pour_obtention in services.Player.talents_possedes)
            and (talent not in services.Player.talents_possedes)
        ):
            if services.Player.stigma_negatif == "Incompatible":
                services.Player.nombre_de_red_coin -= cout_du_talent
                print(
                    "Vous buvez le liquide incolore contenu dans les redcoins et faites circuler votre mana comme indiqué par le code..."
                )
                print("...avant de vomir violemment tout le contenu de votre estomac.")
                print(
                    "On dirait que votre corps n'est pas compatible avec les redcoins."
                )
                services.Affichage.EntreePourContinuer()
            elif services.Player.malediction == "Pur":
                print(
                    "Alors que vous alliez ouvrir un redcoin, d'anciennes forces maudites vous envoient un uppercut dans l'estomac."
                )
                print("Vous vous évanouissez et votre corps inconscient s'écroule sur le sol.")
                services.Affichage.EntreePourContinuer()
                print("...")
                services.Affichage.EntreePourContinuer()
                print("...")
                services.Affichage.EntreePourContinuer()
                print("Vous vous réveillez quelques heures plus tard, essuyez la bave qui coule de vos lèvres, et rangez le redcoin.")
                services.Affichage.EntreePourContinuer()
            else:
                services.Player.talents_possedes.append(talent)
                services.Player.nombre_de_red_coin -= cout_du_talent
                print(
                    "Vous buvez le liquide incolore contenu dans les redcoins et faites circuler votre mana comme indiqué par le code ."
                )
                print(f"Vous gagnez le talent [{talent}] !")
                services.Affichage.EntreePourContinuer()
                CheckForFusionOfTalent(talent)


def CheckForFusionOfTalent(talent):
    commentaire = "...?"
    if talent in [
        "Oeuil Magique",
        "Pira",
        "Elektron",
        "Tsumeta-Sa",
        "Mathair",
        "Fos",
        "Haddee",
    ]:
        if "Oeuil Magique" in services.Player.talents_possedes:
            if "Pira" in services.Player.talents_possedes:
                commentaire += "\nLes talents Oeuil Magique et Pira interragissent dans votre corps et donnent naissance a un nouveau talent !"
                talent = "Oculus Ignis"
                services.Player.talents_possedes.append(talent)
                commentaire += f"\nVous gagnez le talent [{talent}] !"
            if "Elektron" in services.Player.talents_possedes:
                commentaire += "\nLes talents Oeuil Magique et Elektron interragissent dans votre corps et donnent naissance a un nouveau talent !"
                talent = "Oculus de Caelo"
                services.Player.talents_possedes.append(talent)
                commentaire += f"\nVous gagnez le talent [{talent}] !"
            if "Tsumeta-Sa" in services.Player.talents_possedes:
                commentaire += "\nLes talents Oeuil Magique et Tsumeta-Sa interragissent dans votre corps et donnent naissance a un nouveau talent !"
                talent = "Oculus Glacies"
                services.Player.talents_possedes.append(talent)
                commentaire += f"\nVous gagnez le talent [{talent}] !"
            if "Mathair" in services.Player.talents_possedes:
                commentaire += "\nLes talents Oeuil Magique et Mathair interragissent dans votre corps et donnent naissance a un nouveau talent !"
                talent = "Oculus Terrae"
                services.Player.talents_possedes.append(talent)
                commentaire += f"\nVous gagnez le talent [{talent}] !"
            if "Fos" in services.Player.talents_possedes:
                commentaire += "\nLes talents Oeuil Magique et Fos interragissent dans votre corps et donnent naissance a un nouveau talent !"
                talent = "Corporalis Oculus"
                services.Player.talents_possedes.append(talent)
                commentaire += f"\nVous gagnez le talent [{talent}] !"
            if "Haddee" in services.Player.talents_possedes:
                commentaire += "\nLes talents Oeuil Magique et Haddee interragissent dans votre corps et donnent naissance a un nouveau talent !"
                talent = "Sanguis Oculus"
                services.Player.talents_possedes.append(talent)
                commentaire += f"\nVous gagnez le talent [{talent}] !"
    if talent in ["Eboulis", "Grand Froid"]:
        if ("Eboulis" in services.Player.talents_possedes) and (
            "Grand Froid" in services.Player.talents_possedes
        ):
            commentaire += "\nLes talents Eboulis et Grand Froid interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Avalanche"
            services.Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"
    if talent in ["Oeuil Magique", "Connaissance"]:
        if ("Oeuil Magique" in services.Player.talents_possedes) and (
            "Connaissance" in services.Player.talents_possedes
        ):
            commentaire += "\nLes talents Oeuil Magique et Connaissance interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Metamorphosis"
            services.Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"
    if talent in ["Luciole", "Pyromage"]:
        if ("Luciole" in services.Player.talents_possedes) and (
            "Pyromage" in services.Player.talents_possedes
        ):
            commentaire += "\nLes talents Luciole et Pyromage interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Bougie Magique"
            services.Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"
    if talent in ["Suroxygenation", "Réflex"]:
        if ("Suroxygenation" in services.Player.talents_possedes) and (
            "Réflex" in services.Player.talents_possedes
        ):
            commentaire += "\nLes talents Suroxygenation et Réflex interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Ultra-Instinct"
            services.Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"
    if talent in ["Cycle Glaciaire", "Pyromage", "Patience", "Carte du Gout", "Nectar"]:
        if (
            ("Cycle Glaciaire" in services.Player.talents_possedes)
            and ("Pyromage" in services.Player.talents_possedes)
            and ("Patience" in services.Player.talents_possedes)
            and ("Carte du Gout" in services.Player.talents_possedes)
            and ("Nectar" in services.Player.talents_possedes)
        ):
            commentaire += "\nLes talents Cycle Glaciaire, Pyromage, Patience, Carte du Gout et Nectar interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Réjuvénation"
            services.Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"
    if talent in [
        "Affinitée de Feu",
        "Affinitée de Foudre",
        "Affinitée de Glace",
        "Affinitée de Terre",
        "Affinitée Physique",
        "Affinitée de Sang",
    ]:
        if (
            ("Affinitée de Feu" in services.Player.talents_possedes)
            and ("Affinitée de Foudre" in services.Player.talents_possedes)
            and ("Affinitée de Glace" in services.Player.talents_possedes)
            and ("Affinitée de Terre" in services.Player.talents_possedes)
            and ("Affinitée de Sang" in services.Player.talents_possedes)
            and ("Affinitée Physique" in services.Player.talents_possedes)
        ):
            commentaire += (
                "\nLes talents Affinitée de Feu, Affinitée de Foudre,"
                " Affinitée de Glace, Affinitée de Terre, Affinitée Physique"
                " et Affinitée de Sang interragissent dans votre corps et "
                "donnent naissance a un nouveau talent !"
            )
            talent = "Elémento-Réceptif"
            services.Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"
    if talent in [
        "Rapide",
        "Grand Froid",
        "Réflex",
        "Conditions Limites",
        "Aura de Feu",
        "Poussière de Diamants",
    ]:
        if (
            ("Rapide" in services.Player.talents_possedes)
            and ("Grand Froid" in services.Player.talents_possedes)
            and ("Réflex" in services.Player.talents_possedes)
            and ("Conditions Limites" in services.Player.talents_possedes)
            and ("Aura de Feu" in services.Player.talents_possedes)
            and ("Poussière de Diamants" in services.Player.talents_possedes)
        ):
            commentaire += (
                "\nLes talents Rapide, Grand Froid,"
                " Réflex, Conditions Limites, Aura de Feu"
                " et Poussière de Diamants interragissent dans votre corps et "
                "donnent naissance a un nouveau talent !"
            )
            talent = "Grand Pandémonium Elémentaire"
            services.Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"
    if talent in ["Baron Rouge", "Pyrosorcier", "Connaissance"]:
        if (
            ("Baron Rouge" in services.Player.talents_possedes)
            and ("Pyrosorcier" in services.Player.talents_possedes)
            and ("Connaissance" in services.Player.talents_possedes)
        ):
            commentaire += "\nLes talents Baron Rouge, Pyrosorcier et Connaissance interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Maitre du Mana"
            services.Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"
    if talent in ["Pira", "Pyromage", "Rafale"]:
        if (
            ("Pira" in services.Player.talents_possedes)
            and ("Pyromage" in services.Player.talents_possedes)
            and ("Rafale" in services.Player.talents_possedes)
        ):
            commentaire += "\nLes talents Pira, Pyromage et Rafale interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Libération de Feu"
            services.Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"

    if talent in ["Elektron", "Facture", "Luciole"]:
        if (
            ("Elektron" in services.Player.talents_possedes)
            and ("Facture" in services.Player.talents_possedes)
            and ("Luciole" in services.Player.talents_possedes)
        ):
            commentaire += "\nLes talents Elektron, Facture et Luciole interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Libération de Foudre"
            services.Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"
    if talent in ["Tsumeta-Sa", "Cycle Glaciaire", "Grand Froid"]:
        if (
            ("Tsumeta-Sa" in services.Player.talents_possedes)
            and ("Cycle Glaciaire" in services.Player.talents_possedes)
            and ("Grand Froid" in services.Player.talents_possedes)
        ):
            commentaire += "\nLes talents Tsumeta-Sa, Cycle Glaciaire et Grand Froid interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Libération de Glace"
            services.Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"

    if talent in ["Mathair", "Fracturation", "Eboulis"]:
        if (
            ("Mathair" in services.Player.talents_possedes)
            and ("Fracturation" in services.Player.talents_possedes)
            and ("Eboulis" in services.Player.talents_possedes)
        ):
            commentaire += "\nLes talents Mathair, Fracturation et Eboulis interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Libération de Terre"
            services.Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"

    if talent in ["Fos", "Oeuil Magique", "Réflex"]:
        if (
            ("Fos" in services.Player.talents_possedes)
            and ("Oeuil Magique" in services.Player.talents_possedes)
            and ("Réflex" in services.Player.talents_possedes)
        ):
            commentaire += "\nLes talents Fos, Oeuil Magique et Réflex interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Libération Physique"
            services.Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"

    if talent in ["Haddee", "Anticoagulants", "Baron Rouge"]:
        if (
            ("Haddee" in services.Player.talents_possedes)
            and ("Anticoagulants" in services.Player.talents_possedes)
            and ("Baron Rouge" in services.Player.talents_possedes)
        ):
            commentaire += "\nLes talents Haddee, Anticoagulants et Baron Rouge interragissent dans votre corps et donnent naissance a un nouveau talent !"
            talent = "Libération de Sang"
            services.Player.talents_possedes.append(talent)
            commentaire += f"\nVous gagnez le talent [{talent}] !"
    if commentaire != "...?":
        print(commentaire)
        services.Affichage.EntreePourContinuer()
