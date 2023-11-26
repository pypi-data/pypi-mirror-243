# -*- coding: utf-8 -*-

from .moleculargrid import MolecularGrid
from pyqint import PyQInt
import numpy as np
import time
from packaging import version
from copy import deepcopy

# couple of hardcoded variables for the DIIS algorithm
SUBSPACE_LENGTH = 3
SUBSPACE_START = 4

class DFT():
    def __init__(self, mol, 
                       basis='sto3g', 
                       accuracy='normal',
                       functional='svwn5',
                       verbose=False):
        """
        Build dft class
        """    
        self.__mol = mol
        self.__integrator = PyQInt()
        self.__basis = basis
        self.__verbose = verbose
        self.__time_stats = {}
        self.__itermax = 100
        self.__alpha = 0.9 # linear mixing constant
        self.__functional = functional

    def get_matrices(self):
        """
        Get the matrices used in the SCF procedure
        """
        matrices = {
            'S' : self.__S,
            'T' : self.__T,
            'V' : self.__V,
            'C' : self.__C,
            'J' : self.__J,
            'P' : self.__P,
            'XC' : self.__XC,
            'F' : self.__F
        }
        
        return matrices
    
    def get_molgrid_copy(self):
        """
        Get a copy of the underlying molgrid object
        """
        return deepcopy(self.__molgrid)
    
    def get_density_at_points(self, spoints):
        """
        Get the electron density at points
        """
        return self.__molgrid.get_density_at_points(spoints, self.__P)
    
    def get_gradient_at_points(self, spoints):
        """
        Get the electron density at points
        """
        return self.__molgrid.get_gradient_at_points(spoints, self.__P)
    
    def scf(self, tol=1e-5):
        """
        Perform the self-consistent field procedure
        """
        # construct stagnant matrices
        self.__setup()
        
        # create empty P matrix as initial guess
        self.__P = np.zeros_like(self.__S)

        # start SCF iterative procedure
        nitfin = 0
        for niter in range(0, self.__itermax):
            start = time.time()
            energy = self.__iterate(niter, 
                                    giis=True if nitfin == 0 else False,
                                    mix=0.9)
            self.__energies.append(energy)
            stop = time.time()
            itertime = stop - start
            self.__time_stats['iterations'].append(itertime)
            
            if self.__verbose:
                print('%03i | Energy: %12.6f | %0.4f ms' % (niter+1, energy, itertime))
            
            if niter > 2:
                ediff = np.abs(energy - self.__energies[-2])
                if ediff < 1e-6:
                    # terminate giis self-convergence and continue with mixing
                    nitfin += 1
                    
                    if nitfin < 3:
                        continue
                    
                    # terminate self-convergence cycle
                    if self.__verbose:
                        print("Stopping SCF cycle, convergence reached.")
                    break

        return energy
    
    def get_construction_times(self):
        """
        Return construct times dictionary from MolecularGrid to get insights
        into the time to construct particular properties
        """
        return self.__molgrid.construct_times
    
    def __iterate(self, niter, giis=True, mix=0.9):
        """
        Perform single-step iteration
        """
        # calculate J and XC matrices based on the current electron
        # density estimate as captured in the density matrix P
        if niter > SUBSPACE_START and giis:
            try:
                diis_coeff = self.__calculate_diis_coefficients(self.__evs_diis)
                self.__F = self.__extrapolate_fock_from_diis_coefficients(self.__fmats_diis, diis_coeff)
                self.__Fprime = self.__X.transpose().dot(self.__F).dot(self.__X)
                self.__e, self.__Cprime = np.linalg.eigh(self.__Fprime)
                self.__C = self.__X.dot(self.__Cprime)
                N = len(self.__cgfs)
                self.__P = np.zeros_like(self.__S)
                nelec = np.sum([nucleus[1] for nucleus in self.__nuclei])
                for i in range(N):
                    for j in range(N):
                        for k in range(0,int(nelec/2)):
                            self.__P[i,j] += 2.0 * self.__C[i,k] * self.__C[j,k]
            except np.linalg.LinAlgError: # set giis to False if not working
                giis = False
        
        # calculate J and XC matrices based on the current electron
        # density estimate as captured in the density matrix P
        if np.any(self.__P):
            self.__molgrid.build_density(self.__P, normalize=True)
            self.__J = self.__calculate_J()
            self.__XC, self.__Exc = self.__calculate_XC()
        
        # print('h', self.__H)
        # print('J', self.__J/2)
        # print('XC', self.__XC)
        
        # calculate Fock matrix
        self.__F = self.__H + self.__J + self.__XC
        
        # print('F', self.__F)
        # print('enuc', self.__enuc)
        # print('P', self.__P)
        
        # perform unitary transformation on Fock matrix
        self.__Fprime = self.__X.transpose().dot(self.__F).dot(self.__X)
        
        # diagonalize Fock matrix
        self.__e, self.__Cprime = np.linalg.eigh(self.__Fprime)
        
        # back-transform
        self.__C = self.__X.dot(self.__Cprime)
        
        # calculate total electronic energy
        M = self.__T + self.__V + 0.5 * self.__J
        
        # print('one', np.einsum('ji,ij', self.__P, self.__T + self.__V))
        # print('J', 0.5 * np.einsum('ji,ij', self.__P, self.__J))
        # print('XC', np.einsum('ji,ij', self.__P, self.__XC))
        # print('XC', self.__Exc)
        
        energy = np.einsum('ji,ij', self.__P, M) + self.__Exc + self.__enuc
        
        # for the first few iterations, build a new density
        # matrix from the coefficients, else, resort to the DIIS
        # algorithm
        if niter <= SUBSPACE_START or not giis:
            N = len(self.__cgfs)
            P = np.zeros_like(self.__S)
            nelec = np.sum([nucleus[1] for nucleus in self.__nuclei])
            for i in range(0,N):
                for j in range(0,N):
                    for k in range(0,int(nelec/2)):
                        P[i,j] += 2.0 * self.__C[i,k] * self.__C[j,k]
            self.__P = (1.0 - mix) * self.__P + mix * P # use linear mixing

        # calculate DIIS coefficients
        e = (self.__F.dot(self.__P.dot(self.__S)) - \
             self.__S.dot(self.__P.dot(self.__F))).flatten()   # calculate error vector
        self.__enorm = np.linalg.norm(e)                       # store error vector norm
        self.__fmats_diis.append(self.__F)                     # add Fock matrix to list
        self.__pmat_diis.append(self.__P)                      # add density matrix to list
        self.__evs_diis.append(e)

        # prune size of the old Fock, density and error vector lists
        # only SUBSPACE_LENGTH iterations are used to guess the new
        # solution
        if len(self.__fmats_diis) > SUBSPACE_LENGTH:
            self.__fmats_diis = self.__fmats_diis[-SUBSPACE_LENGTH:]
            self.__pmat_diis = self.__pmat_diis[-SUBSPACE_LENGTH:]
            self.__evs_diis = self.__evs_diis[-SUBSPACE_LENGTH:]
        
        return energy
    
    def __setup(self):
        """
        Construct the bare classes and matrices necessary to start the
        self-consistent-field procedure
        """
        # construct basis functions and nuclei
        self.__cgfs, self.__nuclei = self.__mol.build_basis(self.__basis)
        
        # build molecular grid
        self.__molgrid = MolecularGrid(self.__nuclei, 
                                       self.__cgfs, 
                                       nspheres=32, 
                                       nangpts='110', 
                                       lmax=8,
                                       functional=self.__functional)
        self.__molgrid.initialize() # molecular grid uses late initialization

        # build one-electron matrices; because these matrices are Hermetian,
        # we only have to evaluate the upper half and then simply copy the
        # upper half to the lower half
        N = len(self.__cgfs)
        self.__S = np.zeros((N,N))
        self.__T = np.zeros_like(self.__S)
        self.__V = np.zeros_like(self.__S)
        for j in range(0,N):
            cgf1 = self.__cgfs[j]
            for i in range(j,N):
                cgf2 = self.__cgfs[i]
                self.__S[j,i] = self.__integrator.overlap(cgf1, cgf2)
                self.__T[j,i] = self.__integrator.kinetic(cgf1, cgf2)
                
                # in principle, the nuclear attraction could also be directly
                # obtained from the molecular grid, but analytical evaluation
                # is faster
                for k,nucleus in enumerate(self.__nuclei):
                    vjik = self.__integrator.nuclear(cgf1, cgf2, nucleus[0], nucleus[1])
                    self.__V[j,i] += vjik
                
                # copy upper triangle elements to lower triangle
                if i != j:
                    self.__S[i,j] = self.__S[j,i]
                    self.__T[i,j] = self.__T[j,i]
                    self.__V[i,j] = self.__V[j,i]
        
        # build single-electron matrix
        self.__H = self.__T + self.__V
        
        # diagonalize S and use it to construct the unitary transformation 
        # matrix that orthonormalizes the basis set
        s, U = np.linalg.eigh(self.__S)
        self.__X = U.dot(np.diag(1.0/np.sqrt(s)))
        
        # create empty matrices for the coulomb and exchange-correlation
        # energies
        self.__J = np.zeros_like(self.__S)
        self.__XC = np.zeros_like(self.__S)
        self.__Exc = 0.0
        
        # create zero density matrix
        self.__P = np.zeros_like(self.__S)
        
        # calculate nuclear repulsion
        self.__enuc = 0.0
        for i in range(0, len(self.__nuclei)):
            for j in range(i+1, len(self.__nuclei)):
                r = np.linalg.norm(self.__nuclei[i][0] - self.__nuclei[j][0])
                self.__enuc += self.__nuclei[i][1] * self.__nuclei[j][1] / r
        
        # build containers to store per-iteration data
        self.__energies = []
        self.__time_stats['iterations'] = []
        self.__fmats_diis = []
        self.__pmat_diis = []
        self.__evs_diis = []
        
    def __calculate_J(self):
        """
        Calculate the coulombic interaction matrix using the
        molecular grid
        """
        return self.__molgrid.calculate_coulombic_matrix()
    
    def __calculate_XC(self):
        """
        Calculate the exchange-correlation matrix and the
        exchange-correlation energy
        """
        X, ex = self.__molgrid.calculate_exchange()
        C, ec = self.__molgrid.calculate_correlation()
        
        return X+C, ex + ec
               
    def __calculate_diis_coefficients(self, evs_diis):
        """
        Calculate the DIIS coefficients
        """
        B = np.zeros((len(evs_diis)+1, len(evs_diis)+1))
        B[-1,:] = -1
        B[:,-1] = -1
        B[-1,-1]=  0

        rhs = np.zeros((len(evs_diis)+1, 1))
        rhs[-1,-1] = -1

        for i in range(len(evs_diis)):
            for j in range(i+1):
                B[i,j] = np.dot(evs_diis[i].transpose(), evs_diis[j])
                B[j,i] = B[i,j]

        *diis_coeff, _ = np.linalg.solve(B,rhs)

        return diis_coeff

    def __extrapolate_fock_from_diis_coefficients(self, fmats_diis, diis_coeff):
        """
        Extrapolate the Fock matrix from the DIIS coefficients
        """
        norbs = fmats_diis[-1].shape[0]
        fguess = np.zeros((norbs,norbs))

        for i in range(len(fmats_diis)):
            fguess += fmats_diis[i]*diis_coeff[i]

        return fguess
        