#!/usr/bin/env python3

from pybest.linalg import DenseLinalgFactory
from pybest.modelhamiltonians import Hubbard
from pybest.occ_model import AufbauOccModel
from pybest.wrappers import RHF

# Define LinalgFactory for 6 sites
# --------------------------------
lf = DenseLinalgFactory(6)

# Define Occupation model and expansion coefficients
# --------------------------------------------------
occ_model = AufbauOccModel(lf, nel=6)
orb = lf.create_orbital()


# Initialize Hubbard class
# ------------------------
modelham = Hubbard(lf, pbc=True)


# One and two-body interaction terms defined for the on-site basis
# ----------------------------------------------------------------
# t-param, t = -1
hopping = modelham.compute_one_body(-1)
# U-param, U = 2
onsite = modelham.compute_two_body(2)


# Overlap matrix for on-site basis
# --------------------------------
olp = modelham.compute_overlap()


# Do a Hartree-Fock calculation
# -----------------------------
hf = RHF(lf, occ_model)
hf_output = hf(hopping, onsite, 0.0, olp, orb)
