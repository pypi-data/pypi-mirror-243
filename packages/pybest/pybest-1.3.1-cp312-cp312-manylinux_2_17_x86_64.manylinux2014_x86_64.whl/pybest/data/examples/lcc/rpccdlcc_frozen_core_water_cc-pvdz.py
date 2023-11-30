#!/usr/bin/env python3

from pybest.cc import RpCCDLCCD, RpCCDLCCSD
from pybest.context import context
from pybest.gbasis import (
    compute_eri,
    compute_kinetic,
    compute_nuclear,
    compute_nuclear_repulsion,
    compute_overlap,
    get_gobasis,
)
from pybest.geminals import RpCCD
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
## Do OO-pCCD optimization and 1 frozen core orbital (stored in occ_model) ####
###############################################################################
pccd = RpCCD(lf, occ_model)
pccd_output = pccd(kin, ne, eri, hf_output)

###############################################################################
### Do RpCCD-LCCSD calculation and 1 frozen core orbital (stored in occ_model)
###############################################################################
lccd = RpCCDLCCD(lf, occ_model)
lccd_output = lccd(kin, ne, eri, pccd_output)

###############################################################################
### Do RpCCD-LCCSD calculation and 1 frozen core orbital (stored in occ_model)
###############################################################################
lccsd = RpCCDLCCSD(lf, occ_model)
lccsd_output = lccsd(kin, ne, eri, pccd_output)
