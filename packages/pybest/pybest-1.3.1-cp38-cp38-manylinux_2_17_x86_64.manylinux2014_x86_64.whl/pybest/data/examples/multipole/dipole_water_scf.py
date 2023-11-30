#!/usr/bin/env python3

from pybest import context
from pybest.gbasis import (
    compute_dipole,
    compute_eri,
    compute_kinetic,
    compute_nuclear,
    compute_nuclear_repulsion,
    compute_overlap,
    get_gobasis,
)
from pybest.linalg import DenseLinalgFactory
from pybest.occ_model import AufbauOccModel
from pybest.utils import get_com
from pybest.wrappers import RHF, compute_dipole_moment

# Define coordinate file
# ----------------------
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
orb_a = lf.create_orbital()

# Decide how to occupy the orbitals (default Aufbau occupation)
# -------------------------------------------------------------
occ_model = AufbauOccModel(factory)

# Get center of mass
# ------------------
x, y, z = get_com(factory)

# electric dipole moment integrals of the atomic basis set wrt COM
# ----------------------------------------------------------------
dipole = compute_dipole(factory, x=x, y=y, z=z)

# Converge RHF
# ------------
hf = RHF(lf, occ_model)
hf_output = hf(kin, ne, eri, nuc, olp, orb_a)

# Compute dipole moment
# ---------------------
dipole_moment = compute_dipole_moment(dipole, hf_output)
