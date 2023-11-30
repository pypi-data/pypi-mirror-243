#!/usr/bin/env python3

from pybest import context
from pybest.geminals import ROOpCCD
from pybest.io import IOData
from pybest.occ_model import AufbauOccModel

# Read Hamiltonian from some FCIDUMP file
# ---------------------------------------
fcidump = context.get_fn("test/water.FCIDUMP")
mol = IOData.from_file(fcidump)

# Define occupation model (using lf instance and total number of electrons)
# -------------------------------------------------------------------------
occ_model = AufbauOccModel(mol.lf, nel=10)


# Do OOpCCD optimization
# ----------------------
oopccd = ROOpCCD(mol.lf, occ_model)
oopccd_output = oopccd(mol.one, mol.two, mol)
