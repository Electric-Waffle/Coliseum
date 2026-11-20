"""Sauvegarde permanente (s0ve.txt) : tout ce qui reste débloqué d'une run à l'autre."""

import ast

from coliseum import services


class SoveManagement:

    def __init__(self):
        pass

    def ModifieArtefactDansSove(self, type_de_action, artefact):

        donnees_de_s0ve = services.Observation.GetPermanentThingsFromS0ve()

        chaine_de_caractere = donnees_de_s0ve["Artefact Debloques"]
        liste_de_artefact = ast.literal_eval(chaine_de_caractere)


        if type_de_action == "Ajout":
            liste_de_artefact.append(artefact)

        elif type_de_action == "Checke":
            if artefact in liste_de_artefact:
                return True
            else:
                return False
            
        elif type_de_action == "Donne":
            return liste_de_artefact
            
        donnees_de_s0ve["Artefact Debloques"] = liste_de_artefact

        services.Observation.SetPermanentThingsToS0ve(donnees_de_s0ve)

    def ModifieCompteurDeDropDansSove(self, type_de_action, materiau):
        """Compteur de malchance des drops de matériaux (voir combat/drop.py).

        - "Donne"    : nombre d'échecs consécutifs pour ce matériau ;
        - "Echec"    : en ajoute un ;
        - "Reussite" : remet le compteur à zéro.

        ATTENTION : la clé n'existe pas dans les anciens s0ve.txt. `get` avec
        un dictionnaire vide évite l'erreur ; la clé est créée au premier
        enregistrement.
        """
        donnees_de_s0ve = services.Observation.GetPermanentThingsFromS0ve()
        compteurs = ast.literal_eval(donnees_de_s0ve.get("Compteur de drop", "{}"))

        if type_de_action == "Donne":
            return compteurs.get(materiau, 0)
        elif type_de_action == "Echec":
            compteurs[materiau] = compteurs.get(materiau, 0) + 1
        elif type_de_action == "Reussite":
            compteurs[materiau] = 0

        donnees_de_s0ve["Compteur de drop"] = compteurs
        services.Observation.SetPermanentThingsToS0ve(donnees_de_s0ve)

    def ModifieRumeursDansSove(self, type_de_action, numero_de_la_rumeur):

        donnees_de_s0ve = services.Observation.GetPermanentThingsFromS0ve()

        chaine_de_caractere = donnees_de_s0ve["Rumeurs"]
        liste_de_rumeurs = ast.literal_eval(chaine_de_caractere)


        if type_de_action == "Ajout":
            liste_de_rumeurs.append(numero_de_la_rumeur)

        elif type_de_action == "Checke":
            if numero_de_la_rumeur in liste_de_rumeurs:
                return True
            else:
                return False
            
        elif type_de_action == "Donne":
            return liste_de_rumeurs
            
        donnees_de_s0ve["Rumeurs"] = liste_de_rumeurs

        services.Observation.SetPermanentThingsToS0ve(donnees_de_s0ve)

    def ModifieRecettesDansSove(self, type_de_action, numero_de_la_recette):

        donnees_de_s0ve = services.Observation.GetPermanentThingsFromS0ve()

        chaine_de_caractere = donnees_de_s0ve["Recettes"]
        liste_de_recettes = ast.literal_eval(chaine_de_caractere)


        if type_de_action == "Ajout":
            liste_de_recettes.append(numero_de_la_recette)

        elif type_de_action == "Checke":
            if numero_de_la_recette in liste_de_recettes:
                return True
            else:
                return False
            
        elif type_de_action == "Donne":
            return liste_de_recettes
            
        donnees_de_s0ve["Recettes"] = liste_de_recettes

        services.Observation.SetPermanentThingsToS0ve(donnees_de_s0ve)

    def ModifieArtefactProposeDansSove(self, type_de_action, artefact):

        donnees_de_s0ve = services.Observation.GetPermanentThingsFromS0ve()

        chaine_de_caractere = donnees_de_s0ve["Artefact Proposé"]
        liste_de_artefact = ast.literal_eval(chaine_de_caractere)


        if type_de_action == "Ajout":
            liste_de_artefact.append(artefact)

        elif type_de_action == "Enleve":
            liste_de_artefact.remove(artefact)

        elif type_de_action == "Donne":
            return liste_de_artefact
            
        donnees_de_s0ve["Artefact Proposé"] = liste_de_artefact

        services.Observation.SetPermanentThingsToS0ve(donnees_de_s0ve)

    def  ModifieActionsConnuesDansSove(self, type_de_action, action="None"):

        donnees_de_s0ve = services.Observation.GetPermanentThingsFromS0ve()

        chaine_de_caractere = donnees_de_s0ve["Actions Connues"]
        liste_de_actions = ast.literal_eval(chaine_de_caractere)


        if type_de_action == "Ajout":
            liste_de_actions.append(action)

        elif type_de_action == "Enleve":
            liste_de_actions.remove(action)

        elif type_de_action == "Checke":
            if action in liste_de_actions:
                return True
            else:
                return False

        elif type_de_action == "Donne":
            return liste_de_actions
            
        donnees_de_s0ve["Actions Connues"] = liste_de_actions

        services.Observation.SetPermanentThingsToS0ve(donnees_de_s0ve)
        
    def ModifieTagsDansSove(self, type_de_action, tag):

        donnees_de_s0ve = services.Observation.GetPermanentThingsFromS0ve()

        chaine_de_caractere = donnees_de_s0ve["Tags Permanents"]
        liste_de_tags = ast.literal_eval(chaine_de_caractere)


        if type_de_action == "Ajout":
            liste_de_tags.append(tag)

        elif type_de_action == "Enleve":
            liste_de_tags.remove(tag)

        elif type_de_action == "Checke":
            if tag in liste_de_tags:
                return True
            else:
                return False

        elif type_de_action == "Donne":
            return liste_de_tags
            
        donnees_de_s0ve["Tags Permanents"] = liste_de_tags

        services.Observation.SetPermanentThingsToS0ve(donnees_de_s0ve)

    def  ModifieDechetsDansSove(self, type_de_action, objet, nombre=None):

        donnees_de_s0ve = services.Observation.GetPermanentThingsFromS0ve()

        chaine_de_caractere = donnees_de_s0ve["Déchets"]
        dictionaire_de_dechets = ast.literal_eval(chaine_de_caractere)
        liste_de_dechets = dictionaire_de_dechets

        if type_de_action == "Ajout":
            liste_de_dechets[objet] += nombre
            

        elif type_de_action == "Enleve":
            liste_de_dechets[objet] -= nombre

        elif type_de_action == "Limite":
            if liste_de_dechets[objet] >= nombre:
                return True
            else:
                return False
            
        elif type_de_action == "Donne":
            return liste_de_dechets
            
        elif type_de_action == "Nombre":
            return liste_de_dechets[objet]
            
        donnees_de_s0ve["Déchets"] = liste_de_dechets

        services.Observation.SetPermanentThingsToS0ve(donnees_de_s0ve)

    def  ModifieLivraisonDansSove(self, type_de_action, objet, nombre=0):

        donnees_de_s0ve = services.Observation.GetPermanentThingsFromS0ve()

        chaine_de_caractere = donnees_de_s0ve["Livraison"]
        dictionaire_de_dechets = ast.literal_eval(chaine_de_caractere)
        liste_de_dechets = dictionaire_de_dechets

        if type_de_action == "Ajout":
            liste_de_dechets[objet] += 1
            
        elif type_de_action == "Nombre":
            return liste_de_dechets[objet]
        
        elif type_de_action == "Limite":

            if liste_de_dechets[objet] >= nombre:
                return True
            else:
                return False
            
        donnees_de_s0ve["Livraison"] = liste_de_dechets

        services.Observation.SetPermanentThingsToS0ve(donnees_de_s0ve)

    def  PutInSove(self):
        donnees_de_s0ve = services.Observation.GetPermanentThingsFromS0ve()  
            
        dictionaire_de_entree = {}
        
        donnees_de_s0ve["Cigogne Blanche"] = dictionaire_de_entree

        services.Observation.SetPermanentThingsToS0ve(donnees_de_s0ve)

    def  ModifieCigogneBlancheDansSove(self, theme, type_de_action, entree="None"):

        donnees_de_s0ve = services.Observation.GetPermanentThingsFromS0ve()

        chaine_de_caractere = donnees_de_s0ve["Cigogne Blanche"]
        dictionaire_de_entree = ast.literal_eval(chaine_de_caractere)

        liste_de_entree = dictionaire_de_entree[theme]

        if type_de_action == "Donne":
            return liste_de_entree

        if type_de_action == "Checke":
            if entree in liste_de_entree:
                return True
            else:
                return False

        if type_de_action == "Ajout":

            liste_de_entree.append(entree)

            dictionaire_de_entree[theme] = liste_de_entree

        donnees_de_s0ve["Cigogne Blanche"] = dictionaire_de_entree

        services.Observation.SetPermanentThingsToS0ve(donnees_de_s0ve)

    def RajouteEntreeAuLivreCigogneBlancheSiOnAPas(self, theme, entree):
        if not self.ModifieCigogneBlancheDansSove(theme,"Checke",entree):
            self.ModifieCigogneBlancheDansSove(theme,"Ajout",entree)
