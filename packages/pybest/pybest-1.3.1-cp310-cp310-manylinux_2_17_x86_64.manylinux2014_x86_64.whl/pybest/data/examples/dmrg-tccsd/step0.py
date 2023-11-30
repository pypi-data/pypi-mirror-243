#!/usr/bin/env python3
""" Getting one- and two-body integrals in the ROOpCCD orbital basis for
the CN+ molecule."""

from pybest.gbasis import (
    compute_eri,
    compute_kinetic,
    compute_nuclear,
    compute_nuclear_repulsion,
    compute_overlap,
    get_gobasis,
)
from pybest.geminals import ROOpCCD
from pybest.io import IOData
from pybest.linalg import DenseLinalgFactory
from pybest.occ_model import AufbauOccModel
from pybest.orbital_utils import split_core_active, transform_integrals
from pybest.wrappers import RHF

###############################################################################
## Set up molecule, define basis set ##########################################
###############################################################################
# get the XYZ file from PyBEST's test data directory
obasis = get_gobasis("cc-pvdz", "data/cn+.xyz")
lf = DenseLinalgFactory(obasis.nbasis)
occ_model = AufbauOccModel(obasis, charge=1)
###############################################################################
## Construct Hamiltonian ######################################################
###############################################################################
kin = compute_kinetic(obasis)
ne = compute_nuclear(obasis)
eri = compute_eri(obasis)
e_core = compute_nuclear_repulsion(obasis)
olp = compute_overlap(obasis)
orb_a = lf.create_orbital()
###############################################################################
## Do a Hartree-Fock calculation ##############################################
###############################################################################
hf = RHF(lf, occ_model)
hf_output = hf(kin, ne, eri, e_core, olp, orb_a)
###############################################################################
# Do pCCD using RHF orbitals as an inital guess for solver ####################
###############################################################################
pccd = ROOpCCD(lf, occ_model)
pccd_out = pccd(kin, ne, eri, olp, hf_output)
###############################################################################
# Transform Hamiltonian to MO basis
###############################################################################
mo_ints = transform_integrals(kin, ne, eri, hf_output.orb_a)
one = mo_ints.one[0]
two = mo_ints.two[0]
###############################################################################
# Write all integrals to a FCIDUMP file
###############################################################################
data = IOData(one=one, two=two, e_core=e_core, ms2=0, nelec=12)
data.to_file("all.FCIDUMP")
###############################################################################
# Get CAS Hamiltonian
###############################################################################
mo_ints_cas = split_core_active(one, two, ncore=2, nactive=8, e_core=e_core)
one_cas = mo_ints_cas.one
two_cas = mo_ints_cas.two
###############################################################################
# Write CAS integrals to a FCIDUMP file
###############################################################################
data = IOData(one=one_cas, two=two_cas, e_core=e_core, ms2=0, nelec=8)
data.to_file("cas.FCIDUMP")
