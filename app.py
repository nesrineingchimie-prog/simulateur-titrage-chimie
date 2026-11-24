import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

import analyse
import chimie
import config

st.set_page_config(page_title="Simulateur Industriel de Titrage", layout="wide")
st.title("Outil d'aide à la décision — Simulation & Analyse de Titrage")

# --- BARRE LATÉRALE : CHOIX DE L'UTILITÉ ET PARAMÈTRES ---
st.sidebar.header("1. Utilité industrielle")
utilite = st.sidebar.selectbox("Choisissez le type de dosage", config.UTILITES)

st.sidebar.header("2. Réactifs, concentrations et volumes")
fichier_csv = st.sidebar.file_uploader("Importer un CSV (colonnes : Vb_mL, pH)", type=["csv"])

if utilite == config.UTILITES[0]:
    acide_sel = st.sidebar.selectbox("Acide fort", list(config.ACIDES_FORTS.keys()))
    nom_acide = st.sidebar.text_input("Nom acide", "Acide fort") if acide_sel == "Personnalisé" else acide_sel

    base_sel = st.sidebar.selectbox("Base forte", list(config.BASES_FORTES.keys()))
    nom_base = st.sidebar.text_input("Nom base", "Base forte") if base_sel == "Personnalisé" else base_sel

    ca = st.sidebar.number_input("Concentration initiale acide Ca (mol/L)", min_value=0.0001, value=0.1, step=0.01, format="%.4f")
    va_ml = st.sidebar.number_input("Volume initial acide Va (mL)", min_value=0.1, value=20.0, step=1.0, format="%.2f")
    cb = st.sidebar.number_input("Concentration base Cb (mol/L)", min_value=0.0001, value=0.1, step=0.01, format="%.4f")
    v_max_ml = st.sidebar.slider("Volume maximal titrant versé (mL)", min_value=1.0, max_value=100.0, value=40.0, step=0.5)

    label_reactif = f"{nom_acide} + {nom_base}"
    xlabel = "Volume de base versée Vb (mL)"
    conc_titrant = cb
    vol_initial_ml = va_ml
    volumes_ml, phs = chimie.ph_acide_fort_base_forte(ca, va_ml, cb, v_max_ml)

elif utilite == config.UTILITES[1]:
    base_sel = st.sidebar.selectbox("Base forte", list(config.BASES_FORTES.keys()))
    nom_base = st.sidebar.text_input("Nom base", "Base forte") if base_sel == "Personnalisé" else base_sel

    acide_sel = st.sidebar.selectbox("Acide fort", list(config.ACIDES_FORTS.keys()))
    nom_acide = st.sidebar.text_input("Nom acide", "Acide fort") if acide_sel == "Personnalisé" else acide_sel

    cb = st.sidebar.number_input("Concentration initiale base Cb (mol/L)", min_value=0.0001, value=0.1, step=0.01, format="%.4f")
    vb_ml = st.sidebar.number_input("Volume initial base Vb (mL)", min_value=0.1, value=20.0, step=1.0, format="%.2f")
    ca = st.sidebar.number_input("Concentration acide Ca (mol/L)", min_value=0.0001, value=0.1, step=0.01, format="%.4f")
    v_max_ml = st.sidebar.slider("Volume maximal titrant versé (mL)", min_value=1.0, max_value=100.0, value=40.0, step=0.5)

    label_reactif = f"{nom_base} + {nom_acide}"
    xlabel = "Volume d'acide versé Va (mL)"
    conc_titrant = ca
    vol_initial_ml = vb_ml
    volumes_ml, phs = chimie.ph_base_forte_acide_fort(cb, vb_ml, ca, v_max_ml)

elif utilite == config.UTILITES[2]:
    acide_sel = st.sidebar.selectbox("Acide faible", list(config.ACIDES_FAIBLES.keys()))
    if acide_sel == "Personnalisé":
        nom_acide = st.sidebar.text_input("Nom acide faible", "Acide faible")
        pka = st.sidebar.number_input("pKa de l'acide", min_value=0.0, max_value=14.0, value=4.76, step=0.05, format="%.2f")
    else:
        nom_acide = acide_sel
        pka = config.ACIDES_FAIBLES[acide_sel]
        st.sidebar.info(f"pKa sélectionné : *{pka:.2f}*")

    base_sel = st.sidebar.selectbox("Base forte", list(config.BASES_FORTES.keys()))
    nom_base = st.sidebar.text_input("Nom base", "Base forte") if base_sel == "Personnalisé" else base_sel

    ca = st.sidebar.number_input("Concentration initiale acide Ca (mol/L)", min_value=0.0001, value=0.1, step=0.01, format="%.4f")
    va_ml = st.sidebar.number_input("Volume initial acide Va (mL)", min_value=0.1, value=20.0, step=1.0, format="%.2f")
    cb = st.sidebar.number_input("Concentration base Cb (mol/L)", min_value=0.0001, value=0.1, step=0.01, format="%.4f")
    v_max_ml = st.sidebar.slider("Volume maximal titrant versé (mL)", min_value=1.0, max_value=100.0, value=40.0, step=0.5)

    label_reactif = f"{nom_acide} + {nom_base}"
    xlabel = "Volume de base versée Vb (mL)"
    conc_titrant = cb
    vol_initial_ml = va_ml
    volumes_ml, phs = chimie.ph_acide_faible_base_forte(ca, va_ml, cb, pka, v_max_ml)

