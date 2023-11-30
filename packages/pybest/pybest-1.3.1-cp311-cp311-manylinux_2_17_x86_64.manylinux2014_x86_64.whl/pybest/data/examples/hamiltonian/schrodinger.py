#!/usr/bin/env python3

from pybest import context
from pybest.gbasis import (
    compute_dipole,
    compute_eri,
    compute_kinetic,
    compute_nuclear,
    compute_nuclear_repulsion,
    compute_overlap,
    compute_quadrupole,
    get_gobasis,
)
from pybest.linalg import DenseLinalgFactory
from pybest.utils import get_com

# Molecular Schroedinger Hamiltonian for the water molecule
# ---------------------------------------------------------

# Define coordinate file
# ----------------------------------------------------
coord = context.get_fn("test/water.xyz")

# Create a Gaussian basis set
# ---------------------------
factory = get_gobasis("cc-pvdz", coord)

# Create a linalg factory
# -----------------------
lf = DenseLinalgFactory(factory.nbasis)

# Compute integrals in the atom-centered Gaussian basis set
# ---------------------------------------------------------
kin = compute_kinetic(factory)
ne = compute_nuclear(factory)
eri = compute_eri(factory)
nuc = compute_nuclear_repulsion(factory)

# Compute overlap matrix of atom-centered basis set
# -------------------------------------------------
olp = compute_overlap(factory)

# Create orbitals that store the AO/MO coefficients
# -------------------------------------------------
orb = lf.create_orbital()

# Get center of mass
# ------------------
x, y, z = get_com(factory)

# electric dipole moment integrals of the atomic basis set wrt COM
# ----------------------------------------------------------------
olp, mux, muy, muz, origin = compute_dipole(factory, x=x, y=y, z=z)

# electric quadrupole moment integrals of the atomic basis set wrt COM
# --------------------------------------------------------------------
olp, mux, muy, muz, muxx, muxy, muxz, muyy, muyz, muzz = compute_quadrupole(
    factory, x=x, y=y, z=z
)
