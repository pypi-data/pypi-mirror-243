"""
This module contains the implementations for the material interfaces.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
from PreDoCS.MaterialAnalysis.CLT import Laminate as Laminate_predocs
from PreDoCS.MaterialAnalysis.ElementProperties import IsotropicElementStiffness, \
    CompositeElementStiffness, IsotropicElement, CompositeElement
from PreDoCS.MaterialAnalysis.Interfaces import IMaterial
from PreDoCS.util.Logging import get_module_logger

log = get_module_logger(__name__)


class IsotropicMaterial(IMaterial):
    """
    Description of an isotropic material.
    
    Attributes
    ----------
    _name: str
        Name of the material.
    _thickness: float
        Thickness of the material.
    _density: float
        Density of the material.
    _stiffness: IElementStifness
        Stiffness data of the material.
    _E: float
        Modulus of elasticity of the material.
    _nu: float
        Poisson's ratio of the material.
    """
    def __init__(self, name, thickness, density, E, nu):
        """
        Class initialisation
        
        Parameters
        ----------
        name: str
            Name of the material.
        thickness: float
            Thickness of the material.
        density: float
            Density of the material.
        E: float
            Modulus of elasticity of the material.
        nu: float
            Poisson's ratio of the material.
        """
        self._name = name
        self._thickness = thickness
        self._density = density
        self._E = E
        self._nu = nu

    @staticmethod
    def from_E_and_G(name, thickness, density, E, G):
        """
        Create isotropic material from modulus of elasticity and shear modulus.
        
        Parameters
        ----------
        name: str
            Name of the material.
        thickness: float
            Thickness of the material.
        density: float
            Density of the material.
        E: float
            Modulus of elasticity of the material.
        G: float
            Shear modulus of the material.
        """
        nu = E / (2*G) - 1
        return IsotropicMaterial(name, thickness, density, E, nu)

    @staticmethod
    def from_E_and_nu(name, thickness, density, E, nu):
        """
        Create isotropic material from modulus of elasticity and poisson's ratio.
        
        Parameters
        ----------
        name: str
            Name of the material.
        thickness: float
            Thickness of the material.
        density: float
            Density of the material.
        E: float
            Modulus of elasticity of the material.
        nu: float
            Poisson's ratio of the material.
        """
        return IsotropicMaterial(name, thickness, density, E, nu)

    @property
    def name(self):
        """str: Name of the material."""
        return self._name

    @property
    def uid(self):
        """str: UID of the material. Same as name."""
        return self.name
    
    @property
    def thickness(self):
        """float: Thickness of the material."""
        return self._thickness
    
    @thickness.setter
    def thickness(self, value):
        self._thickness = value
    
    @property
    def density(self):
        """float: Density of the material."""
        return self._density

    @property
    def stiffness(self):
        """IElementStiffness: Stiffness of the material."""
        return self._stiffness

    @stiffness.setter
    def stiffness(self, value):
        self._stiffness = value
    
    @property
    def E(self):
        """float: Modulus of elasticity of the material."""
        return self._E
            
    @property
    def nu(self):
        """float: Poisson's ratio of the material."""
        return self._nu
            
    @property
    def G(self):
        """float: Shear modulus of the material."""
        return self._E / (2 + 2 * self._nu)


class CompositeMaterial(Laminate_predocs):
    """
    Description of an composite material. 
    
    Attributes
    ----------
    _stiffness: IElementStiffness
        Stiffness data of the material.
    
    """
    def __init__(self, name, layup):
        """
        Constructor.
        
        Parameters
        ----------
        name: str
            Name of the material.
        layup: list((Ply, float, float))
            The layup of the laminate. List of plys, tuple for each ply: (Ply, thickness, orientation).
        """
        Laminate_predocs.__init__(self, name, layup)
        self._stiffness = None
    
    @property
    def stiffness(self):
        """IElementStiffness: Stiffness of the material."""
        return self._stiffness

    @stiffness.setter
    def stiffness(self, value):
        self._stiffness = value

    
def get_stiffness_for_material(material, element_type, **element_kwargs):
    """
    Returns the homogenous material data of the material for the element type.
    
    Parameters
    ----------
    material: IMaterial
        The material.
    element_type: class <- IElement
        The element type.
    engineering_constants_method: str
        See CLT.Laminate.get_engineering_constants.
    
    Returns
    -------
    IElementStiffness
        The stiffness of the element.
    """
    # New stiffness
    if isinstance(material, IsotropicMaterial) and issubclass(element_type, IsotropicElement):
        stiffness = IsotropicElementStiffness.from_isotropic_material(material)
    elif isinstance(material, IsotropicMaterial) and issubclass(element_type, CompositeElement):
        stiffness = CompositeElementStiffness.from_isotropic_material(material)
    elif isinstance(material, CompositeMaterial) and issubclass(element_type, IsotropicElement):
        assert 'engineering_constants_method' in element_kwargs
        stiffness = IsotropicElementStiffness.from_composite_material(material, element_kwargs['engineering_constants_method'])
    elif isinstance(material, CompositeMaterial) and issubclass(element_type, CompositeElement):
        stiffness = CompositeElementStiffness.from_composite_material(material)
    else:
        raise RuntimeError('Material type "{}" or element type "{}" not defined'.format(str(type(material)), str(element_type)))
    return stiffness


def get_stiffness_for_material_VCP(material, element_type, **element_kwargs):
    """
    Returns the homogenous material data of the material for the element type.

    Parameters
    ----------
    material: IMaterial
        The material.
    element_type: class <- IElement
        The element type.
    engineering_constants_method: str
        See CLT.Laminate.get_engineering_constants.

    Returns
    -------
    IElementStiffness
        The stiffness of the element.
    """
    try:
        from lightworks.mechana.skins.metal import Sheet as Sheet_lw
        from lightworks.mechana.skins.composite import Laminate as Laminate_lw
        from lightworks.mechana.skins.composite import LaminationParameter as LaminationParameter_lw
    except ImportError:
        message = 'Modul lightworks.mechana not found. Material world VCP can not be used.'
        log.error(message)
        raise ImportError(message)

    if isinstance(material, Sheet_lw) and issubclass(element_type, IsotropicElement):
        stiffness = IsotropicElementStiffness.from_skin(material)
    elif isinstance(material, Sheet_lw) and issubclass(element_type, CompositeElement):
        stiffness = CompositeElementStiffness.from_skin(material)
    elif isinstance(material, Laminate_lw) and issubclass(element_type, IsotropicElement):
        assert ('method' in element_kwargs)
        stiffness = IsotropicElementStiffness.from_skin(material, **element_kwargs)
    elif isinstance(material, Laminate_lw) and issubclass(element_type, CompositeElement):
        stiffness = CompositeElementStiffness.from_skin(material)
    elif isinstance(material, LaminationParameter_lw) and issubclass(element_type, IsotropicElement):
        assert ('method' in element_kwargs)
        stiffness = IsotropicElementStiffness.from_skin(material, **element_kwargs)
    elif isinstance(material, LaminationParameter_lw) and issubclass(element_type, CompositeElement):
        stiffness = CompositeElementStiffness.from_skin(material)
    else:
        raise RuntimeError(
            'Material type "{}" or element type "{}" not defined'.format(str(type(material)), str(element_type)))

    return stiffness
