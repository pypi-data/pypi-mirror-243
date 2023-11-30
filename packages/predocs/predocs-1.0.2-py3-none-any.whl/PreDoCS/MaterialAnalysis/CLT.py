"""
This module is an implementation of the classical laminate theory (CLT) with an extension for transverse shear stiffness.
Further information are available at [Jones1999]_ and [Schürmann2007]_.

The laminate is build of plys of orthotropic material stacked together.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
import numpy as np
from math import sin, cos

from PreDoCS.util.Logging import get_module_logger
log = get_module_logger(__name__)


class Ply(object):
    """
    This class represents an orthoropic ply. The ply is assumed as homogenous and its mechanical behaviour can be described
    by nine independent constants: three elastic moduli, three shear moduli and three Poisson's ratios.
    The ply-coordinate-system is the 1-2-3-coordinate system. The 3-direction is the thickness direction of the ply,
    the 1- and 2-directions are the orthotropic axis. Further information at [Jones1999]_, pp. 63.
    The assumption of zero stress in thickness direction is made, see [Jones1999]_, pp. 70.
    The stiffness matrix is splitted in two parts: the first part for the CLT (disk load only) and the second part for transverse shear stiffness.
    
    Attributes
    ----------
    _name: str
        Name of the ply.
    _density: float
        Mass density of the ply.
    _Q_c: numpy.ndarray
        Disk stiffness matrix of the ply.
    _Q_t: numpy.ndarray
        Transverse shear stiffness matrix of the ply.
    """
    def __init__(self, name, density, Q_c, Q_t):
        """
        Constructor.
        
        Parameters
        ----------
        name: str
            Name of the ply.
        density: float
            Mass density of the ply.
        Q_c: numpy.ndarray
            Disk stiffness matrix of the ply.
        Q_t: numpy.ndarray
            Transverse shear stiffness matrix of the ply.
        """
        self._name = name
        self._density = density
        self._Q_c = Q_c
        self._Q_t = Q_t
    
    @staticmethod
    def from_engineering_constants_orthotropic_for_becas(name, density, E1, E2, E3, nu12, nu13, nu23, G12, G31, G23):
        """
        Creates ply from given engineering constants of a orthotropic material.
        The assumption of zero stress in thickness direction is made, see [Jones1999]_, pp. 70.
        Additionally saves the engineering constants for the BECAS calculations to the object.
        
        Parameters
        ----------
        name: str
            Name of the ply.
        density: float
            Mass density of the ply.
        E1: float
            Elastic modulus in 1-direction.
        E2: float
            Elastic modulus in 2-direction.
        E3: float
            Elastic modulus in 3-direction.
        nu12: float
            Poisson's ratio (extension-extension coupling coefficient), transverse extension in 2-direction for an axial extension in 1-direction.
        nu13: float
            Poisson's ratio (extension-extension coupling coefficient), transverse extension in 3-direction for an axial extension in 1-direction.
        nu23: float
            Poisson's ratio (extension-extension coupling coefficient), transverse extension in 3-direction for an axial extension in 2-direction.
        G12: float
            Shear modulus in the 1-2-plane.
        G31: float
            Shear modulus in the 3-1-plane.
        G23: float
            Shear modulus in the 2-3-plane.
        """
        ply = Ply.from_engineering_constants_orthotropic(name, density, E1, E2, nu12, G12, G31, G23)
        ply.E1 = E1
        ply.E2 = E2
        ply.E3 = E3
        ply.nu12 = nu12
        ply.nu13 = nu13
        ply.nu23 = nu23
        ply.G12 = G12
        ply.G31 = G31
        ply.G23 = G23
        return ply
    
    @staticmethod
    def from_engineering_constants_transverse_isotropic_for_becas(name, density, E1, E2, nu12, nu22, G21):
        """
        Creates ply from given engineering constants of a transverse isotropic material.
        The assumption of zero stress in thickness direction is made, see [Jones1999]_, pp. 70.
        Additionally saves the engineering constants for the BECAS calculations to the object.
        
        Parameters
        ----------
        name: str
            Name of the ply.
        density: float
            Mass density of the ply.
        E1: float
            Elastic modulus in 1-direction.
        E2: float
            Elastic modulus normal to the 1-direction.
        nu12: float
            Major Poisson's ratio (extension-extension coupling coefficient), transverse extension normal to 1-direction for an axial extension in 1-direction.
        nu22: float
            Poisson's ratio (extension-extension coupling coefficient), transverse extension normal to the 1-direction for an axial extension normal to the 1-direction.
        G21: float
            Shear modulus in a plane containing the 1-axis.
        density: float
            Mass density of the ply.
        """
        E3 = E2
        nu13 = nu12
        nu23 = nu22
        G22 = E2/(2*(1+nu22))
        G23 = G22
        G12 = G21
        G31 = G21
        
        ply = Ply.from_engineering_constants_transverse_isotropic(name, density, E1, E2, nu12, nu22, G21)
        ply.E1 = E1
        ply.E2 = E2
        ply.E3 = E3
        ply.nu12 = nu12
        ply.nu13 = nu13
        ply.nu23 = nu23
        ply.G12 = G12
        ply.G31 = G31
        ply.G23 = G23
        return ply
    
    @staticmethod
    def from_engineering_constants_orthotropic(name, density, E1, E2, nu12, G12, G31, G23):
        """
        Creates ply from given engineering constants of a orthotropic material.
        The assumption of zero stress in thickness direction is made, see [Jones1999]_, pp. 70.
        
        Parameters
        ----------
        name: str
            Name of the ply.
        density: float
            Mass density of the ply.
        E1: float
            Elastic modulus in 1-direction.
        E2: float
            Elastic modulus in 2-direction.
        nu12: float
            Poisson's ratio (extension-extension coupling coefficient), transverse extension in 2-direction for an axial extension in 1-direction.
        G12: float
            Shear modulus in the 1-2-plane.
        G31: float
            Shear modulus in the 3-1-plane.
        G23: float
            Shear modulus in the 2-3-plane.
        """
        Q11 = -E1**2/(E2*nu12**2 - E1)
        Q22 = -E1*E2/(E2*nu12**2 - E1)
        Q12 = -E1*E2*nu12/(E2*nu12**2 - E1)
        Q44 = G23
        Q55 = G31
        Q66 = G12
        
        Q_c = np.array([[Q11, Q12,  0.],
                        [Q12, Q22,  0.],
                        [ 0.,  0., Q66]])
        Q_t = np.array([[Q44,  0.],
                        [ 0., Q55]])
        
        return Ply(name, density, Q_c, Q_t)
    
    @staticmethod
    def from_stiffness_matrix_orthotropic(name, density, C11, C22, C33, C44, C55, C66, C12, C13, C23):
        """
        Creates ply from given stiffness matrix C of a orthotropic material, see [Jones1999]_, pp. 59.
        The assumption of zero stress in thickness direction is made, see [Jones1999]_, pp. 70.
        
        Parameters
        ----------
        name: str
            Name of the ply.
        density: float
            Mass density of the ply.
        Cxy: float
            Component xy of the stiffness matrix.
        """
        Q11 = C11 - C13**2/C33
        Q22 = C22 - C23**2/C33
        Q12 = C12 - C13*C23/C33
        Q_c = np.array([[Q11, Q12,  0.],
                        [Q12, Q22,  0.],
                        [ 0.,  0., C66]])
        Q_t = np.array([[C44,  0.],
                        [ 0., C55]])
        return Ply(name, density, Q_c, Q_t)
    
    @staticmethod
    def from_engineering_constants_transverse_isotropic(name, density, E1, E2, nu12, nu22, G21):
        """
        Creates ply from given engineering constants of a transverse isotropic material.
        The assumption of zero stress in thickness direction is made, see [Jones1999]_, p. 70.
        
        Parameters
        ----------
        name: str
            Name of the ply.
        density: float
            Mass density of the ply.
        E1: float
            Elastic modulus in 1-direction.
        E2: float
            Elastic modulus normal to the 1-direction.
        nu12: float
            Major Poisson's ratio (extension-extension coupling coefficient), transverse extension normal to 1-direction for an axial extension in 1-direction.
        nu22: float
            Poisson's ratio (extension-extension coupling coefficient), transverse extension normal to the 1-direction for an axial extension normal to the 1-direction.
        G21: float
            Shear modulus in a plane containing the 1-axis.
        """
        G22 = E2/(2*(1+nu22))
        return Ply.from_engineering_constants_orthotropic(name, density, E1, E2, nu12, G21, G21, G22)
    
    @staticmethod
    def from_stiffness_matrix_transverse_isotropic(name, density, C11, C22, C44, C66, C12, C23):
        """
        Creates ply from given stiffness matrix C of a transverse isotropic material.
        The assumption of zero stress in thickness direction is made, see [Jones1999]_, pp. 70.
        
        Parameters
        ----------
        name: str
            Name of the ply.
        density: float
            Mass density of the ply.
        Cxy: float
            Component xy of the stiffness matrix.
        """
        return Ply.from_stiffness_matrix_orthotropic(name, density, C11, C22, C22, C44, C44, C66, C12, C12, C23)
    
    @property
    def name(self):
        """str: Name of the ply."""
        return self._name

    @property
    def uid(self):
        """str: UID of the ply. Same as name."""
        return self.name
    
    @property
    def density(self):
        """float: Mass density of the ply."""
        return self._density

    @property
    def Q_c(self):
        """numpy.ndarray: Disk stiffness matrix of the ply."""
        return self._Q_c
     
    @property
    def Q_t(self):
        """numpy.ndarray: Transverse shear stiffness matrix of the ply."""
        return self._Q_t
    
    def Q_rotated(self, Theta):
        """
        Returns the stiffness matrix of the ply in a rotated coordinate system rotated with the given angle in a
        mathematical positive direction about the third axis of the ply coodrdinate system, see [Jones1999]_, pp. 74.
        The stiffness matrix is splitted in two parts:
        the first part for the CLT (disk load only) and the second part for transverse shear stiffness.
        
        Parameters
        ----------
        Theta: float
            The rotaion angle in radians.
        
        Returns
        -------
        numpy.ndarray
            Disk stiffness matrix of the ply in the rotated coordinate system.
        numpy.ndarray
            Transverse shear stiffness matrix of the ply in the rotated coordinate system.
        """
        Q_c = self._Q_c
        Q_t = self._Q_t
        Q_c_rotated = np.dot(np.dot(np.dot(np.dot(Ply.T_c_inverse(Theta), Q_c), Ply.R_c()), Ply.T_c(Theta)), Ply.R_c_inv())
        Q_t_rotated = np.dot(np.dot(np.dot(np.dot(Ply.T_t_inverse(Theta), Q_t), Ply.R_t()), Ply.T_t(Theta)), Ply.R_t_inv())
        return Q_c_rotated, Q_t_rotated

    @staticmethod
    def R_c():
        """
        Returns the R matrix for the rotation of the ply disk stiffness matrix. The R matrix converts the tensor strains to the
        engineering strains for the disk stiffness matrix, see [Jones1999]_, pp. 75.
        
        Returns
        -------
        numpy.ndarray
            Disk R matrix.
        """
        return np.array([[1., 0., 0.],
                         [0., 1., 0.],
                         [0., 0., 2.]])
    
    @staticmethod
    def R_c_inv():
        """
        Returns the inverse R matrix for the rotation of the ply disk stiffness matrix. The inverse R matrix converts the engineering
        strains to the tensor strains for the disk stiffness matrix, see [Jones1999]_, pp. 75.
        
        Returns
        -------
        numpy.ndarray
            Inverse disk R matrix.
        """
        return np.array([[1., 0.,  0.],
                         [0., 1.,  0.],
                         [0., 0., 0.5]])
    
    @staticmethod
    def R_t():
        """
        Returns the R matrix for the rotation of the ply transverse shear stiffness matrix. The R matrix converts the tensor strains to the
        engineering strains for the disk stiffness matrix.
        
        Returns
        -------
        numpy.ndarray
            Transverse shear R matrix.
        """
        return np.array([[2., 0.],
                         [0., 2.]])
    @staticmethod
    def R_t_inv():
        """
        Returns the inverse R matrix for the rotation of the ply transverse shear stiffness matrix. The inverse R matrix converts
        the engineering strains to the tensor strains for the disk stiffness matrix.
        
        Returns
        -------
        numpy.ndarray
            Inverse transverse shear R matrix.
        """
        return np.array([[0.5,  0.],
                         [ 0., 0.5]])
    
    @staticmethod
    def T_c(Theta):
        """
        Returns the rotation matrix for the rotation of the ply disk stiffness matrix, see [Jones1999]_, pp. 75.
        
        Returns
        -------
        numpy.ndarray
            Rotation matrix.
        """
        s = sin(Theta)
        c = cos(Theta)
        return np.array([[  c*c, s*s,   2*c*s ],
                         [  s*s, c*c,  -2*c*s ],
                         [ -c*s, c*s, c*c-s*s ]])
    
    @staticmethod
    def T_c_inverse(Theta):
        """
        Returns the inverse rotation matrix for the rotation of the ply disk stiffness matrix, see [Jones1999]_, pp. 75.
        
        Returns
        -------
        numpy.ndarray
            Inverse rotation matrix.
        """
        s = sin(Theta)
        c = cos(Theta)
        return np.array([[ c*c,  s*s,  -2*c*s ],
                         [ s*s,  c*c,   2*c*s ],
                         [ c*s, -c*s, c*c-s*s ]])
    
    @staticmethod
    def T_t(Theta):
        """
        Returns the rotation matrix for the rotation of the ply shear stiffness stiffness matrix.
        
        Returns
        -------
        numpy.ndarray
            Rotation matrix.
        """
        s = sin(Theta)
        c = cos(Theta)
        return np.array([[ c, -s ],
                         [ s,  c ]])
    
    @staticmethod
    def T_t_inverse(Theta):
        """
        Returns the inverse rotation matrix for the rotation of the ply shear stiffness stiffness matrix.
        
        Returns
        -------
        numpy.ndarray
            Inverse rotation matrix.
        """
        s = sin(Theta)
        c = cos(Theta)
        return np.array([[  c, s ],
                         [ -s, c ]])
        
class Laminate(object):
    """
    This class represents a laminate build of plys of orthotropic material stacked together. The coordinate system of the laminate is the
    x-y-z-coordinate-system, the z-axis equals the 3-axis of the plys and the thickness direction. The laminate can be charged with
    disk- and plate-loads (A-B-D-matrices), see [Jones1999]_, pp. 187. An extension for transverse shear loads is made (A_s-matrix).
    
    Attributes
    ----------
    _name: str
        Name of the laminate.
    _layup: list((Ply, float, float))
        The layup of the laminate, list of plys. Tuple for each ply: (ply, thickness, orientation).
    """
    def __init__(self, name, layup):
        """
        Constructor.
        
        Parameters
        ----------
        name: str
            Name of the laminate.
        layup: list((Ply, float, float))
            The layup of the laminate, list of plys. Tuple for each ply: (ply, thickness, orientation).
        """
        self._name = name
        self._layup = layup
    
    def get_ABD_matrices(self, reference_surface=None):
        """
        Returns the stiffness matrices of the laminate, see [Jones1999]_, p. 198.
        
        Parameters
        ----------
        reference_surface: float (default: None)
            Offset in n-direction from the lower side of the lowest layer to the reference surface. None for the middle surface as reference surface.
        
        Returns
        -------
        numpy.ndarray
            Extensional stiffness matrix of the laminate (A-matrix, 3x3).
        numpy.ndarray
            Coupling stiffness matrix of the laminate (B-matrix, 3x3).
        numpy.ndarray
            Bending stiffness matrix of the laminate (D-matrix, 3x3).
        numpy.ndarray
            Transverse shear stiffness matrix of the laminate (A_s-matrix, 2x2).
        """
        size_ABD = 3
        size_A_s = 2
        A = np.zeros((size_ABD, size_ABD))
        B = np.zeros((size_ABD, size_ABD))
        D = np.zeros((size_ABD, size_ABD))
        A_s = np.zeros((size_A_s, size_A_s))
        if reference_surface is None:
            reference_surface = self.thickness / 2.
        z_last = -reference_surface
        for (ply, thickness, orientation) in self._layup:
            Q_c_laminate, Q_t_laminate = ply.Q_rotated(orientation)
            A += Q_c_laminate * thickness
            B += Q_c_laminate * ((z_last+thickness)**2 - z_last**2) / 2.
            D += Q_c_laminate * ((z_last+thickness)**3 - z_last**3) / 3.
            A_s += Q_t_laminate * thickness
            z_last += thickness
        return A, B, D, A_s
        
    def get_ABD_matrix(self, reference_surface=None):
        """
        Returns the combined stiffness matrix of the laminate.
        
        Parameters
        ----------
        reference_surface: float (default: None)
            Offset in n-direction from the lower side of the lowest layer to the reference surface. None for the middle surface as reference surface.
        
        Returns
        -------
        numpy.ndarray
            Laminate extension and bendig stiffness matrix (ABD-matrix, 6x6).
        """
        A, B, D, A_s = self.get_ABD_matrices(reference_surface)
        ABD = np.vstack((np.hstack((A, B)), np.hstack((B.T, D))))
        return ABD
    
    @staticmethod
    def ADB_matrix_to_dict(A, D, B, A_s):
        """
        Converts the laminate stiffness matrices to dict's. For the A, B and D matrices the indices 11, 22, 66, 12, 16 and 26 are set,
        for the A_s matrix the indices 44, 55 and 45 are set.
        
        Returns
        -------
        numpy.ndarray
            Extensional stiffness matrix of the laminate (A-matrix).
        numpy.ndarray
            Coupling stiffness matrix of the laminate (B-matrix).
        numpy.ndarray
            Bending stiffness matrix of the laminate (D-matrix).
        numpy.ndarray
            Transverse shear stiffness matrix of the laminate (A_s-matrix).
        """
        A_dict = {11:A[0,0], 22:A[1,1], 66:A[2,2], 12:A[0,1], 16:A[0,2], 26:A[1,2]}
        B_dict = {11:B[0,0], 22:B[1,1], 66:B[2,2], 12:B[0,1], 16:B[0,2], 26:B[1,2]}
        D_dict = {11:D[0,0], 22:D[1,1], 66:D[2,2], 12:D[0,1], 16:D[0,2], 26:D[1,2]}
        A_s_dict = {44:A_s[0,0], 55:A_s[1,1], 45:A_s[0,1]}
        return A_dict, B_dict, D_dict, A_s_dict
    
    def get_ABD_dict(self, reference_surface=None):
        """
        Returns the stiffness matrices of the laminate as dicts's, see [Jones1999]_, p. 198. The neutral plane is calculated
        according to [Schürmann2007]_, pp. 335.
        
        Parameters
        ----------
        reference_surface: float (default: None)
            Offset in n-direction from the lower side of the lowest layer to the reference surface. None for the middle surface as reference surface.
        
        Returns
        -------
        numpy.ndarray
            Extensional stiffness matrix of the laminate (A-matrix, 3x3).
        numpy.ndarray
            Coupling stiffness matrix of the laminate (B-matrix, 3x3).
        numpy.ndarray
            Bending stiffness matrix of the laminate (D-matrix, 3x3).
        numpy.ndarray
            Transverse shear stiffness matrix of the laminate (A_s-matrix, 2x2).
        """
        A, B, D, A_s = self.get_ABD_matrices(reference_surface)
        return Laminate.ADB_matrix_to_dict(A, D, B, A_s)

    @staticmethod
    def get_engineering_constants_base(ABD, thickness, method, ABD_inv=None):
        """
        Returns the engineering constants of the laminate (E_1, E_2, G).

        Parameters
        ----------
        ABD: numpy.ndarray
            The ABD stiffness matrix of the laminate.
        thickness: float
            The thickness of the laminate.
        method: str (default: 'with_poisson_effect')
            Method, how to calculate the engineering constants. Possible choices:
                'with_poisson_effect': see [Schürmann2007]_, p. 226.
                'without_poisson_effect':
                'wiedemann': see [Wiedemann2007]_, p. 155.
                'song': No stress in 1-direction, no strain in the other direction, see [Song].
        ABD_inv: numpy.ndarray (default: None)
            If available, the interted ABD stiffness matrix of the laminate.

        Returns
        -------
        float
            Elastic modulus in 1-direction.
        float
            Elastic modulus in 2-direction.
        float
            Shear modulus in the 1-2-plane (membrane shear modulus).
        """
        t = thickness
        if ABD_inv is None:
            ABD_inv = np.linalg.inv(ABD)
        if method == 'with_poisson_effect':
            E_1 = 1. / (ABD_inv[0, 0] * t)
            E_2 = 1. / (ABD_inv[1, 1] * t)
            G = 1. / (ABD_inv[2, 2] * t)
            return E_1, E_2, G
        elif method == 'without_poisson_effect':
            E_1 = ABD[0, 0] / t
            E_2 = ABD[1, 1] / t
            G = ABD[2, 2] / t
            return E_1, E_2, G
        elif method == 'song':
            K_11 = (ABD[0, 0] * ABD[1, 1] - ABD[0, 1] ** 2) / ABD[1, 1]
            K_22 = (ABD[1, 1] * ABD[2, 2] - ABD[1, 2] ** 2) / ABD[1, 1]
            return K_11 / t, None, K_22 / t
        elif method == 'wiedemann':
            E_1 = 1. / (ABD_inv[0, 0] * t)
            E_2 = 1. / (ABD_inv[1, 1] * t)
            G = 1. / ((ABD_inv[2, 2] / 2 + ABD_inv[0, 1]) * t)
            return E_1, E_2, G
        else:
            raise RuntimeError('Method not known')

    def get_engineering_constants(self, method='with_poisson_effect', reference_surface=None):
        """
        Returns the engineering constants of the laminate (E_1, E_2, G).
        
        Parameters
        ----------
        method: str (default: 'with_poisson_effect')
            Method, how to calculate the engineering constants. Possible choices:
                'with_poisson_effect': see [Schürmann2007]_, p. 226.
                'without_poisson_effect': 
                'wiedemann': see [Wiedemann2007]_, p. 155.
                'song': No stress in 1-direction, no strain in the other direction, see [Song].
        reference_surface: float (default: None)
            Offset in n-direction from the lower side of the lowest layer to the reference surface. None for the middle surface as reference surface.

        Returns
        -------
        float
            Elastic modulus in 1-direction.
        float
            Elastic modulus in 2-direction.
        float
            Shear modulus in the 1-2-plane (membrane shear modulus).
        """
        A, B, D, A_s = self.get_ABD_matrices(reference_surface)
        ABD = np.vstack((np.hstack((A, B)), np.hstack((B.T, D))))
        return Laminate.get_engineering_constants_base(ABD, self.thickness, method)
    
    @property
    def name(self):
        """str: Name of the laminate."""
        return self._name

    @property
    def uid(self):
        """str: UID of the laminate. Same as name."""
        return self.name

    @property
    def thickness(self):
        """float: Thickness of the laminate."""
        return sum([thickness for (ply, thickness, orientation) in self._layup])
    
    @property
    def density(self):
        """float: Mass density of the laminate."""
        return sum([ply.density*thickness for (ply, thickness, orientation) in self._layup]) / self.thickness
    
    @property
    def layup(self):
        """
        list((Ply, float, float)):
            The layup of the laminate, list of plys. Tuple for each ply (ply, thickness, orientation).
        """
        return self._layup
