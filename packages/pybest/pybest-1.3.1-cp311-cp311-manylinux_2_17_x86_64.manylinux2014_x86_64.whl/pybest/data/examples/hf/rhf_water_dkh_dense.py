#!/usr/bin/env python3

from pybest import context
from pybest.gbasis import (
    compute_dkh,
    compute_eri,
    compute_nuclear_repulsion,
    compute_overlap,
    get_gobasis,
)
from pybest.linalg import DenseLinalgFactory
from pybest.occ_model import AufbauOccModel
from pybest.wrappers import RHF

# Hartree-Fock calculation
# ------------------------

# Load the coordinates from file.
# Use the XYZ file from PyBEST's test data directory.
fn_xyz = context.get_fn("test/water.xyz")

# Create a Gaussian basis set
factory = get_gobasis("cc-pvdz", fn_xyz)

# Create a linalg factory
lf = DenseLinalgFactory(factory.nbasis)

# Compute integrals
olp = compute_overlap(factory)
dkh = compute_dkh(factory)
eri = compute_eri(factory)
external = compute_nuclear_repulsion(factory)

# Create alpha orbitals
orb_a = lf.create_orbital()

# Decide how to occupy the orbitals (5 alpha electrons)
occ_model = AufbauOccModel(factory)

# Converge RHF
hf = RHF(lf, occ_model)

# the order of the arguments does not matter
hf_output = hf(dkh, eri, external, olp, orb_a)

# Write SCF results to a molden file
hf_output.to_file("water-scf.molden")
