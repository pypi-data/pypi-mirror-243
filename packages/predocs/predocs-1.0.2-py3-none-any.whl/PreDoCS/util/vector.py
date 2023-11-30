"""
.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#  Copyright: 2021 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.
from PreDoCS.util.Logging import get_module_logger

log = get_module_logger(__name__)

try:
    from lightworks.utils.vector import Vector

except ImportError:
    log.info('Modul lightworks.utils.vector not found. Use PreDoCS Vector class.')
    import numpy as np
    
    
    class Vector(np.ndarray):
        """
        Represents a n-dimensional vector. The class inherits from numpy.ndarray.
        """
    
        def __new__(cls, input_array=(0, 0)):
            """
            Constructor.
    
            Parameters
            ----------
            input_array : numpy.array, numpy.matrix, list, tuple (default: (0, 0))
                Components of the vector.
            """
            obj = np.asarray(input_array).view(cls).astype(float)
            return obj
    
        @property
        def x(self):
            """float: The first component of the vector."""
            return self[0]
    
        @property
        def y(self):
            """float: The second component of the vector."""
            return self[1]
    
        @property
        def z(self):
            """
            Returns
            -------
            float
                The third component of the vector.
    
            Raises
            ------
            IndexError
                If the third component is not defined.
            """
            return self[2]
    
        def __eq__(self, other):
            return np.array_equal(self, other)
    
        def __ne__(self, other):
            return not np.array_equal(self, other)
    
        def __iter__(self):
            for x in np.nditer(self):
                yield x.item()
    
        def __lt__(self, other):
            """
            Overrides the '<'-operator. Compares the vectors lexicographically.
    
            Returns
            -------
            bool
                True, if self is smaller than other.
    
            Raises
            ------
            NotImplemented
                If other is not an instance of Vector.
            """
            if isinstance(other, Vector):
                return list(self) < list(other)
            else:
                raise NotImplementedError()
    
        def __gt__(self, other):
            """
            see __lt__() method
            """
            if isinstance(other, Vector):
                return list(self) > list(other)
            else:
                raise NotImplementedError()
    
        def dist(self, other):
            """
            Returns the distance between this and an other vector.
    
            Parameters
            ----------
            other : Vector
                The other vector, the dimensions must agree.
    
            Returns
            -------
            float
                Distance.
            """
            return np.linalg.norm(self - other)
    
        @property
        def length(self):
            """float: Length of the vector."""
            return np.linalg.norm(self)
    
        @property
        def normalised(self):
            """Vector: The normalized vector."""
            return self / self.length
    
        def angle_between(self, other):
            """
            Returns the angle between this and an other vector.
    
            Parameters
            ----------
            other : Vector
                The other vector. Two- or three-dimensional. Dimensions must agree.
    
            Returns
            -------
            float
                angle between this and an other vector in RAD.
            """
            return np.arccos(np.clip(np.dot(self.normalised, other.normalised), -1.0, 1.0))
    
        @property
        def angle_in_plane(self):
            """
            float:
                Returns the angle of this vector in the x-y-plane. This vector has to be two-dimensional.
                The angel is signed (mathematical direction of rotation) and is between -PI and PI.
            """
            assert (len(self) == 2)  # Two-dimensional vector
            if self.y == 0:
                if self.x > 0:
                    return 0
                else:
                    return np.pi
            else:
                return np.sign(self.y) * Vector([1., 0.]).angle_between(self)
    
