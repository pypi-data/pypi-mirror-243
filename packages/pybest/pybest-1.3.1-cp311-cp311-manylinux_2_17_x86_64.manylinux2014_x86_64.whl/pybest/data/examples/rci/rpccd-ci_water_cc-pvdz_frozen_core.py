#!/usr/bin/env python3

from pybest.ci import RpCCDCID, RpCCDCISD
from pybest.context import context
from pybest.gbasis import (
    compute_eri,
    compute_kinetic,
    compute_nuclear,
    compute_nuclear_repulsion,
    compute_overlap,
    get_gobasis,
)
from pybest.geminals import ROOpCCD
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
## Define occupation model, orbitals, and overlap #############################
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
er = compute_eri(obasis)
external = compute_nuclear_repulsion(obasis)

###############################################################################
## Do a Hartree-Fock calculation ##############################################
###############################################################################
hf = RHF(lf, occ_model)
hf_out = hf(kin, ne, er, external, olp, orb_a)

###############################################################################
## Do an OO-pCCD calculation ##################################################
###############################################################################
pccd = ROOpCCD(lf, occ_model)
pccd_out = pccd(kin, ne, er, hf_out)

###############################################################################
## Do RpCCD-CID calculation using Davidson diagonalization
###############################################################################
rcid = RpCCDCID(lf, occ_model)
rcid_out = rcid(kin, ne, er, pccd_out)

###############################################################################
## Do RpCCD-CISD calculation using Davidson diagonalization
###############################################################################
rcisd = RpCCDCISD(lf, occ_model)
rcisd_out = rcisd(kin, ne, er, pccd_out)
