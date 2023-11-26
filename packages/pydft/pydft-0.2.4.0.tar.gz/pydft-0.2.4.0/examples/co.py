# -*- coding: utf-8 -*-
from pydft import MoleculeBuilder,DFT

#
# Example: Calculate total electronic energy for CO using standard
#          settings.
#

CO = MoleculeBuilder().get_molecule("CO")
dft = DFT(CO, basis='sto3g')
en = dft.scf(1e-4)
print("Total electronic energy: %f Ht" % en)