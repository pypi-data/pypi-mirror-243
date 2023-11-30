"""
This module contains the material interfaces.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
from abc import ABC, abstractmethod


class IMaterial(ABC):
    """
    Description of an general material.
    """
    @property
    @abstractmethod
    def name(self):
        """str: Name of the material."""
        pass
    
    @property
    @abstractmethod
    def thickness(self):
        """float: Thickness of the material."""
        pass
    
    @property
    @abstractmethod
    def density(self):
        """float: Density of the material."""
        pass
    
    @property
    @abstractmethod
    def stiffness(self):
        """IElementStiffness: Stiffness of the material."""
        pass
