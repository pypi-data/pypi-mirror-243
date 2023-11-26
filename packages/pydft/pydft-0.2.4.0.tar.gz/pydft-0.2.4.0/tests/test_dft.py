import unittest
from pydft import MoleculeBuilder, DFT
import numpy as np

class TestDFT(unittest.TestCase):

    def test_helium(self):
        """
        Test DFT calculation of Helium atom
        """
        mol_builder = MoleculeBuilder()
        mol = mol_builder.get_molecule('He')

        # construct dft object
        dft = DFT(mol, basis='sto3g', accuracy='normal')
        energy = dft.scf()

        answer = -2.809567
        np.testing.assert_almost_equal(energy, answer, 4)

    def test_h2o(self):
        """
        Test DFT calculation of water molecule
        """
        mol_builder = MoleculeBuilder()
        mol = mol_builder.get_molecule('H2O')

        # construct dft object
        dft = DFT(mol, basis='sto3g', accuracy='normal')
        energy = dft.scf()

        answer = -74.93912092888502
        np.testing.assert_almost_equal(energy, answer, 4)

    def test_co(self):
        """
        Test DFT calculation of CO molecule
        """
        mol_builder = MoleculeBuilder()
        mol = mol_builder.get_molecule('CO')

        # construct dft object
        dft = DFT(mol, basis='sto3g', accuracy='normal')
        energy = dft.scf()

        answer = -111.14709591293297
        np.testing.assert_almost_equal(energy, answer, 4)
        
    def test_bf3(self):
        """
        Test DFT calculation of BF3 molecule
        """
        mol_builder = MoleculeBuilder()
        mol = mol_builder.get_molecule('bf3')

        # construct dft object
        dft = DFT(mol, basis='sto3g', accuracy='normal')
        energy = dft.scf()

        answer = -318.1137612672585
        np.testing.assert_almost_equal(energy, answer, 4)
    
    def test_ch4(self):
        """
        Test DFT calculation of methane molecule
        """
        mol_builder = MoleculeBuilder()
        mol = mol_builder.get_molecule('ch4')

        # construct dft object
        dft = DFT(mol, basis='sto3g', accuracy='normal')
        energy = dft.scf()

        answer = -39.800956828327074
        np.testing.assert_almost_equal(energy, answer, 4)
    
    def test_co2(self):
        """
        Test DFT calculation of co2 molecule
        """
        mol_builder = MoleculeBuilder()
        mol = mol_builder.get_molecule('co2')

        # construct dft object
        dft = DFT(mol, basis='sto3g', accuracy='normal')
        energy = dft.scf()

        answer = -185.0130242213974
        np.testing.assert_almost_equal(energy, answer, 4)
    
    def test_ethylene(self):
        """
        Test DFT calculation of an ethylene molecule
        """
        mol_builder = MoleculeBuilder()
        mol = mol_builder.get_molecule('ethylene')

        # construct dft object
        dft = DFT(mol, basis='sto3g', accuracy='normal')
        energy = dft.scf()

        answer = -77.16181445629252
        np.testing.assert_almost_equal(energy, answer, 4)
        
    def test_h2(self):
        """
        Test DFT calculation of hydrogen molecule
        """
        mol_builder = MoleculeBuilder()
        mol = mol_builder.get_molecule('h2')

        # construct dft object
        dft = DFT(mol, basis='sto3g', accuracy='normal')
        energy = dft.scf()

        answer = -1.1570136
        np.testing.assert_almost_equal(energy, answer, 4)
        
    def test_lih(self):
        """
        Test DFT calculation of LiH molecule
        """
        mol_builder = MoleculeBuilder()
        mol = mol_builder.get_molecule('lih')

        # construct dft object
        dft = DFT(mol, basis='sto3g', accuracy='normal')
        energy = dft.scf()

        answer = -7.865538865354658
        np.testing.assert_almost_equal(energy, answer, 4)
        
    def test_nh3(self):
        """
        Test DFT calculation of NH3 molecule
        """
        mol_builder = MoleculeBuilder()
        mol = mol_builder.get_molecule('nh3')

        # construct dft object
        dft = DFT(mol, basis='sto3g', accuracy='normal')
        energy = dft.scf()

        answer = -58.43021582243169
        np.testing.assert_almost_equal(energy, answer, 4)
    
    # def test_benzene(self):
    #     """
    #     Test DFT calculation of benzene molecule
    #     """
    #     mol_builder = MoleculeBuilder()
    #     mol = mol_builder.get_molecule('benzene')

    #     # construct dft object
    #     dft = DFT(mol, basis='sto3g', accuracy='normal')
    #     energy = dft.scf()

    #     answer = -228.0695756259556
    #     np.testing.assert_almost_equal(energy, answer, 4)

if __name__ == '__main__':
    unittest.main()
