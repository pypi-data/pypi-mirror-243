#!/usr/bin/env python3

import numpy as np

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
from pybest.linalg import DenseLinalgFactory
from pybest.occ_model import AufbauOccModel
from pybest.orbital_utils import transform_integrals
from pybest.wrappers import RHF

###############################################################################
## Set up molecule, define basis set ##########################################
###############################################################################
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
## Construct the Hamiltonian ##################################################
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
## Do OO-pCCD optimization ####################################################
###############################################################################
oopccd = ROOpCCD(lf, occ_model)
oopccd_output = oopccd(kin, ne, eri, hf_output)

###############################################################################
## Calculate the exact orbital Hessian of pCCD ################################
###############################################################################
# transform integrals for restricted orbitals oopccd_.orb_a
t_ints = transform_integrals(kin, ne, eri, oopccd_output)

# transformed one-electron integrals: attribute 'one' (list)
(one,) = t_ints.one  # or: one = ti_.one[0]
# transformed two-electron integrals: attribute 'two' (list)
(two,) = t_ints.two  # or: two = ti_.two[0]

# calculate the exact orbital hessian of OOpCCD
hessian = oopccd.get_exact_hessian(one, two)

# diagonalize the exact orbital Hessian
eigv = np.linalg.eigvalsh(hessian)

print(eigv)
