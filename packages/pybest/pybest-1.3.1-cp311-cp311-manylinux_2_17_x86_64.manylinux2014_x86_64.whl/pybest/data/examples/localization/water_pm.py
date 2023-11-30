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
from pybest.localization import PipekMezey
from pybest.occ_model import AufbauOccModel
from pybest.part import get_mulliken_operators
from pybest.wrappers import RHF

###############################################################################
## Set up molecule, define basis set ##########################################
###############################################################################
# Use the XYZ file from PyBEST's test data directory.
fn_xyz = context.get_fn("test/water.xyz")
factory = get_gobasis("cc-pvdz", fn_xyz)
###############################################################################
## Define Occupation model, expansion coefficients and overlap ################
###############################################################################
lf = DenseLinalgFactory(factory.nbasis)
occ_model = AufbauOccModel(factory)
orb_a = lf.create_orbital(factory.nbasis)
olp = compute_overlap(factory)
###############################################################################
## Construct Hamiltonian ######################################################
###############################################################################
kin = compute_kinetic(factory)
ne = compute_nuclear(factory)
eri = compute_eri(factory)
external = compute_nuclear_repulsion(factory)
###############################################################################
## Do a Hartree-Fock calculation ##############################################
###############################################################################
hf = RHF(lf, occ_model)
hf_output = hf(kin, ne, eri, external, olp, orb_a)

###############################################################################
## Define Mulliken projectors #################################################
###############################################################################
mulliken = get_mulliken_operators(factory)
###############################################################################
## Pipek-Mezey localizaton ####################################################
###############################################################################
loc = PipekMezey(lf, occ_model, mulliken)
###############################################################################
## occupied block #############################################################
###############################################################################
loc(hf_output, "occ")
###############################################################################
## virtual block ##############################################################
###############################################################################
loc(hf_output, "virt")


###############################################################################
## dump Molden file; hf_output already contains the orb_a attribute ###########
###############################################################################
hf_output.to_file("water.molden")
