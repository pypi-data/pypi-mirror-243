#!/usr/bin/env python3

from pybest import context
from pybest.cc import RpCCDLCCD, RpCCDLCCSD
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
from pybest.orbital_entanglement import (
    OrbitalEntanglementRpCCD,
    OrbitalEntanglementRpCCDLCC,
)
from pybest.wrappers import RHF

###############################################################################
## Set up molecule, define basis set ##########################################
###############################################################################
# Use the XYZ file from PyBEST's test data directory.
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
hf_output = hf(kin, ne, er, external, olp, orb_a)

###############################################################################
## Do OO-pCCD optimization ####################################################
###############################################################################
pccd = ROOpCCD(lf, occ_model)
pccd_output = pccd(kin, ne, er, hf_output)

###############################################################################
## pCCD-LCCD calculation ######################################################
###############################################################################
lccd = RpCCDLCCD(lf, occ_model)
lccd_output = lccd(kin, ne, er, pccd_output, lambda_equations=True)

###############################################################################
## pCCD-LCCSD calculation ######################################################
###############################################################################
lccsd = RpCCDLCCSD(lf, occ_model)
lccsd_output = lccsd(kin, ne, er, pccd_output, lambda_equations=True)

###############################################################################
## Do orbital entanglement analysis for pCCD ###################################
###############################################################################
entanglement = OrbitalEntanglementRpCCD(lf, pccd_output)
entanglement()

###############################################################################
## Do orbital entanglement analysis for pCCD-LCCD ##############################
###############################################################################
entanglement = OrbitalEntanglementRpCCDLCC(lf, lccd_output)
entanglement()

###############################################################################
## Do orbital entanglement analysis for pCCD-LCCSD #############################
###############################################################################
entanglement = OrbitalEntanglementRpCCDLCC(lf, lccsd_output)
entanglement()
