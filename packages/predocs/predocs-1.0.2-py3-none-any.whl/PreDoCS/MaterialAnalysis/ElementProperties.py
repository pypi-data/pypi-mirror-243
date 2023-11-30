"""
This module contains the cross section element classes and the stiffness properties for the different materials.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
import numpy as np
from PreDoCS.MaterialAnalysis.CLT import Laminate

from PreDoCS.CrossSectionAnalysis.DiscreetCrossSectionGeometry import DiscreetCrossSectionGeometry
from PreDoCS.CrossSectionAnalysis.Interfaces import IElement, IElementStiffness

from PreDoCS.util.Logging import get_module_logger
log = get_module_logger(__name__)


class IsotropicElementStiffness(IElementStiffness):
    """
    Stiffness for an isotropic element.
    
    Attributes
    ----------
    _thickness: float
        Thickness of the material.
    _density: float
        Density of the material.
    _E: float
        Modulus of elasticity of the material.
    _G: float
        Modulus of shear of the material.
    """
    def __init__(self, thickness, density, E, G):
        """
        Constructor.
        
        Parameters
        ----------
        thickness: float
            Thickness of the material.
        E: float
            Modulus of elasticity of the material.
        G: float
            Modulus of shear of the material.
        """
        self._thickness = thickness
        self._density = density
        self._E = E
        self._G = G
    
    @staticmethod
    def from_isotropic_material(material):
        """
        Returns the isotropic homogenous material data from an isotropic material.
        
        Parameters
        ----------
        material: IsotropicMaterial
            The material.
        
        Returns
        -------
        IsotropicHomogenousMaterialData
            The material data.
        """
        return IsotropicElementStiffness(material.thickness, material.density, material.E, material.G)

    @staticmethod
    def from_skin(skin, **kwargs):
        """
        Returns the isotropic homogenous material data from an isotropic material.

        Parameters
        ----------
        skin: IsotropicMaterial
            The material.

        Returns
        -------
        IsotropicHomogenousMaterialData
            The material data.
        """
        E_1, E_2, G = skin.get_engineering_constants(**kwargs)

        return IsotropicElementStiffness(skin.thickness, skin.density, E_1, G)
    
    @staticmethod
    def from_composite_material(material, engineering_constants_method):
        """
        Returns the isotropic homogenous material data from an composite material. [Schürmann2007]_, p. 226
        
        Parameters
        ----------
        material: CompositeMaterial
            The material.
        engineering_constants_method: str
            See CLT.Laminate.get_engineering_constants.
        
        Returns
        -------
        IsotropicHomogenousMaterialData
            The material data.
        """
        E_1, E_2, G = material.get_engineering_constants(engineering_constants_method)
        return IsotropicElementStiffness(material.thickness, material.density, E_1, G)

    @staticmethod
    def dict_to_matrix(dictionary, matrix_size, translation_vector):
        result = np.zeros((matrix_size, matrix_size))
        for r in range(matrix_size):
            for c in range(r, matrix_size):
                result[r, c] = dictionary[translation_vector[r] * 10 + translation_vector[c]]
        return result

    @property
    def thickness(self):
        """float: Thickness of the material."""
        return self._thickness
    
    @property
    def density(self):
        """float: Density of the material."""
        return self._density
            
    @property
    def E(self):
        """float: Modulus of elasticity of the material."""
        return self._E
            
    @property
    def G(self):
        """float: Modulus of shear of the material."""
        return self._G
    
    def __eq__(self, other):
        """
        Parameters
        ----------
        other: IsotropicHomogenousMaterialData
            Other material data.
    
        Returns
        -------
        bool
            True, if the both materials are identical.
        
        Raises
        ------
        TypeError
            If other is not an instance of IsotropicHomogenousMaterialData.
        """
        if isinstance(other, IsotropicElementStiffness):
            return self._thickness == other._thickness and self._E == other._E and self._G == other._G
        else:
            raise TypeError()
    
    def stress_state_from_strain_state_function(self, strain_state):
        """
        Calculates the stress state of an composite element from an given strain state.
        
        Parameters
        ----------
        strain_state: dict(str, function(float))
            Stain state:
                normal_strain: function(float)
                    Strain in z-direction as function of the contur coordinate.
                shear_strain: function(float)
                    Shear strain in contur direction as function of the contur coordinate.
                    
        Returns
        -------
        dict(str, function(float))
            Stress state:
                normal_flow: function(float)
                    Normal flow in z-direction as function of the contur coordinate.
                shear_flow: function(float)
                    Shear flow in contur direction as function of the contur coordinate.
        """
        return {'normal_flow': lambda s: self._thickness * self._E * strain_state['normal_strain'](s),
                'shear_flow': lambda s: self._thickness * self._G * strain_state['shear_strain'](s)}


class IsotropicElement(DiscreetCrossSectionGeometry.Element):
    """
    A discreet element of an isotropic cross section.
    """    
    def __init__(self, element_id, node1, node2, component):
        """
        Constructor.
        
        Parameters
        ----------
        """
        super().__init__(element_id, node1, node2, component)


class CompositeElementStiffness(IElementStiffness):
    """
    Stiffness for a composite element.
    
    Attributes
    ----------
    _thickness: float
        Thickness of the material.
    _density: float
        Density of the material.
    _A: dict(int, float)
        Matrix of in-plane stiffness (3x3).
    _B: dict(int, float)
        Matrix of coupling stiffness (3x3).
    _D: dict(int, float)
        Matrix of bending stiffness (3x3).
    _A_s: dict(int, float)
        Matrix of transverse shear stiffness (2x2).
    """
    def __init__(self, thickness, density, A, B, D, A_s, engineering_constants_method='song', E=None, G=None):
        """
        Constructor.
        
        Parameters
        ----------
        thickness: float
            Thickness of the material.
        A: dict(int, float)
            Matrix of in-plane stiffness (3x3).
        D: dict(int, float)
            Matrix of bending stiffness (3x3).
        B: dict(int, float)
            Matrix of coupling stiffness (3x3).
        A_s: dict(int, float)
            Matrix of transverse shear stiffness (2x2).
        """
        self._thickness = thickness
        self._density = density
        self._A = A
        self._B = B
        self._D = D
        self._A_s = A_s

        # Normal stiffness
        K_normal = np.zeros((8, 6))

        K_normal[0, 0] = (A[11] * A[22] - A[12] ** 2) / A[22]
        K_normal[0, 1] = (-A[12] * A[26] + A[16] * A[22]) / A[22]
        K_normal[0, 2] = (-A[12] * B[22] + A[22] * B[12]) / A[22]
        K_normal[0, 3] = (-A[12] * B[12] + A[22] * B[11]) / A[22]
        K_normal[0, 4] = (-A[12] * B[26] + A[22] * B[16]) / A[22]
        # K_normal[0,5] = 0
        # K_normal[0,6] = 0
        # K_normal[0,7] = 0
        K_normal[1, 0] = (-A[12] * A[26] + A[16] * A[22]) / A[22]
        K_normal[1, 1] = (A[22] * A[66] - A[26] ** 2) / A[22]
        K_normal[1, 2] = (A[22] * B[26] - A[26] * B[22]) / A[22]
        K_normal[1, 3] = (A[22] * B[16] - A[26] * B[12]) / A[22]
        K_normal[1, 4] = (A[22] * B[66] - A[26] * B[26]) / A[22]
        # K_normal[1,5] = 0
        # K_normal[1,6] = 0
        # K_normal[1,7] = 0
        K_normal[2, 0] = (-A[12] * B[22] + A[22] * B[12]) / A[22]
        K_normal[2, 1] = (A[22] * B[26] - A[26] * B[22]) / A[22]
        K_normal[2, 2] = (A[22] * D[22] - B[22] ** 2) / A[22]
        K_normal[2, 3] = (A[22] * D[12] - B[12] * B[22]) / A[22]
        K_normal[2, 4] = (A[22] * D[26] - B[22] * B[26]) / A[22]
        # K_normal[2,5] = 0
        # K_normal[2,6] = 0
        # K_normal[2,7] = 0
        K_normal[3, 0] = (-A[12] * B[12] + A[22] * B[11]) / A[22]
        K_normal[3, 1] = (A[22] * B[16] - A[26] * B[12]) / A[22]
        K_normal[3, 2] = (A[22] * D[12] - B[12] * B[22]) / A[22]
        K_normal[3, 3] = (A[22] * D[11] - B[12] ** 2) / A[22]
        K_normal[3, 4] = (A[22] * D[16] - B[12] * B[26]) / A[22]
        # K_normal[3,5] = 0
        # K_normal[3,6] = 0
        # K_normal[3,7] = 0
        K_normal[4, 0] = (-A[12] * B[26] + A[22] * B[16]) / A[22]
        K_normal[4, 1] = (A[22] * B[66] - A[26] * B[26]) / A[22]
        K_normal[4, 2] = (A[22] * D[26] - B[22] * B[26]) / A[22]
        K_normal[4, 3] = (A[22] * D[16] - B[12] * B[26]) / A[22]
        K_normal[4, 4] = (A[22] * D[66] - B[26] ** 2) / A[22]
        # K_normal[4,5] = 0
        # K_normal[4,6] = 0
        # K_normal[4,7] = 0
        # K_normal[5,0] = 0
        # K_normal[5,1] = 0
        # K_normal[5,2] = 0
        # K_normal[5,3] = 0
        # K_normal[5,4] = 0
        K_normal[5, 5] = (A_s[44] * A_s[55] - A_s[45] ** 2) / A_s[44]
        # K_normal[5,6] = 0
        # K_normal[5,7] = 0
        K_normal[6, 0] = -A[12] / A[22]
        K_normal[6, 1] = -A[26] / A[22]
        K_normal[6, 2] = -B[22] / A[22]
        K_normal[6, 3] = -B[12] / A[22]
        K_normal[6, 4] = -B[26] / A[22]
        # K_normal[6,5] = 0
        # K_normal[6,6] = 0
        # K_normal[6,7] = 0
        # K_normal[7,0] = 0
        # K_normal[7,1] = 0
        # K_normal[7,2] = 0
        # K_normal[7,3] = 0
        # K_normal[7,4] = 0
        K_normal[7, 5] = -A_s[45] / A_s[44]
        # K_normal[7,6] = 0
        # K_normal[7,7] = 0

        self._K_normal = K_normal


        # Stiffness for Song
        K_Song = K_normal[[0, 1, 3, 4, 5], :][:, [0, 1, 3, 5]]

        self._K_Song = {
            11: K_Song[0, 0],
            12: K_Song[0, 1],
            13: K_Song[0, 2],
            21: K_Song[1, 0],
            22: K_Song[1, 1],
            23: K_Song[1, 2],
            41: K_Song[2, 0],
            42: K_Song[2, 1],
            43: K_Song[2, 2],
            51: K_Song[3, 0],
            52: K_Song[3, 1],
            53: K_Song[3, 2]}


        # Stiffness for Jung
        K_semiinvers_simple = np.zeros((8, 6))

        Delta = A[22] * A[66] * D[22] - A[22] * B[26] ** 2 - A[26] ** 2 * D[22] + 2 * A[26] * B[22] * B[26] - A[
            66] * B[22] ** 2

        K_semiinvers_simple[0, 0] = (A[11] * A[22] * A[66] * D[22] - A[11] * A[22] * B[26] ** 2 - A[11] * A[26] ** 2 *
                                     D[22] + 2 * A[11] * A[26] * B[22] * B[26] - A[11] * A[66] * B[22] ** 2 - A[
                                         12] ** 2 * A[66] * D[22] + A[12] ** 2 * B[26] ** 2 + 2 * A[12] * A[16] * A[
                                         26] * D[22] - 2 * A[12] * A[16] * B[22] * B[26] - 2 * A[12] * A[26] * B[12] *
                                     B[26] + 2 * A[12] * A[66] * B[12] * B[22] - A[16] ** 2 * A[22] * D[22] + A[
                                         16] ** 2 * B[22] ** 2 + 2 * A[16] * A[22] * B[12] * B[26] - 2 * A[16] * A[26] *
                                     B[12] * B[22] - A[22] * A[66] * B[12] ** 2 + A[26] ** 2 * B[12] ** 2) / Delta
        K_semiinvers_simple[0, 1] = (A[12] * A[26] * B[16] * D[22] - A[12] * A[26] * B[26] * D[12] - A[12] * A[66] * B[
            12] * D[22] + A[12] * A[66] * B[22] * D[12] + A[12] * B[12] * B[26] ** 2 - A[12] * B[16] * B[22] * B[26] -
                                     A[16] * A[22] * B[16] * D[22] + A[16] * A[22] * B[26] * D[12] + A[16] * A[26] * B[
                                         12] * D[22] - A[16] * A[26] * B[22] * D[12] - A[16] * B[12] * B[22] * B[26] +
                                     A[16] * B[16] * B[22] ** 2 + A[22] * A[66] * B[11] * D[22] - A[22] * A[66] * B[
                                         12] * D[12] - A[22] * B[11] * B[26] ** 2 + A[22] * B[12] * B[16] * B[26] - A[
                                         26] ** 2 * B[11] * D[22] + A[26] ** 2 * B[12] * D[12] + 2 * A[26] * B[11] * B[
                                         22] * B[26] - A[26] * B[12] ** 2 * B[26] - A[26] * B[12] * B[16] * B[22] - A[
                                         66] * B[11] * B[22] ** 2 + A[66] * B[12] ** 2 * B[22]) / Delta
        K_semiinvers_simple[0, 2] = (-A[12] * A[26] * B[26] * D[26] + A[12] * A[26] * B[66] * D[22] + A[12] * A[66] * B[
            22] * D[26] - A[12] * A[66] * B[26] * D[22] - A[12] * B[22] * B[26] * B[66] + A[12] * B[26] ** 3 + A[16] *
                                     A[22] * B[26] * D[26] - A[16] * A[22] * B[66] * D[22] - A[16] * A[26] * B[22] * D[
                                         26] + A[16] * A[26] * B[26] * D[22] + A[16] * B[22] ** 2 * B[66] - A[16] * B[
                                         22] * B[26] ** 2 - A[22] * A[66] * B[12] * D[26] + A[22] * A[66] * B[16] * D[
                                         22] + A[22] * B[12] * B[26] * B[66] - A[22] * B[16] * B[26] ** 2 + A[26] ** 2 *
                                     B[12] * D[26] - A[26] ** 2 * B[16] * D[22] - A[26] * B[12] * B[22] * B[66] - A[
                                         26] * B[12] * B[26] ** 2 + 2 * A[26] * B[16] * B[22] * B[26] + A[66] * B[12] *
                                     B[22] * B[26] - A[66] * B[16] * B[22] ** 2) / Delta
        K_semiinvers_simple[0, 3] = (-A[12] * A[26] * D[22] + A[12] * B[22] * B[26] + A[16] * A[22] * D[22] - A[16] * B[
            22] ** 2 - A[22] * B[12] * B[26] + A[26] * B[12] * B[22]) / Delta
        K_semiinvers_simple[0, 4] = (A[12] * A[26] * B[26] - A[12] * A[66] * B[22] - A[16] * A[22] * B[26] + A[16] * A[
            26] * B[22] + A[22] * A[66] * B[12] - A[26] ** 2 * B[12]) / Delta
        # K_semiinvers_simple[0,5] = 0
        # K_semiinvers_simple[0,6] = 0
        # K_semiinvers_simple[0,7] = 0
        K_semiinvers_simple[1, 0] = (A[12] * A[26] * B[16] * D[22] - A[12] * A[26] * B[26] * D[12] - A[12] * A[66] * B[
            12] * D[22] + A[12] * A[66] * B[22] * D[12] + A[12] * B[12] * B[26] ** 2 - A[12] * B[16] * B[22] * B[26] -
                                     A[16] * A[22] * B[16] * D[22] + A[16] * A[22] * B[26] * D[12] + A[16] * A[26] * B[
                                         12] * D[22] - A[16] * A[26] * B[22] * D[12] - A[16] * B[12] * B[22] * B[26] +
                                     A[16] * B[16] * B[22] ** 2 + A[22] * A[66] * B[11] * D[22] - A[22] * A[66] * B[
                                         12] * D[12] - A[22] * B[11] * B[26] ** 2 + A[22] * B[12] * B[16] * B[26] - A[
                                         26] ** 2 * B[11] * D[22] + A[26] ** 2 * B[12] * D[12] + 2 * A[26] * B[11] * B[
                                         22] * B[26] - A[26] * B[12] ** 2 * B[26] - A[26] * B[12] * B[16] * B[22] - A[
                                         66] * B[11] * B[22] ** 2 + A[66] * B[12] ** 2 * B[22]) / Delta
        K_semiinvers_simple[1, 1] = (A[22] * A[66] * D[11] * D[22] - A[22] * A[66] * D[12] ** 2 - A[22] * B[16] ** 2 *
                                     D[22] + 2 * A[22] * B[16] * B[26] * D[12] - A[22] * B[26] ** 2 * D[11] - A[
                                         26] ** 2 * D[11] * D[22] + A[26] ** 2 * D[12] ** 2 + 2 * A[26] * B[12] * B[
                                         16] * D[22] - 2 * A[26] * B[12] * B[26] * D[12] - 2 * A[26] * B[16] * B[22] *
                                     D[12] + 2 * A[26] * B[22] * B[26] * D[11] - A[66] * B[12] ** 2 * D[22] + 2 * A[
                                         66] * B[12] * B[22] * D[12] - A[66] * B[22] ** 2 * D[11] + B[12] ** 2 * B[
                                         26] ** 2 - 2 * B[12] * B[16] * B[22] * B[26] + B[16] ** 2 * B[22] ** 2) / Delta
        K_semiinvers_simple[1, 2] = (-A[22] * A[66] * D[12] * D[26] + A[22] * A[66] * D[16] * D[22] + A[22] * B[16] * B[
            26] * D[26] - A[22] * B[16] * B[66] * D[22] - A[22] * B[26] ** 2 * D[16] + A[22] * B[26] * B[66] * D[12] +
                                     A[26] ** 2 * D[12] * D[26] - A[26] ** 2 * D[16] * D[22] - A[26] * B[12] * B[26] *
                                     D[26] + A[26] * B[12] * B[66] * D[22] - A[26] * B[16] * B[22] * D[26] + A[26] * B[
                                         16] * B[26] * D[22] + 2 * A[26] * B[22] * B[26] * D[16] - A[26] * B[22] * B[
                                         66] * D[12] - A[26] * B[26] ** 2 * D[12] + A[66] * B[12] * B[22] * D[26] - A[
                                         66] * B[12] * B[26] * D[22] - A[66] * B[22] ** 2 * D[16] + A[66] * B[22] * B[
                                         26] * D[12] - B[12] * B[22] * B[26] * B[66] + B[12] * B[26] ** 3 + B[16] * B[
                                         22] ** 2 * B[66] - B[16] * B[22] * B[26] ** 2) / Delta
        K_semiinvers_simple[1, 3] = (A[22] * B[16] * D[22] - A[22] * B[26] * D[12] - A[26] * B[12] * D[22] + A[26] * B[
            22] * D[12] + B[12] * B[22] * B[26] - B[16] * B[22] ** 2) / Delta
        K_semiinvers_simple[1, 4] = (A[22] * A[66] * D[12] - A[22] * B[16] * B[26] - A[26] ** 2 * D[12] + A[26] * B[
            12] * B[26] + A[26] * B[16] * B[22] - A[66] * B[12] * B[22]) / Delta
        # K_semiinvers_simple[1,5] = 0
        # K_semiinvers_simple[1,6] = 0
        # K_semiinvers_simple[1,7] = 0
        K_semiinvers_simple[2, 0] = (-A[12] * A[26] * B[26] * D[26] + A[12] * A[26] * B[66] * D[22] + A[12] * A[66] * B[
            22] * D[26] - A[12] * A[66] * B[26] * D[22] - A[12] * B[22] * B[26] * B[66] + A[12] * B[26] ** 3 + A[16] *
                                     A[22] * B[26] * D[26] - A[16] * A[22] * B[66] * D[22] - A[16] * A[26] * B[22] * D[
                                         26] + A[16] * A[26] * B[26] * D[22] + A[16] * B[22] ** 2 * B[66] - A[16] * B[
                                         22] * B[26] ** 2 - A[22] * A[66] * B[12] * D[26] + A[22] * A[66] * B[16] * D[
                                         22] + A[22] * B[12] * B[26] * B[66] - A[22] * B[16] * B[26] ** 2 + A[26] ** 2 *
                                     B[12] * D[26] - A[26] ** 2 * B[16] * D[22] - A[26] * B[12] * B[22] * B[66] - A[
                                         26] * B[12] * B[26] ** 2 + 2 * A[26] * B[16] * B[22] * B[26] + A[66] * B[12] *
                                     B[22] * B[26] - A[66] * B[16] * B[22] ** 2) / Delta
        K_semiinvers_simple[2, 1] = (-A[22] * A[66] * D[12] * D[26] + A[22] * A[66] * D[16] * D[22] + A[22] * B[16] * B[
            26] * D[26] - A[22] * B[16] * B[66] * D[22] - A[22] * B[26] ** 2 * D[16] + A[22] * B[26] * B[66] * D[12] +
                                     A[26] ** 2 * D[12] * D[26] - A[26] ** 2 * D[16] * D[22] - A[26] * B[12] * B[26] *
                                     D[26] + A[26] * B[12] * B[66] * D[22] - A[26] * B[16] * B[22] * D[26] + A[26] * B[
                                         16] * B[26] * D[22] + 2 * A[26] * B[22] * B[26] * D[16] - A[26] * B[22] * B[
                                         66] * D[12] - A[26] * B[26] ** 2 * D[12] + A[66] * B[12] * B[22] * D[26] - A[
                                         66] * B[12] * B[26] * D[22] - A[66] * B[22] ** 2 * D[16] + A[66] * B[22] * B[
                                         26] * D[12] - B[12] * B[22] * B[26] * B[66] + B[12] * B[26] ** 3 + B[16] * B[
                                         22] ** 2 * B[66] - B[16] * B[22] * B[26] ** 2) / Delta
        K_semiinvers_simple[2, 2] = (A[22] * A[66] * D[22] * D[66] - A[22] * A[66] * D[26] ** 2 - A[22] * B[26] ** 2 *
                                     D[66] + 2 * A[22] * B[26] * B[66] * D[26] - A[22] * B[66] ** 2 * D[22] - A[
                                         26] ** 2 * D[22] * D[66] + A[26] ** 2 * D[26] ** 2 + 2 * A[26] * B[22] * B[
                                         26] * D[66] - 2 * A[26] * B[22] * B[66] * D[26] - 2 * A[26] * B[26] ** 2 * D[
                                         26] + 2 * A[26] * B[26] * B[66] * D[22] - A[66] * B[22] ** 2 * D[66] + 2 * A[
                                         66] * B[22] * B[26] * D[26] - A[66] * B[26] ** 2 * D[22] + B[22] ** 2 * B[
                                         66] ** 2 - 2 * B[22] * B[26] ** 2 * B[66] + B[26] ** 4) / Delta
        K_semiinvers_simple[2, 3] = (-A[22] * B[26] * D[26] + A[22] * B[66] * D[22] + A[26] * B[22] * D[26] - A[26] * B[
            26] * D[22] - B[22] ** 2 * B[66] + B[22] * B[26] ** 2) / Delta
        K_semiinvers_simple[2, 4] = (A[22] * A[66] * D[26] - A[22] * B[26] * B[66] - A[26] ** 2 * D[26] + A[26] * B[
            22] * B[66] + A[26] * B[26] ** 2 - A[66] * B[22] * B[26]) / Delta
        # K_semiinvers_simple[2,5] = 0
        # K_semiinvers_simple[2,6] = 0
        # K_semiinvers_simple[2,7] = 0
        K_semiinvers_simple[3, 0] = (A[12] * A[26] * D[22] - A[12] * B[22] * B[26] - A[16] * A[22] * D[22] + A[16] * B[
            22] ** 2 + A[22] * B[12] * B[26] - A[26] * B[12] * B[22]) / Delta
        K_semiinvers_simple[3, 1] = (-A[22] * B[16] * D[22] + A[22] * B[26] * D[12] + A[26] * B[12] * D[22] - A[26] * B[
            22] * D[12] - B[12] * B[22] * B[26] + B[16] * B[22] ** 2) / Delta
        K_semiinvers_simple[3, 2] = (A[22] * B[26] * D[26] - A[22] * B[66] * D[22] - A[26] * B[22] * D[26] + A[26] * B[
            26] * D[22] + B[22] ** 2 * B[66] - B[22] * B[26] ** 2) / Delta
        K_semiinvers_simple[3, 3] = (A[22] * D[22] - B[22] ** 2) / Delta
        K_semiinvers_simple[3, 4] = (-A[22] * B[26] + A[26] * B[22]) / Delta
        # K_semiinvers_simple[3,5] = 0
        # K_semiinvers_simple[3,6] = 0
        # K_semiinvers_simple[3,7] = 0
        K_semiinvers_simple[4, 0] = (-A[12] * A[26] * B[26] + A[12] * A[66] * B[22] + A[16] * A[22] * B[26] - A[16] * A[
            26] * B[22] - A[22] * A[66] * B[12] + A[26] ** 2 * B[12]) / Delta
        K_semiinvers_simple[4, 1] = (-A[22] * A[66] * D[12] + A[22] * B[16] * B[26] + A[26] ** 2 * D[12] - A[26] * B[
            12] * B[26] - A[26] * B[16] * B[22] + A[66] * B[12] * B[22]) / Delta
        K_semiinvers_simple[4, 2] = (-A[22] * A[66] * D[26] + A[22] * B[26] * B[66] + A[26] ** 2 * D[26] - A[26] * B[
            22] * B[66] - A[26] * B[26] ** 2 + A[66] * B[22] * B[26]) / Delta
        K_semiinvers_simple[4, 3] = (-A[22] * B[26] + A[26] * B[22]) / Delta
        K_semiinvers_simple[4, 4] = (A[22] * A[66] - A[26] ** 2) / Delta
        # K_semiinvers_simple[4,5] = 0
        # K_semiinvers_simple[4,6] = 0
        # K_semiinvers_simple[4,7] = 0
        # K_semiinvers_simple[5,0] = 0
        # K_semiinvers_simple[5,1] = 0
        # K_semiinvers_simple[5,2] = 0
        # K_semiinvers_simple[5,3] = 0
        # K_semiinvers_simple[5,4] = 0
        K_semiinvers_simple[5, 5] = A_s[55] - A_s[45] ** 2 / A_s[44]
        # K_semiinvers_simple[5,6] = 0
        # K_semiinvers_simple[5,7] = 0
        K_semiinvers_simple[6, 0] = (-A[12] * A[66] * D[22] + A[12] * B[26] ** 2 + A[16] * A[26] * D[22] - A[16] * B[
            22] * B[26] - A[26] * B[12] * B[26] + A[66] * B[12] * B[22]) / Delta
        K_semiinvers_simple[6, 1] = (A[26] * B[16] * D[22] - A[26] * B[26] * D[12] - A[66] * B[12] * D[22] + A[66] * B[
            22] * D[12] + B[12] * B[26] ** 2 - B[16] * B[22] * B[26]) / Delta
        K_semiinvers_simple[6, 2] = (-A[26] * B[26] * D[26] + A[26] * B[66] * D[22] + A[66] * B[22] * D[26] - A[66] * B[
            26] * D[22] - B[22] * B[26] * B[66] + B[26] ** 3) / Delta
        K_semiinvers_simple[6, 3] = (-A[26] * D[22] + B[22] * B[26]) / Delta
        K_semiinvers_simple[6, 4] = (A[26] * B[26] - A[66] * B[22]) / Delta
        # K_semiinvers_simple[6,5] = 0
        # K_semiinvers_simple[6,6] = 0
        # K_semiinvers_simple[6,7] = 0
        # K_semiinvers_simple[7,0] = 0
        # K_semiinvers_simple[7,1] = 0
        # K_semiinvers_simple[7,2] = 0
        # K_semiinvers_simple[7,3] = 0
        # K_semiinvers_simple[7,4] = 0
        K_semiinvers_simple[7, 5] = -A_s[45] / A_s[44]
        # K_semiinvers_simple[7,6] = 0
        # K_semiinvers_simple[7,7] = 0

        self._K_Jung = K_semiinvers_simple

        # Todo only calculate E and G if not from isotropic material

        if not E and not G:
            self._E, tmp, self._G = self.get_engineering_constants(method=engineering_constants_method)
            self._engineering_constants_method = engineering_constants_method
        else:
            self._E = E
            self._G = G

    @staticmethod
    def from_isotropic_material(material):
        """
        Returns the composite homogenous material data from an isotropic material. ([Jones1999]_, p. 204)
        or Schürmann p. 224 equation 10.11

        Parameters
        ----------
        material: IsotropicMaterial
            The material.

        Returns
        -------
        CompositeHomogenousMaterialData
            The material data.
        """
        nu = material.nu
        t = material.thickness
        A = material.E * t / (1 - nu ** 2) * np.array([[1, nu, 0],
                                                       [nu, 1, 0],
                                                       [0, 0, (1 - nu) / 2]])  # [Jones1999]_, eq. 4.27
        B = np.zeros((3, 3))  # [Jones1999]_, eq. 4.26
        D = A * t ** 2 / 12  # [Jones1999]_, eq. 4.29
        A_s = (material.E * t / (2 * (1 + nu))) * np.eye(2, 2)
        A_dict, B_dict, D_dict, A_s_dict = Laminate.ADB_matrix_to_dict(A, D, B, A_s)
        return CompositeElementStiffness(t, material.density, A_dict, B_dict, D_dict, A_s_dict, E=material.E, G=material.G)

    @staticmethod
    def from_skin(skin):
        """
        Returns the composite homogenous metal_sheet data from an isotropic metal_sheet. ([Jones1999]_, p. 204)

        Parameters
        ----------
        skin: IsotropicMaterial
            The metal_sheet.

        Returns
        -------
        CompositeHomogenousMaterialData
            The metal_sheet data.
        """
        A = skin.abd[:3, :3]
        B = skin.abd[:3, 3:]
        D = skin.abd[3:, 3:]
        A_s = skin.a_s
        t = skin.thickness
        density = skin.density

        A_dict = {11: A[0, 0], 22: A[1, 1], 66: A[2, 2], 12: A[0, 1], 16: A[0, 2], 26: A[1, 2]}
        B_dict = {11: B[0, 0], 22: B[1, 1], 66: B[2, 2], 12: B[0, 1], 16: B[0, 2], 26: B[1, 2]}
        D_dict = {11: D[0, 0], 22: D[1, 1], 66: D[2, 2], 12: D[0, 1], 16: D[0, 2], 26: D[1, 2]}
        A_s_dict = {44: A_s[0, 0], 55: A_s[1, 1], 45: A_s[0, 1]}

        return CompositeElementStiffness(t, density, A_dict, B_dict, D_dict, A_s_dict)
    
    @staticmethod
    def from_composite_material(material):
        """
        Returns the composite homogenous material data from an composite material.
        
        Parameters
        ----------
        material: CompositeMaterial
            The material.
        
        Returns
        -------
        CompositeElementStiffness
            The element stiffness.
        """
        A, B, D, A_s = material.get_ABD_dict(reference_surface=None)
        return CompositeElementStiffness(material.thickness, material.density, A, B, D, A_s)

    @staticmethod
    def from_laminate_material(material):
        ABD = material.abd
        A = ABD[0:3, 0:3]
        B = ABD[3:, 0:3]
        D = ABD[3:, 3:]
        A_s = material.a_s

        A_dict = {11: A[0, 0], 22: A[1, 1], 66: A[2, 2], 12: A[0, 1], 16: A[0, 2], 26: A[1, 2]}
        B_dict = {11: B[0, 0], 22: B[1, 1], 66: B[2, 2], 12: B[0, 1], 16: B[0, 2], 26: B[1, 2]}
        D_dict = {11: D[0, 0], 22: D[1, 1], 66: D[2, 2], 12: D[0, 1], 16: D[0, 2], 26: D[1, 2]}
        A_s_dict = {44: A_s[0, 0], 55: A_s[1, 1], 45: A_s[0, 1]}

        return CompositeElementStiffness(material.thickness, material.density, A_dict, B_dict, D_dict, A_s_dict)
    
    @property
    def thickness(self):
        """float: Thickness of the material."""
        return self._thickness
    
    @property
    def density(self):
        """float: Density of the material."""
        return self._density
            
    @property
    def A(self):
        """dict(int, float): Matrix of in-plane stiffness (3x3)."""
        return self._A
            
    @property
    def B(self):
        """dict(int, float): Matrix of coupling stiffness (3x3)."""
        return self._B
            
    @property
    def D(self):
        """
        Returns
        -------
        dict(int, float)
            Matrix of bending stiffness (3x3).
        """
        return self._D
            
    @property
    def A_s(self):
        """
        Returns
        -------
        dict(int, float)
            Matrix of transverse shear stiffness (2x2).
        """
        return self._A_s
    
    @property
    def K_Song(self):
        """dict(int, float): Material properties of the element."""
        return self._K_Song

    @property
    def K_Jung(self):
        """numpy.ndarray: Material properties of the element."""
        return self._K_Jung

    @property
    def K_normal(self):
        """numpy.ndarray: Material properties of the element."""
        return self._K_normal

    @property
    def E(self):
        """E: float"""
        return self._E

    @property
    def G(self):
        """G: float"""
        return self._G

    def __eq__(self, other):
        """
        Parameters
        ----------
        other: CompositeHomogenousMaterialData
            Other material data.
    
        Returns
        -------
        bool
            True, if the both materials are identical.
        
        Raises
        ------
        TypeError
            If other is not an instance of CompositeHomogenousMaterialData.
        """
        if isinstance(other, CompositeElementStiffness):
            return self._thickness == other._thickness and self._A == other._A and self._B == other._B and\
                   self._D == other._D and self._A_s == other._A_s
        else:
            raise TypeError()

    @property
    def torsion_compliance(self):
        """float: Shear compliance in contour direction under pure torsion."""
        # Entspricht dem G*t aus der Schürmann-Berechnung
        # A = self._A
        # K_11 = A[22] - A[12]**2/A[11]
        # K_12 = A[26] - A[12]*A[16]/A[11]
        # K_22 = A[66] - A[16]**2/A[11]
        #return 1. / (K_22 * (1 - K_22*K_12/K_11)) # Song # TODO: wieso diese Formel?
        return 1./self._K_Jung[3,3]#1. / (K_22 - K_12**2/K_11) # Hardt
    
    def stress_state_from_strain_state_function(self, strain_state):
        """
        Calculates the stress state from an given strain state.

        Parameters
        ----------
        strain_state: dict(str, function(float))
            Stain state:
                epsilon_zz_0: function(float)
                    Axial strain from primary warping as function of the contur coordinate.
                gamma_zs: function(float)
                    Membran shear strain as function of the contur coordinate.
                kappa_zz: function(float)
                    Curvature from secondary warping as function of the contur coordinate.
                gamma_zn: function(float)
                    Transverse shear strain as function of the contur coordinate.
                    
        Returns
        -------
        dict(str, function(float))
            Stress state as function of the contur coordinate:
                Resultant forces:    N_zz, N_zs, N_zn, N_sn
                Resultant moments:   M_zz, M_zs
        """    
        K = self._K_Song
        A_s = self._A_s
        with_transverse_shear_stiffness = True

        N_zz = lambda s: K[11] * strain_state['epsilon_zz_0'](s) + K[12] * strain_state['gamma_zs'](s) + K[13] * strain_state['kappa_zz'](s)
        N_zs = lambda s: K[21] * strain_state['epsilon_zz_0'](s) + K[22] * strain_state['gamma_zs'](s) + K[23] * strain_state['kappa_zz'](s)
        M_zz = lambda s: K[41] * strain_state['epsilon_zz_0'](s) + K[42] * strain_state['gamma_zs'](s) + K[43] * strain_state['kappa_zz'](s)
        M_zs = lambda s: K[51] * strain_state['epsilon_zz_0'](s) + K[52] * strain_state['gamma_zs'](s) + K[53] * strain_state['kappa_zz'](s)
        N_zn = lambda s: (A_s[44] * strain_state['gamma_zn'](s)) if with_transverse_shear_stiffness else 0
        N_sn = lambda s: (A_s[45] * strain_state['gamma_zn'](s)) if with_transverse_shear_stiffness else 0
        
        return {'N_zz': N_zz, 'N_zs': N_zs, 'N_zn': N_zn, 'N_sn': N_sn, 'M_zz': M_zz, 'M_zs': M_zs}

    def get_engineering_constants(self, method='with_poisson_effect'):
        """
        Returns the engineering constants of the laminate (E_1, E_2, G) from a composite stiffness.

        Parameters
        ----------
        method: str (default: 'with_poisson_effect')
            Method, how to calculate the engineering constants. Possible choices:
                'with_poisson_effect': see [Schürmann2007]_, p. 226.
                'without_poisson_effect':
                'wiedemann': see [Wiedemann2007]_, p. 155.
                'song': No stress in 1-direction, no strain in the other direction, see [Song].

        Returns
        -------
        float
            Elastic modulus in 1-direction.
        float
            Elastic modulus in 2-direction.
        float
            Shear modulus in the 1-2-plane (membrane shear modulus).
        """
        composite_stiffness = self

        translation_vector = [1, 2, 6]
        A_dict = composite_stiffness.A
        B_dict = composite_stiffness.B
        D_dict = composite_stiffness.D
        #A_s_dict = composite_stiffness.A_s
        A_matrix = IsotropicElementStiffness.dict_to_matrix(A_dict, 3, translation_vector)
        B_matrix = IsotropicElementStiffness.dict_to_matrix(B_dict, 3, translation_vector)
        D_matrix = IsotropicElementStiffness.dict_to_matrix(D_dict, 3, translation_vector)
        #A_s_matrix = IsotropicElementStiffness.dict_to_matrix(A_s_dict, 2, [4, 5])
        ABD = np.vstack((np.hstack((A_matrix, B_matrix)), np.hstack((B_matrix.T, D_matrix))))

        return Laminate.get_engineering_constants_base(ABD, composite_stiffness.thickness, method)


class CompositeElement(DiscreetCrossSectionGeometry.Element):
    """
    A discreet element of an composite cross section.
    
    Attributes
    ----------
    _torsional_function_value: float
        Value of the torsional function for this element.
    _node1_warping: float
        Value of the warping function for this element at node1.
    _node2_warping: float
        Value of the warping function for this element at node2.
    _K: dict(int, float)
        Material properties of the element.
    """    
    def __init__(self, element_id, node1, node2, component):
        """
        Constructor.
        
        Parameters
        ----------
        """
        super().__init__(element_id, node1, node2, component)
        self._torsional_function_value = None
        self._node1_warping = None
        self._node2_warping = None
        
    @property
    def torsional_function_value(self):
        """float: Value of the torsional function for this element."""
        return self._torsional_function_value
    
    @torsional_function_value.setter
    def torsional_function_value(self, value):
        self._torsional_function_value = value
    
    @property
    def node1_warping(self):
        """float: Value of the warping function for this element at node1."""
        return self._node1_warping
    
    @node1_warping.setter
    def node1_warping(self, value):
        self._node1_warping = value

    @property
    def node2_warping(self):
        """float: Value of the warping function for this element at node2."""
        return self._node2_warping

    @node2_warping.setter
    def node2_warping(self, value):
        self._node2_warping = value

    def r_midsurface(self, pole):
        """
        Returns
        -------
        float
            Geometic quantity, see [Jung2002]_, p. 108.
        """
        return (self.midsurface_position.x - pole.x) * self.dy_ds - (self.midsurface_position.y - pole.y) * self.dx_ds

    def r_nodes(self, pole):
        """
        Returns
        -------
        float
            Geometic quantity, see [Jung2002]_, p. 108.
        """
        return (self.position.x - pole.x) * self.dy_ds - (self.position.y - pole.y) * self.dx_ds

    def q(self, s, pole):
        """
        Returns
        -------
        float
            Geometic quantity, see [Jung2002]_, p. 108.
        """
        return -((self.node1_midsurface_position.y + s*self.dy_ds) - pole.y) * self.dy_ds - \
                ((self.node1_midsurface_position.x + s*self.dx_ds) - pole.x) * self.dx_ds
