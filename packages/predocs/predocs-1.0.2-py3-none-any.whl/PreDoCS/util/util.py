"""
Helping functions for PreDoCS.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
import json
import os
import numpy as np
from cloudpickle import cloudpickle
from scipy.interpolate import interp1d
from scipy.spatial.transform import Rotation as R

from PreDoCS.util.vector import Vector
from PreDoCS.util.Logging import get_module_logger
log = get_module_logger(__name__)

try:
    from lightworks.cpacs_interface.loads import create_moved_load_vector

except ImportError:
    log.info('Modul lightworks.cpacs_interface.loads not found. Use PreDoCS function.')

    def create_moved_load_vector(va, vn, fa, ma):
        """
        Loads are moved within the cross section plane from the load reference points to the load application points.

        Parameters
        ----------
        va: Vector
            positioning of the old force and moment vector fa, ma
        vn: Vector
            positioning of the new force and moment vector fn, m,
        fa: Vector
            old force vector
        ma: Vector
            old moment vector
        Returns
        -------
        fn: Vector
            new force vector
        mn: Vector
            new Moment vector
        """
        vna = va - vn

        fn = fa
        mn = ma + np.cross(vna, fa)

        return fn, mn


def intersect(a, b):
    """
    Returns the intersection of two lists.
        
    Parameters
    ----------
    a: list(object)
        First list.
    b: list(object)
        Second list.
        
    Returns
    -------
    list
        Intersection.
    """
    return list(set(a) & set(b))


def get_EI_eta(phi, EI_x, EI_y, EI_xy):
    """
    Calculates the elastic second moment of area around the eta-axis, if the coordinate system is rotated about phi.
    Eta is the rotated x-axis, xi the rotated y-axis.

    Parameters
    ----------
    phi: float
        Rotation angle in RAD.
    EI_x: float
        Elastic second moment of area around the x-axis.
    EI_y: float
        Elastic second moment of area around the y-axis.
    EI_x: float
        Elastic moment of deviation around the x- and y-axis.
        
    Returns
    -------
    float
        Elastic second moment of area around the eta-axis.
    """
    return (EI_x+EI_y)/2. + (EI_x - EI_y)/2. * np.cos(2.*phi) + EI_xy * np.sin(2.*phi)


def get_EI_xi(phi, EI_x, EI_y, EI_xy):
    """
    Calculates the elastic second moment of area around the xi-axis, if the coordinate system is rotated about phi.
    Eta is the rotated x-axis, xi the rotated y-axis.
    
    Parameters
    ----------
    phi: float
        Rotation angle in RAD.
    EI_x: float
        Elastic second moment of area around the x-axis.
    EI_y: float
        Elastic second moment of area around the y-axis.
    EI_x: float
        Elastic moment of deviation around the x- and y-axis.
        
    Returns
    -------
    float
        Elastic second moment of area around the xi-axis.
    """
    return (EI_x+EI_y)/2. - (EI_x - EI_y)/2. * np.cos(2.*phi) - EI_xy * np.sin(2.*phi)


def get_EI_eta_xi(phi, EI_x, EI_y, EI_xy):
    """
    Calculates the elastic moment of deviation around the eta- and xi-axis, if the coordinate system is rotated about phi.
    Eta is the rotated x-axis, xi the rotated y-axis.

    Parameters
    ----------
    phi: float
        Rotation angle in RAD.
    EI_x: float
        Elastic second moment of area around the x-axis.
    EI_y: float
        Elastic second moment of area around the y-axis.
    EI_x: float
        Elastic moment of deviation around the x- and y-axis.
        
    Returns
    -------
    float
        Elastic moment of deviation around the eta- and xi-axis.
    """
    return - (EI_x - EI_y)/2. * np.sin(2.*phi) + EI_xy * np.cos(2.*phi)


def get_polygon_area(x,y):
    """
    Returns the area of a polygon. [https://en.wikipedia.org/wiki/Shoelace_formula]
         
    Parameters
    ----------
    x: list(float)
        List of x-coordinates of the polygon edges.
    y: list(float)
        List of y-coordinates of the polygon edges.
        
    Returns
    -------
    float
        Area of the polygon.
    """
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))


def transform_direction(augmented_transformation_matrix, vector):
    """
    Transformation of a direction vector with an augmented transformation matrix (only linear mapping, no translation).
    [https://en.wikipedia.org/wiki/Affine_transformation]
        
    Parameters
    ----------
    augmented_transformation_matrix: numpy.ndarray
        Augmented transformation matrix.
    vector: Vector
        Vector to transform.

    Returns
    -------
    Vector
        Transformed vector.
    """
    if augmented_transformation_matrix.shape[0] == 4 or vector.shape[0] == 2:
        transformation_matrix = augmented_transformation_matrix[:-1, :-1]
    elif augmented_transformation_matrix.shape[0] == 3 and vector.shape[0] == 3:
        transformation_matrix = augmented_transformation_matrix
    else:
        raise RuntimeError("Wrong dimension")

    v = np.dot(transformation_matrix, vector)
    return Vector(v.flatten())


def transform_location(augmented_transformation_matrix, vector):
    """
    Transformation of a location vector with an augmented transformation matrix.
    [https://en.wikipedia.org/wiki/Affine_transformation]
        
    Parameters
    ----------
    augmented_transformation_matrix: numpy.ndarray
        Augmented transformation matrix.
    vector: Vector
        Vector to transform.

    Returns
    -------
    Vector
        Transformed vector.
    """
    y_ = np.dot(augmented_transformation_matrix, np.append(vector, 1))
    return Vector(y_.flatten()[:-1])


def create_augmented_transformation_matrix_2d(alpha=0., translation_vector=Vector([0., 0.]), scaling=1.):
    """
    Creates an augmented transformation matrix for a two-dimensional transformation.
    [https://en.wikipedia.org/wiki/Affine_transformation]
        
    Parameters
    ----------
    alpha: float (default: 0.)
        Rotation angle in the plane in RAD.
    vector: Vector (default: Vector([0., 0.]))
        Translation vector in the plane.
    scaling: float (default: 1.)
        Scale factor.

    Returns
    -------
    numpy.ndarray
        Augmented transformation matrix.
    """
    scale = np.array([[ scaling,       0, 0 ],
                      [       0, scaling, 0 ],
                      [       0,       0, 1 ]])
    translate = np.array([[ 1, 0, translation_vector.x ],
                          [ 0, 1, translation_vector.y ],
                          [ 0, 0,                    1 ]])
    rotate = np.array([[ np.cos(alpha), -np.sin(alpha), 0 ],
                       [ np.sin(alpha),  np.cos(alpha), 0 ],
                       [             0,              0, 1 ]])
    return translate @ rotate @ scale


def create_transformation_matrix(reference_point, reference_axis_z):
    """
    Returns the

    A Transformation matrix contains a rotary matrix and a translational part to convert between coordinate systems.
    The rotary matrix is the upper left 3x3 Matrix, were each column represents a base vector of the new coordinate
    system. The upper right 3x1 vector is the translational vector directing towards the origin of the original
    coordinate system from the perspective of the new coordinate system.

    The PreDoCS coordinate system is defined having its origin at the wing root, with the z-axis as wing axis. The
    x-axis is in the x-y-plane of the original coordinate system and perpendicular to the z-axis. The y axis is
    perpendicular to the x-axis and the y-axis in the sense of a right-handed coordinate system.

    The x-base-vector is therefore defined as the projection of the given z-base-vector into the original x-y-plane
    rotated by +90 degree.

    The y-base-vector is calculated as the negative cross-product of the x-base-vector and the z-base-vector

    Parameters
    ----------
    reference_point: Vector
        The origin for the PreDoCS coordinate system
    reference_axis_z: Vector
        The z axis of the PreDoCS coordinate system
    Return
    ------
    transformation_matrix: ndarray
        The transformation matrix
    """
    # Rotation angle = 90°
    alpha = np.pi / 2

    # Rotary matrix
    rotary_matrix = np.asarray([[np.cos(alpha), -np.sin(alpha)],
                                [np.sin(alpha), np.cos(alpha)]])

    # Normalise reference axis z
    reference_axis_z = reference_axis_z.normalised

    # x reference axis
    axis_z = reference_axis_z[0:2]
    axis_x = np.dot(rotary_matrix, axis_z)
    reference_axis_x = Vector(np.concatenate([axis_x, [0]])).normalised

    # y reference axis is orthogonal to x and z axis. The sign is to achieve a rightful coordinate system
    reference_axis_y = Vector(- np.cross(reference_axis_x, reference_axis_z))

    # 3D Rotary Matrix the columns of the rotary matrix are the base vectors of the new coordinate system
    rotary_matrix_3d = np.concatenate([[reference_axis_x], [reference_axis_y], [reference_axis_z]])

    # Translational vector in predocs coordinate system
    global_origin_from_predocs = -np.dot(rotary_matrix_3d, reference_point)

    # Affine Transformation
    transformation_matrix = np.concatenate(
        [rotary_matrix_3d, np.asanyarray([global_origin_from_predocs]).transpose()], axis=1)
    transformation_matrix = np.concatenate([transformation_matrix, [[0, 0, 0, 1]]])

    return transformation_matrix


def invert_transformation_matrix(transformation_matrix):
    """
    Invert a given transformation matrix and return is. A rotary matrix is inverted if transposed.

    A Transformation matrix contains a rotary matrix and a translational part to convert between coordinate systems.
    The rotary matrix is the upper left 3x3 Matrix, were each column represents a base vector of the new coordinate
    system. The upper right 3x1 vector is the translational vector directing towards the origin of the original
    coordinate system from the perspective of the new coordinate system.

    Parameters
    ----------
    transformation_matrix: ndarray
        4x4 ndarray

    Return
    ------
    back_transformation_matrix: ndaray
        4x4 ndarray
    """
    # Get rotary matrix
    transformation_rotary_matrix = transformation_matrix[0:3, 0:3]

    # Invert rotary matrix and translation vector
    back_transformation_matrix_rotary = transformation_rotary_matrix.transpose()

    # Get transformation vector and change direction (Points from one coordinate system origin to the other)
    transformation_translation_vector = transformation_matrix[0:3, 3]

    # Transform translation vector into PreDoCS coordinates (PreDoCS origin from global)
    back_transformation_translation_vector = -np.dot(back_transformation_matrix_rotary, transformation_translation_vector)

    # Set inverted matrix together
    back_transformation_matrix = np.concatenate(
        [back_transformation_matrix_rotary, back_transformation_translation_vector.reshape(3, 1)], axis=1)
    back_transformation_matrix = np.concatenate([back_transformation_matrix, [[0, 0, 0, 1]]])

    return back_transformation_matrix


def create_transfomration_matrix_by_angles(translation, phi, theta, psi):
    """
    Create the 4x4 transformation matrix by a 3x1 translation vector and 3 angles in radians

    Parameters
    ----------
    translation: ndarray
        [[x, y, z]]
    phi: float
        rotation around x in radians
    theta: float
        rotation around y in radians
    psi: float
        rotation around x in radians

    Return
    ------
    T: ndarray
        4x4 affine transformation matrix
    """
    sin = np.sin(phi)
    cos = np.cos(phi)

    r1 = np.asarray([[1, 0, 0], [0, cos, -sin], [0, sin, cos]])

    sin = np.sin(theta)
    cos = np.cos(theta)

    r2 = np.asarray([[cos, 0, sin], [0, 1, 0], [-sin, 0, cos]])

    sin = np.sin(psi)
    cos = np.cos(psi)

    r3 = np.asarray([[cos, -sin, 0], [sin, cos, 0], [0, 0, 1]])

    r = r3 @ r2 @ r1

    T1 = np.concatenate([r, translation], axis=1)
    T = np.concatenate([T1, [[0, 0, 0, 1]]], axis=0)

    return T

def create_rotation_matrix_from_directions(dir_1, dir_2):
    """
    Creates a rotation matrix between dir_1 and dir_2, that yield dir_1 = T * dir_2, where T is the rotation matrix
    Parameters
    ----------
    dir_1: Vector
        [x1, y1, z1]
    dir_2: Vector
        [x2, y2, z2]

    Return
    ------
    T: ndarray
        3x3 rotiation matrix
    """

    dir_1 = dir_1.normalised
    dir_2 = dir_2.normalised

    # Calculate the roation axis
    rot_axis = Vector(np.cross(dir_1, dir_2))
    rot_angle = np.arcsin(rot_axis.length) # Angle from cross product of two vectors with length 1

    if rot_angle < 1e-10: # No rotation needed, return identity matrix
        return np.identity(3)
    else: # Euler axis
        rot_axis = rot_angle * rot_axis.normalised

        # get Rotation and return as matrix
        rotation = R.from_rotvec(rot_axis)

        return rotation.as_matrix()

def enclosed_area_vector(cells):
    """
    Parameters
    ----------
    cells: list(Cell)
        List of cells.
        
    Returns
    -------
    np.array
        Vector of the enclosed area of the cells.
    """
    return np.array([c.area for c in cells])


def idx(a):
    """
    Returns a numpy matrix index from a readable two-digit number. 22 -> (1,1); 52 -> (4,1)
    
    Parameters
    ----------
    a: int
        Two-digit integer.
        
    Returns
    -------
    (int, int)
        Numpy matrix index.
    """
    s = str(a)
    return (int(s[0])-1, int(s[1])-1)


def check_symmetric(m, tol=1e-8):
    """
    Checks, if a matrix is symmetric.
    
    Parameters
    ----------
    m: numpy.ndarray
        The matrix.
    tol: float (default: 1e-8)
        The absolute tolerance of two identical elements.
        
    Returns
    -------
    bool
        True, if the matrix is symmetric.
    """
    return np.allclose(m, m.T, atol=tol)


def symmetrize(m):
    """
    Returns a symmetric matrix from a matrix where only the upper or lower triangular matrix are set.
    
    Parameters
    ----------
    m: numpy.ndarray
        The matrix.
        
    Returns
    -------
    numpy.ndarray
        The symmetric matrix.
    """
    return m + m.T - np.diag(np.diag(m))


def get_matrix_string(m):
    """
    Returns the matrix as string.
    
    Parameters
    ----------
    m: numpy.ndarray
        The matrix.
    
    Returns
    -------
    str
        The matrix string.
    """
    s = ''
    for row in range(m.shape[0]):
        for col in range(m.shape[1]):
            s = '{} {:5e}\t'.format(s, m[row, col])
        s += '\n'
    return s


def print_matrix(m):
    """
    Prints a matrix.
    
    Parameters
    ----------
    m: numpy.ndarray
        The matrix.
    """
    print(get_matrix_string(m))


def normal_vector_2d(vector):
    """
    Returns the vector standing normal on the given vector in the x-y-plane.
    
    Parameters
    ----------
    vector: Vector
        The given vector.
    
    Returns
    -------
    Vector
        The normal vector.
    """
    vector_3d = Vector([vector.x, vector.y, 0])
    depth_vector_3d = Vector([0, 0, 1])
    normal_vector_3d = Vector(np.cross(vector_3d, depth_vector_3d))
    return Vector([normal_vector_3d.x, normal_vector_3d.y])


def get_shear_principal_axis_stiffness_and_angle(stiffness_matrix):
    """
    Returns the shear principal axis angle and stiffness.

    Parameters
    ----------
    numpy.ndarray
        3x3 cross section stiffness matrix. 1: shear x, 2: shear y, 3: torsion.

    Returns
    -------
    Vector
        Shear principal stiffness.
    float
        Shear principal axis angle in RAD.
    """
    K_1 = stiffness_matrix[0:2, 0:2]
    K_2 = stiffness_matrix[2:3, 2:3]
    K_3 = stiffness_matrix[0:2, 2:3]

    # Pure bending matrix (with the assumption that the normal force is zero)
    K_shear = K_1 - K_3 @ np.linalg.inv(K_2) @ K_3.T
    shear_paa, shear_pas = get_principal_axis_angle(K_shear)

    return shear_pas, shear_paa


def get_elatic_center_and_bending_principal_axis_angle(stiffness_matrix):
    """
    Returns the elastic center and the principal axis angle. [Giavotto1983]_, p. 7 and [BECAS2012]_, pp. 8,9

    Parameters
    ----------
    numpy.ndarray
        3x3 cross section stiffness matrix. 1: extension, 2: bending x, 3: bending y.

    Returns
    -------
    Vector
        Elastic center of the cross section.
    Vector
        Elastic principal second moments of area.
    float
        Principal axis angle in RAD.
    """
    ec = Vector([-stiffness_matrix[0, 2] / stiffness_matrix[0, 0], stiffness_matrix[0, 1] / stiffness_matrix[0, 0]])

    K_1 = stiffness_matrix[0:1, 0:1]
    K_2 = stiffness_matrix[1:3, 1:3]
    K_3 = stiffness_matrix[0:1, 1:3]

    # Pure bending matrix (with the assumption that the normal force is zero)
    K_bending = K_2 - K_3.T @ np.linalg.inv(K_1) @ K_3
    #log.debug(f'K_bending: {K_bending}')
    paa, pas = get_principal_axis_angle(K_bending)

    return ec, pas, paa


def get_principal_axis_angle(stiffness_matrix):
    """
    Returns principal axis angle from a 2x2 matrix. [BECAS2012]_, pp. 8,9
    The first axis is the one with the bigger stiffness (pas[0] > pas[1]).
    
    Parameters
    ----------
    numpy.ndarray
        2x2 stiffness matrix.
    
    Returns
    -------
    float
        Principal axis angle in RAD.
    Vector
        Principal axis stiffness.
    """
    w, v = np.linalg.eigh(stiffness_matrix)
    if w[0] > w[1]: # X-axis has the bigger stiffness
        X = Vector(v[:,0].flatten())
        pas = Vector([w[0], w[1]])
    else:
        X = Vector(v[:,1].flatten())
        pas = Vector([w[1], w[0]])
    return X.angle_in_plane, pas


def modified_kwargs(argsdict, **kwargs):
    res = argsdict.copy()
    for kw, arg in kwargs.items():
        res[kw] = arg
    return res

# TODO: diese Berechnung NICHT im HA-Koos machen!
def calc_shear_center(load_states, shear_atm, shear_atm_inv, transverse_shear=False):
    """
    Returns the shear center of the cross section in the cross section coordinate system.

    Parameters
    ----------
    load_states: dict(IElement, list(float)):
        Load states for an element:
            0: N_zs caused by a unit transverse force in x shear principle direction.
            1: N_zs  caused by a unit transverse force in y shear principle direction.
            2: N_zn caused by a unit transverse force in x shear principle direction.
            3: N_zn caused by a unit transverse force in y shear principle direction.
    shear_atm: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the cross section to the shear principal axis
        coordinate system.
    shear_atm_inv: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the shear principal axis to the cross section
        coordinate system.
    transverse_shear: bool (default: False)
        True, if transverse shear is included in the shear center calculation.

    Returns
    -------
    Vector
        Shear center of the cross section in the cross section coordinate system.
    """
    # TODO: hin- und rücktransformation überhaupt nötig?
    X_sc = 0.
    Y_sc = 0.
    for element in load_states.keys():
        # Element position in the  principal axis coordinate system
        position_element_principal_axis = transform_location(shear_atm, element.midsurface_position)
        position_element_principal_axis_3d = Vector([position_element_principal_axis.x, position_element_principal_axis.y, 0.])
        
        # Element length-vector in the principal axis coordinate system
        del_s = transform_direction(shear_atm, element.length_vector)
        del_s_3d = Vector([del_s.x, del_s.y, 0.])
        
        lever_membrane = np.cross(position_element_principal_axis_3d, del_s_3d)[2]
        
        if transverse_shear:
            # Element thickness-vector in the principal axis coordinate system
            del_n = element.length * transform_direction(shear_atm, element.thickness_vector).normalised
            del_n_3d = Vector([del_n.x, del_n.y, 0.])
            lever_transverse = np.cross(position_element_principal_axis_3d, del_n_3d)[2]
        
        X_sc += load_states[element][1] * lever_membrane +\
                ((load_states[element][3] * lever_transverse) if transverse_shear else 0.)
        Y_sc -= load_states[element][0] * lever_membrane +\
                ((load_states[element][2] * lever_transverse) if transverse_shear else 0.)
        
    # Transform SC from principal axis coordinate system in the cross section coordinate system
    return transform_location(shear_atm_inv, Vector([X_sc, Y_sc]))


def get_poles(cs_processor_list):
    """
    Returns the poles (shear center) of a list of cross section processors.

    Parameters
    ----------
    cs_processor_list: list
        [cs_processor, cs_processor,...]

    Returns
    -------
    poles: list
        list of [(x1, y1, z1), (x2, y2, z2), ...] the poles (load application points) of each cross section.
    """
    poles = []
    for processor in cs_processor_list:
        poles.append([processor.pole.x, processor.pole.y, processor.z_beam])

    return poles


def one(iterable):
    """
    https://stackoverflow.com/a/16801605/10417332
    :param iterable:
    :return:
    """
    i = iter(iterable)
    return any(i) and not any(i)


def dict_to_matrix(d, size):
    # TODO: doc
    m = np.zeros(size)
    for r in range(size[0]):
        for c in range(size[1]):
            m[r, c] = d[(r+1)*10 + (c+1)]
    return m


def export_csv(x, y, name, path):
    """

    Parameter
    ---------
    x: ndarray
        flat ndarray containing the x values
    y: ndarray
        flat ndarray containing the y values
    name: str
        example.csv
    path: str
        os.getcwd()

    """

    xy = np.concatenate([[x], [y]], axis=0)

    pathname = os.path.join(path, name)
    np.savetxt(pathname, xy.T, fmt='%8.2f', delimiter=' ')


def make_linear_function(l, f1, f2):
    def func_linear(s):
        return (f2 - f1) / l * s + f1
    return func_linear


def make_quadratic_function(l, f1, f2, f3):
    def func_quadratic(s):
        a = 2 * (f1 + f2 - 2 * f3) / l ** 2
        b = -(3 * f1 + f2 - 4 * f3) / l
        c = f1
        return a * s * s + b * s + c
    return func_quadratic


def is_number(value):
    """
    Checks, if the object is a number.

    Parameters
    ----------
    value: ?
        The object.

    Returns
    -------
    bool
        True, if value is a number, otherwise False
    """
    try:
        float(value)
        return True
    except:
        return False


def all_close(a, b, **kwargs):
    """
    Checks if all all elements of an array are close. Uses the numpy.isclose() function.
    """
    return np.all(np.isclose(a, b, **kwargs))


def get_matrix_interpolation_function(x_matrices, matrices, **kwargs):
    """
    Creates a matrix of interpolation functions from a list of matrices at given positions
    using spline interpolation for default.

    Parameters
    ----------
    x_matrices: list(float)
        List of coordinates of the matrices.
    matrices: list(numpy.ndarray)
        The matrices to interpolate.
    kwargs:
        kwargs from scipy.interpolate.interp1d. Default values:
            - kind='cubic'
            - fill_value='extrapolate'

    Returns
    -------
    function(float) -> numpy.ndarray
        Matrix interpolation function.
    """
    matrices = np.array(matrices)
    #assert matrices.ndim == 3
    assert len(x_matrices) == matrices.shape[0]

    return interp1d(x_matrices, matrices,
                    axis=0,
                    kind=kwargs.get('kind', 'linear'),
                    fill_value=kwargs.get('fill_value', 'extrapolate'),
                    **kwargs)


def get_interpolated_stiffness_and_inertia_matrices(
        cross_section_data: list[tuple['ICrossSectionStiffness', 'ICrossSectionInertia']],
        z_cross_sections: list[float],
        z_interpolate: list[float]
):
    """
    Interpolate the cross section stiffness and inertia data from `cross_section_data` and `z_cross_sections`
    to the positions given in `z_interpolate` using spline interpolation.

    Parameters
    ----------
    cross_section_data
        List of the cross section data.
    z_cross_sections
        List of z-coordinates of the cross sections.
    z_interpolate
        List of z-coordinates for the interpolated matrices.

    Returns
    -------
    list(numpy.ndarray)
        List of the cross section stiffness matrices.
    list(numpy.ndarray)
        List of the cross section inertia matrices.
    """
    interpolated_stiffness_matrices = get_matrix_interpolation_function(
        z_cross_sections,
        [d[0].stiffness_matrix for d in cross_section_data]
    )(z_interpolate)
    interpolated_inertia_matrices = get_matrix_interpolation_function(
        z_cross_sections,
        [d[1].inertia_matrix for d in cross_section_data]
    )(z_interpolate)
    return interpolated_stiffness_matrices, interpolated_inertia_matrices

def pt_is_in_plane_dir(p0, p_normal, pt):
    """
    Checks if the point pt lies in positive normal direction of the plane defined by the point p0 and normal direction
    p_normal

    Parameters
    ----------
    p0: Vector
        reference point of the plane
    p_normal: Vector
        normal direction of the plane
    pt: Vector
        Point to check

    Returns
    -------
    boolean
        True if the point lies in positive normal direction of the plane or in the plane itself
    """

    # get the intersection point of the point to the plane
    intersection = line_plane_intersection(pt, p_normal, p0, p_normal)

    dir_plane_to_pt = pt - intersection
    dir_plane_to_pt = dir_plane_to_pt.normalised
    if np.allclose(dir_plane_to_pt, p_normal) or all(np.isnan(dir_plane_to_pt)):
        return True
    else: # negative direction
        return False


def line_plane_intersection(l0, l_dir, p0, p_normal, eps = 1e-6):
    """
    Finds the intersection point of the line "l0 + x * l_dir" and the plane, defined by a point and normal direction

    Parameters
    ----------
    l0: Vector
        reference point for line
    l_dir: Vector
        reference direction of the line
    p0: Vector
        reference point of the plane
    p_normal: Vector
        normal direction of the plane

    Returns
    -------
    Vector
        Point of intersection. If no intersection is found, "None" is returned
    """

    l_dot_p = l_dir.dot(p_normal)

    if abs(l_dot_p) > eps:
        w = l0 - p0
        si = -p_normal.dot(w) / l_dot_p
        pt_int = w + si * l_dir + p0

        return pt_int
    else:
        return None


def flatten_sublists(list_):
    return [item for sublist in list_ for item in sublist]


def save_persist_data_json(file: str, data: object, indent: int = 2):
    """
    Saves data as JSON to file.

    Parameters
    ----------
    file
        The file where to save.
    data
        The data.
    indent:
        The intent for the JSON file.
    """
    with open(file, 'w') as f:
        json.dump(data, f, indent=indent)


def load_persist_data_json(file: str) -> object:
    """
    Load data as JSON from a file.

    Parameters
    ----------
    file
        The file.

    Returns
    -------
    object
        The data.
    """
    with open(file, 'r') as f:
        return json.load(f)


def save_persist_data_cloudpickle(file: str, data: object):
    """
    Saves data as cloudpickle to file.

    Parameters
    ----------
    file
        The file where to save.
    data
        The data.
    """
    with open(file, 'wb') as f:
        cloudpickle.dump(data, f)


def load_persist_data_cloudpickle(file: str) -> object:
    """
    Load data as cloudpickle from a file.

    Parameters
    ----------
    file
        The file.

    Returns
    -------
    object
        The data.
    """
    with open(file, 'rb') as f:
        return cloudpickle.load(f)
