#!/usr/bin/env python3

from pybest.cc import RfpCCD, RfpCCSD
from pybest.context import context
from pybest.gbasis import (
    compute_cholesky_eri,
    compute_kinetic,
    compute_nuclear,
    compute_nuclear_repulsion,
    compute_overlap,
    get_gobasis,
)
from pybest.geminals import ROOpCCD
from pybest.linalg import CholeskyLinalgFactory
from pybest.localization import PipekMezey
from pybest.occ_model import AufbauOccModel
from pybest.part import get_mulliken_operators
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
lf = CholeskyLinalgFactory(obasis.nbasis)
occ_model = AufbauOccModel(obasis)
orb_a = lf.create_orbital(obasis.nbasis)
olp = compute_overlap(obasis)
###############################################################################
## Construct Hamiltonian ######################################################
###############################################################################
kin = compute_kinetic(obasis)
ne = compute_nuclear(obasis)
eri = compute_cholesky_eri(obasis, threshold=1e-8)
nr = compute_nuclear_repulsion(obasis)
###############################################################################
## Do a Hartree-Fock calculation ##############################################
###############################################################################
hf = RHF(lf, occ_model)
hf_output = hf(kin, ne, eri, nr, olp, orb_a)
###############################################################################
# Localize orbitals to improve pCCD convergence ###############################
###############################################################################
mulliken = get_mulliken_operators(obasis)
loc = PipekMezey(lf, occ_model, mulliken)
loc(orb_a, "occ")
loc(orb_a, "virt")
###############################################################################
# Do pCCD #####################################################################
###############################################################################
pccd = ROOpCCD(lf, occ_model)
pccd_output = pccd(hf_output, kin, ne, eri, e_core=nr)
###############################################################################
### Do pCCD-fpCCD calculation #################################################
###############################################################################
ccd = RfpCCD(lf, occ_model)
ccd_output = ccd(pccd_output, kin, ne, eri)
###############################################################################
### Do pCCD-fpCCSD calculation ################################################
###############################################################################
ccsd = RfpCCSD(lf, occ_model)
ccsd_output = ccsd(pccd_output, kin, ne, eri)
