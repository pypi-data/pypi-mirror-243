#!/usr/bin/env python3

from pybest import context
from pybest.gbasis import (
    compute_dkh,
    compute_nuclear_repulsion,
    compute_overlap,
    get_gobasis,
)
from pybest.linalg import DenseLinalgFactory

# DKH2 Hamiltonian for the U dimer (the lowest closed-shell state)
# --------------------------------

# Define coordinate file
# ----------------------
coord = context.get_fn("test/u2.xyz")

# Create a Gaussian basis set
# ---------------------------
factory = get_gobasis("ano-rcc-vdz", coord)

# Create a linalg factory
# -----------------------
lf = DenseLinalgFactory(factory.nbasis)

# Compute integrals in the atom-centered Gaussian basis set
# ---------------------------------------------------------
dkh = compute_dkh(factory)
nuc = compute_nuclear_repulsion(factory)
# ERI are not computed in this example

# Compute overlap matrix of atom-centered basis set
# -------------------------------------------------
olp = compute_overlap(factory)

# Create orbitals that store the AO/MO coefficients
# -------------------------------------------------
orb = lf.create_orbital()