else:
    base_sel = st.sidebar.selectbox("Base faible", list(config.BASES_FAIBLES.keys()))
    if base_sel == "Personnalisé":
        nom_base = st.sidebar.text_input("Nom base faible", "Base faible")
        pka_conj = st.sidebar.number_input("pKa de l'acide conjugué", min_value=0.0, max_value=14.0, value=9.25, step=0.05, format="%.2f")
    else:
        nom_base = base_sel
        pka_conj = config.BASES_FAIBLES[base_sel]
        st.sidebar.info(f"pKa (couple conjugué) : *{pka_conj:.2f}*")

    acide_sel = st.sidebar.selectbox("Acide fort", list(config.ACIDES_FORTS.keys()))
    nom_acide = st.sidebar.text_input("Nom acide", "Acide fort") if acide_sel == "Personnalisé" else acide_sel

    cb = st.sidebar.number_input("Concentration initiale base Cb (mol/L)", min_value=0.0001, value=0.1, step=0.01, format="%.4f")
    vb_ml = st.sidebar.number_input("Volume initial base Vb (mL)", min_value=0.1, value=20.0, step=1.0, format="%.2f")
    ca = st.sidebar.number_input("Concentration acide Ca (mol/L)", min_value=0.0001, value=0.1, step=0.01, format="%.4f")
    v_max_ml = st.sidebar.slider("Volume maximal titrant versé (mL)", min_value=1.0, max_value=100.0, value=40.0, step=0.5)

    label_reactif = f"{nom_base} + {nom_acide}"
    xlabel = "Volume d'acide versé Va (mL)"
    conc_titrant = ca
    vol_initial_ml = vb_ml
    volumes_ml, phs = chimie.ph_base_faible_acide_fort(cb, vb_ml, ca, pka_conj, v_max_ml)


# --- ANALYSE DES RÉSULTATS ---
veq_estime, derivee = analyse.estimer_volume_equivalent(volumes_ml, phs)
pouvoir_tampon = analyse.calculer_pouvoir_tampon(
    volumes_ml, phs, conc_titrant, vol_initial_ml, derivee=derivee
)

# --- ZONE PRINCIPALE : INDICATEURS ET COURBE ---
st.subheader(utilite)

col1, col2, col3 = st.columns(3)
col1.metric("Volume équivalent estimé", f"{veq_estime:.2f} mL")
col2.metric("Pouvoir tampon maximal", f"{np.max(pouvoir_tampon):.4f} mol/(L·pH)")
col3.metric("pH à l'équivalence (simulé)", f"{np.interp(veq_estime, volumes_ml, phs):.2f}")

fig, ax1 = plt.subplots(figsize=(9.5, 4.8))
ax1.plot(volumes_ml, phs, color="blue", linewidth=2.2, label=f"pH ({label_reactif})")
ax1.axvline(veq_estime, color="red", linestyle="--", label=f"Veq = {veq_estime:.2f} mL")
ax1.set_xlabel(xlabel)
ax1.set_ylabel("pH", color="black")
ax1.set_ylim(0, 14)
ax1.tick_params(axis="y", labelcolor="purple")
ax1.grid(True, linestyle=":", alpha=0.6)

ax2 = ax1.twinx()
ax2.plot(volumes_ml, pouvoir_tampon, color="black", linestyle="-.", linewidth=1.6, label="Pouvoir tampon β")
ax2.set_ylabel("Pouvoir tampon β [mol / (L·pH)]", color="silver")
ax2.tick_params(axis="y", labelcolor="gold")

if fichier_csv is not None:
    df_csv, erreur_csv = analyse.charger_donnees_csv(fichier_csv)
    if erreur_csv is not None:
        st.warning(erreur_csv)
    else:
        ax1.scatter(df_csv["Vb_mL"], df_csv["pH"], color="#00C853", s=45, zorder=5, label="Mesures CSV")

lignes_1, labels_1 = ax1.get_legend_handles_labels()
lignes_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lignes_1 + lignes_2, labels_1 + labels_2, loc="best")

st.pyplot(fig)