# Liste des 4 utilités industrielles proposées à l'utilisateur
UTILITES = [
    "1. Dosage d'un acide fort par une base forte",
    "2. Dosage d'une base forte par un acide fort",
    "3. Dosage d'un acide faible par une base forte",
    "4. Dosage d'une base faible par un acide fort",
]

# Catalogues de réactifs prédéfinis + option personnalisée
ACIDES_FORTS = {
    "Acide chlorhydrique (HCl)": None,
    "Acide nitrique (HNO3)": None,
    "Personnalisé": None,
}

BASES_FORTES = {
    "Soude (NaOH)": None,
    "Potasse (KOH)": None,
    "Personnalisé": None,
}

ACIDES_FAIBLES = {
    "Acide acétique (CH3COOH)": 4.76,
    "Acide formique (HCOOH)": 3.75,
    "Acide lactique": 3.86,
    "Acide benzoïque": 4.20,
    "Personnalisé": None,
}

BASES_FAIBLES = {
    "Ammoniaque (NH3)": 9.25,
    "Aniline": 4.60,
    "Méthylamine": 10.66,
    "Personnalisé": None,
}

# Constantes physico-chimiques à 25 °C
KE_25C = 1.0e-14
NB_POINTS_COURBE = 300