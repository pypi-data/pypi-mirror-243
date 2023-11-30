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
from pybest.geminals import ROOpCCD
from pybest.ip_eom import RIPpCCD
from pybest.linalg import DenseLinalgFactory
from pybest.occ_model import AufbauOccModel
from pybest.wrappers import RHF

###############################################################################
## Set up molecule, define basis set ##########################################
###############################################################################
# get the XYZ file from PyBEST's test data directory
fn_xyz = context.get_fn("test/no.xyz")
obasis = get_gobasis("cc-pvdz", fn_xyz)

###############################################################################
## Define Occupation model, expansion coefficients and overlap ################
###############################################################################
lf = DenseLinalgFactory(obasis.nbasis)
orb_a = lf.create_orbital(obasis.nbasis)
olp = compute_overlap(obasis)
# we need to add 1 additional electron
occ_model = AufbauOccModel(obasis, charge=-1)

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
## Do OO-pCCD optimization ####################################################
###############################################################################
oopccd = ROOpCCD(lf, occ_model)
oopccd_output = oopccd(kin, ne, eri, hf_output)

###############################################################################
### Do RIP-pCCD calculation for 1 unpaired electron ###########################
###############################################################################
ip = RIPpCCD(lf, occ_model, alpha=1)
ip_output = ip(kin, ne, eri, oopccd_output, nroot=4)

###############################################################################
### Do RIP-pCCD calculation for 3 unpaired electrons ##########################
###############################################################################
ip = RIPpCCD(lf, occ_model, alpha=3)
ip_output = ip(kin, ne, eri, oopccd_output, nroot=4)
