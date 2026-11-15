"""Techniques et sorts que le joueur peut apprendre, classés par rang, et sorts de soin utilisables hors combat."""

# 0nom 1description 2stigma+ 3stigma- 4stigma* 5techniques
# 6sorts 7items 8talents 9vie 10mana 11force
# 12inteligence 13defence 14tauxcoupcrit
# 15degatcoupcrit 16tauxsortcrit 17degatsortcrit
# 18tauxesquive 19gold
LISTETECHNIQUES = [
    "Attaque Légère",
    "Lance Rapide", 
    "Lance Statique",
    "Lance Electrique",
    "Lance de l'Eclair",
    "Lance Foudroyante",
    "Lance de la Mort Blanche",
    "Bô Chaud",  #
    "Bô Brulant",  #
    "Bô Enflammé",  #
    "Bô de la Fournaise",
    "Bô Magmatique",
    "Bô Solaire",
    "Katana Bleu",
    "Katana Froid",
    "Katana Givré",
    "Katana Glacial",
    "Katana Polaire",
    "Katana Zéro",
    "Corne Argile",  #
    "Corne Lapis",  #
    "Corne Granite",  #
    "Corne Obsidienne",
    "Corne de la Montagne",
    "Corne Continentale",
    "Poing Léger",  #
    "Poing Renforcé",  #
    "Poing Lourd",  #
    "Poing Maitrisé",  #
    "Poing Fatal",  #
    "Poing de la Comète",
    "Dague Volevie",
    "Dague Siphoneuse",
    "Dague Vampirique",
    "Dague Parasite",
    "Dague Destructrice",
    "Dague Créatrice",
]


LISTESORTS = [
    "Tir Arcanique",
    "Faisceau Rapide",
    "Faisceau Statique",
    "Faisceau Electrique",
    "Faisceau de l'Eclair",
    "Faisceau Foudroyant",
    "Faisceau de la Mort Blanche",
    "Thermosphère Chaude",
    "Thermosphère Brulante",
    "Thermosphère Enflammée",
    "Thermosphère de la Fournaise",
    "Thermosphère Magmatique",
    "Thermosphère Solaire",
    "Pic Bleu",
    "Pic Froid",
    "Pic Givré",
    "Pic Glacial",
    "Pic Polaire",
    "Pic Zéro",
    "Création d'Argile",
    "Création de Lapis",
    "Création de Granite",
    "Création Obsidienne",
    "Création de la Montagne",
    "Création Continentale",
    "Explosion Légère",
    "Explosion Renforcée",
    "Explosion Lourde",
    "Explosion Maitrisée",
    "Explosion Fatale",
    "Explosion de la Comète",
    "Dance Volevie",
    "Dance Siphoneuse",
    "Dance Vampirique",
    "Dance Parasite",
    "Dance Destructrice",
    "Dance Créatrice",
    "Sonata Pitoyable",  # 3% ou 8pv
    "Sonata Miséricordieuse",  # 5% ou 15pv
    "Sonata Empathique",  # 12% ou 20pv
    "Sonata Sincère",  # 17% ou 25pv
    "Sonata Bienveillante",  # 20% ou 33pv
    "Sonata Absolutrice",  # 25% ou 40pv
]


LISTEACTIONRANG1 = [
    "Lance Rapide",
    "Bô Chaud", 
    "Katana Bleu",
    "Corne Argile",
    "Poing Léger",
    "Dague Volevie",
    "Faisceau Rapide",
    "Thermosphère Chaude",
    "Pic Bleu",
    "Création d'Argile",
    "Explosion Légère",
    "Dance Volevie",
    "Sonata Pitoyable",
]


LISTEACTIONRANG2 = [
    "Lance Statique",
    "Bô Brulant",
    "Katana Froid",
    "Corne Lapis",
    "Poing Renforcé",
    "Dague Siphoneuse",
    "Faisceau Statique",
    "Thermosphère Brulante",
    "Pic Froid",
    "Création de Lapis",
    "Explosion Renforcée",
    "Dance Siphoneuse",
    "Sonata Miséricordieuse",
]


LISTEACTIONRANG3 = [
    "Lance Electrique",
    "Bô Enflammé",
    "Katana Givré",
    "Corne Granite",
    "Poing Lourd",
    "Dague Vampirique",
    "Faisceau Electrique",
    "Thermosphère Enflammée",
    "Pic Givré",
    "Création de Granite",
    "Explosion Lourde",
    "Dance Vampirique",
    "Sonata Empathique",
]


LISTEACTIONRANG4 = [
    "Lance de l'Eclair",
    "Bô de la Fournaise",
    "Katana Glacial",
    "Corne Obsidienne",
    "Poing Maitrisé",
    "Dague Parasite",
    "Faisceau de l'Eclair",
    "Thermosphère de la Fournaise",
    "Pic Glacial",
    "Création Obsidienne",
    "Explosion Maitrisée",
    "Dance Parasite",
    "Sonata Sincère", 
]


ANNUAIRESORTSSOIN = {  # cout moins élevé quand utilise sort en dehors combat
    "Sonata Pitoyable": 6,
    "Sonata Miséricordieuse": 13,
    "Sonata Empathique": 18,
    "Sonata Sincère": 23,
    "Sonata Bienveillante": 18,
    "Sonata Absolutrice": 38,
}


ANNUAIREDESCRIPTIONSORTSSOIN = {
    "Sonata Pitoyable": "Un bruit pathétique vous enveloppe et apaise la douleur de vos blessures.",
    "Sonata Miséricordieuse": "Un son a peine apréciable se plaque contre votre peau et referme vos blessures.",
    "Sonata Empathique": "Une musique potable soulage votre âme et vos blessures.",
    "Sonata Sincère": "Un chant cristallin inspire votre esprit et revigore votre corps.",
    "Sonata Bienveillante": "Une chorale glorieuse vous fait oublier les problèmes de votre situation et cicatrise vos blessures.",
    "Sonata Absolutrice": "Une mélodie féerique ramène votre être tout entier a un état optimal.",
}


POURCENTAGESORTSOIN = {
    "Sonata Pitoyable": 5,
    "Sonata Miséricordieuse": 7,
    "Sonata Empathique": 14,
    "Sonata Sincère": 19,
    "Sonata Bienveillante": 22,
    "Sonata Absolutrice": 27,
}


SOINMINIMUMSORTSOIN = {
    "Sonata Pitoyable": 10,
    "Sonata Miséricordieuse": 17,
    "Sonata Empathique": 22,
    "Sonata Sincère": 27,
    "Sonata Bienveillante": 35,
    "Sonata Absolutrice": 42,
}
