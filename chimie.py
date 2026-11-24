import numpy as np
import config


def _resoudre_h_plus(lhs_grid, rhs_grid, h_grid):
    """Trouve la valeur de [H+] minimisant l'écart d'électroneutralité."""
    residu = np.abs(lhs_grid - rhs_grid)
    return h_grid[np.argmin(residu)]


# 1. Acide fort par base forte
def ph_acide_fort_base_forte(ca, va_ml, cb, v_max_ml, nb_points=config.NB_POINTS_COURBE):
    va = va_ml / 1000.0
    volumes_ml = np.linspace(0.1, v_max_ml, nb_points)
    phs = []
    na = ca * va

    for vb_ml in volumes_ml:
        vb = vb_ml / 1000.0
        nb = cb * vb
        v_tot = va + vb

        if na > nb:
            ph = -np.log10((na - nb) / v_tot)
        elif nb > na:
            ph = 14.0 + np.log10((nb - na) / v_tot)
        else:
            ph = 7.0
        phs.append(ph)

    return volumes_ml, np.array(phs)


# 2. Base forte par acide fort
def ph_base_forte_acide_fort(cb, vb_ml, ca, v_max_ml, nb_points=config.NB_POINTS_COURBE):
    vb = vb_ml / 1000.0
    volumes_ml = np.linspace(0.1, v_max_ml, nb_points)
    phs = []
    nb = cb * vb

    for va_ml in volumes_ml:
        va = va_ml / 1000.0
        na = ca * va
        v_tot = vb + va

        if nb > na:
            ph = 14.0 + np.log10((nb - na) / v_tot)
        elif na > nb:
            ph = -np.log10((na - nb) / v_tot)
        else:
            ph = 7.0
        phs.append(ph)

    return volumes_ml, np.array(phs)


# 3. Acide faible par base forte
def ph_acide_faible_base_forte(ca, va_ml, cb, pka, v_max_ml, nb_points=config.NB_POINTS_COURBE):
    va = va_ml / 1000.0
    volumes_ml = np.linspace(0.1, v_max_ml, nb_points)
    phs = []

    na = ca * va
    ka = 10.0 ** (-pka)
    ke = config.KE_25C
    h_grid = np.logspace(-14, 0, 2000)
    oh_grid = ke / h_grid

    for vb_ml in volumes_ml:
        vb = vb_ml / 1000.0
        nb = cb * vb
        v_tot = va + vb

        ca_dil = na / v_tot
        cb_dil = nb / v_tot

        # Électroneutralité : [H+] + [Na+] = [A-] + [HO-]
        lhs = h_grid + cb_dil
        rhs = (ca_dil * ka / (h_grid + ka)) + oh_grid
        h_plus = _resoudre_h_plus(lhs, rhs, h_grid)
        phs.append(-np.log10(h_plus))

    return volumes_ml, np.array(phs)


# 4. Base faible par acide fort
def ph_base_faible_acide_fort(cb, vb_ml, ca, pka_conj, v_max_ml, nb_points=config.NB_POINTS_COURBE):
    vb = vb_ml / 1000.0
    volumes_ml = np.linspace(0.1, v_max_ml, nb_points)
    phs = []

    nb = cb * vb
    pkb = 14.0 - pka_conj
    kb = 10.0 ** (-pkb)
    ke = config.KE_25C
    h_grid = np.logspace(-14, 0, 2000)
    oh_grid = ke / h_grid

    for va_ml in volumes_ml:
        va = va_ml / 1000.0
        na = ca * va
        v_tot = vb + va

        cb_dil = nb / v_tot
        ca_dil = na / v_tot

        # Électroneutralité : [H+] + [BH+] = [Cl-] + [HO-]
        lhs = h_grid + (cb_dil * (h_grid / (kb + h_grid)))
        rhs = ca_dil + oh_grid
        h_plus = _resoudre_h_plus(lhs, rhs, h_grid)
        phs.append(-np.log10(h_plus))

    return volumes_ml, np.array(phs)
    


