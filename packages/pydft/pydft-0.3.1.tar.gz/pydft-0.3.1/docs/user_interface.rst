.. _user-interface:
.. index:: userinterface

User Interface
==============

.. note::
	:program:`PyDFT` leverages a lot of the functionality from
	`PyQInt <https://pyqint.imc-tue.nl/>`_, including the :code:`Molecule`
	and `MoleculeBuilder` classes.

Building molecules
------------------

Molecules can be built either directly using the :code:`Molecule` class or via
a :code:`MoleculeBuilder` convenience routine.

Molecule class
##############

To manually build a molecule, one first need to construct a :code:`Molecule`
object after which one or more atoms can be assigned to the molecule. If no
:code:`unit` is specified, it is assumed that all coordinates are given in
atomic units (i.e. Bohr units).

.. code:: python

	from pyqint import Molecule
	mol = Molecule('co')
	mol.add_atom('C', 0.0, 0.0, 0.0, unit='angstrom')
	mol.add_atom('O', 0.0, 0.0, 1.2, unit='angstrom')

MoleculeBuilder class
#####################

Alternatively, a Molecule can be constructed from the :code:`MoleculeBuilder` 
class which uses a name. For more information about the :code:`MoleculeBuilder` 
class, please consult the
`PyQInt documentation on the MoleculeBuilder class <https://pyqint.imc-tue.nl/user_interface.html#using-the-moleculebuilder-class>`_.

.. code:: python

	co = MoleculeBuilder().from_name("CO")

Performing DFT calculations
---------------------------

DFT calculations are handled by the :code:`DFT` class. Upon object initialization,
one needs to assign a molecule and specify the basis set as shown in the example
below. To execute the self-consistent field calculation, one uses the
:code:`scf` routine.

.. code:: python

	from pydft import DFT
	from pyqint import MoleculeBuilder

	co = MoleculeBuilder().from_name("CO")
	dft = DFT(co, basis='sto3g')
	en = dft.scf(1e-4)
	print("Total electronic energy: %f Ht" % en)

The :code:`DFT` class handles a number of additional arguments, as specified
below.

.. list-table:: List of additional arguments for the :code:`DFT` class
   :widths: 25 25 25
   :header-rows: 1

   * - Argument
     - Default value
     - Description
   * - :code:`accuracy`
     - :code:`normal`
     - Specifies the resolution of the angular and radial grids.
   * - :code:`functional`
     - :code:`svwn5`
     - Selects the type of exchange-correlation functional. Current options are
       :code:`svwn5` and :code:`pbe`.
   * - :code:`verbose`
     - :code:`False`
     - Whether the SCF algorithm should provide verbose output.

For example, the code below will initialize a :code:`DFT` object using the
PBE exchange-correlation functional and using verbose output.

.. code:: python

	from pydft import DFT
	from pyqint import MoleculeBuilder

	co = MoleculeBuilder().from_name("CO")
	dft = DFT(co, basis='sto3g', functional='pbe', verbose=True)
	en = dft.scf(1e-4)
	print("Total electronic energy: %f Ht" % en)

Executing the script above yields the following output::

	001 | Energy:    21.258092 | 0.0005 ms
	002 | Energy:  -107.716894 | 0.1110 ms
	003 | Energy:  -108.173705 | 0.0820 ms
	004 | Energy:  -109.920502 | 0.0815 ms
	005 | Energy:  -108.086105 | 0.0815 ms
	006 | Energy:  -111.489702 | 0.0805 ms
	007 | Energy:  -110.612255 | 0.0830 ms
	008 | Energy:  -110.430382 | 0.0810 ms
	009 | Energy:  -111.609381 | 0.0795 ms
	010 | Energy:  -111.654924 | 0.0830 ms
	011 | Energy:  -111.656379 | 0.0835 ms
	012 | Energy:  -111.656618 | 0.0825 ms
	013 | Energy:  -111.656604 | 0.0810 ms
	014 | Energy:  -111.656604 | 0.0815 ms
	015 | Energy:  -111.656604 | 0.0800 ms
	016 | Energy:  -111.656604 | 0.0800 ms
	Stopping SCF cycle, convergence reached.
	Total electronic energy: -111.656604 Ht

The :code:`scf` method of the :code:`DFT` class takes a single argument which
is the convergence tolerance. By default, this value is set to :code:`1e-5`.

Analyzing the Becke grid
========================

All numerical integrations are performed by means of Gauss-Chebychev and Lebedev
quadrature using the Becke grid. It is possible to produce a contour plot of
the fuzzy cells on a plane. An example is provided below.

.. code:: python

	from pydft import MolecularGrid
	from pyqint import MoleculeBuilder
	import numpy as np
	import matplotlib.pyplot as plt

	# construct molecule
	mol = MoleculeBuilder().from_name('benzene')
	cgfs, atoms = mol.build_basis('sto3g')

	# construct molecular grid
	molgrid = MolecularGrid(atoms, cgfs)

	# produce grid of sampling points to calculate the atomic
	# weight coefficients for
	N = 150
	sz = 8
	x = np.linspace(-sz,sz,N)
	xv,yv = np.meshgrid(x,x)
	points = np.array([[x,y,0] for x,y in zip(xv.flatten(),yv.flatten())])

	# calculate the atomic weights
	mweights = molgrid.calculate_weights_at_points(points, k=3)

	# plot the atomic weights
	plt.figure(dpi=144)
	plt.imshow(np.max(mweights,axis=0).reshape((N,N)),
	           extent=(-sz,sz,-sz,sz), interpolation='bicubic')
	plt.xlabel('x [a.u.]')
	plt.ylabel('y [a.u.]')
	plt.colorbar()
	plt.grid(linestyle='--', color='black', alpha=0.5)

	# add the atoms to the plot
	r = np.zeros((len(atoms), 3))
	for i,at in enumerate(atoms):
	    r[i] = at[0]
	plt.scatter(r[0:6,0], r[0:6,1], s=50.0, color='grey', edgecolor='black')
	plt.scatter(r[6:12,0], r[6:12,1], s=50.0, color='white', edgecolor='black')

	plt.tight_layout()

.. image:: _static/img/user_interface/becke_fuzzy_grid_benzene.png

.. note::

	Producing such a contour plot is only meaningful for planar molecules such
	as benzene. For more complex molecules such as methane, it is rather
	difficult to make sense of the fuzzy cells upon projection on a plane.