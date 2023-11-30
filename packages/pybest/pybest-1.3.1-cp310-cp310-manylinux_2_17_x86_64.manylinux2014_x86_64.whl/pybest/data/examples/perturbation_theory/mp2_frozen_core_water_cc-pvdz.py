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
from pybest.linalg import DenseLinalgFactory
from pybest.occ_model import AufbauOccModel
from pybest.pt import RMP2
from pybest.wrappers import RHF

###############################################################################
## Set up molecule, define basis set ##########################################
###############################################################################
# get the XYZ file from PyBEST's test data directory
fn_xyz = context.get_fn("test/water.xyz")
obasis = get_gobasis("cc-pvdz", fn_xyz)
###############################################################################
## Define Occupation model, expansion coefficients and overlap ################
###############################################################################
lf = DenseLinalgFactory(obasis.nbasis)
occ_model = AufbauOccModel(obasis, ncore=1)
orb_a = lf.create_orbital(obasis.nbasis)
olp = compute_overlap(obasis)
###############################################################################
## Construct Hamiltonian ######################################################
###############################################################################
kin = compute_kinetic(obasis)
ne = compute_nuclear(obasis)
eri = compute_eri(obasis)
external = compute_nuclear_repulsion(obasis)

###############################################################################
## Do a Hartree-Fock calculation ##############################################
###############################################################################
hf = RHF(lf, occ_model)
hf_output = hf(kin, ne, eri, external, olp, orb_a)

###############################################################################
## Do RMP2 calculation with 1 frozen core orbital #############################
###############################################################################
mp2 = RMP2(lf, occ_model)
mp2_output = mp2(kin, ne, eri, hf_output)

###############################################################################
## Do RMP2 calculation with single excitations included #######################
###############################################################################
mp2 = RMP2(lf, occ_model)
mp2_output = mp2(kin, ne, eri, hf_output, singles=True)

###############################################################################
## Do RMP2 calculation AND determine natural orbitals #########################
###############################################################################
mp2 = RMP2(lf, occ_model)
mp2_output = mp2(kin, ne, eri, hf_output, natorb=True)

###############################################################################
## Do RMP2 calculation AND determine natural orbitals INCLUDING ###############
## orbital relaxation contributions ###########################################
###############################################################################
mp2 = RMP2(lf, occ_model)
mp2_output = mp2(kin, ne, eri, hf_output, natorb=True, relaxation=True)
