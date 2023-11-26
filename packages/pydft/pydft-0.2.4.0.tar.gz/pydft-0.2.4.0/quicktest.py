import unittest
from pyqint import Molecule
from pydft import MoleculeBuilder, DFT
import numpy as np

class TestDFT(unittest.TestCase):
    """
    Perform a quick test to verify whether all DFT routines
    are properly working
    """

    def test_helium(self):
        """
        Test DFT calculation of Helium atom
        """
        mol_builder = MoleculeBuilder()
        mol = mol_builder.get_molecule('He')

        # construct dft object
        dft = DFT(mol, basis='sto3g', accuracy='normal', functional='pbe')
        energy = dft.scf()

        answer = -2.83013
        np.testing.assert_almost_equal(energy, answer, 4)

    def test_co(self):
        """
        Test DFT calculation of CO molecule
        """
        mol = Molecule()
        mol.add_atom('O', 0.,0.,0.5153398806, unit='angstrom')
        mol.add_atom('C', 0.,0.,-0.6871198408, unit='angstrom')

        # construct dft object
        dft = DFT(mol, basis='sto3g', accuracy='normal', functional='pbe')
        energy = dft.scf()

        answer = -111.6566307279118
        np.testing.assert_almost_equal(energy, answer, 4)
    
    def test_h2(self):
        """
        Test DFT calculation of CO molecule
        """
        mol_builder = MoleculeBuilder()
        mol = mol_builder.get_molecule('H2')

        # construct dft object
        dft = DFT(mol, basis='sto3g', accuracy='normal', functional='pbe')
        energy = dft.scf()

        answer = -1.1520709324298675
        np.testing.assert_almost_equal(energy, answer, 4)

if __name__ == '__main__':
    unittest.main()
