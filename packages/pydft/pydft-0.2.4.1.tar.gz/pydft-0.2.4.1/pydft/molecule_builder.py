import os
from pyqint import Molecule

class MoleculeBuilder:
    """
    Class that handles loading of template molecules
    """
    def __init__(self):
        __molecules = ['He']

    def get_molecule(self, molname):
        """
        Read a molecule and return it
        """
        fname = os.path.join(os.path.dirname(__file__), 'molecules', molname.lower() + '.xyz')
        with open(fname, 'r') as f:
            lines = f.readlines()
            
            nratoms = int(lines[0].strip())

            mol = Molecule(molname)
            for line in lines[2:2+nratoms]:
                pieces = line.split()
                mol.add_atom(pieces[0], float(pieces[1]), float(pieces[2]), float(pieces[3]), unit='angstrom')

            return mol