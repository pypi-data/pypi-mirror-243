#!/usr/bin/env python3

from pybest.cc import RCCD, RCCSD
from pybest.context import context
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
occ_model = AufbauOccModel(obasis)
orb_a = lf.create_orbital(obasis.nbasis)
olp = compute_overlap(obasis)
###############################################################################
## Construct Hamiltonian ######################################################
###############################################################################
kin = compute_kinetic(obasis)
ne = compute_nuclear(obasis)
eri = compute_eri(obasis)
nr = compute_nuclear_repulsion(obasis)
###############################################################################
## Do a Hartree-Fock calculation ##############################################
###############################################################################
hf = RHF(lf, occ_model)
hf_output = hf(kin, ne, eri, nr, olp, orb_a)
###############################################################################
### Do RHF-CCD calculation ####################################################
###############################################################################
ccd = RCCD(lf, occ_model)
ccd_output = ccd(kin, ne, eri, hf_output)
###############################################################################
### Do RHF-CCSD calculation ###################################################
###############################################################################
ccsd = RCCSD(lf, occ_model)
ccsd_output = ccsd(kin, ne, eri, hf_output)
