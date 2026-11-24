# Simulateur & Analyseur Modulaire de Titrage Acido-Basique
Application interactive développée en **Python** avec **Streamlit** pour simuler des courbes de titrageacido-basique , estimer le volume équivalent , calculer le pouvoir tampon β et comparer les modèles théoriques à des mesures expérimentales .
---
## Objective du projet 
- Traduire les équilibres acido-basiques (acides et bases forts ou faibles) en modèle numériques exploitables .
- Estimer automatiquement le volume équivalent via la dérivée numérique (dpH/dV) et suivre l'évolution du pouvoir tampon β .
- Importer et valider des relevés expérimentaux aux format CSV ('Vb_mL','pH') afin de confronter les mesures réelles à la courbe simulée.
---
## Fonctionnalités principales
- **4 configuration de titrage prises en charge :*
1.Acide fort par base forte .
2.Base forte par acide fort . 
3.Acide faible par base forte . 
4.Base faible par acide fort .
-**Catalogue de réactifs intégré**(pKa prédifinis à 25°C) avec option de saisie personnalisée. 
-**Indicateurs clés en temps réel :**volume équivalentestimé(mL), pouvoir tampon maximal et pH à l'équivalence .
-**Visualisation double axe ** (courb de pH et pouvoir tampon β) avec superposition optionnelle des points expérimentaux CSV .
---
## Achitecture du projet 
Le code est structuré en 4 modules indépendants afin de séparer les constantes, les calculs chimiques, le traitementdu signal et l'interface utilisateur :

''' text
mon_dosage/
├── config.py          # Constantes physico-chimiques (Ke à 25 °C) et catalogues de réactifs
├── chimie.py          # Modèles de calcul de pH (cas forts et électroneutralité pour espèces faibles)
├── analyse.py         # Calcul de dpH/dV, volume équivalent, pouvoir tampon β et validation CSV
├── app.py             # Interface Streamlit, indicateurs et graphiques double axe
├── requirements.txt   # Dépendances Python du projet
└── README.md          # Documentation du projet


 