#!/usr/bin/env python3

from pybest.ci import RCID, RCIS, RCISD
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
er = compute_eri(obasis)
external = compute_nuclear_repulsion(obasis)

###############################################################################
## Do a Hartree-Fock calculation ##############################################
###############################################################################
hf = RHF(lf, occ_model)
hf_out = hf(kin, ne, er, external, olp, orb_a)

###############################################################################
## Do RHF-CIS calculation using Davidson diagonalization
###############################################################################
rcis = RCIS(lf, occ_model)
rcis_out = rcis(kin, ne, er, hf_out)
###############################################################################
## Do RHF-CID calculation using Davidson diagonalization
###############################################################################
rcid = RCID(lf, occ_model)
rcid_out = rcid(kin, ne, er, hf_out)
###############################################################################
## Do RHF-CISD calculation using Davidson diagonalization
###############################################################################
rcisd = RCISD(lf, occ_model)
rcisd_out = rcisd(kin, ne, er, hf_out)
###############################################################################
## Do RHF-CISD calculation for the ground state and 4 excited states
###############################################################################
rcisd = RCISD(lf, occ_model)
rcisd_out = rcisd(kin, ne, er, hf_out, nroot=5)
###############################################################################
## Do RHF-CIS calculation using SD representation
###############################################################################
rcis = RCIS(lf, occ_model, csf=False)
rcis_out = rcis(kin, ne, er, hf_out)
###############################################################################
## Do RHF-CID calculation using SD representation
###############################################################################
rcid = RCID(lf, occ_model, csf=False)
rcid_out = rcid(kin, ne, er, hf_out)
###############################################################################
## Do RHF-CISD calculation using SD representation
###############################################################################
rcisd = RCISD(lf, occ_model, csf=False)
rcisd_out = rcisd(kin, ne, er, hf_out)
