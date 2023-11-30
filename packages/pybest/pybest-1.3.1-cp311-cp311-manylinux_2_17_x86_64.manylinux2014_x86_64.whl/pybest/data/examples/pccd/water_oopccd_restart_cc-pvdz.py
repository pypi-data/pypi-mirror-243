#!/usr/bin/env python3

from pybest import context
from pybest.gbasis import (
    compute_eri,
    compute_kinetic,
    compute_nuclear,
    get_gobasis,
)
from pybest.geminals import ROOpCCD
from pybest.linalg import DenseLinalgFactory
from pybest.occ_model import AufbauOccModel

# You need to execute `water_oopccd_cc-pvdz.py` first, before running
# this example script.


###############################################################################
## Set up molecule, define basis set ##########################################
###############################################################################
fn_xyz = context.get_fn("test/water.xyz")
obasis = get_gobasis("cc-pvdz", fn_xyz)
###############################################################################
## Define Occupation model, expansion coefficients and overlap ################
###############################################################################
lf = DenseLinalgFactory(obasis.nbasis)
occ_model = AufbauOccModel(obasis)
###############################################################################
## Construct Hamiltonian ######################################################
###############################################################################
kin = compute_kinetic(obasis)
ne = compute_nuclear(obasis)
eri = compute_eri(obasis)

###############################################################################
## Restart an OO-pCCD calculation from default restart file ###################
###############################################################################
oopccd = ROOpCCD(lf, occ_model)
oopccd_output = oopccd(
    kin, ne, eri, restart="pybest-results/checkpoint_pccd.h5"
)
