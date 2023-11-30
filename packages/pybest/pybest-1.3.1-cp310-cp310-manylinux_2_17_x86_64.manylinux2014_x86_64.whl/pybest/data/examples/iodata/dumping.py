#!/usr/bin/env python3

from pybest import context
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
from pybest.orbital_utils import transform_integrals
from pybest.wrappers import RHF

# Define coordinate file.
# ----------------------------------------------------
coord = context.get_fn("test/water.xyz")

# Create a Gaussian basis set
# ---------------------------
factory = get_gobasis("cc-pvdz", coord)
lf = DenseLinalgFactory(factory.nbasis)
occ_model = AufbauOccModel(factory)
orb = lf.create_orbital()

# Construct Hamiltonian
# ---------------------
kin = compute_kinetic(factory)
ne = compute_nuclear(factory)
eri = compute_eri(factory)
e_core = compute_nuclear_repulsion(factory)
olp = compute_overlap(factory)

# Get Hartree-Fock MOs
# --------------------
hf = RHF(lf, occ_model)
hf_output = hf(kin, ne, eri, e_core, orb, olp)

# Assign to IOData using constructor
# ----------------------------------
data = IOData(kin=kin, ne=ne, eri=eri, e_core=e_core)

# Update IOData: add new attribute (orbitals)
# -------------------------------------------
data.orb_a = orb

# Update IOData: delete attribute (orbitals)
# ------------------------------------------
del data.orb_a

# Update IOData: modify attribute (core energy)
# ---------------------------------------------
data.e_core = 5.0

# Print content of IOData
# -----------------------
print(data.__dict__)

# Dump to internal checkpoint file
# --------------------------------
data.to_file("checkpoint.h5")

# Construct IOData container for xyz
# Both atoms and coordinates are stored in gobasis
# ------------------------------------------------
data = IOData(atom=factory.atom, coordinates=factory.coordinates)

# Dump to xyz file
# ----------------
data.to_file("mol.xyz")


# Write SCF results to a molden file
# ----------------------------------
# First, construct IOData container, include gobasis and orbitals as attribute
data = IOData(gobasis=factory, orb_a=orb)
# Now, we can write the molden file
# ---------------------------------
data.to_file("water-scf.molden")


# Transform Hamiltinian to MO basis
# ---------------------------------
# transform integrals for restricted orbitals orb
t_ints = transform_integrals(kin, ne, eri, orb)

# transformed one-electron integrals: attribute 'one' (list)
(one,) = t_ints.one  # or: one = ti_.one[0]
# transformed two-electron integrals: attribute 'two' (list)
(two,) = t_ints.two  # or: two = ti_.two[0]

# Write to a FCIDUMP file
# -----------------------
data = IOData(one=one, two=two, e_core=e_core, nelec=20, ms2=0)
data.to_file("hamiltonian_mo.FCIDUMP")
