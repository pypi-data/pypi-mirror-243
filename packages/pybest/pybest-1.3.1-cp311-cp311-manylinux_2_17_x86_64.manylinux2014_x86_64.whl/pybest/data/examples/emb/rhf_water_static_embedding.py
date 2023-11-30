#!/usr/bin/env python3
"""Calculates a dipole moment in the presence of the
static embedding potential."""
from pybest import context
from pybest.gbasis import (
    compute_dipole,
    compute_eri,
    compute_kinetic,
    compute_nuclear,
    compute_nuclear_repulsion,
    compute_overlap,
    compute_static_embedding,
    get_embedding,
    get_gobasis,
)
from pybest.linalg import DenseLinalgFactory
from pybest.occ_model import AufbauOccModel
from pybest.utils import get_com
from pybest.wrappers import RHF, compute_dipole_moment

# Load the coordinates and embedding_pot from PyBEST's test data directory
# ------------------------------------------------------------------------
coordinates_xyz = context.get_fn("test/water_emb.xyz")
embedding_pot = context.get_fn("test/water_emb.emb")

# Get basis set and static emebedding potential
# ---------------------------------------------
gobasis = get_gobasis("sto-6g", coordinates_xyz)
embedding_pot = get_embedding(embedding_pot)

# Create a linalg factory instance
# --------------------------------
lf = DenseLinalgFactory(gobasis.nbasis)

# Compute standard QC integrals
# -----------------------------
olp = compute_overlap(gobasis)
kin = compute_kinetic(gobasis)
ne = compute_nuclear(gobasis)
er = compute_eri(gobasis)
external = compute_nuclear_repulsion(gobasis)

# Compute static embedding potential generated with PyADF
# -------------------------------------------------------
emb = compute_static_embedding(gobasis, embedding_pot)

# Create alpha orbitals
# ---------------------
orb_a = lf.create_orbital()

# Choose an occupation model
# --------------------------
occ_model = AufbauOccModel(gobasis)

# Get center of charge
# --------------------
x, y, z = get_com(gobasis)

# Electric dipole moment integrals of the atomic basis set wrt COM
# ----------------------------------------------------------------
dipole = compute_dipole(gobasis, x=x, y=y, z=z)

# HF with the embedding_pot using the non-relativistic QC Hamiltonian
# -------------------------------------------------------------------
hf_emb = RHF(lf, occ_model)
hf_output_emb = hf_emb(kin, ne, er, external, emb, olp, orb_a)
dipole_moment = compute_dipole_moment(dipole, hf_output_emb)
