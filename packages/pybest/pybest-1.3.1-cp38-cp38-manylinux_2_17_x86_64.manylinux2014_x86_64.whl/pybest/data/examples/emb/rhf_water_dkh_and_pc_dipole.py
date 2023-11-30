#!/usr/bin/env python3
"""Calculates a dipole moment in the presence of point charges and the DKH2 Hamiltonian."""

from pybest import context
from pybest.gbasis import (
    compute_dipole,
    compute_dkh,
    compute_eri,
    compute_kinetic,
    compute_nuclear,
    compute_nuclear_pc,
    compute_nuclear_repulsion,
    compute_overlap,
    compute_point_charges,
    get_charges,
    get_gobasis,
)
from pybest.linalg import DenseLinalgFactory
from pybest.occ_model import AufbauOccModel
from pybest.utils import get_com
from pybest.wrappers import RHF, compute_dipole_moment

# Load the coordinates and charges from PyBEST's test data directory
# ------------------------------------------------------------------
coordinates_xyz = context.get_fn("test/water_pc.xyz")
pc_xyz = context.get_fn("test/water_pc.pc")

# Get basis set and external charges
# ----------------------------------
gobasis = get_gobasis("cc-pvdz", coordinates_xyz)
charges = get_charges(pc_xyz)

# Create a linalg factory instance
# --------------------------------
lf = DenseLinalgFactory(gobasis.nbasis)

# Compute standard QC integrals
# -----------------------------
olp = compute_overlap(gobasis)
kin = compute_kinetic(gobasis)
ne = compute_nuclear(gobasis)
eri = compute_eri(gobasis)
external = compute_nuclear_repulsion(gobasis)

# Calculate the interaction of point charges with electrons
# ---------------------------------------------------------
pc = compute_point_charges(gobasis, charges)

# Calculate the interaction of point charges with nuclei
# ------------------------------------------------------
external += compute_nuclear_pc(gobasis, charges)

# Create alpha orbitals
# ---------------------
orb_a = lf.create_orbital()

# Choose an occupation model
# --------------------------
occ_model = AufbauOccModel(gobasis)

# Get the center of mass
# ----------------------
x, y, z = get_com(gobasis)

# Electric dipole moment integrals of the atomic basis set wrt COM
# ----------------------------------------------------------------
dipole = compute_dipole(gobasis, x=x, y=y, z=z)

# HF with the point charges in the non-relativistic QC Hamiltonian
# ----------------------------------------------------------------
hf_pc = RHF(lf, occ_model)
hf_pc_output = hf_pc(eri, kin, ne, external, pc, olp, orb_a)

# Compute HF dipole moment using non-relativistic QC Hamiltonian
# --------------------------------------------------------------
dipole_moment = compute_dipole_moment(dipole, hf_pc_output)

# HF with the point charges in the DKH Hamiltonian
# ------------------------------------------------
dkh_pc = compute_dkh(gobasis, charges)
hf_dkh_pc = RHF(lf, occ_model)
hf_dkh_pc_output = hf_dkh_pc(dkh_pc, eri, pc, external, olp, orb_a)

# Compute HF dipole moment using the DKH2 Hamiltonian
# ---------------------------------------------------
dipole_moment = compute_dipole_moment(dipole, hf_dkh_pc_output)
