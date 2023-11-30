#!/usr/bin/env python3

import numpy as np

from pybest.gbasis import (
    compute_eri,
    compute_kinetic,
    compute_nuclear,
    compute_nuclear_repulsion,
    compute_overlap,
    get_gobasis,
)
from pybest.io import IOData
from pybest.linalg import DenseLinalgFactory
from pybest.occ_model import AufbauOccModel
from pybest.units import angstrom
from pybest.wrappers import RHF

# Hartree-Fock calculation
# ------------------------

# Construct a molecule from scratch
bond_length = 1.098 * angstrom
mol = IOData(title="dinitrogen")
mol.coordinates = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, bond_length]])
mol.atom = np.array(["N", "N"])

# Create a Gaussian basis set
factory = get_gobasis("cc-pvdz", mol)

# Create a linalg factory
lf = DenseLinalgFactory(factory.nbasis)

# Compute integrals
olp = compute_overlap(factory)
kin = compute_kinetic(factory)
ne = compute_nuclear(factory)
eri = compute_eri(factory)
external = compute_nuclear_repulsion(factory)

# Create alpha orbitals
orb_a = lf.create_orbital()

# Decide how to occupy the orbitals (7 alpha electrons)
occ_model = AufbauOccModel(factory)

# Converge WFN
hf = RHF(lf, occ_model)
hf_output = hf(kin, ne, eri, external, olp, orb_a)

# Write SCF results to a file
hf_output.to_file("n2-scf.molden")
