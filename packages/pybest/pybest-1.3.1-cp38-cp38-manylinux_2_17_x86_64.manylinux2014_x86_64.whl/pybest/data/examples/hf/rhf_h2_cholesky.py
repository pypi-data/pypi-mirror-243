#!/usr/bin/env python3


from pybest import context
from pybest.gbasis import (
    compute_cholesky_eri,
    compute_kinetic,
    compute_nuclear,
    compute_nuclear_repulsion,
    compute_overlap,
    get_gobasis,
)
from pybest.linalg import CholeskyLinalgFactory
from pybest.occ_model import AufbauOccModel
from pybest.wrappers import RHF

# Hartree-Fock calculation
# ------------------------

# Construct a molecule from scratch
# Create a Gaussian basis set
factory = get_gobasis("cc-pvdz", context.get_fn("test/h2.xyz"))

# Create a linalg factory
lf = CholeskyLinalgFactory(factory.nbasis)

# Compute integrals
olp = compute_overlap(factory)
kin = compute_kinetic(factory)
ne = compute_nuclear(factory)

# set CD threshold to 1e-8 (default 1e-3)
eri = compute_cholesky_eri(factory, threshold=1e-8)
external = compute_nuclear_repulsion(factory)

# Create alpha orbitals
orb_a = lf.create_orbital()

# Decide how to occupy the orbitals (1 alpha electron)
occ_model = AufbauOccModel(factory)

# Converge WFN
hf = RHF(lf, occ_model)
hf_output = hf(kin, ne, eri, external, olp, orb_a)

# Write SCF results to a molden file
hf_output.to_file("h2-scf.molden")
