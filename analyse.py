import numpy as np
import pandas as pd


def estimer_volume_equivalent(volumes_ml, phs):
    """Estime le volume équivalent (en mL) à partir du maximum de la dérivée dpH/dV."""
    volumes_ml = np.asarray(volumes_ml, dtype=float)
    phs = np.asarray(phs, dtype=float)

    derivee = np.gradient(phs, volumes_ml)
    idx_max = int(np.argmax(derivee))
    veq_estime = float(volumes_ml[idx_max])
    return veq_estime, derivee


def calculer_pouvoir_tampon(volumes_ml, phs, conc_titrant, vol_initial_ml, derivee=None):
    """Calcule le pouvoir tampon beta = |d(n_titrant / V_total) / dpH|."""
    volumes_ml = np.asarray(volumes_ml, dtype=float)
    phs = np.asarray(phs, dtype=float)

    if derivee is None:
        derivee = np.gradient(phs, volumes_ml)

    # Quantité de réactif titrant (mol) par litre de solution totale (L)
    n_par_L = (conc_titrant * (volumes_ml / 1000.0)) / ((vol_initial_ml + volumes_ml) / 1000.0)
    dnb_L = np.gradient(n_par_L, volumes_ml)

    masque_valide = np.abs(derivee) > 1e-6
    denominateur_securise = np.where(masque_valide, derivee, 1.0)
    beta = np.where(masque_valide, np.abs(dnb_L / denominateur_securise), 0.0)
    return beta


def charger_donnees_csv(fichier_csv):
    """Charge un CSV expérimental et vérifie la présence des colonnes Vb_mL et pH."""
    try:
        df = pd.read_csv(fichier_csv)
    except Exception as exc:
        return None, f"Impossible de lire le fichier CSV : {exc}"

    colonnes_requises = {"Vb_mL", "pH"}
    if not colonnes_requises.issubset(df.columns):
        return None, "Le fichier CSV doit contenir exactement les colonnes 'Vb_mL' et 'pH'."

    return df, None
