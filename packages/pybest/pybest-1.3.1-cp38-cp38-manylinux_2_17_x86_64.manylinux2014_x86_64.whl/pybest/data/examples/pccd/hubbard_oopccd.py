#!/usr/bin/env python3

from pybest.geminals import ROOpCCD
from pybest.linalg import DenseLinalgFactory
from pybest.modelhamiltonians import Hubbard
from pybest.occ_model import AufbauOccModel
from pybest.wrappers import RHF

###############################################################################
## Define Occupation model, expansion coefficients and overlap ################
###############################################################################
lf = DenseLinalgFactory(6)
occ_model = AufbauOccModel(lf, nel=6)
orb_a = lf.create_orbital()
###############################################################################
## Initialize an instance of the Hubbard class ################################
###############################################################################
modelham = Hubbard(lf, pbc=True)
olp = modelham.compute_overlap()
###############################################################################
# t-param, t = -1 #############################################################
###############################################################################
kin = modelham.compute_one_body(-1)
###############################################################################
# U-param, U = 2 ##############################################################
###############################################################################
two = modelham.compute_two_body(1)

###############################################################################
## Do a Hartree-Fock calculation ##############################################
###############################################################################
hf = RHF(lf, occ_model)
hf_output = hf(kin, two, 0.0, orb_a, olp)

###############################################################################
## Do OO-pCCD optimization ####################################################
###############################################################################
oopccd = ROOpCCD(lf, occ_model)
oopccd_output = oopccd(kin, two, hf_output)
