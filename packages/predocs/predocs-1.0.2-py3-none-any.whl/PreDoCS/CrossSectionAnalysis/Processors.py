"""
This module contains processors for the calculation of cross section properties.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
from abc import abstractmethod

import numpy as np
from scipy.optimize import minimize_scalar

from PreDoCS.CrossSectionAnalysis.DiscreetCrossSectionGeometry import DiscreetCrossSectionGeometry
from PreDoCS.CrossSectionAnalysis.Interfaces import EulerBernoulliWithTorsionStiffness, \
    TimoschenkoWithRestrainedWarpingStiffness, EulerBernoulliWithTorsionDisplacements, \
    TimoschenkoWithRestrainedWarpingDisplacements, IElementLoadState
from PreDoCS.CrossSectionAnalysis.Interfaces import ICrossSectionProcessor, \
    CrossSectionInertia, IElement
from PreDoCS.MaterialAnalysis.ElementProperties import CompositeElement, IsotropicElement
from PreDoCS.MaterialAnalysis.Materials import get_stiffness_for_material_VCP
from PreDoCS.util.Logging import get_module_logger, DuplicateFilter
from PreDoCS.util.util import create_augmented_transformation_matrix_2d, \
    enclosed_area_vector, get_elatic_center_and_bending_principal_axis_angle, \
    symmetrize, idx, transform_location, transform_direction, \
    calc_shear_center, get_shear_principal_axis_stiffness_and_angle
from PreDoCS.util.vector import Vector

log = get_module_logger(__name__)


def get_element_type_from_cross_section_processor_name(name):
    """
    Returns the element class for the given cross section processor string.

    Parameters
    ----------
    name: str
        Name of the cross section processor ('Song', 'Jung', 'Hybrid', 'Isotropic').

    Returns
    -------
    class <- IElement:
        The element class.
    """
    if name in ['Song', 'Jung', 'Hybrid']:
        return CompositeElement
    elif name == 'Isotropic':
        return IsotropicElement
    else:
        raise RuntimeError('Unknown cross section processor name')


def get_cross_section_processor_from_name(name):
    """
    Returns the cross section processor class for the given cross section processor string.

    Parameters
    ----------
    name: str
        Name of the cross section processor ('Song', 'Jung', 'Hybrid', 'Isotropic').

    Returns
    -------
    class <- ICrossSectionProcessor:
        The cross section processor class.
    """
    if name == 'Song':
        return SongCrossSectionProcessor
    if name == 'Hybrid':
        return HybridCrossSectionProcessor
    elif name == 'Jung':
        return JungCrossSectionProcessor
    elif name == 'Isotropic':
        return IsotropicCrossSectionProcessor
    else:
        raise RuntimeError(f'Unknown cross section processor name "{name}"')


class ElementLoadState(IElementLoadState):
    """
    Stain and stress state of an element.

    Attributes
    ----------
    _strain_state: dict(str, float)
        Stain state of an element.
    _stress_state: dict(str, float)
        Stress state of an element.
    """

    def __init__(self, strain_state, stress_state):
        """
        Constructor.

        Parameters
        ----------
        strain_state: dict(str, float)
            Stain state of an isotropic element.
        stress_state: dict(str, float)
            Stress state of an isotropic element.
        """
        self._strain_state = strain_state
        self._stress_state = stress_state

    @property
    def strain_state(self):
        """dict(str, float): Stain state of an element."""
        return self._strain_state

    @strain_state.setter
    def strain_state(self, value):
        self._strain_state = value

    @property
    def stress_state(self):
        """dict(str, float): Stress state of an element."""
        return self._stress_state

    @stress_state.setter
    def stress_state(self, value):
        self._stress_state = value


class CrossSectionProcessor(ICrossSectionProcessor):
    """
    Represents a basis cross section processor.

    Attributes
    ----------
    _id: int
        Id of the cross section.
    _z_beam: float
        Z-coordinate of the cross section in the beam.

    _update_required: bool
        True, if a new calculation is required.

    _discreet_geometry: DiscreetCrossSectionGeometry
        The discreet geometry of the cross section.
  
    _elastic_center: Vector
        Elastic center of the cross section.
    _principal_axis_angle: float
        Angle between elastic coordinate system and principal axis coordinate system in RAD.
    _shear_center: Vector
        Shear center of the cross section.
   
    _transform_cross_section_to_elastic_atm: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the cross section to the elastic coordinate system.
    _transform_elastic_to_cross_section_atm: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the cross section to the elastic coordinate system.
    _transform_elastic_to_principal_axis_atm: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the elastic to the principal axis coordinate system.
    _transform_principal_axis_to_elastic_atm: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the principal axis to the elastic coordinate system.
    _transform_cross_section_to_principal_axis_atm: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the cross section to the principal axis coordinate system.
    _transform_principal_axis_to_cross_section_atm: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the principal axis to the cross section coordinate system.

    _stiffness: IStiffness
        Stiffness for the cross section.
    _cog: Vector
        Center of gravity of the cross section.
    _inertia: IInertia
        Inertia for the cross section.
    """
    def __init__(self, cross_section_id=0, z_beam=0.0, **kwargs):
        """
        Constructor.

        Parameters
        ----------
        cross_section_id: int (default: 0)
            Id of the cross section.
        z_beam: float (default: 0.0)
            Z-coordinate of the cross section in the beam.
        """
        self._update_required = False
        self._discreet_geometry = None
        self._id = cross_section_id
        self._z_beam = z_beam
        self._shear_center = Vector([0, 0])

    @property
    def id(self):
        """int : Id of the cross section."""
        return self._id

    @property
    def z_beam(self):
        """float: Z-coordinate of the cross section in the beam."""
        return self._z_beam

    @property
    def discreet_geometry(self):
        """DiscreetCrossSectionGeometry: The discreet geometry for the cross section analysis."""
        return self._discreet_geometry
    
    @discreet_geometry.setter
    def discreet_geometry(self, value):
        open_ends = list({n for n in value.nodes if len(list(value.get_neighbor_nodes(n))) == 1})
        assert len(open_ends) == 0, 'Cross Section geometry is not closed. PreDoCS Cross Section Processors only work with closed cross secitons.'
        self._discreet_geometry = value
        self._update_required = True
    
    @abstractmethod
    def _update_if_required(self):
        """
        Update the cached values and does the cross section calculation for all load cases if required.
        """
        pass
        
    @property
    def stiffness(self):
        """ICrossSectionStiffness: Returns the cross section stiffness."""
        self._update_if_required()
        return self._stiffness
    
    @property
    def CoG(self):
        """Vector: Center of gravity of the cross section."""
        self._update_if_required()
        return self._cog

    @property
    def inertia(self):
        """IInertia: Returns the cross section inertia."""
        self._update_if_required()
        return self._inertia

    @property
    def pole(self):
        """
        Vector:
             Rotation pole of the rigid body rotation of the cross section.
        """
        self._update_if_required()
        return self._shear_center

    def _calc_inertia(self):
        """
        See [Chen2010]_, https://en.wikipedia.org/wiki/Moment_of_inertia.
        
        Returns
        -------
        Vector
            Center of gravity of the cross section.
        IInertia
            Returns the cross section inertia.
        """
        mu = 0
        s_x = 0
        s_y = 0
        i_xx = 0
        i_xy = 0
        i_yy = 0
        elements = self._discreet_geometry.elements
        for element in elements:
            l = element.length
            pos1 = element.node1_midsurface_position
            pos2 = element.node2_midsurface_position
            x1 = pos1.x
            y1 = pos1.y
            x2 = pos2.x
            y2 = pos2.y

            int_const = l
            int_x = l/2*(x1+x2)
            int_y = l/2*(y1+y2)
            int_x_x = l/3*(x1**2+x1*x2+x2**2)
            int_y_y = l/3*(y1**2+y1*y2+y2**2)
            int_x_y = l/6*((2*x1+x2)*y1 + (x1+2*x2)*y2)

            # TODO get densitiy from IElement stiffness! There is no need for the usage of material here.
            density_t = element.material.density * element.thickness
            
            mu += density_t * int_const
            s_x += density_t * int_x
            s_y += density_t * int_y
            i_xx += density_t * int_x_x
            i_xy += density_t * int_x_y
            i_yy += density_t * int_y_y
        
        return Vector([s_x/mu, s_y/mu]),\
               CrossSectionInertia(np.array([[mu   , 0     , 0     , 0     , 0     , -s_y      ],
                                             [0    , mu    , 0     , 0     , 0     , s_x       ],
                                             [0    , 0     , mu    , s_y   , -s_x  , 0         ],
                                             [0    , 0     , s_y   , i_yy  , -i_xy , 0         ],
                                             [0    , 0     , -s_x  , -i_xy , i_xx  , 0         ],
                                             [-s_y , s_x   , 0     , 0     , 0     , i_xx+i_yy ]]))
    
    @property
    def elastic_center(self):
        """Vector: Elastic center of the cross section."""
        self._update_if_required()
        return self._elastic_center
    
    @property
    def principal_axis_angle(self):
        """
        float:
            Angle between elastic coordinate system and principal axis coordinate system in RAD.
        """
        self._update_if_required()
        return self._principal_axis_angle
    
    @property
    def shear_center(self):
        """Vector: Shear center of the cross section."""
        self._update_if_required()
        return self._shear_center
    
    def _set_augmented_transformation_matrices(self):
        """
        Calculates the augmented transformation matrices.
        """
        self._transform_cross_section_to_elastic_atm = create_augmented_transformation_matrix_2d(0, -self._elastic_center)
        self._transform_elastic_to_cross_section_atm = np.linalg.inv(self._transform_cross_section_to_elastic_atm)

        self._transform_elastic_to_principal_axis_atm = create_augmented_transformation_matrix_2d(-self._principal_axis_angle, Vector([0, 0]))
        self._transform_principal_axis_to_elastic_atm = np.linalg.inv(self._transform_elastic_to_principal_axis_atm)

        self._transform_cross_section_to_principal_axis_atm = \
            self._transform_elastic_to_principal_axis_atm @ self._transform_cross_section_to_elastic_atm
        self._transform_principal_axis_to_cross_section_atm = np.linalg.inv(self._transform_cross_section_to_principal_axis_atm)

        if hasattr(self, '_shear_center') and hasattr(self, '_shear_principal_axis_angle'):
            cs2shear_atm = create_augmented_transformation_matrix_2d(0, -self._shear_center)
            shear2shear_pa_atm = create_augmented_transformation_matrix_2d(-self._shear_principal_axis_angle, Vector([0, 0]))

            self._transform_cross_section_to_shear_principal_axis_atm = shear2shear_pa_atm @ cs2shear_atm
            self._transform_shear_principal_axis_to_cross_section_atm = np.linalg.inv(self._transform_cross_section_to_shear_principal_axis_atm)

    @property
    def transform_cross_section_to_elastic_atm(self):
        """
        numpy.ndarray:
            Augmented transformation matrix for the affine transformation from the cross section to the elastic coordinate system.
        """
        self._update_if_required()
        return self._transform_cross_section_to_elastic_atm
    
    @property
    def transform_elastic_to_cross_section_atm(self):
        """
        numpy.ndarray:
            Augmented transformation matrix for the affine transformation from the cross section to the elastic coordinate system.
        """
        self._update_if_required()
        return self._transform_elastic_to_cross_section_atm
    
    @property
    def transform_elastic_to_principal_axis_atm(self):
        """
        numpy.ndarray:
            Augmented transformation matrix for the affine transformation from the elastic to the principal axis coordinate system.
        """
        self._update_if_required()
        return self._transform_elastic_to_principal_axis_atm
    
    @property
    def transform_principal_axis_to_elastic_atm(self):
        """
        numpy.ndarray:
            Augmented transformation matrix for the affine transformation from the principal axis to the elastic coordinate system.
        """
        self._update_if_required()
        return self._transform_principal_axis_to_elastic_atm

    @property
    def transform_cross_section_to_principal_axis_atm(self):
        """
        numpy.ndarray:
            Augmented transformation matrix for the affine transformation from the cross section to the principal axis coordinate system.
        """
        self._update_if_required()
        return self._transform_cross_section_to_principal_axis_atm
    
    @property
    def transform_principal_axis_to_cross_section_atm(self):
        """
        numpy.ndarray:
            Augmented transformation matrix for the affine transformation from the principal axis to the cross section coordinate system.
        """
        self._update_if_required()
        return self._transform_principal_axis_to_cross_section_atm

    @staticmethod
    def get_cutted_discreet_geometry_from_discreet_geometry(discreet_geometry):
        """
        Cut all cells of a multicell discreet geometry in such a way that no closed cells remain.

        Parameter
        ---------
        discreet_geometry: DiscreetCrossSectionGeometry
            The uncutted discreet geometry.

        Returns
        -------
        DiscreetCrossSectionGeometry
            The cutted discreet geometry.
        """
        # Cut cells
        cutted_discreet_geometry = discreet_geometry.copy()
        nodes_used = set()

        # For each cell
        segment_border_nodes = set(cutted_discreet_geometry.segment_border_nodes)
        for cell in discreet_geometry.cells:
            # Select cut node
            branch_nodes = {n for n in cutted_discreet_geometry.nodes if
                            len(cutted_discreet_geometry.get_neighbor_nodes(n)) > 2}
            cell_nodes = set(cell.nodes)
            unused_branch_nodes_in_cell = (branch_nodes & cell_nodes) - nodes_used
            if len(unused_branch_nodes_in_cell) > 0:
                cut_node = sorted(unused_branch_nodes_in_cell, key=lambda n: n.id)[0]
            else:
                cut_node = sorted(cell_nodes & segment_border_nodes, key=lambda n: n.id)[0]
            cell.cut_node = cut_node

            # Cut
            nodes_set = set(cutted_discreet_geometry.get_neighbor_nodes(cut_node)) & (cell_nodes - nodes_used)
            neighbors_cut_node = sorted(nodes_set, key=lambda n: n.id)
            # log.debug(f'cut: cut node {cut_node.id}, other node: {neighbors_cut_node[0].id}')
            cutted_discreet_geometry.cut_discreet_geometry(cut_node, neighbors_cut_node[0])
            nodes_used.update(cell_nodes)

        return cutted_discreet_geometry

    def _set_contur_integral_values_recursive(self, contur_integrals_function, contur_integral_names):
        """
        Set the contur integral values.

        Parameters
        ----------
        contur_integrals_function: function
            Function that calculates the contur integral values for one element:
                Parameters
                ----------
                cross_section_processor: CrossSectionProcessor
                    The cross section processor.
                element: IElement
                    The element
                integration_in_element_direction: bool
                    True if the integrations is performed in the element direction.
                last_node: INode
                    Last node.
                current_node: INode
                    Current node.
                last_position: Vector
                    Position of the last node.
                current_position: Vector
                    Position of the current node.
                last_values: dict(str, float)
                    Contur integral values at the last node.

                Returns
                -------
                dict(str, float)
                    Contur integral values at the current node.
                dict(str, float)
                    Contur integral values at the middle of the element.
        contur_integral_names: list(str)
            List of all contur integral names that are calculated by contur_integrals_function.
        """
        # TODO: bei add_branches_on_nodes False hat das Ergebnis des s-Integrals keine Richtung?

        for n in self._cutted_discreet_geometry.nodes:
            n.visited = False

        start_node = self._cutted_discreet_geometry.nodes[0]
        start_node.integral_values.update({name: 0 for name in contur_integral_names})
        self._set_contur_integral_values_rekursive_inner(start_node, contur_integrals_function, contur_integral_names)

    def _set_contur_integral_values_rekursive_inner(self, last_node, contur_integrals_function, contur_integral_names):
        """
        Set the contur integral values.

        Parameters
        ----------
        contur_integrals_function: function
            Function that calculates the contur integral values for one element:
                Parameters
                ----------
                cross_section_processor: CrossSectionProcessor
                    The cross section processor.
                element: IElement
                    The element
                integration_in_element_direction: bool
                    True if the integrations is performed in the element direction.
                last_node: INode
                    Last node.
                current_node: INode
                    Current node.
                last_position: Vector
                    Position of the last node.
                current_position: Vector
                    Position of the current node.
                last_values: dict(str, float)
                    Contur integral values at the last node.

                Returns
                -------
                dict(str, float)
                    Contur integral values at the current node.
                dict(str, float)
                    Contur integral values at the middle of the element.
        contur_integral_names: list(str)
            List of all contur integral names that are calculated by contur_integrals_function.
        """
        neighbor_nodes = [n for n in self._cutted_discreet_geometry.get_neighbor_nodes(last_node) if not n.visited]
        for current_node in neighbor_nodes:

            current_node.visited = True
            element = self._cutted_discreet_geometry.get_element_from_nodes(last_node, current_node)

            element_uncut = [e for e in self._discreet_geometry.elements if element.id == e.id]
            assert len(element_uncut) == 1
            element_uncut = element_uncut[0]


            integration_in_element_direction = element.node1 == last_node
            element_uncut.is_in_global_integration_direction = integration_in_element_direction

            if integration_in_element_direction:
                # Integration in element direction
                last_position = element.node1_midsurface_position
                next_position = element.node2_midsurface_position
            else:
                # Integration against element direction
                last_position = element.node2_midsurface_position
                next_position = element.node1_midsurface_position

            last_values = last_node.integral_values
            l_values, l_half_values = contur_integrals_function(self, element, integration_in_element_direction,
                                                                last_node, current_node,
                                                                last_position, next_position,
                                                                last_values)

            current_node.integral_values.update(l_values)

            if integration_in_element_direction:
                element_uncut.integral_values_0.update(last_values)
                element_uncut.integral_values_l_half.update(l_half_values)
                element_uncut.integral_values_l.update(l_values)
            else:
                element_uncut.integral_values_0.update(l_values)
                element_uncut.integral_values_l_half.update(l_half_values)
                element_uncut.integral_values_l.update(last_values)
                # element_uncut.integral_values_0.update({k: -v for k, v in l_values.items()})
                # element_uncut.integral_values_l_half.update({k: -v for k, v in l_half_values.items()})
                # element_uncut.integral_values_l.update({k: -v for k, v in last_values.items()})

            self._set_contur_integral_values_rekursive_inner(current_node, contur_integrals_function, contur_integral_names)

    def _set_contur_integral_values(self, contur_integrals_function, contur_integral_names):
        """
        Set the contur integral values.

        Parameters
        ----------
        contur_integrals_function: function
            Function that calculates the contur integral values for one element:
                Parameters
                ----------
                cross_section_processor: CrossSectionProcessor
                    The cross section processor.
                element: IElement
                    The element
                integration_in_element_direction: bool
                    True if the integrations is performed in the element direction.
                last_node: INode
                    Last node.
                current_node: INode
                    Current node.
                last_position: Vector
                    Position of the last node.
                current_position: Vector
                    Position of the current node.
                last_values: dict(str, float)
                    Contur integral values at the last node.

                Returns
                -------
                dict(str, float)
                    Contur integral values at the current node.
                dict(str, float)
                    Contur integral values at the middle of the element.
        contur_integral_names: list(str)
            List of all contur integral names that are calculated by contur_integrals_function.
        """
        # TODO: bei add_branches_on_nodes False hat das Ergebnis des s-Integrals keine Richtung?
        for e in self._cutted_discreet_geometry.elements:
            e.visited = False

        for n in self._cutted_discreet_geometry.nodes:
            n.num_visits = 0

        # Free ends
        free_ends = [n for n in self._cutted_discreet_geometry.nodes if
                     len(list(self._cutted_discreet_geometry.get_neighbor_nodes(n))) == 1]
        start_nodes = free_ends
        end_node = start_nodes.pop()

        for start_node in start_nodes:
            # print('Start node: ' + str(start_node.id))
            last_node = start_node
            last_node.num_visited = 1
            last_node.integral_values.update({name: 0 for name in contur_integral_names})
            current_node = self._cutted_discreet_geometry.get_neighbor_nodes(start_node)[0]
            while True:
                element = self._cutted_discreet_geometry.get_element_from_nodes(last_node, current_node)

                element_uncut = [e for e in self._discreet_geometry.elements if element.id == e.id]
                assert len(element_uncut) == 1
                element_uncut = element_uncut[0]

                if element.visited:
                    raise RuntimeError('One element can not be processed more than one time.')

                current_node.num_visits += 1
                element.visited = True

                integration_in_element_direction = element.node1 == last_node
                element_uncut.is_in_global_integration_direction = integration_in_element_direction

                if integration_in_element_direction:
                    # Integration in element direction
                    last_position = element.node1_midsurface_position
                    next_position = element.node2_midsurface_position
                else:
                    # Integration against element direction
                    last_position = element.node2_midsurface_position
                    next_position = element.node1_midsurface_position

                last_values = last_node.integral_values
                l_values, l_half_values = contur_integrals_function(self, element, integration_in_element_direction,
                                                                    last_node, current_node,
                                                                    last_position, next_position,
                                                                    last_values)

                if integration_in_element_direction:
                    element_uncut.integral_values_0.update(last_values)
                    element_uncut.integral_values_l_half.update(l_half_values)
                    element_uncut.integral_values_l.update(l_values)
                else:
                    # TODO: nur relevant für s-Integrale mit Richtung?
                    element_uncut.integral_values_0.update({k: -l_values[k] for k in contur_integral_names
                                                            if k in l_values})
                    element_uncut.integral_values_l_half.update({k: -l_half_values[k] for k in contur_integral_names
                                                                 if k in l_half_values})
                    element_uncut.integral_values_l.update({k: -last_values[k] for k in contur_integral_names
                                                            if k in last_values})

                current_node_neighbors = list(self._cutted_discreet_geometry.get_neighbor_nodes(current_node))
                if len(current_node_neighbors) == 2:
                    # Normal node
                    if current_node.num_visits > 1:
                        raise RuntimeError('A non branch node can be visited only once')
                    current_node.integral_values.update(l_values)

                    # Go on for the path
                    tmp = current_node
                    nodes_set = set(current_node_neighbors) - {last_node}
                    assert len(nodes_set) == 1
                    current_node = nodes_set.pop()
                    last_node = tmp
                elif len(current_node_neighbors) > 2:
                    # Branch node
                    if current_node.num_visits > 1:
                        # Node already visited
                        current_node.integral_values.update({k: current_node.integral_values[k] + v
                                                             for k, v in l_values.items()})
                        if len(current_node_neighbors) == current_node.num_visits:
                            raise RuntimeError('Path finished on a branch node, not allowed')
                        elif len(current_node_neighbors) == current_node.num_visits + 1:
                            # Only one not visited branch, go on for the path
                            # print('Only one not visited branch, go on for the path: ' + str(current_node.id))
                            tmp = current_node
                            current_node = None
                            for node in current_node_neighbors:
                                element = self._cutted_discreet_geometry.get_element_from_nodes(tmp, node)
                                if not element.visited:
                                    current_node = node
                                    break
                            if not current_node:
                                raise RuntimeError('Path finished on a branch node, not allowed (all neighbor nodes already visited)')
                            last_node = tmp
                        else:
                            # Termination condition: Not enough visits
                            # print('Termination condition: Not enough visits: ' + str(current_node.id))
                            break
                    else:
                        # Termination condition: first visit at a branch node
                        # print('Termination condition: first visit at a branch node: ' + str(current_node.id))
                        current_node.integral_values.update(l_values)
                        break
                else:
                    # Free node
                    if not current_node == end_node:
                        raise RuntimeError('Path does not finished at an end node')
                    # print('End node: ' + str(current_node.id))
                    # TODO: Werte müssen gleich sein
                    #if not add_branches_on_nodes:
                        #print('{} must equal {}'.format({k: current_node.integral_values[k] for k in contur_integral_names},
                        #                                {k: l_values[k] for k in contur_integral_names}))
                    break

    @DuplicateFilter(log)
    def update_components(self, component2material, processor_type):
        """
        Update the the processor's component and material properties. Only the abd matrix is needed for skins.

        Parameter
        ---------
        component2material: dict
            Translation dictionary from PreDoCS component to material
        processor_type: str
            The processor type needed for the stiffness calculation
        """
        element_type = get_element_type_from_cross_section_processor_name(processor_type)
        for component in self.discreet_geometry.components:
            if component in component2material:
                # Update material
                component.material = component2material[component]

                # Update material stiffness
                # TODO Think about shifting stiffness to component instead of material.
                component.material.stiffness = get_stiffness_for_material_VCP(component.material, element_type)
            else:
                log.warning(f'Component "{component.id}" with material "{component.material.name}" '
                            #f'from {component.node1.position} to {component.node2.position} '
                            'could not be updated because it is not part of the structural model / optimisation process.')

        # Update processor
        self._update_required = True

    def calc_element_min_max_load_state(self, element, displacements, **kwargs):
        """
        Calculate the minimum and maximum element load states (strain and stress).

        Parameters
        ----------
        element: IElement
            The element.
        displacements: ICrossSectionDisplacements
            Displacements of the cross section.

        Returns
        -------
        (IElementLoadState, IElementLoadState)
            The minimum and maximum load states of the discreet elements of the cross section.
        """
        log.warning('''The generic CrossSectionProcessor.calc_element_min_max_load_state method is very slow.
                        Please overwrite it in every subclass.''')
        load_state = self.calc_element_load_state(element, displacements)

        min_strain_state = {}
        max_strain_state = {}
        for key, func in load_state.strain_state.items():
            min_strain_state[key] = minimize_scalar(func, bounds=(0, element.length), method='bounded').fun
            max_strain_state[key] = minimize_scalar(lambda s: -func(s), bounds=(0, element.length), method='bounded').fun

        min_stress_state = {}
        max_stress_state = {}
        for key, func in load_state.stress_state.items():
            min_stress_state[key] = minimize_scalar(func, bounds=(0, element.length), method='bounded').fun
            max_stress_state[key] = minimize_scalar(lambda s: -func(s), bounds=(0, element.length), method='bounded').fun

        return ElementLoadState(min_strain_state, min_stress_state),\
               ElementLoadState(max_strain_state, max_stress_state)

    def calc_element_min_max_load_states(self, displacements, **kwargs):
        """
        Calculate the minimum and maximum element load states (strain and stress).

        Parameters
        ----------
        displacements: ICrossSectionDisplacements
            Displacements of the cross section.

        Returns
        -------
        dict(IElement, (IElementLoadState, IElementLoadState))
            The minimum and maximum load states of the discreet elements of the cross section.
        """
        self._update_if_required()
        return {e: self.calc_element_min_max_load_state(e, displacements) for e in self.discreet_geometry.elements}


class BaseCompositeCrossSectionProcessor(CrossSectionProcessor):
    """
    Base methods for composite cross section processing.
    
    Attributes
    ----------
    _transform_cross_section_to_shear_principal_axis_atm: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the cross section to the shear principal axis coordinate system.
    _transform_shear_principal_axis_to_cross_section_atm: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the shear principal axis to the cross section coordinate system.
    """
    
    @property
    def transform_cross_section_to_shear_principal_axis_atm(self):
        """
        numpy.ndarray:
            Augmented transformation matrix for the affine transformation from the cross section to the shear principal axis coordinate system.
        """
        self._update_if_required()
        return self._transform_cross_section_to_shear_principal_axis_atm
    
    @property
    def transform_shear_principal_axis_to_cross_section_atm(self):
        """
        numpy.ndarray:
            Augmented transformation matrix for the affine transformation from the shear principal axis to the cross section coordinate system.
        """
        self._update_if_required()
        return self._transform_shear_principal_axis_to_cross_section_atm
    
    def _set_torsional_function_values(self, cells):
        """
        Sets the torsional function values of the elements.

        Parameters
        ----------
        cells: list(Cell)
            List of the cells of the cross section.
        """
        segments = self._discreet_geometry.segments
        num_segments = len(segments)
        
        l = np.array([segment.length for segment in segments])
        alpha = np.array([segment.material.stiffness.torsion_compliance for segment in segments])
        C = np.diag(np.multiply(l, alpha))
        M = BaseCompositeCrossSectionProcessor._get_segment_cell_mapping(segments, cells)
        M_T = M.T
        A_enclosed = enclosed_area_vector(cells)
        
        # Solve LGS
        t = np.linalg.solve(np.dot(np.dot(M, C), M_T), 2. * A_enclosed)

        psi = np.multiply(alpha, np.dot(M_T, t))
        
        # Set the torsional function values to the elements
        for segment_index in range(num_segments):
            segment = segments[segment_index]
            for element in segment.elements:
                if DiscreetCrossSectionGeometry.is_element_in_direction_of_segment(element, segment):
                    element.torsional_function_value = psi[segment_index]
                else:
                    element.torsional_function_value = -psi[segment_index]
    
    def _get_warping(self, pole):
        """
        Returns the warping of the nodes.

        Parameters
        ----------
        pole: Vector
            Rotation pole for the warping calculation.
        
        Returns
        -------
        dict(INode, float)
            Warping for each node.
        """
        nodes = self._discreet_geometry.nodes
        start_node = nodes[0]
        warping_dict = {start_node: 0.}  # INode: float
        for node in set(nodes) - {start_node}:
            path = self._discreet_geometry.get_shortest_path(start_node, node)
            F_w = 0.
            for node_index in range(len(path)-1):
                e = self._discreet_geometry.get_element_from_nodes(path[node_index], path[node_index+1])
                if e.node1 == path[node_index]:
                    # Integration in element direction
                    F_w += (e.r_nodes(pole) - e.torsional_function_value) * e.length
                else:
                    F_w -= (e.r_nodes(pole) - e.torsional_function_value) * e.length
            warping_dict[node] = F_w
        
        return {node: value for (node, value) in warping_dict.items()}
    
    def _set_element_warping(self, node_warpings):
        """
        Sets the warping function values of the elements.
        
        Parameters
        ----------
        node_warpings: dict(INode, float)
            Warping for each node.
        """
        elements = self._discreet_geometry.elements
        for element in elements:
            element.node1_warping = node_warpings[element.node1]
            element.node2_warping = node_warpings[element.node2]

    @staticmethod
    def _get_segment_cell_mapping(segments, cells):
        """
        Returns the segment-cell-mapping matrix with respect to the cell circulating and the segment direction.
        
        Parameters
        ----------
        segments: list(Segments)
            List of segments.
        cells: list(Cell)
            List of cells.
        
        Returns
        -------
        numpy.ndarray
            Segment-cell-mapping matrix.
        """
        num_segments = len(segments)
        num_cells = len(cells)
        Z = np.zeros((num_cells, num_segments))
        # Create mapping matrix
        for cell_index in range(num_cells):
            cell = cells[cell_index]
            for segment_index in range(num_segments):
                segment = segments[segment_index]
            
                if segment in cell.segments:
                    if DiscreetCrossSectionGeometry.is_segment_in_direction_of_cell(segment, cell):
                        Z[cell_index, segment_index] = 1.
                    else:
                        Z[cell_index, segment_index] = -1.
        return Z

    def calc_element_load_states(self, displacements):
        """
        Calculate the element load states (strain and stress) as function of the element contour coordinate.

        Parameters
        ----------
        displacements: ICrossSectionDisplacements
            Displacements of the cross section.

        Returns
        -------
        dict(CompositeElement, CompositeLoadState)
            The load states of the discreet elements of the cross section as function of the element contour coordinate.
        """
        self._update_if_required()
        return {e: self.calc_element_load_state(e, displacements) for e in self.discreet_geometry.elements}

    def calc_load_case(self, internal_loads):
        """
        Calculate the cross section displacements and element states (strain and stress) as function
        of the element contour coordinate for one load case.
        
        Parameters
        ----------
        internal_loads: ICrossSectionLoads
            Cross section internal loads.
        
        Returns
        -------
        ICrossSectionDisplacements
            Displacements of the cross section.
        dict(CompositeElement, CompositeLoadState)
            The load states of the discreet elements of the cross section as function of the element contour coordinate.
        """
        self._update_if_required()
        displacements = self.calc_displacements(internal_loads)
        return displacements, self.calc_element_load_states(displacements)

    def _set_segment_cell_mapping(self, identity_matrix_size, cells):
        """
        Returns the segment-cell-mapping matrix with respect to the cell circulating and the segment direction.

        Parameters
        ----------
        identity_matrix_size: int
            Size of the identity matrix.
        cells: list(Cell) (default: None)
            List of cells.

        Returns
        -------
        numpy.ndarray
            Segment-cell-mapping matrix.
        """
        segments = self._discreet_geometry.segments
        num_cells = len(cells)
        Z_dict = {}
        I = np.identity(identity_matrix_size)

        # Create mapping matrix
        for segment in segments:
            Z = np.zeros((identity_matrix_size, identity_matrix_size*num_cells))
            for cell_index in range(num_cells):
                cell = cells[cell_index]
                if segment in cell.segments:
                    if DiscreetCrossSectionGeometry.is_segment_in_direction_of_cell(segment, cell):
                        Z[:, identity_matrix_size*cell_index:identity_matrix_size*(cell_index+1)] = I
                    else:
                        Z[:, identity_matrix_size*cell_index:identity_matrix_size*(cell_index+1)] = -I
            Z_dict[segment] = Z
        self._Z_dict = Z_dict


class IsotropicCrossSectionProcessor(CrossSectionProcessor):
    """
    Represents a isotropic cross section analysis. The cross section has to be thin-walled and made of isotropic
    material. The discreet geometry has to be made of one or multiple closed sections.
    It is possible to calculate the normal flow per element through extension and bending.
    Furthermore the shear flow through torsion and transverse force is calculated.
    Four displacements(extension, two curvatures, twisting) from the internal loads can be determined.
    The calculations are based of [Mahnken2015]_, pp. 436 and [Wiedemann2007]_, pp. 372-376.

    Coordinate systems:
        * x-y: cross section coordinate system, arbitrary.
        * i-j: elastic coordinate system, same alignment as x-y but origin in the elastic center of the cross section.
        * X-Y: principal axis coordinate system, same origin as i-j but axis alignment to the principal axis.

    Attributes
    ----------
    _cutted_discreet_geometry: DiscreetCrossSectionGeometry
        The cutted discreet geometry of the cross section.

    _EA: float
        Extension stiffness.

    _ES_x: float
        Elastic moment of area around the x-axis.
    _ES_y: float
        Elastic moment of area around the y-axis.

    _EI_x: float
        Elastic second moment of area around the x-axis.
    _EI_y: float
        Elastic second moment of area around the y-axis.
    _EI_xy: float
        Elastic moment of deviation around the x- and y-axis.

    _EI_X: float
        Elastic principal second moment of area around the X-axis.
    _EI_Y: float
        Elastic principal second moment of area around the Y-axis.
    _GI_t: float
        Torsional stiffness of the cross section.

    _stiffness_matrix: numpy.ndarray
        Stiffness matrix for Euler-Bernoulli bending.
    _compliance_matrix: numpy.ndarray
        Complience matrix for Euler-Bernoulli bending.
    """

    def __init__(self, cross_section_id=0, z_beam=0.0, **kwargs):
        """
        Constructor.

        Parameters
        ----------
        cross_section_id: int (default: 0)
            Id of the cross section.
        z_beam: float (default: 0.0)
            Z-coordinate of the cross section in the beam.
        """
        super().__init__(cross_section_id, z_beam)

    def _update_if_required(self):
        """
        Update the cached values.
        """
        if self._update_required:
            self._update_required = False

            self._cog, self._inertia = self._calc_inertia()

            sm = self._get_stiffness_matrix()
            self._stiffness_matrix = sm
            self._compliance_matrix = np.linalg.inv(self._stiffness_matrix)

            self._EA = sm[0, 0]
            self._ES_x = sm[0, 1]
            self._ES_y = -sm[0, 2]
            self._EI_x = sm[1, 1]
            self._EI_y = sm[2, 2]
            self._EI_xy = sm[1, 2]

            # self._elastic_center =  Vector([self._ES_y / self._EA, self._ES_x / self._EA])
            self._elastic_center, psma, self._principal_axis_angle = get_elatic_center_and_bending_principal_axis_angle(
                sm)
            self._EI_X = psma.x
            self._EI_Y = psma.y

            self._set_augmented_transformation_matrices()

            self._GI_t = self._get_torsional_stiffness_and_set_element_shear_flow_from_torsion_distribution()

            self._cutted_discreet_geometry = CrossSectionProcessor.get_cutted_discreet_geometry_from_discreet_geometry(
                self._discreet_geometry)
            self._set_element_shear_flow_from_transverse_force_distribution()

            self._shear_center = calc_shear_center({e: (e.q_X_mean, e.q_Y_mean) for e in self._discreet_geometry.elements},
                                                   self._transform_cross_section_to_principal_axis_atm,
                                                   self._transform_principal_axis_to_cross_section_atm)

            self._stiffness = EulerBernoulliWithTorsionStiffness(self._stiffness_matrix, self._GI_t)

    def _get_stiffness_matrix(self):
        """
        Returns the stiffness matrix of the cross section.

        Returns
        -------
        numpy.ndarray
            3x3 cross section stiffness matrix.
        """
        S_half = np.zeros((3, 3))
        elements = self._discreet_geometry.elements
        for element in elements:
            l = element.length
            x1 = element.node1_midsurface_position.x
            y1 = element.node1_midsurface_position.y
            x2 = element.node2_midsurface_position.x
            y2 = element.node2_midsurface_position.y
            
            E_e = element.material.stiffness.E
            t_e = element.thickness
            
            int_const = l
            int_x = l/2*(x1+x2)
            int_y = l/2*(y1+y2)
            int_x_x = l/3*(x1**2+x1*x2+x2**2)
            int_y_y = l/3*(y1**2+y1*y2+y2**2)
            int_x_y = l/6*((2*x1+x2)*y1 + (x1+2*x2)*y2)
            
            S_half[idx(11)] += E_e*int_const*t_e
            S_half[idx(12)] += E_e*int_y*t_e
            S_half[idx(13)] += -E_e*int_x*t_e
            S_half[idx(22)] += E_e*int_y_y*t_e
            S_half[idx(23)] += -E_e*int_x_y*t_e
            S_half[idx(33)] += E_e*int_x_x*t_e

        return symmetrize(S_half)

    @staticmethod
    def _element_shear_compliance_vector(elements):
        """
        Parameters
        ----------
        elements: list(IsotropicElement)
            List of elements.

        Returns
        -------
        numpy.ndarray
            Vector of the shear compliance of the elements (l/(G*t)).
        """
        S_vector = [element.length / (element.material.stiffness.G * element.thickness) for element in elements]
        return np.array(S_vector)

    @staticmethod
    def _cell_element_mapping(cells, elements):
        """
        Returns the cells-elements mapping matrix with respect to the global machining direction.

        Parameters
        ----------
        cells: list(Cell)
            List of cells.
        elements: list(IsotropicElement)
            List of elements.

        Returns
        -------
        numpy.ndarray
            Cells-elements mapping matrix.
        """
        num_elements = len(elements)
        num_cells = len(cells)
        Z = np.zeros((num_elements, num_cells))

        # Create mapping matrix
        for element_idx in range(num_elements):
            element = elements[element_idx]
            Z_row = np.zeros(num_cells)
            for cell_index in range(num_cells):
                cell = cells[cell_index]
                if element in cell.elements:
                    if DiscreetCrossSectionGeometry.is_element_in_direction_of_elements(element, cell.elements):
                        Z_row[cell_index] = 1.
                    else:
                        Z_row[cell_index] = -1.
            Z[element_idx, :] = Z_row

        return Z

    def _get_torsional_stiffness_and_set_element_shear_flow_from_torsion_distribution(self):
        """
        Calculates the torsional stiffness of the cross section.

        Returns
        -------
        float
            The torsional stiffness of the cross section.
        """
        # Calc shear flow closed cells
        elements = self._discreet_geometry.elements
        cells = self._discreet_geometry.cells
        A_enclosed = enclosed_area_vector(cells)

        # Cell-element mapping matrix (with element directions)
        Z_matrix = IsotropicCrossSectionProcessor._cell_element_mapping(cells, elements)
        Z_T_matrix = np.transpose(Z_matrix)
        S_matrix = np.diag(IsotropicCrossSectionProcessor._element_shear_compliance_vector(
            elements))  # Element shear compliance as diagonal matrix

        # Setup LSG for the distribution of the circulating shear flows to the cells (coeff * q_0/twisting = b)
        coeff = np.dot(Z_T_matrix, np.dot(S_matrix, Z_matrix))
        b = np.multiply(2., A_enclosed)

        # Solve LGS
        torsional_shar_flow_distribution_vector = np.linalg.solve(coeff, b)

        # Torsional stiffness of the cross section
        GI_t = 2. * np.dot(A_enclosed, torsional_shar_flow_distribution_vector)

        # Shear flow per "1"-twisting
        q_t_1 = np.dot(Z_matrix, torsional_shar_flow_distribution_vector)
        for i in range(len(elements)):
            elements[i].q_t_1 = q_t_1[i]

        return GI_t

    @staticmethod
    def _contur_integral_functions(cross_section_processor, element, integration_in_element_direction,
                                   last_node, current_node, last_position, current_position, last_values):
        """
        Calculates the contur integral values for one element.

        Parameters
        ----------
        cross_section_processor: CrossSectionProcessor
            The cross section processor.
        element: IElement
            The element
        integration_in_element_direction: bool
            True if the integrations is performed in the element direction.
        last_node: INode
            Last node.
        current_node: INode
            Current node.
        last_position: Vector
            Position of the last node.
        current_position: Vector
            Position of the current node.
        last_values: dict(str, float)
            Contur integral values at the last node.

        Returns
        -------
        dict(str, float)
            Contur integral values at the current node.
        dict(str, float)
            Contur integral values at the middle of the element.
        """
        # Element position in principal axis coordinate system
        last_pos_principal_axis = transform_location(cross_section_processor._transform_cross_section_to_principal_axis_atm, last_position)
        next_pos_principal_axis = transform_location(cross_section_processor._transform_cross_section_to_principal_axis_atm, current_position)

        x1 = last_pos_principal_axis.x
        x2 = next_pos_principal_axis.x
        y1 = last_pos_principal_axis.y
        y2 = next_pos_principal_axis.y

        l = element.length
        E = element.material.stiffness.E
        t = element.thickness

        l_values = {}
        l_half_values = {}

        l_values['q_c_X'] = last_values['q_c_X'] - t * E * l * (x1 + x2) / 2 / cross_section_processor._EI_Y
        l_values['q_c_Y'] = last_values['q_c_Y'] - t * E * l * (y1 + y2) / 2 / cross_section_processor._EI_X

        l_half_values['q_c_X'] = last_values['q_c_X'] - t * E * l * (3 * x1 + x2) / 8 / cross_section_processor._EI_Y
        l_half_values['q_c_Y'] = last_values['q_c_Y'] - t * E * l * (3 * y1 + y2) / 8 / cross_section_processor._EI_X

        return l_values, l_half_values

    def _set_element_shear_flow_from_transverse_force_distribution(self):
        """
        Calculates the shear flow distribution for the elements trough transverse force in principal axis direction.
        [Wiedemann2007]_, pp. 373-376
        """
        # Clear contur integral values
        for n in self._cutted_discreet_geometry.nodes:
            n.integral_values = dict()
        for e in self._cutted_discreet_geometry.elements:
            e.integral_values_0 = dict()
            e.integral_values_l_half = dict()
            e.integral_values_l = dict()

        # Shear flow at the cutted cross section
        self._set_contur_integral_values(IsotropicCrossSectionProcessor._contur_integral_functions, ['q_c_X', 'q_c_Y'])

        # Shear flow at the closed cross section
        cells = self._discreet_geometry.cells
        elements = self._discreet_geometry.elements
        num_elements = len(elements)
        # Cell-element mapping matrix (with element directions)
        Z_matrix = IsotropicCrossSectionProcessor._cell_element_mapping(cells, elements)
        Z_T_matrix = np.transpose(Z_matrix)
        S_matrix = np.diag(IsotropicCrossSectionProcessor._element_shear_compliance_vector(
            elements))  # Element shear compliance as diagonal matrix

        # Shear flow at the cutted cross section as vector
        q_c_X_vector = np.zeros(num_elements)
        q_c_Y_vector = np.zeros(num_elements)
        for i in range(num_elements):
            element = elements[i]

            q_c_X1 = element.integral_values_0['q_c_X']
            q_c_X2 = element.integral_values_l['q_c_X']
            q_c_X3 = element.integral_values_l_half['q_c_X']
            element.q_X_c_mean = (q_c_X1 + q_c_X2 + 4*q_c_X3)/6
            q_c_X_vector[i] = element.q_X_c_mean

            q_c_Y1 = element.integral_values_0['q_c_Y']
            q_c_Y2 = element.integral_values_l['q_c_Y']
            q_c_Y3 = element.integral_values_l_half['q_c_Y']
            element.q_Y_c_mean = (q_c_Y1 + q_c_Y2 + 4*q_c_Y3)/6
            q_c_Y_vector[i] = element.q_Y_c_mean

        # Setup LSG for the distribution of the circulating shear flows to the cells (coeff * q_0_i = b_i)
        coeff = Z_T_matrix @ S_matrix @ Z_matrix
        b_X = - Z_T_matrix @ S_matrix @ q_c_X_vector
        b_Y = - Z_T_matrix @ S_matrix @ q_c_Y_vector

        # Solve LGS
        q_0_X_vector = np.linalg.solve(coeff, b_X)
        q_0_Y_vector = np.linalg.solve(coeff, b_Y)

        # Resulting shear flow
        delta_q_X_vector = Z_matrix @ q_0_X_vector
        delta_q_Y_vector = Z_matrix @ q_0_Y_vector

        # Set resulting shear flow in the elements
        for i in range(num_elements):
            elements[i].q_X_mean = elements[i].q_X_c_mean + delta_q_X_vector[i]
            elements[i].integral_values_0['q_X'] = elements[i].integral_values_0['q_c_X'] + delta_q_X_vector[i]
            elements[i].integral_values_l['q_X'] = elements[i].integral_values_l['q_c_X'] + delta_q_X_vector[i]
            elements[i].integral_values_l_half['q_X'] = elements[i].integral_values_l_half['q_c_X'] + delta_q_X_vector[i]

            elements[i].q_Y_mean = elements[i].q_Y_c_mean + delta_q_Y_vector[i]
            elements[i].integral_values_0['q_Y'] = elements[i].integral_values_0['q_c_Y'] + delta_q_Y_vector[i]
            elements[i].integral_values_l['q_Y'] = elements[i].integral_values_l['q_c_Y'] + delta_q_Y_vector[i]
            elements[i].integral_values_l_half['q_Y'] = elements[i].integral_values_l_half['q_c_Y'] + delta_q_Y_vector[i]

    def calc_displacements(self, internal_loads):
        """
        Calculate the cross section displacements.

        Parameters
        ----------
        internal_loads: ClassicInternalLoads
            Cross section internal loads.

        Returns
        -------
        EulerBernoulliWithTorsionDisplacements
            Displacements of the cross section.
        """
        self._update_if_required()

        epsilon = np.dot(self._compliance_matrix, np.array(
            [internal_loads.forces.z, internal_loads.moments.x, internal_loads.moments.y])).flatten()

        delta_T = np.cross(-self.shear_center, Vector([internal_loads.forces.x, internal_loads.forces.y]))
        T = internal_loads.moments.z + delta_T
        twisting = T / self._GI_t

        return EulerBernoulliWithTorsionDisplacements(epsilon[0], Vector([epsilon[1], epsilon[2]]), twisting)

    def calc_element_load_state(self, element, displacements, transverse_force=Vector([0, 0])):
        """
       Calculate the element load state (strain and stress) as function of the element contour coordinate.

        Parameters
        ----------
        element: IElement
            The element.
        displacements: EulerBernoulliWithTorsionDisplacements
            Displacements of the cross section.
        transverse_force: Vector (default: Vector([0,0]))
            The transverse force.

        Returns
        -------
        dict(IsotropicElement, IsotropicLoadState)
            The load states of the discreet elements of the cross section.
        """
        self._update_if_required()

        # Transform transverse force into the principal axis coordinate system
        Q_principal_axis = transform_direction(self._transform_cross_section_to_principal_axis_atm, transverse_force)

        l = element.length
        q_X1 = element.integral_values_0['q_X']
        q_X2 = element.integral_values_l['q_X']
        q_X3 = element.integral_values_l_half['q_X']

        q_Y1 = element.integral_values_0['q_Y']
        q_Y2 = element.integral_values_l['q_Y']
        q_Y3 = element.integral_values_l_half['q_Y']

        def x(s): return element.node1_midsurface_position.x + element.dx_ds * s

        def y(s): return element.node1_midsurface_position.y + element.dy_ds * s

        def normal_strain(s): return displacements.extension + displacements.curvature.x * y(s) - \
                                     displacements.curvature.y * x(s)

        def normal_flow(s): return normal_strain(s) * element.thickness * element.material.stiffness.E

        def shear_flow(s):
            return element.q_t_1 * displacements.twisting + \
                                  Q_principal_axis.x * ((q_X1*l**2 - l*s*(3*q_X1 + q_X2 - 4*q_X3) + 2*s**2*(q_X1 + q_X2 - 2*q_X3))/l**2) + \
                                  Q_principal_axis.y * ((q_Y1*l**2 - l*s*(3*q_Y1 + q_Y2 - 4*q_Y3) + 2*s**2*(q_Y1 + q_Y2 - 2*q_Y3))/l**2)

        def shear_strain(s): return shear_flow(s) / element.thickness / element.material.stiffness.G

        return ElementLoadState(
            {'normal_strain': lambda s: element.get_function_with_bounds(normal_strain, s),
             'shear_strain': lambda s: element.get_function_with_bounds(shear_strain, s)},
            {'normal_flow': lambda s: element.get_function_with_bounds(normal_flow, s),
             'shear_flow': lambda s: element.get_function_with_bounds(shear_flow, s)})

    def calc_element_load_states(self, displacements, transverse_force=Vector([0, 0])):
        """
       Calculate the element load states (strain and stress) as function of the element contour coordinate.

        Parameters
        ----------
        displacements: EulerBernoulliWithTorsionDisplacements
            Displacements of the cross section.
        transverse_force: Vector (default: Vector([0,0]))
            The transverse force.

        Returns
        -------
        dict(IsotropicElement, IsotropicLoadState)
            The load states of the discreet elements of the cross section.
        """
        return {e: self.calc_element_load_state(e, displacements, transverse_force)
                for e in self.discreet_geometry.elements}

    def calc_load_case(self, internal_loads):
        """
        Calculate the cross section displacements and element states (strain and stress) as function
        of the element contour coordinate for one load case.

        Parameters
        ----------
        internal_loads: ClassicInternalLoads
            Cross section internal loads.

        Returns
        -------
        EulerBernoulliWithTorsionDisplacements
            Displacements of the cross section.
        dict(IsotropicElement, IsotropicLoadState)
            The load states of the discreet elements of the cross section.
        """
        self._update_if_required()
        displacements = self.calc_displacements(internal_loads)
        return displacements,\
               self.calc_element_load_states(displacements, Vector([internal_loads.forces.x, internal_loads.forces.y]))


class HybridCrossSectionProcessor(CrossSectionProcessor):
    """
    This class is a two in one cross section processor. The main cross section processor is a composite cross section
    processor, but for the calculation of the warping and therefore the rotation pole (shear center)
    of the cross section, the `IsotropicCrossSectionProcessor` ia used.

    Attributes
    ----------
    _main_processor: BaseCompositeCrossSectionProcessor
        The main cross section processor.
    _isotropic_cs_processor: IsotropicCrossSectionProcessor
        The isotropic cross section processor for the shear center calculation.
    """

    def __init__(self, cross_section_id=0, z_beam=0.0, **kwargs):
        """
        Constructor.

        Parameters
        ----------
        cross_section_id: int (default: 0)
            Id of the cross section.
        z_beam: float (default: 0.0)
            Z-coordinate of the cross section in the beam.
        """

        super().__init__(cross_section_id, z_beam)
        if 'hybrid_processor' in kwargs:
            self._main_processor = kwargs['hybrid_processor']
        else:
            self._main_processor = 'Jung'
            log.warning(
                'Main cross section processor unknown. '
                'Hybrid processor initialised with Jung main cross section processor'
            )

    def _update_if_required(self):
        """
        Update the cached values.
        """
        if self._update_required:
            self._update_required = False

            # Do the isotropic calculation (for the shear center)
            isotropic_cs_processor = IsotropicCrossSectionProcessor(self.id, self.z_beam)
            isotropic_cs_processor.discreet_geometry = self.discreet_geometry
            sc_isotropic = isotropic_cs_processor.shear_center
            self._isotropic_cs_processor = isotropic_cs_processor

            # Do the main calculation (for the stiffness matrix and element strains and stresses
            main_cs_processor = get_cross_section_processor_from_name(self._main_processor)(self.id, self.z_beam)
            main_cs_processor.discreet_geometry = self.discreet_geometry
            main_cs_processor._shear_center = sc_isotropic
            main_cs_processor._update_required = True
            self._main_cs_processor = main_cs_processor

            # Copy data from the two cross section processors in this class
            self._stiffness = main_cs_processor.stiffness
            self._cog, self._inertia = self._calc_inertia()
            self._shear_center = sc_isotropic

            self._elastic_center = main_cs_processor.elastic_center
            self._principal_axis_angle = main_cs_processor.principal_axis_angle

            self._transform_cross_section_to_elastic_atm = main_cs_processor.transform_cross_section_to_elastic_atm
            self._transform_elastic_to_cross_section_atm = main_cs_processor.transform_elastic_to_cross_section_atm
            self._transform_elastic_to_principal_axis_atm = main_cs_processor.transform_elastic_to_principal_axis_atm
            self._transform_principal_axis_to_elastic_atm = main_cs_processor.transform_principal_axis_to_elastic_atm
            self._transform_cross_section_to_principal_axis_atm = main_cs_processor.transform_cross_section_to_principal_axis_atm
            self._transform_principal_axis_to_cross_section_atm = main_cs_processor.transform_principal_axis_to_cross_section_atm

            self._transform_cross_section_to_shear_principal_axis_atm = main_cs_processor.transform_cross_section_to_shear_principal_axis_atm
            self._transform_shear_principal_axis_to_cross_section_atm = main_cs_processor.transform_shear_principal_axis_to_cross_section_atm

    @property
    def transform_cross_section_to_shear_principal_axis_atm(self):
        """
        numpy.ndarray:
            Augmented transformation matrix for the affine transformation from the cross section to the shear principal axis coordinate system.
        """
        self._update_if_required()
        return self._transform_cross_section_to_shear_principal_axis_atm

    @property
    def transform_shear_principal_axis_to_cross_section_atm(self):
        """
        numpy.ndarray:
            Augmented transformation matrix for the affine transformation from the shear principal axis to the cross section coordinate system.
        """
        self._update_if_required()
        return self._transform_shear_principal_axis_to_cross_section_atm

    def calc_element_load_states(self, displacements):
        """
        Calculate the element load states (strain and stress) as function of the element contour coordinate.

        Parameters
        ----------
        displacements: TimoschenkoWithRestrainedWarpingDisplacements
            Displacements of the cross section.

        Returns
        -------
        dict(CompositeElement, CompositeLoadState)
            The load states of the discreet elements of the cross section as function of the element contour coordinate.
        """
        return {e: self.calc_element_load_state(e, displacements) for e in self.discreet_geometry.elements}

    def calc_load_case(self, internal_loads):
        """
        Calculate the cross section displacements and element states (strain and stress) as function
        of the element contour coordinate for one load case.

        Parameters
        ----------
        internal_loads: ClassicCrossSectionLoadsWithBimoment
            Cross section internal loads.

        Returns
        -------
        TimoschenkoWithRestrainedWarpingDisplacements
            Displacements of the cross section.
        dict(CompositeElement, CompositeLoadState)
            The load states of the discreet elements of the cross section as function of the element contour coordinate.
        """
        self._update_if_required()
        displacements = self.calc_displacements(internal_loads)
        return displacements, self.calc_element_load_states(displacements)

    def calc_displacements(self, internal_loads):
        """
        Calculate the cross section displacements.

        Parameters
        ----------
        internal_loads: ClassicCrossSectionLoadsWithBimoment
            Cross section internal loads.

        Returns
        -------
        TimoschenkoWithRestrainedWarpingDisplacements
            Displacements of the cross section.
        """
        self._update_if_required()
        return self._main_cs_processor.calc_displacements(internal_loads)

    def calc_element_load_state(self, element, displacements):
        """
        Calculate the element load state (strain and stress) as function of the element contour coordinate.

        Parameters
        ----------
        element: CompositeElement
            The element.
        displacements: TimoschenkoWithRestrainedWarpingDisplacements
            Displacements of the cross section.

        Returns
        -------
        dict(CompositeElement, CompositeLoadState)
            The load states of the discreet elements of the cross section as function of the element contour coordinate.
        """
        self._update_if_required()
        return self._main_cs_processor.calc_element_load_state(element, displacements)

    def calc_element_min_max_load_state(self, element, displacements):
        """
        Calculate the minimum and maximum element load states (strain and stress).

        Parameters
        ----------
        element: IElement
            The element.
        displacements: ICrossSectionDisplacements
            Displacements of the cross section.

        Returns
        -------
        (IElementLoadState, IElementLoadState)
            The minimum and maximum load states of the discreet elements of the cross section.
        """
        self._update_if_required()
        return self._main_cs_processor.calc_element_min_max_load_state(element, displacements)


class SongCrossSectionProcessor(BaseCompositeCrossSectionProcessor):
    """
    Represents a anisotropic cross section analysis for thin-walled composite structures.
    The discreet geometry has to be made of one or multiple closed cells. The contour elements are under
    plate load and transverse shear. Seven displacements(three strains, tree curvatures, derivation of twisting)
    from the internal loads can be determined. The calculations are based of
    [Song1990]_, [Qin2002]_ and [Librescu1991]_.
    
    Coordinate systems:
        * x-y: cross section coordinate system, arbitrary.
        
    Attributes
    ----------
    _stiffness_matrix: numpy.ndarray
        Timoschenko bending with restrained warping stiffness matrix (7x7).
    _compliance_matrix: numpy.ndarray
        Timoschenko bending with restrained warping complience matrix (7x7).
    _transform_cross_section_to_shear_principal_axis_atm: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the cross section to the shear principal axis coordinate system.
    _transform_shear_principal_axis_to_cross_section_atm: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the shear principal axis to the cross section coordinate system.
    """
    def __init__(self, cross_section_id=0, z_beam=0.0, **kwargs):
        """
        Constructor.

        Parameters
        ----------
        cross_section_id: int (default: 0)
            Id of the cross section.
        z_beam: float (default: 0.0)
            Z-coordinate of the cross section in the beam.
        """
        super().__init__(cross_section_id, z_beam)

    def _update_if_required(self):
        """
        Update the cached values and does the cross section calculation for all load cases if required.
        """
        if self._update_required:
            self._update_required = False
            
            self._cog, self._inertia = self._calc_inertia()
            
            self._set_torsional_function_values(self._discreet_geometry.cells)

            E_3 = np.identity(3)
            pole = self.pole
            node_warpings_true_pole = self._get_warping(pole)
            stiffness_matrix_elastic_true_pole = self._get_stiffness_matrix(True, E_3, pole, node_warpings_true_pole)
            Pi = -stiffness_matrix_elastic_true_pole[idx(37)]/stiffness_matrix_elastic_true_pole[idx(33)]
            node_warpings = {node: value - Pi for (node, value) in node_warpings_true_pole.items()}
            self._set_element_warping(node_warpings)
            
            self._stiffness_matrix = self._get_stiffness_matrix(True, E_3, pole, node_warpings)
            self._compliance_matrix = np.linalg.inv(self._stiffness_matrix)
            self._stiffness = TimoschenkoWithRestrainedWarpingStiffness(self._stiffness_matrix)

            self._elastic_center, psma, self._principal_axis_angle = get_elatic_center_and_bending_principal_axis_angle(self._stiffness_matrix[2:5, 2:5])
            self._shear_principal_axis_angle = self._principal_axis_angle
            self._set_augmented_transformation_matrices()

    def _get_stiffness_matrix(self, warping_part, atm, pole, node_warpings):
        """
        Returns the stiffness matrix of the cross section.
        
        Parameters
        ----------
        warping_part: bool
            If True, the last row and column (restrained warping) is calculated.
        atm: numpy.ndarray
            Augmented transformation matrix into the coordinate system for the stiffness calculation.
        pole: Vector
            Rotation pole of the rigid body rotation of the cross section. Not yet transformed.
        node_warpings: dict(INode, float)
            Warping for each node.
        
        Returns
        -------
        numpy.ndarray
            7x7 cross section stiffness matrix.
        """
        S_half = np.zeros((7, 7))
        if warping_part:
            pole = transform_location(atm, pole)
        elements = self._discreet_geometry.elements
        for element in elements:
            l = element.length
            pos1 = transform_location(atm, element.node1_midsurface_position)
            pos2 = transform_location(atm, element.node2_midsurface_position)
            x1 = pos1.x
            y1 = pos1.y
            x2 = pos2.x
            y2 = pos2.y
            dx_ds = (x2-x1)/l
            dy_ds = (y2-y1)/l
            psi_e = element.torsional_function_value
            
            if warping_part:
                a1 = -(y1-pole.y)*dy_ds - (x1-pole.x)*dx_ds
                a2 = -(y2-pole.y)*dy_ds - (x2-pole.x)*dx_ds
                F_w1 = node_warpings[element.node1]
                F_w2 = node_warpings[element.node2]
            
            K = element.material.stiffness.K_Song
            A_s = element.material.stiffness.A_s

            int_const = l
            int_x = l/2*(x1+x2)
            int_y = l/2*(y1+y2)
            int_x_x = l/3*(x1**2+x1*x2+x2**2)
            int_y_y = l/3*(y1**2+y1*y2+y2**2)
            int_x_y = l/6*((2*x1+x2)*y1 + (x1+2*x2)*y2)
            
            if warping_part:
                int_a = l/2*(a1+a2)
                int_x_a = l/6*((2*a1+a2)*x1 + (a1+2*a2)*x2)
                int_y_a = l/6*((2*a1+a2)*y1 + (a1+2*a2)*y2)
                int_a_a = l/3*(a1**2+a1*a2+a2**2)
                int_F_w = l/2*(F_w1+F_w2)
                int_x_F_w = l/6*((2*F_w1+F_w2)*x1 + (F_w1+2*F_w2)*x2)
                int_y_F_w = l/6*((2*F_w1+F_w2)*y1 + (F_w1+2*F_w2)*y2)
                int_F_w_a = l/6*((2*F_w1+F_w2)*a1 + (F_w1+2*F_w2)*a2)
                int_F_w_F_w = l/3*(F_w1**2+F_w1*F_w2+F_w2**2)
            
            S_half[idx(11)] += (K[22]*dx_ds**2 + A_s[44]*dy_ds**2)*int_const
            S_half[idx(12)] += -(A_s[44] - K[22])*dx_ds*dy_ds*int_const
            S_half[idx(13)] += K[21]*dx_ds*int_const
            S_half[idx(14)] += -K[23]*dx_ds**2*int_const + K[21]*dx_ds*int_y
            S_half[idx(15)] += -K[23]*dx_ds*dy_ds*int_const - K[21]*dx_ds*int_x
            S_half[idx(16)] += K[22]*dx_ds*int_const*psi_e
            S_half[idx(22)] += (A_s[44]*dx_ds**2 + K[22]*dy_ds**2)*int_const
            S_half[idx(23)] += K[21]*dy_ds*int_const
            S_half[idx(24)] += -K[23]*dx_ds*dy_ds*int_const + K[21]*dy_ds*int_y
            S_half[idx(25)] += -K[23]*dy_ds**2*int_const - K[21]*dy_ds*int_x
            S_half[idx(26)] += K[22]*dy_ds*int_const*psi_e
            S_half[idx(33)] += K[11]*int_const
            S_half[idx(34)] += -K[13]*dx_ds*int_const + K[11]*int_y
            S_half[idx(35)] += -K[13]*dy_ds*int_const - K[11]*int_x
            S_half[idx(36)] += K[12]*int_const*psi_e
            S_half[idx(44)] += K[43]*dx_ds**2*int_const - (K[13] + K[41])*dx_ds*int_y + K[11]*int_y_y
            S_half[idx(45)] += K[43]*dx_ds*dy_ds*int_const + K[41]*dx_ds*int_x - K[13]*dy_ds*int_y - K[11]*int_x_y
            S_half[idx(46)] += -(K[42]*dx_ds*int_const - K[12]*int_y)*psi_e
            S_half[idx(55)] += K[43]*dy_ds**2*int_const + (K[13] + K[41])*dy_ds*int_x + K[11]*int_x_x
            S_half[idx(56)] += -(K[42]*dy_ds*int_const + K[12]*int_x)*psi_e
            S_half[idx(66)] += K[22]*int_const*psi_e**2

            if warping_part:
                S_half[idx(17)] += -K[21]*dx_ds*int_F_w - K[23]*dx_ds*int_a
                S_half[idx(27)] += -K[21]*dy_ds*int_F_w - K[23]*dy_ds*int_a
                S_half[idx(37)] += -K[11]*int_F_w - K[13]*int_a
                S_half[idx(47)] += K[41]*dx_ds*int_F_w + K[43]*dx_ds*int_a - K[11]*int_y_F_w - K[13]*int_y_a
                S_half[idx(57)] += K[41]*dy_ds*int_F_w + K[43]*dy_ds*int_a + K[11]*int_x_F_w + K[13]*int_x_a
                S_half[idx(67)] += -(K[21]*int_F_w + K[23]*int_a)*psi_e
                S_half[idx(77)] += K[11]*int_F_w_F_w + (K[13] + K[41])*int_F_w_a + K[43]*int_a_a

        return symmetrize(S_half)
    
    def calc_displacements(self, internal_loads):
        """
        Calculate the cross section displacements.
        
        Parameters
        ----------
        internal_loads: ClassicCrossSectionLoadsWithBimoment
            Cross section internal loads.
        
        Returns
        -------
        TimoschenkoWithRestrainedWarpingDisplacements
            Displacements of the cross section.
        """
        self._update_if_required()
        load_vector = np.append(internal_loads.forces, np.append(internal_loads.moments, internal_loads.bimoment))
        displacements = np.dot(self._compliance_matrix, load_vector).flatten()
        return TimoschenkoWithRestrainedWarpingDisplacements(Vector(displacements[0:3]), Vector(displacements[3:6]),
                                                             displacements[6])

    def calc_element_load_state(self, element, displacements):
        """
        Calculate the element load state (strain and stress) as function of the element contour coordinate.

        Parameters
        ----------
        element: IElement
            The element.
        displacements: TimoschenkoWithRestrainedWarpingDisplacements
            Displacements of the cross section.

        Returns
        -------
        dict(CompositeElement, CompositeLoadState)
            The load states of the discreet elements of the cross section as function of the element contour coordinate.
        """
        self._update_if_required()

        dx_ds = element.dx_ds
        dy_ds = element.dy_ds

        def x(s): return element.node1_midsurface_position.x + dx_ds * s

        def y(s): return element.node1_midsurface_position.y + dy_ds * s

        def warping(s): return element.node1_warping + (element.node2_warping - element.node1_warping) * s / element.length

        # Displacements
        gamma_xz = displacements.strain[0]
        gamma_yz = displacements.strain[1]
        w_0_d = displacements.strain[2]
        Theta_x_d = displacements.curvature[0]
        Theta_y_d = displacements.curvature[1]
        phi_d = displacements.curvature[2]
        phi_dd = displacements.twisting_derivation

        # Strain state: kinematic
        def epsilon_zz_0(s): return w_0_d + - Theta_y_d * x(s) + Theta_x_d * y(s) - phi_dd * warping(s)

        def kappa_zz(s): return - Theta_y_d * dy_ds - Theta_x_d * dx_ds - phi_dd * element.q(s, self.pole)

        def gamma_zs(s): return gamma_xz * dx_ds + gamma_yz * dy_ds + element.torsional_function_value * phi_d

        def gamma_zn(s): return gamma_xz * dy_ds - gamma_yz * dx_ds

        strain_state = {'epsilon_zz_0': lambda s: element.get_function_with_bounds(epsilon_zz_0, s),
                        'gamma_zs': lambda s: element.get_function_with_bounds(gamma_zs, s),
                        'kappa_zz': lambda s: element.get_function_with_bounds(kappa_zz, s),
                        'gamma_zn': lambda s: element.get_function_with_bounds(gamma_zn, s)}

        # Stress state: material laws
        stress_state = element.material.stiffness.stress_state_from_strain_state_function(strain_state)

        # Load state
        return ElementLoadState(strain_state, stress_state)


class JungCrossSectionProcessor(BaseCompositeCrossSectionProcessor):
    """
    Represents a anisotropic cross section analysis for thin-walled composite structures.
    The geometry has to be made of one or multiple closed sections. The contour elements are
    under plate load and transverse shear. Seven displacements(three strains, tree curvatures, derivation of twisting)
    from the internal loads can be determined. The calculations are based of [Jung2002b]_.

    Attributes
    ----------
    _stiffness_matrix: numpy.ndarray
        Timoschenko bending with restrained warping stiffness matrix (7x7).
    _compliance_matrix: numpy.ndarray
        Timoschenko bending with restrained warping complience matrix (7x7).
    _transform_cross_section_to_shear_principal_axis_atm: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the cross section to the shear principal axis coordinate system.
    _transform_shear_principal_axis_to_cross_section_atm: numpy.ndarray
        Augmented transformation matrix for the affine transformation from the shear principal axis to the cross section coordinate system.

    _Q, _P, _R: numpy.ndarray
        Matrices for the calcualtion of the cucualting shear flows.
    _b, _B: numpy.ndarray
        Matrices for intermediate calcualtion.
    _p: numpy.ndarray
        MAtrix for the shear correction.
    _K_bb, _K_bv, _K_vv: numpy.ndarray
        Parts of the stiffness matrix.
    """

    def __init__(self, cross_section_id=0, z_beam=0.0, **kwargs):
        """
        Constructor.

        Parameters
        ----------
        cross_section_id: int (default: 0)
            Id of the cross section.
        z_beam: float (default: 0.0)
            Z-coordinate of the cross section in the beam.
        """
        super().__init__(cross_section_id, z_beam)

    def _update_if_required(self):
        """
        Update the cached values.
        """
        if self._update_required:
            self._update_required = False

            self._cog, self._inertia = self._calc_inertia()

            cells = self._discreet_geometry.cells

            self._set_torsional_function_values(cells)
            self._cutted_discreet_geometry = CrossSectionProcessor.get_cutted_discreet_geometry_from_discreet_geometry(
                self._discreet_geometry)

            # Clear contur integral values
            for n in self._cutted_discreet_geometry.nodes:
                n.integral_values = dict()
            for e in self._cutted_discreet_geometry.elements:
                e.integral_values_0 = dict()
                e.integral_values_l_half = dict()
                e.integral_values_l = dict()

            # Calculate warping
            self._set_contur_integral_values_recursive(JungCrossSectionProcessor._contur_integral_functions_warping,
                                                       ['int_rtorsional_ds'])

            int_omega_ds = 0.
            int_ds = 0.
            for e in self._discreet_geometry.elements:
                int_omega_ds += (e.integral_values_0['int_rtorsional_ds'] +\
                                 e.integral_values_l['int_rtorsional_ds']) / 2. * e.length
                int_ds += e.length

            omega_offset = - int_omega_ds / int_ds
            for n in self.discreet_geometry.nodes:
                n.integral_values['int_rtorsional_ds'] += omega_offset
            for e in self.discreet_geometry.elements:
                e.integral_values_0['int_rtorsional_ds'] += omega_offset
                e.integral_values_l['int_rtorsional_ds'] += omega_offset

            self._set_contur_integral_values(JungCrossSectionProcessor._contur_integral_functions,
                                             ['int_A11_ds',
                                              'int_B16_ds',
                                              'int_D16_ds',
                                              'int_A11_x_ds',
                                              'int_A11_y_ds',
                                              'int_A11_omega_ds',
                                              'int_B16_x_ds',
                                              'int_B16_y_ds',
                                              'int_B16_omega_ds'])

            self._set_segment_cell_mapping(4, cells)

            # Set H matrices to elements
            for segment, Z in self._Z_dict.items():
                for element in segment.elements:
                    if DiscreetCrossSectionGeometry.is_element_in_direction_of_segment(element, segment):
                        element.Z = Z
                    else:
                        element.Z = -Z

            self._set_cell_matrices(cells)

            # Solve ist faster than using inverse of Q
            self._b = np.linalg.solve(self._Q, self._P)
            self._B = np.linalg.solve(self._Q, self._R)

            for e in self._discreet_geometry.elements:
                e.b = e.Z @ self._b
                e.B = e.Z @ self._B

            self._set_cross_section_matrix_K_bb()

            # TODO: nicht invertieren sondern LGS lösen, K_bb ist schlecht konditioniert
            self._K_bb_inv = np.linalg.inv(self._K_bb)

            self._set_element_f_r_matrices()

            self._set_cross_section_matrix_p()

            self._set_cross_section_matrices_K_vv_and_K_bv()

            p1 = self._p[:, 0:5]
            p2 = self._p[:, 5:7]

            K_bb = self._K_bb
            K_vv = self._K_vv
            K_bv = self._K_bv

            K11 = K_bb + 2 * K_bv @ p1 + p1.T @ K_vv @ p1
            K12 = K_bv @ p2 + p1.T @ K_vv @ p2
            K22 = p2.T @ K_vv @ p2

            K = np.vstack((np.hstack((K11, K12)), np.hstack((K12.T, K22))))

            # Rearrange the K matrix: shear stiffness from the back to the front
            V = np.zeros((7, 7))
            ones = ((0, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 0), (6, 1))
            for r, c in ones:
                V[r, c] = 1.
            K = V.T @ K @ V

            self._stiffness_matrix = K
            self._compliance_matrix = np.linalg.inv(self._stiffness_matrix)
            self._stiffness = TimoschenkoWithRestrainedWarpingStiffness(self._stiffness_matrix)

            self._elastic_center, self._principal_axis_stiffness, self._principal_axis_angle = \
                get_elatic_center_and_bending_principal_axis_angle(self._stiffness_matrix[2:5, 2:5])

            # TODO: stimmt das so?
            self._shear_principal_axis_stiffness, self._shear_principal_axis_angle = \
                get_shear_principal_axis_stiffness_and_angle(self._stiffness_matrix[0:3, 0:3])

            self._set_augmented_transformation_matrices()

    def _set_cell_matrices(self, cells):
        """
        Set the Q, P and R matrices.

        Parameters
        ----------
        cells: list(Cell)
            List of cells.
        """
        num_cells = len(cells)

        Q = np.zeros((4*num_cells, 4*num_cells))
        P = np.zeros((4*num_cells, 5))
        R = np.zeros((4*num_cells, 5))

        for cell_idx in range(num_cells):
            cell = cells[cell_idx]
            Q_cell = np.zeros((4, 4*num_cells))
            P_cell = np.zeros((4, 5))
            R_cell = np.zeros((4, 5))
            A_i = cell.area
            elements = cell.elements
            for element in elements:
                is_element_in_direction_of_cell = DiscreetCrossSectionGeometry.is_element_in_direction_of_elements(
                    element, cell.elements
                )
                direction_factor = 1. if is_element_in_direction_of_cell else -1.
                direction_factor_global = (1. if element.is_in_global_integration_direction else -1.) * direction_factor

                l = element.length
                C = element.material.stiffness.K_Jung
                Z_element = element.Z

                pos1 = element.node1_midsurface_position
                pos2 = element.node2_midsurface_position

                omega1 = element.node1.integral_values['int_rtorsional_ds']
                omega2 = element.node2.integral_values['int_rtorsional_ds']

                x1 = pos1.x
                x2 = pos2.x
                y1 = pos1.y
                y2 = pos2.y

                int_A11_ds1 = direction_factor_global * element.integral_values_0['int_A11_ds']
                int_A11_ds2 = direction_factor_global * element.integral_values_l['int_A11_ds']
                int_B16_ds1 = direction_factor_global * element.integral_values_0['int_B16_ds']
                int_B16_ds2 = direction_factor_global * element.integral_values_l['int_B16_ds']
                int_D16_ds1 = direction_factor_global * element.integral_values_0['int_D16_ds']
                int_D16_ds2 = direction_factor_global * element.integral_values_l['int_D16_ds']
                int_A11_x_ds1 = direction_factor_global * element.integral_values_0['int_A11_x_ds']
                int_A11_x_ds2 = direction_factor_global * element.integral_values_l['int_A11_x_ds']
                int_A11_y_ds1 = direction_factor_global * element.integral_values_0['int_A11_y_ds']
                int_A11_y_ds2 = direction_factor_global * element.integral_values_l['int_A11_y_ds']
                int_A11_omega_ds1 = direction_factor_global * element.integral_values_0['int_A11_omega_ds']
                int_A11_omega_ds2 = direction_factor_global * element.integral_values_l['int_A11_omega_ds']
                int_B16_x_ds1 = direction_factor_global * element.integral_values_0['int_B16_x_ds']
                int_B16_x_ds2 = direction_factor_global * element.integral_values_l['int_B16_x_ds']
                int_B16_y_ds1 = direction_factor_global * element.integral_values_0['int_B16_y_ds']
                int_B16_y_ds2 = direction_factor_global * element.integral_values_l['int_B16_y_ds']
                int_B16_omega_ds1 = direction_factor_global * element.integral_values_0['int_B16_omega_ds']
                int_B16_omega_ds2 = direction_factor_global * element.integral_values_l['int_B16_omega_ds']
                int_A11_x_ds3 = direction_factor_global * element.integral_values_l_half['int_A11_x_ds']
                int_A11_y_ds3 = direction_factor_global * element.integral_values_l_half['int_A11_y_ds']
                int_A11_omega_ds3 = direction_factor_global * element.integral_values_l_half['int_A11_omega_ds']
                int_B16_x_ds3 = direction_factor_global * element.integral_values_l_half['int_B16_x_ds']
                int_B16_y_ds3 = direction_factor_global * element.integral_values_l_half['int_B16_y_ds']
                int_B16_omega_ds3 = direction_factor_global * element.integral_values_l_half['int_B16_omega_ds']

                Q_element_half = np.zeros((4, 4))
                P_element = np.zeros((4, 5))
                R_element = np.zeros((4, 5))

                Q_element_half[0, 0] = C[3, 3] * l
                Q_element_half[0, 1] = C[4, 3] * l
                Q_element_half[0, 2] = (1 / 2) * C[4, 3] * l * x1 + (1 / 2) * C[4, 3] * l * x2
                Q_element_half[0, 3] = (1 / 2) * C[4, 3] * l * y1 + (1 / 2) * C[4, 3] * l * y2
                Q_element_half[1, 1] = C[4, 4] * l
                Q_element_half[1, 2] = (1 / 2) * C[4, 4] * l * x1 + (1 / 2) * C[4, 4] * l * x2
                Q_element_half[1, 3] = (1 / 2) * C[4, 4] * l * y1 + (1 / 2) * C[4, 4] * l * y2
                Q_element_half[2, 2] = (1 / 3) * C[4, 4] * l * x1 ** 2 + (1 / 3) * C[4, 4] * l * x1 * x2 + (1 / 3) * C[
                    4, 4] * l * x2 ** 2
                Q_element_half[2, 3] = (1 / 3) * C[4, 4] * l * x1 * y1 + (1 / 6) * C[4, 4] * l * x1 * y2 + (1 / 6) * C[
                    4, 4] * l * x2 * y1 + (1 / 3) * C[4, 4] * l * x2 * y2
                Q_element_half[3, 3] = (1 / 3) * C[4, 4] * l * y1 ** 2 + (1 / 3) * C[4, 4] * l * y1 * y2 + (1 / 3) * C[
                    4, 4] * l * y2 ** 2

                P_element[0, 0] = C[0, 3] * l
                P_element[0, 1] = (1 / 2) * C[0, 3] * l * y1 + (1 / 2) * C[0, 3] * l * y2 - C[3, 1] * x1 + C[3, 1] * x2
                P_element[0, 2] = (1 / 2) * C[3, 0] * l * x1 + (1 / 2) * C[3, 0] * l * x2 - C[3, 1] * y1 + C[3, 1] * y2
                P_element[0, 3] = 2 * C[2, 3] * l
                P_element[0, 4] = (1 / 2) * C[1, 3] * x1 ** 2 - 1 / 2 * C[1, 3] * x2 ** 2 + (1 / 2) * C[
                    1, 3] * y1 ** 2 - 1 / 2 * C[1, 3] * y2 ** 2 + (1 / 2) * C[3, 0] * l * omega1 + (1 / 2) * C[
                                      3, 0] * l * omega2
                P_element[1, 0] = C[0, 4] * l
                P_element[1, 1] = (1 / 2) * C[0, 4] * l * y1 + (1 / 2) * C[0, 4] * l * y2 - C[4, 1] * x1 + C[4, 1] * x2
                P_element[1, 2] = (1 / 2) * C[4, 0] * l * x1 + (1 / 2) * C[4, 0] * l * x2 - C[4, 1] * y1 + C[4, 1] * y2
                P_element[1, 3] = 2 * C[2, 4] * l
                P_element[1, 4] = (1 / 2) * C[1, 4] * x1 ** 2 - 1 / 2 * C[1, 4] * x2 ** 2 + (1 / 2) * C[
                    1, 4] * y1 ** 2 - 1 / 2 * C[1, 4] * y2 ** 2 + (1 / 2) * C[4, 0] * l * omega1 + (1 / 2) * C[
                                      4, 0] * l * omega2
                P_element[2, 0] = (1 / 2) * C[0, 4] * l * x1 + (1 / 2) * C[0, 4] * l * x2
                P_element[2, 1] = (1 / 3) * C[0, 4] * l * x1 * y1 + (1 / 6) * C[0, 4] * l * x1 * y2 + (1 / 6) * C[
                    0, 4] * l * x2 * y1 + (1 / 3) * C[0, 4] * l * x2 * y2 - 1 / 2 * C[4, 1] * x1 ** 2 + (1 / 2) * C[
                                      4, 1] * x2 ** 2
                P_element[2, 2] = (1 / 3) * C[4, 0] * l * x1 ** 2 + (1 / 3) * C[4, 0] * l * x1 * x2 + (1 / 3) * C[
                    4, 0] * l * x2 ** 2 - 1 / 2 * C[4, 1] * x1 * y1 + (1 / 2) * C[4, 1] * x1 * y2 - 1 / 2 * C[
                                      4, 1] * x2 * y1 + (1 / 2) * C[4, 1] * x2 * y2
                P_element[2, 3] = C[2, 4] * l * x1 + C[2, 4] * l * x2
                P_element[2, 4] = (1 / 3) * C[1, 4] * x1 ** 3 + (1 / 3) * C[1, 4] * x1 * y1 ** 2 - 1 / 6 * C[
                    1, 4] * x1 * y1 * y2 - 1 / 6 * C[1, 4] * x1 * y2 ** 2 - 1 / 3 * C[1, 4] * x2 ** 3 + (1 / 6) * C[
                                      1, 4] * x2 * y1 ** 2 + (1 / 6) * C[1, 4] * x2 * y1 * y2 - 1 / 3 * C[
                                      1, 4] * x2 * y2 ** 2 + (1 / 3) * C[4, 0] * l * omega1 * x1 + (1 / 6) * C[
                                      4, 0] * l * omega1 * x2 + (1 / 6) * C[4, 0] * l * omega2 * x1 + (1 / 3) * C[
                                      4, 0] * l * omega2 * x2
                P_element[3, 0] = (1 / 2) * C[0, 4] * l * y1 + (1 / 2) * C[0, 4] * l * y2
                P_element[3, 1] = (1 / 3) * C[0, 4] * l * y1 ** 2 + (1 / 3) * C[0, 4] * l * y1 * y2 + (1 / 3) * C[
                    0, 4] * l * y2 ** 2 - 1 / 2 * C[4, 1] * x1 * y1 - 1 / 2 * C[4, 1] * x1 * y2 + (1 / 2) * C[
                                      4, 1] * x2 * y1 + (1 / 2) * C[4, 1] * x2 * y2
                P_element[3, 2] = (1 / 3) * C[4, 0] * l * x1 * y1 + (1 / 6) * C[4, 0] * l * x1 * y2 + (1 / 6) * C[
                    4, 0] * l * x2 * y1 + (1 / 3) * C[4, 0] * l * x2 * y2 - 1 / 2 * C[4, 1] * y1 ** 2 + (1 / 2) * C[
                                      4, 1] * y2 ** 2
                P_element[3, 3] = C[2, 4] * l * y1 + C[2, 4] * l * y2
                P_element[3, 4] = (1 / 3) * C[1, 4] * x1 ** 2 * y1 + (1 / 6) * C[1, 4] * x1 ** 2 * y2 - 1 / 6 * C[
                    1, 4] * x1 * x2 * y1 + (1 / 6) * C[1, 4] * x1 * x2 * y2 - 1 / 6 * C[1, 4] * x2 ** 2 * y1 - 1 / 3 * \
                                  C[1, 4] * x2 ** 2 * y2 + (1 / 3) * C[1, 4] * y1 ** 3 - 1 / 3 * C[1, 4] * y2 ** 3 + (
                                              1 / 3) * C[4, 0] * l * omega1 * y1 + (1 / 6) * C[
                                      4, 0] * l * omega1 * y2 + (1 / 6) * C[4, 0] * l * omega2 * y1 + (1 / 3) * C[
                                      4, 0] * l * omega2 * y2

                R_element[0, 0] = (1 / 2) * C[3, 3] * int_A11_ds1 * l + (1 / 2) * C[3, 3] * int_A11_ds2 * l + (1 / 2) * \
                                  C[4, 3] * int_B16_ds1 * l + (1 / 2) * C[4, 3] * int_B16_ds2 * l
                R_element[0, 1] = (1 / 6) * C[3, 3] * int_A11_y_ds1 * l + (1 / 6) * C[3, 3] * int_A11_y_ds2 * l + (
                            2 / 3) * C[3, 3] * int_A11_y_ds3 * l + (1 / 6) * C[4, 3] * int_B16_y_ds1 * l + (1 / 6) * C[
                                      4, 3] * int_B16_y_ds2 * l + (2 / 3) * C[4, 3] * int_B16_y_ds3 * l
                R_element[0, 2] = -1 / 6 * C[3, 3] * int_A11_x_ds1 * l - 1 / 6 * C[3, 3] * int_A11_x_ds2 * l - 2 / 3 * \
                                  C[3, 3] * int_A11_x_ds3 * l - 1 / 6 * C[4, 3] * int_B16_x_ds1 * l - 1 / 6 * C[
                                      4, 3] * int_B16_x_ds2 * l - 2 / 3 * C[4, 3] * int_B16_x_ds3 * l
                R_element[0, 3] = C[3, 3] * int_B16_ds1 * l + C[3, 3] * int_B16_ds2 * l + C[4, 3] * int_D16_ds1 * l + C[
                    4, 3] * int_D16_ds2 * l
                R_element[0, 4] = -1 / 6 * C[3, 3] * int_A11_omega_ds1 * l - 1 / 6 * C[
                    3, 3] * int_A11_omega_ds2 * l - 2 / 3 * C[3, 3] * int_A11_omega_ds3 * l - 1 / 6 * C[
                                      4, 3] * int_B16_omega_ds1 * l - 1 / 6 * C[4, 3] * int_B16_omega_ds2 * l - 2 / 3 * \
                                  C[4, 3] * int_B16_omega_ds3 * l
                R_element[1, 0] = (1 / 2) * C[4, 3] * int_A11_ds1 * l + (1 / 2) * C[4, 3] * int_A11_ds2 * l + (1 / 2) * \
                                  C[4, 4] * int_B16_ds1 * l + (1 / 2) * C[4, 4] * int_B16_ds2 * l
                R_element[1, 1] = (1 / 6) * C[4, 3] * int_A11_y_ds1 * l + (1 / 6) * C[4, 3] * int_A11_y_ds2 * l + (
                            2 / 3) * C[4, 3] * int_A11_y_ds3 * l + (1 / 6) * C[4, 4] * int_B16_y_ds1 * l + (1 / 6) * C[
                                      4, 4] * int_B16_y_ds2 * l + (2 / 3) * C[4, 4] * int_B16_y_ds3 * l
                R_element[1, 2] = -1 / 6 * C[4, 3] * int_A11_x_ds1 * l - 1 / 6 * C[4, 3] * int_A11_x_ds2 * l - 2 / 3 * \
                                  C[4, 3] * int_A11_x_ds3 * l - 1 / 6 * C[4, 4] * int_B16_x_ds1 * l - 1 / 6 * C[
                                      4, 4] * int_B16_x_ds2 * l - 2 / 3 * C[4, 4] * int_B16_x_ds3 * l
                R_element[1, 3] = C[4, 3] * int_B16_ds1 * l + C[4, 3] * int_B16_ds2 * l + C[4, 4] * int_D16_ds1 * l + C[
                    4, 4] * int_D16_ds2 * l
                R_element[1, 4] = -1 / 6 * C[4, 3] * int_A11_omega_ds1 * l - 1 / 6 * C[
                    4, 3] * int_A11_omega_ds2 * l - 2 / 3 * C[4, 3] * int_A11_omega_ds3 * l - 1 / 6 * C[
                                      4, 4] * int_B16_omega_ds1 * l - 1 / 6 * C[4, 4] * int_B16_omega_ds2 * l - 2 / 3 * \
                                  C[4, 4] * int_B16_omega_ds3 * l
                R_element[2, 0] = (1 / 3) * C[4, 3] * int_A11_ds1 * l * x1 + (1 / 6) * C[
                    4, 3] * int_A11_ds1 * l * x2 + (1 / 6) * C[4, 3] * int_A11_ds2 * l * x1 + (1 / 3) * C[
                                      4, 3] * int_A11_ds2 * l * x2 + (1 / 3) * C[4, 4] * int_B16_ds1 * l * x1 + (
                                              1 / 6) * C[4, 4] * int_B16_ds1 * l * x2 + (1 / 6) * C[
                                      4, 4] * int_B16_ds2 * l * x1 + (1 / 3) * C[4, 4] * int_B16_ds2 * l * x2
                R_element[2, 1] = (1 / 6) * C[4, 3] * int_A11_y_ds1 * l * x1 + (1 / 6) * C[
                    4, 3] * int_A11_y_ds2 * l * x2 + (1 / 3) * C[4, 3] * int_A11_y_ds3 * l * x1 + (1 / 3) * C[
                                      4, 3] * int_A11_y_ds3 * l * x2 + (1 / 6) * C[4, 4] * int_B16_y_ds1 * l * x1 + (
                                              1 / 6) * C[4, 4] * int_B16_y_ds2 * l * x2 + (1 / 3) * C[
                                      4, 4] * int_B16_y_ds3 * l * x1 + (1 / 3) * C[4, 4] * int_B16_y_ds3 * l * x2
                R_element[2, 2] = -1 / 6 * C[4, 3] * int_A11_x_ds1 * l * x1 - 1 / 6 * C[
                    4, 3] * int_A11_x_ds2 * l * x2 - 1 / 3 * C[4, 3] * int_A11_x_ds3 * l * x1 - 1 / 3 * C[
                                      4, 3] * int_A11_x_ds3 * l * x2 - 1 / 6 * C[
                                      4, 4] * int_B16_x_ds1 * l * x1 - 1 / 6 * C[
                                      4, 4] * int_B16_x_ds2 * l * x2 - 1 / 3 * C[
                                      4, 4] * int_B16_x_ds3 * l * x1 - 1 / 3 * C[4, 4] * int_B16_x_ds3 * l * x2
                R_element[2, 3] = (2 / 3) * C[4, 3] * int_B16_ds1 * l * x1 + (1 / 3) * C[
                    4, 3] * int_B16_ds1 * l * x2 + (1 / 3) * C[4, 3] * int_B16_ds2 * l * x1 + (2 / 3) * C[
                                      4, 3] * int_B16_ds2 * l * x2 + (2 / 3) * C[4, 4] * int_D16_ds1 * l * x1 + (
                                              1 / 3) * C[4, 4] * int_D16_ds1 * l * x2 + (1 / 3) * C[
                                      4, 4] * int_D16_ds2 * l * x1 + (2 / 3) * C[4, 4] * int_D16_ds2 * l * x2
                R_element[2, 4] = -1 / 6 * C[4, 3] * int_A11_omega_ds1 * l * x1 - 1 / 6 * C[
                    4, 3] * int_A11_omega_ds2 * l * x2 - 1 / 3 * C[4, 3] * int_A11_omega_ds3 * l * x1 - 1 / 3 * C[
                                      4, 3] * int_A11_omega_ds3 * l * x2 - 1 / 6 * C[
                                      4, 4] * int_B16_omega_ds1 * l * x1 - 1 / 6 * C[
                                      4, 4] * int_B16_omega_ds2 * l * x2 - 1 / 3 * C[
                                      4, 4] * int_B16_omega_ds3 * l * x1 - 1 / 3 * C[4, 4] * int_B16_omega_ds3 * l * x2
                R_element[3, 0] = (1 / 3) * C[4, 3] * int_A11_ds1 * l * y1 + (1 / 6) * C[
                    4, 3] * int_A11_ds1 * l * y2 + (1 / 6) * C[4, 3] * int_A11_ds2 * l * y1 + (1 / 3) * C[
                                      4, 3] * int_A11_ds2 * l * y2 + (1 / 3) * C[4, 4] * int_B16_ds1 * l * y1 + (
                                              1 / 6) * C[4, 4] * int_B16_ds1 * l * y2 + (1 / 6) * C[
                                      4, 4] * int_B16_ds2 * l * y1 + (1 / 3) * C[4, 4] * int_B16_ds2 * l * y2
                R_element[3, 1] = (1 / 6) * C[4, 3] * int_A11_y_ds1 * l * y1 + (1 / 6) * C[
                    4, 3] * int_A11_y_ds2 * l * y2 + (1 / 3) * C[4, 3] * int_A11_y_ds3 * l * y1 + (1 / 3) * C[
                                      4, 3] * int_A11_y_ds3 * l * y2 + (1 / 6) * C[4, 4] * int_B16_y_ds1 * l * y1 + (
                                              1 / 6) * C[4, 4] * int_B16_y_ds2 * l * y2 + (1 / 3) * C[
                                      4, 4] * int_B16_y_ds3 * l * y1 + (1 / 3) * C[4, 4] * int_B16_y_ds3 * l * y2
                R_element[3, 2] = -1 / 6 * C[4, 3] * int_A11_x_ds1 * l * y1 - 1 / 6 * C[
                    4, 3] * int_A11_x_ds2 * l * y2 - 1 / 3 * C[4, 3] * int_A11_x_ds3 * l * y1 - 1 / 3 * C[
                                      4, 3] * int_A11_x_ds3 * l * y2 - 1 / 6 * C[
                                      4, 4] * int_B16_x_ds1 * l * y1 - 1 / 6 * C[
                                      4, 4] * int_B16_x_ds2 * l * y2 - 1 / 3 * C[
                                      4, 4] * int_B16_x_ds3 * l * y1 - 1 / 3 * C[4, 4] * int_B16_x_ds3 * l * y2
                R_element[3, 3] = (2 / 3) * C[4, 3] * int_B16_ds1 * l * y1 + (1 / 3) * C[
                    4, 3] * int_B16_ds1 * l * y2 + (1 / 3) * C[4, 3] * int_B16_ds2 * l * y1 + (2 / 3) * C[
                                      4, 3] * int_B16_ds2 * l * y2 + (2 / 3) * C[4, 4] * int_D16_ds1 * l * y1 + (
                                              1 / 3) * C[4, 4] * int_D16_ds1 * l * y2 + (1 / 3) * C[
                                      4, 4] * int_D16_ds2 * l * y1 + (2 / 3) * C[4, 4] * int_D16_ds2 * l * y2
                R_element[3, 4] = -1 / 6 * C[4, 3] * int_A11_omega_ds1 * l * y1 - 1 / 6 * C[
                    4, 3] * int_A11_omega_ds2 * l * y2 - 1 / 3 * C[4, 3] * int_A11_omega_ds3 * l * y1 - 1 / 3 * C[
                                      4, 3] * int_A11_omega_ds3 * l * y2 - 1 / 6 * C[
                                      4, 4] * int_B16_omega_ds1 * l * y1 - 1 / 6 * C[
                                      4, 4] * int_B16_omega_ds2 * l * y2 - 1 / 3 * C[
                                      4, 4] * int_B16_omega_ds3 * l * y1 - 1 / 3 * C[4, 4] * int_B16_omega_ds3 * l * y2

                Q_element = symmetrize(Q_element_half)

                Q_cell += direction_factor * Q_element @ Z_element
                P_cell += direction_factor * P_element
                R_cell += direction_factor * direction_factor_global * R_element

            Q[4 * cell_idx:4 * (cell_idx+1), :] = Q_cell
            P_cell[0, 3] += 2 * A_i
            P[4 * cell_idx:4 * (cell_idx+1), :] = P_cell
            R[4 * cell_idx:4 * (cell_idx+1), :] = R_cell

        self._Q = Q
        self._P = P
        self._R = R

    @staticmethod
    def _contur_integral_functions_warping(cross_section_processor, element, integration_in_element_direction,
                                           last_node, current_node, last_position, current_position, last_values):
        """
        Calculates the warping contur integral value for one element.

        Parameters
        ----------
        cross_section_processor: CrossSectionProcessor
            The cross section processor.
        element: IElement
            The element
        integration_in_element_direction: bool
            True if the integrations is performed in the element direction.
        last_node: INode
            Last node.
        current_node: INode
            Current node.
        last_position: Vector
            Position of the last node.
        current_position: Vector
            Position of the current node.
        last_values: dict(str, float)
            Contur integral values at the last node.

        Returns
        -------
        dict(str, float)
            Contur integral values at the current node.
        dict(str, float)
            Contur integral values at the middle of the element.
        """
        l = element.length

        r_torsional = (1. if integration_in_element_direction else -1.) *\
                      (element.r_nodes(cross_section_processor.pole) - element.torsional_function_value)

        l_values = {}
        l_half_values = {}

        l_values['int_rtorsional_ds'] = last_values['int_rtorsional_ds'] + l*r_torsional

        return l_values, l_half_values

    @staticmethod
    def _contur_integral_functions(cross_section_processor, element, integration_in_element_direction,
                                   last_node, current_node, last_position, current_position, last_values):
        """
        Calculates the contur integral values for one element.

        Parameters
        ----------
        cross_section_processor: CrossSectionProcessor
            The cross section processor.
        element: IElement
            The element
        integration_in_element_direction: bool
            True if the integrations is performed in the element direction.
        last_node: INode
            Last node.
        current_node: INode
            Current node.
        last_position: Vector
            Position of the last node.
        current_position: Vector
            Position of the current node.
        last_values: dict(str, float)
            Contur integral values at the last node.

        Returns
        -------
        dict(str, float)
            Contur integral values at the current node.
        dict(str, float)
            Contur integral values at the middle of the element.
        """
        x1 = last_position.x
        x2 = current_position.x
        y1 = last_position.y
        y2 = current_position.y

        l = element.length

        A_11 = element.material.stiffness.K_normal[0, 0]
        B_16 = element.material.stiffness.K_normal[0, 4]
        D_16 = element.material.stiffness.K_normal[2, 4]

        omega1 = last_node.integral_values['int_rtorsional_ds']
        omega2 = current_node.integral_values['int_rtorsional_ds']

        l_values = {}
        l_half_values = {}

        # TODO: ohne idx()
        l_values['int_A11_ds'] = last_values['int_A11_ds'] + A_11 * l
        l_values['int_B16_ds'] = last_values['int_B16_ds'] + B_16 * l
        l_values['int_D16_ds'] = last_values['int_D16_ds'] + D_16 * l
        l_values['int_A11_x_ds'] = last_values['int_A11_x_ds'] + A_11 * l * (x1 + x2) / 2
        l_values['int_A11_y_ds'] = last_values['int_A11_y_ds'] + A_11 * l * (y1 + y2) / 2
        l_values['int_A11_omega_ds'] = last_values['int_A11_omega_ds'] + A_11 * l * (omega1 + omega2) / 2
        l_values['int_B16_x_ds'] = last_values['int_B16_x_ds'] + B_16 * l * (x1 + x2) / 2
        l_values['int_B16_y_ds'] = last_values['int_B16_y_ds'] + B_16 * l * (y1 + y2) / 2
        l_values['int_B16_omega_ds'] = last_values['int_B16_omega_ds'] + B_16 * l * (omega1 + omega2) / 2
        l_half_values['int_A11_x_ds'] = last_values['int_A11_x_ds'] + A_11 * l * (3 * x1 + x2) / 8
        l_half_values['int_A11_y_ds'] = last_values['int_A11_y_ds'] + A_11 * l * (3 * y1 + y2) / 8
        l_half_values['int_A11_omega_ds'] = last_values['int_A11_omega_ds'] + A_11 * l * (3 * omega1 + omega2) / 8
        l_half_values['int_B16_x_ds'] = last_values['int_B16_x_ds'] + B_16 * l * (3 * x1 + x2) / 8
        l_half_values['int_B16_y_ds'] = last_values['int_B16_y_ds'] + B_16 * l * (3 * y1 + y2) / 8
        l_half_values['int_B16_omega_ds'] = last_values['int_B16_omega_ds'] + B_16 * l * (3 * omega1 + omega2) / 8

        return l_values, l_half_values

    def _set_cross_section_matrix_K_bb(self):
        """
        Set the K_bb matrix.
        """

        K_bb_half = np.zeros((5, 5))

        elements = self._discreet_geometry.elements
        for element in elements:
            l = element.length
            C = element.material.stiffness.K_Jung
            b_element = element.b

            pos1 = element.node1_midsurface_position
            pos2 = element.node2_midsurface_position

            omega1 = element.node1.integral_values['int_rtorsional_ds']
            omega2 = element.node2.integral_values['int_rtorsional_ds']

            x1 = pos1.x
            x2 = pos2.x
            y1 = pos1.y
            y2 = pos2.y

            K_bb_half[0, 0] += C[0, 0] * l + C[3, 3] * b_element[0, 0] ** 2 * l + 2 * C[4, 3] * b_element[0, 0] * \
                               b_element[1, 0] * l + C[4, 3] * b_element[0, 0] * b_element[2, 0] * l * x1 + C[4, 3] * \
                               b_element[0, 0] * b_element[2, 0] * l * x2 + C[4, 3] * b_element[0, 0] * b_element[
                                   3, 0] * l * y1 + C[4, 3] * b_element[0, 0] * b_element[3, 0] * l * y2 + C[4, 4] * \
                               b_element[1, 0] ** 2 * l + C[4, 4] * b_element[1, 0] * b_element[2, 0] * l * x1 + C[
                                   4, 4] * b_element[1, 0] * b_element[2, 0] * l * x2 + C[4, 4] * b_element[1, 0] * \
                               b_element[3, 0] * l * y1 + C[4, 4] * b_element[1, 0] * b_element[3, 0] * l * y2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 0] ** 2 * l * x1 ** 2 + (1 / 3) * C[4, 4] * \
                               b_element[2, 0] ** 2 * l * x1 * x2 + (1 / 3) * C[4, 4] * b_element[
                                   2, 0] ** 2 * l * x2 ** 2 + (2 / 3) * C[4, 4] * b_element[2, 0] * b_element[
                                   3, 0] * l * x1 * y1 + (1 / 3) * C[4, 4] * b_element[2, 0] * b_element[
                                   3, 0] * l * x1 * y2 + (1 / 3) * C[4, 4] * b_element[2, 0] * b_element[
                                   3, 0] * l * x2 * y1 + (2 / 3) * C[4, 4] * b_element[2, 0] * b_element[
                                   3, 0] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[3, 0] ** 2 * l * y1 ** 2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 0] ** 2 * l * y1 * y2 + (1 / 3) * C[4, 4] * \
                               b_element[3, 0] ** 2 * l * y2 ** 2
            K_bb_half[0, 1] += (1 / 2) * C[0, 0] * l * y1 + (1 / 2) * C[0, 0] * l * y2 + C[1, 0] * x1 - C[1, 0] * x2 + \
                               C[3, 3] * b_element[0, 0] * b_element[0, 1] * l + C[4, 3] * b_element[0, 0] * b_element[
                                   1, 1] * l + (1 / 2) * C[4, 3] * b_element[0, 0] * b_element[2, 1] * l * x1 + (
                                           1 / 2) * C[4, 3] * b_element[0, 0] * b_element[2, 1] * l * x2 + (1 / 2) * C[
                                   4, 3] * b_element[0, 0] * b_element[3, 1] * l * y1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 0] * b_element[3, 1] * l * y2 + C[4, 3] * b_element[0, 1] * b_element[
                                   1, 0] * l + (1 / 2) * C[4, 3] * b_element[0, 1] * b_element[2, 0] * l * x1 + (
                                           1 / 2) * C[4, 3] * b_element[0, 1] * b_element[2, 0] * l * x2 + (1 / 2) * C[
                                   4, 3] * b_element[0, 1] * b_element[3, 0] * l * y1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 1] * b_element[3, 0] * l * y2 + C[4, 4] * b_element[1, 0] * b_element[
                                   1, 1] * l + (1 / 2) * C[4, 4] * b_element[1, 0] * b_element[2, 1] * l * x1 + (
                                           1 / 2) * C[4, 4] * b_element[1, 0] * b_element[2, 1] * l * x2 + (1 / 2) * C[
                                   4, 4] * b_element[1, 0] * b_element[3, 1] * l * y1 + (1 / 2) * C[4, 4] * b_element[
                                   1, 0] * b_element[3, 1] * l * y2 + (1 / 2) * C[4, 4] * b_element[1, 1] * b_element[
                                   2, 0] * l * x1 + (1 / 2) * C[4, 4] * b_element[1, 1] * b_element[2, 0] * l * x2 + (
                                           1 / 2) * C[4, 4] * b_element[1, 1] * b_element[3, 0] * l * y1 + (1 / 2) * C[
                                   4, 4] * b_element[1, 1] * b_element[3, 0] * l * y2 + (1 / 3) * C[4, 4] * b_element[
                                   2, 0] * b_element[2, 1] * l * x1 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 0] * \
                               b_element[2, 1] * l * x1 * x2 + (1 / 3) * C[4, 4] * b_element[2, 0] * b_element[
                                   2, 1] * l * x2 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 0] * b_element[
                                   3, 1] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 0] * b_element[
                                   3, 1] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 0] * b_element[
                                   3, 1] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 0] * b_element[
                                   3, 1] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 0] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 0] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 0] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 0] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[3, 0] * b_element[
                                   3, 1] * l * y1 ** 2 + (1 / 3) * C[4, 4] * b_element[3, 0] * b_element[
                                   3, 1] * l * y1 * y2 + (1 / 3) * C[4, 4] * b_element[3, 0] * b_element[
                                   3, 1] * l * y2 ** 2
            K_bb_half[0, 2] += -1 / 2 * C[0, 0] * l * x1 - 1 / 2 * C[0, 0] * l * x2 + C[1, 0] * y1 - C[1, 0] * y2 + C[
                3, 3] * b_element[0, 0] * b_element[0, 2] * l + C[4, 3] * b_element[0, 0] * b_element[1, 2] * l + (
                                           1 / 2) * C[4, 3] * b_element[0, 0] * b_element[2, 2] * l * x1 + (1 / 2) * C[
                                   4, 3] * b_element[0, 0] * b_element[2, 2] * l * x2 + (1 / 2) * C[4, 3] * b_element[
                                   0, 0] * b_element[3, 2] * l * y1 + (1 / 2) * C[4, 3] * b_element[0, 0] * b_element[
                                   3, 2] * l * y2 + C[4, 3] * b_element[0, 2] * b_element[1, 0] * l + (1 / 2) * C[
                                   4, 3] * b_element[0, 2] * b_element[2, 0] * l * x1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 2] * b_element[2, 0] * l * x2 + (1 / 2) * C[4, 3] * b_element[0, 2] * b_element[
                                   3, 0] * l * y1 + (1 / 2) * C[4, 3] * b_element[0, 2] * b_element[3, 0] * l * y2 + C[
                                   4, 4] * b_element[1, 0] * b_element[1, 2] * l + (1 / 2) * C[4, 4] * b_element[1, 0] * \
                               b_element[2, 2] * l * x1 + (1 / 2) * C[4, 4] * b_element[1, 0] * b_element[
                                   2, 2] * l * x2 + (1 / 2) * C[4, 4] * b_element[1, 0] * b_element[3, 2] * l * y1 + (
                                           1 / 2) * C[4, 4] * b_element[1, 0] * b_element[3, 2] * l * y2 + (1 / 2) * C[
                                   4, 4] * b_element[1, 2] * b_element[2, 0] * l * x1 + (1 / 2) * C[4, 4] * b_element[
                                   1, 2] * b_element[2, 0] * l * x2 + (1 / 2) * C[4, 4] * b_element[1, 2] * b_element[
                                   3, 0] * l * y1 + (1 / 2) * C[4, 4] * b_element[1, 2] * b_element[3, 0] * l * y2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 0] * b_element[2, 2] * l * x1 ** 2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 0] * b_element[2, 2] * l * x1 * x2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 0] * b_element[2, 2] * l * x2 ** 2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 0] * b_element[3, 2] * l * x1 * y1 + (
                                           1 / 6) * C[4, 4] * b_element[2, 0] * b_element[3, 2] * l * x1 * y2 + (
                                           1 / 6) * C[4, 4] * b_element[2, 0] * b_element[3, 2] * l * x2 * y1 + (
                                           1 / 3) * C[4, 4] * b_element[2, 0] * b_element[3, 2] * l * x2 * y2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 2] * b_element[3, 0] * l * x1 * y1 + (
                                           1 / 6) * C[4, 4] * b_element[2, 2] * b_element[3, 0] * l * x1 * y2 + (
                                           1 / 6) * C[4, 4] * b_element[2, 2] * b_element[3, 0] * l * x2 * y1 + (
                                           1 / 3) * C[4, 4] * b_element[2, 2] * b_element[3, 0] * l * x2 * y2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 0] * b_element[3, 2] * l * y1 ** 2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 0] * b_element[3, 2] * l * y1 * y2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 0] * b_element[3, 2] * l * y2 ** 2
            K_bb_half[0, 3] += 2 * C[2, 0] * l + C[3, 3] * b_element[0, 0] * b_element[0, 3] * l + C[4, 3] * b_element[
                0, 0] * b_element[1, 3] * l + (1 / 2) * C[4, 3] * b_element[0, 0] * b_element[2, 3] * l * x1 + (1 / 2) * \
                               C[4, 3] * b_element[0, 0] * b_element[2, 3] * l * x2 + (1 / 2) * C[4, 3] * b_element[
                                   0, 0] * b_element[3, 3] * l * y1 + (1 / 2) * C[4, 3] * b_element[0, 0] * b_element[
                                   3, 3] * l * y2 + C[4, 3] * b_element[0, 3] * b_element[1, 0] * l + (1 / 2) * C[
                                   4, 3] * b_element[0, 3] * b_element[2, 0] * l * x1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 3] * b_element[2, 0] * l * x2 + (1 / 2) * C[4, 3] * b_element[0, 3] * b_element[
                                   3, 0] * l * y1 + (1 / 2) * C[4, 3] * b_element[0, 3] * b_element[3, 0] * l * y2 + C[
                                   4, 4] * b_element[1, 0] * b_element[1, 3] * l + (1 / 2) * C[4, 4] * b_element[1, 0] * \
                               b_element[2, 3] * l * x1 + (1 / 2) * C[4, 4] * b_element[1, 0] * b_element[
                                   2, 3] * l * x2 + (1 / 2) * C[4, 4] * b_element[1, 0] * b_element[3, 3] * l * y1 + (
                                           1 / 2) * C[4, 4] * b_element[1, 0] * b_element[3, 3] * l * y2 + (1 / 2) * C[
                                   4, 4] * b_element[1, 3] * b_element[2, 0] * l * x1 + (1 / 2) * C[4, 4] * b_element[
                                   1, 3] * b_element[2, 0] * l * x2 + (1 / 2) * C[4, 4] * b_element[1, 3] * b_element[
                                   3, 0] * l * y1 + (1 / 2) * C[4, 4] * b_element[1, 3] * b_element[3, 0] * l * y2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 0] * b_element[2, 3] * l * x1 ** 2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 0] * b_element[2, 3] * l * x1 * x2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 0] * b_element[2, 3] * l * x2 ** 2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 0] * b_element[3, 3] * l * x1 * y1 + (
                                           1 / 6) * C[4, 4] * b_element[2, 0] * b_element[3, 3] * l * x1 * y2 + (
                                           1 / 6) * C[4, 4] * b_element[2, 0] * b_element[3, 3] * l * x2 * y1 + (
                                           1 / 3) * C[4, 4] * b_element[2, 0] * b_element[3, 3] * l * x2 * y2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 3] * b_element[3, 0] * l * x1 * y1 + (
                                           1 / 6) * C[4, 4] * b_element[2, 3] * b_element[3, 0] * l * x1 * y2 + (
                                           1 / 6) * C[4, 4] * b_element[2, 3] * b_element[3, 0] * l * x2 * y1 + (
                                           1 / 3) * C[4, 4] * b_element[2, 3] * b_element[3, 0] * l * x2 * y2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 0] * b_element[3, 3] * l * y1 ** 2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 0] * b_element[3, 3] * l * y1 * y2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 0] * b_element[3, 3] * l * y2 ** 2
            K_bb_half[0, 4] += -1 / 2 * C[0, 0] * l * omega1 - 1 / 2 * C[0, 0] * l * omega2 + (1 / 2) * C[
                1, 0] * x1 ** 2 - 1 / 2 * C[1, 0] * x2 ** 2 + (1 / 2) * C[1, 0] * y1 ** 2 - 1 / 2 * C[1, 0] * y2 ** 2 + \
                               C[3, 3] * b_element[0, 0] * b_element[0, 4] * l + C[4, 3] * b_element[0, 0] * b_element[
                                   1, 4] * l + (1 / 2) * C[4, 3] * b_element[0, 0] * b_element[2, 4] * l * x1 + (
                                           1 / 2) * C[4, 3] * b_element[0, 0] * b_element[2, 4] * l * x2 + (1 / 2) * C[
                                   4, 3] * b_element[0, 0] * b_element[3, 4] * l * y1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 0] * b_element[3, 4] * l * y2 + C[4, 3] * b_element[0, 4] * b_element[
                                   1, 0] * l + (1 / 2) * C[4, 3] * b_element[0, 4] * b_element[2, 0] * l * x1 + (
                                           1 / 2) * C[4, 3] * b_element[0, 4] * b_element[2, 0] * l * x2 + (1 / 2) * C[
                                   4, 3] * b_element[0, 4] * b_element[3, 0] * l * y1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 4] * b_element[3, 0] * l * y2 + C[4, 4] * b_element[1, 0] * b_element[
                                   1, 4] * l + (1 / 2) * C[4, 4] * b_element[1, 0] * b_element[2, 4] * l * x1 + (
                                           1 / 2) * C[4, 4] * b_element[1, 0] * b_element[2, 4] * l * x2 + (1 / 2) * C[
                                   4, 4] * b_element[1, 0] * b_element[3, 4] * l * y1 + (1 / 2) * C[4, 4] * b_element[
                                   1, 0] * b_element[3, 4] * l * y2 + (1 / 2) * C[4, 4] * b_element[1, 4] * b_element[
                                   2, 0] * l * x1 + (1 / 2) * C[4, 4] * b_element[1, 4] * b_element[2, 0] * l * x2 + (
                                           1 / 2) * C[4, 4] * b_element[1, 4] * b_element[3, 0] * l * y1 + (1 / 2) * C[
                                   4, 4] * b_element[1, 4] * b_element[3, 0] * l * y2 + (1 / 3) * C[4, 4] * b_element[
                                   2, 0] * b_element[2, 4] * l * x1 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 0] * \
                               b_element[2, 4] * l * x1 * x2 + (1 / 3) * C[4, 4] * b_element[2, 0] * b_element[
                                   2, 4] * l * x2 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 0] * b_element[
                                   3, 4] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 0] * b_element[
                                   3, 4] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 0] * b_element[
                                   3, 4] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 0] * b_element[
                                   3, 4] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 0] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 0] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 0] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 0] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[3, 0] * b_element[
                                   3, 4] * l * y1 ** 2 + (1 / 3) * C[4, 4] * b_element[3, 0] * b_element[
                                   3, 4] * l * y1 * y2 + (1 / 3) * C[4, 4] * b_element[3, 0] * b_element[
                                   3, 4] * l * y2 ** 2
            K_bb_half[1, 1] += (1 / 3) * C[0, 0] * l * y1 ** 2 + (1 / 3) * C[0, 0] * l * y1 * y2 + (1 / 3) * C[
                0, 0] * l * y2 ** 2 + C[1, 0] * x1 * y1 + C[1, 0] * x1 * y2 - C[1, 0] * x2 * y1 - C[1, 0] * x2 * y2 + C[
                                   1, 1] * x1 ** 2 / l - 2 * C[1, 1] * x1 * x2 / l + C[1, 1] * x2 ** 2 / l + C[3, 3] * \
                               b_element[0, 1] ** 2 * l + 2 * C[4, 3] * b_element[0, 1] * b_element[1, 1] * l + C[
                                   4, 3] * b_element[0, 1] * b_element[2, 1] * l * x1 + C[4, 3] * b_element[0, 1] * \
                               b_element[2, 1] * l * x2 + C[4, 3] * b_element[0, 1] * b_element[3, 1] * l * y1 + C[
                                   4, 3] * b_element[0, 1] * b_element[3, 1] * l * y2 + C[4, 4] * b_element[
                                   1, 1] ** 2 * l + C[4, 4] * b_element[1, 1] * b_element[2, 1] * l * x1 + C[4, 4] * \
                               b_element[1, 1] * b_element[2, 1] * l * x2 + C[4, 4] * b_element[1, 1] * b_element[
                                   3, 1] * l * y1 + C[4, 4] * b_element[1, 1] * b_element[3, 1] * l * y2 + (1 / 3) * C[
                                   4, 4] * b_element[2, 1] ** 2 * l * x1 ** 2 + (1 / 3) * C[4, 4] * b_element[
                                   2, 1] ** 2 * l * x1 * x2 + (1 / 3) * C[4, 4] * b_element[2, 1] ** 2 * l * x2 ** 2 + (
                                           2 / 3) * C[4, 4] * b_element[2, 1] * b_element[3, 1] * l * x1 * y1 + (
                                           1 / 3) * C[4, 4] * b_element[2, 1] * b_element[3, 1] * l * x1 * y2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 1] * b_element[3, 1] * l * x2 * y1 + (
                                           2 / 3) * C[4, 4] * b_element[2, 1] * b_element[3, 1] * l * x2 * y2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 1] ** 2 * l * y1 ** 2 + (1 / 3) * C[4, 4] * \
                               b_element[3, 1] ** 2 * l * y1 * y2 + (1 / 3) * C[4, 4] * b_element[
                                   3, 1] ** 2 * l * y2 ** 2
            K_bb_half[1, 2] += -1 / 3 * C[0, 0] * l * x1 * y1 - 1 / 6 * C[0, 0] * l * x1 * y2 - 1 / 6 * C[
                0, 0] * l * x2 * y1 - 1 / 3 * C[0, 0] * l * x2 * y2 - 1 / 2 * C[1, 0] * x1 ** 2 + (1 / 2) * C[
                                   1, 0] * x2 ** 2 + (1 / 2) * C[1, 0] * y1 ** 2 - 1 / 2 * C[1, 0] * y2 ** 2 + C[
                                   1, 1] * x1 * y1 / l - C[1, 1] * x1 * y2 / l - C[1, 1] * x2 * y1 / l + C[
                                   1, 1] * x2 * y2 / l + C[3, 3] * b_element[0, 1] * b_element[0, 2] * l + C[4, 3] * \
                               b_element[0, 1] * b_element[1, 2] * l + (1 / 2) * C[4, 3] * b_element[0, 1] * b_element[
                                   2, 2] * l * x1 + (1 / 2) * C[4, 3] * b_element[0, 1] * b_element[2, 2] * l * x2 + (
                                           1 / 2) * C[4, 3] * b_element[0, 1] * b_element[3, 2] * l * y1 + (1 / 2) * C[
                                   4, 3] * b_element[0, 1] * b_element[3, 2] * l * y2 + C[4, 3] * b_element[0, 2] * \
                               b_element[1, 1] * l + (1 / 2) * C[4, 3] * b_element[0, 2] * b_element[2, 1] * l * x1 + (
                                           1 / 2) * C[4, 3] * b_element[0, 2] * b_element[2, 1] * l * x2 + (1 / 2) * C[
                                   4, 3] * b_element[0, 2] * b_element[3, 1] * l * y1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 2] * b_element[3, 1] * l * y2 + C[4, 4] * b_element[1, 1] * b_element[
                                   1, 2] * l + (1 / 2) * C[4, 4] * b_element[1, 1] * b_element[2, 2] * l * x1 + (
                                           1 / 2) * C[4, 4] * b_element[1, 1] * b_element[2, 2] * l * x2 + (1 / 2) * C[
                                   4, 4] * b_element[1, 1] * b_element[3, 2] * l * y1 + (1 / 2) * C[4, 4] * b_element[
                                   1, 1] * b_element[3, 2] * l * y2 + (1 / 2) * C[4, 4] * b_element[1, 2] * b_element[
                                   2, 1] * l * x1 + (1 / 2) * C[4, 4] * b_element[1, 2] * b_element[2, 1] * l * x2 + (
                                           1 / 2) * C[4, 4] * b_element[1, 2] * b_element[3, 1] * l * y1 + (1 / 2) * C[
                                   4, 4] * b_element[1, 2] * b_element[3, 1] * l * y2 + (1 / 3) * C[4, 4] * b_element[
                                   2, 1] * b_element[2, 2] * l * x1 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 1] * \
                               b_element[2, 2] * l * x1 * x2 + (1 / 3) * C[4, 4] * b_element[2, 1] * b_element[
                                   2, 2] * l * x2 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 2] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 2] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 2] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 2] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[2, 2] * b_element[
                                   3, 1] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 2] * b_element[
                                   3, 1] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 2] * b_element[
                                   3, 1] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 2] * b_element[
                                   3, 1] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[3, 1] * b_element[
                                   3, 2] * l * y1 ** 2 + (1 / 3) * C[4, 4] * b_element[3, 1] * b_element[
                                   3, 2] * l * y1 * y2 + (1 / 3) * C[4, 4] * b_element[3, 1] * b_element[
                                   3, 2] * l * y2 ** 2
            K_bb_half[1, 3] += C[2, 0] * l * y1 + C[2, 0] * l * y2 + 2 * C[2, 1] * x1 - 2 * C[2, 1] * x2 + C[3, 3] * \
                               b_element[0, 1] * b_element[0, 3] * l + C[4, 3] * b_element[0, 1] * b_element[
                                   1, 3] * l + (1 / 2) * C[4, 3] * b_element[0, 1] * b_element[2, 3] * l * x1 + (
                                           1 / 2) * C[4, 3] * b_element[0, 1] * b_element[2, 3] * l * x2 + (1 / 2) * C[
                                   4, 3] * b_element[0, 1] * b_element[3, 3] * l * y1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 1] * b_element[3, 3] * l * y2 + C[4, 3] * b_element[0, 3] * b_element[
                                   1, 1] * l + (1 / 2) * C[4, 3] * b_element[0, 3] * b_element[2, 1] * l * x1 + (
                                           1 / 2) * C[4, 3] * b_element[0, 3] * b_element[2, 1] * l * x2 + (1 / 2) * C[
                                   4, 3] * b_element[0, 3] * b_element[3, 1] * l * y1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 3] * b_element[3, 1] * l * y2 + C[4, 4] * b_element[1, 1] * b_element[
                                   1, 3] * l + (1 / 2) * C[4, 4] * b_element[1, 1] * b_element[2, 3] * l * x1 + (
                                           1 / 2) * C[4, 4] * b_element[1, 1] * b_element[2, 3] * l * x2 + (1 / 2) * C[
                                   4, 4] * b_element[1, 1] * b_element[3, 3] * l * y1 + (1 / 2) * C[4, 4] * b_element[
                                   1, 1] * b_element[3, 3] * l * y2 + (1 / 2) * C[4, 4] * b_element[1, 3] * b_element[
                                   2, 1] * l * x1 + (1 / 2) * C[4, 4] * b_element[1, 3] * b_element[2, 1] * l * x2 + (
                                           1 / 2) * C[4, 4] * b_element[1, 3] * b_element[3, 1] * l * y1 + (1 / 2) * C[
                                   4, 4] * b_element[1, 3] * b_element[3, 1] * l * y2 + (1 / 3) * C[4, 4] * b_element[
                                   2, 1] * b_element[2, 3] * l * x1 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 1] * \
                               b_element[2, 3] * l * x1 * x2 + (1 / 3) * C[4, 4] * b_element[2, 1] * b_element[
                                   2, 3] * l * x2 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 3] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 3] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 3] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 3] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 1] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 1] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 1] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 1] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[3, 1] * b_element[
                                   3, 3] * l * y1 ** 2 + (1 / 3) * C[4, 4] * b_element[3, 1] * b_element[
                                   3, 3] * l * y1 * y2 + (1 / 3) * C[4, 4] * b_element[3, 1] * b_element[
                                   3, 3] * l * y2 ** 2
            K_bb_half[1, 4] += -1 / 3 * C[0, 0] * l * omega1 * y1 - 1 / 6 * C[0, 0] * l * omega1 * y2 - 1 / 6 * C[
                0, 0] * l * omega2 * y1 - 1 / 3 * C[0, 0] * l * omega2 * y2 - 1 / 2 * C[1, 0] * omega1 * x1 + (1 / 2) * \
                               C[1, 0] * omega1 * x2 - 1 / 2 * C[1, 0] * omega2 * x1 + (1 / 2) * C[
                                   1, 0] * omega2 * x2 + (1 / 3) * C[1, 0] * x1 ** 2 * y1 + (1 / 6) * C[
                                   1, 0] * x1 ** 2 * y2 - 1 / 6 * C[1, 0] * x1 * x2 * y1 + (1 / 6) * C[
                                   1, 0] * x1 * x2 * y2 - 1 / 6 * C[1, 0] * x2 ** 2 * y1 - 1 / 3 * C[
                                   1, 0] * x2 ** 2 * y2 + (1 / 3) * C[1, 0] * y1 ** 3 - 1 / 3 * C[1, 0] * y2 ** 3 + (
                                           1 / 2) * C[1, 1] * x1 ** 3 / l - 1 / 2 * C[1, 1] * x1 ** 2 * x2 / l - 1 / 2 * \
                               C[1, 1] * x1 * x2 ** 2 / l + (1 / 2) * C[1, 1] * x1 * y1 ** 2 / l - 1 / 2 * C[
                                   1, 1] * x1 * y2 ** 2 / l + (1 / 2) * C[1, 1] * x2 ** 3 / l - 1 / 2 * C[
                                   1, 1] * x2 * y1 ** 2 / l + (1 / 2) * C[1, 1] * x2 * y2 ** 2 / l + C[3, 3] * \
                               b_element[0, 1] * b_element[0, 4] * l + C[4, 3] * b_element[0, 1] * b_element[
                                   1, 4] * l + (1 / 2) * C[4, 3] * b_element[0, 1] * b_element[2, 4] * l * x1 + (
                                           1 / 2) * C[4, 3] * b_element[0, 1] * b_element[2, 4] * l * x2 + (1 / 2) * C[
                                   4, 3] * b_element[0, 1] * b_element[3, 4] * l * y1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 1] * b_element[3, 4] * l * y2 + C[4, 3] * b_element[0, 4] * b_element[
                                   1, 1] * l + (1 / 2) * C[4, 3] * b_element[0, 4] * b_element[2, 1] * l * x1 + (
                                           1 / 2) * C[4, 3] * b_element[0, 4] * b_element[2, 1] * l * x2 + (1 / 2) * C[
                                   4, 3] * b_element[0, 4] * b_element[3, 1] * l * y1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 4] * b_element[3, 1] * l * y2 + C[4, 4] * b_element[1, 1] * b_element[
                                   1, 4] * l + (1 / 2) * C[4, 4] * b_element[1, 1] * b_element[2, 4] * l * x1 + (
                                           1 / 2) * C[4, 4] * b_element[1, 1] * b_element[2, 4] * l * x2 + (1 / 2) * C[
                                   4, 4] * b_element[1, 1] * b_element[3, 4] * l * y1 + (1 / 2) * C[4, 4] * b_element[
                                   1, 1] * b_element[3, 4] * l * y2 + (1 / 2) * C[4, 4] * b_element[1, 4] * b_element[
                                   2, 1] * l * x1 + (1 / 2) * C[4, 4] * b_element[1, 4] * b_element[2, 1] * l * x2 + (
                                           1 / 2) * C[4, 4] * b_element[1, 4] * b_element[3, 1] * l * y1 + (1 / 2) * C[
                                   4, 4] * b_element[1, 4] * b_element[3, 1] * l * y2 + (1 / 3) * C[4, 4] * b_element[
                                   2, 1] * b_element[2, 4] * l * x1 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 1] * \
                               b_element[2, 4] * l * x1 * x2 + (1 / 3) * C[4, 4] * b_element[2, 1] * b_element[
                                   2, 4] * l * x2 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 4] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 4] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 4] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 1] * b_element[
                                   3, 4] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 1] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 1] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 1] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 1] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[3, 1] * b_element[
                                   3, 4] * l * y1 ** 2 + (1 / 3) * C[4, 4] * b_element[3, 1] * b_element[
                                   3, 4] * l * y1 * y2 + (1 / 3) * C[4, 4] * b_element[3, 1] * b_element[
                                   3, 4] * l * y2 ** 2
            K_bb_half[2, 2] += (1 / 3) * C[0, 0] * l * x1 ** 2 + (1 / 3) * C[0, 0] * l * x1 * x2 + (1 / 3) * C[
                0, 0] * l * x2 ** 2 - C[1, 0] * x1 * y1 + C[1, 0] * x1 * y2 - C[1, 0] * x2 * y1 + C[1, 0] * x2 * y2 + C[
                                   1, 1] * y1 ** 2 / l - 2 * C[1, 1] * y1 * y2 / l + C[1, 1] * y2 ** 2 / l + C[3, 3] * \
                               b_element[0, 2] ** 2 * l + 2 * C[4, 3] * b_element[0, 2] * b_element[1, 2] * l + C[
                                   4, 3] * b_element[0, 2] * b_element[2, 2] * l * x1 + C[4, 3] * b_element[0, 2] * \
                               b_element[2, 2] * l * x2 + C[4, 3] * b_element[0, 2] * b_element[3, 2] * l * y1 + C[
                                   4, 3] * b_element[0, 2] * b_element[3, 2] * l * y2 + C[4, 4] * b_element[
                                   1, 2] ** 2 * l + C[4, 4] * b_element[1, 2] * b_element[2, 2] * l * x1 + C[4, 4] * \
                               b_element[1, 2] * b_element[2, 2] * l * x2 + C[4, 4] * b_element[1, 2] * b_element[
                                   3, 2] * l * y1 + C[4, 4] * b_element[1, 2] * b_element[3, 2] * l * y2 + (1 / 3) * C[
                                   4, 4] * b_element[2, 2] ** 2 * l * x1 ** 2 + (1 / 3) * C[4, 4] * b_element[
                                   2, 2] ** 2 * l * x1 * x2 + (1 / 3) * C[4, 4] * b_element[2, 2] ** 2 * l * x2 ** 2 + (
                                           2 / 3) * C[4, 4] * b_element[2, 2] * b_element[3, 2] * l * x1 * y1 + (
                                           1 / 3) * C[4, 4] * b_element[2, 2] * b_element[3, 2] * l * x1 * y2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 2] * b_element[3, 2] * l * x2 * y1 + (
                                           2 / 3) * C[4, 4] * b_element[2, 2] * b_element[3, 2] * l * x2 * y2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 2] ** 2 * l * y1 ** 2 + (1 / 3) * C[4, 4] * \
                               b_element[3, 2] ** 2 * l * y1 * y2 + (1 / 3) * C[4, 4] * b_element[
                                   3, 2] ** 2 * l * y2 ** 2
            K_bb_half[2, 3] += -C[2, 0] * l * x1 - C[2, 0] * l * x2 + 2 * C[2, 1] * y1 - 2 * C[2, 1] * y2 + C[3, 3] * \
                               b_element[0, 2] * b_element[0, 3] * l + C[4, 3] * b_element[0, 2] * b_element[
                                   1, 3] * l + (1 / 2) * C[4, 3] * b_element[0, 2] * b_element[2, 3] * l * x1 + (
                                           1 / 2) * C[4, 3] * b_element[0, 2] * b_element[2, 3] * l * x2 + (1 / 2) * C[
                                   4, 3] * b_element[0, 2] * b_element[3, 3] * l * y1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 2] * b_element[3, 3] * l * y2 + C[4, 3] * b_element[0, 3] * b_element[
                                   1, 2] * l + (1 / 2) * C[4, 3] * b_element[0, 3] * b_element[2, 2] * l * x1 + (
                                           1 / 2) * C[4, 3] * b_element[0, 3] * b_element[2, 2] * l * x2 + (1 / 2) * C[
                                   4, 3] * b_element[0, 3] * b_element[3, 2] * l * y1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 3] * b_element[3, 2] * l * y2 + C[4, 4] * b_element[1, 2] * b_element[
                                   1, 3] * l + (1 / 2) * C[4, 4] * b_element[1, 2] * b_element[2, 3] * l * x1 + (
                                           1 / 2) * C[4, 4] * b_element[1, 2] * b_element[2, 3] * l * x2 + (1 / 2) * C[
                                   4, 4] * b_element[1, 2] * b_element[3, 3] * l * y1 + (1 / 2) * C[4, 4] * b_element[
                                   1, 2] * b_element[3, 3] * l * y2 + (1 / 2) * C[4, 4] * b_element[1, 3] * b_element[
                                   2, 2] * l * x1 + (1 / 2) * C[4, 4] * b_element[1, 3] * b_element[2, 2] * l * x2 + (
                                           1 / 2) * C[4, 4] * b_element[1, 3] * b_element[3, 2] * l * y1 + (1 / 2) * C[
                                   4, 4] * b_element[1, 3] * b_element[3, 2] * l * y2 + (1 / 3) * C[4, 4] * b_element[
                                   2, 2] * b_element[2, 3] * l * x1 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 2] * \
                               b_element[2, 3] * l * x1 * x2 + (1 / 3) * C[4, 4] * b_element[2, 2] * b_element[
                                   2, 3] * l * x2 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 2] * b_element[
                                   3, 3] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 2] * b_element[
                                   3, 3] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 2] * b_element[
                                   3, 3] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 2] * b_element[
                                   3, 3] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 2] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 2] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 2] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 2] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[3, 2] * b_element[
                                   3, 3] * l * y1 ** 2 + (1 / 3) * C[4, 4] * b_element[3, 2] * b_element[
                                   3, 3] * l * y1 * y2 + (1 / 3) * C[4, 4] * b_element[3, 2] * b_element[
                                   3, 3] * l * y2 ** 2
            K_bb_half[2, 4] += (1 / 3) * C[0, 0] * l * omega1 * x1 + (1 / 6) * C[0, 0] * l * omega1 * x2 + (1 / 6) * C[
                0, 0] * l * omega2 * x1 + (1 / 3) * C[0, 0] * l * omega2 * x2 - 1 / 2 * C[1, 0] * omega1 * y1 + (
                                           1 / 2) * C[1, 0] * omega1 * y2 - 1 / 2 * C[1, 0] * omega2 * y1 + (1 / 2) * C[
                                   1, 0] * omega2 * y2 - 1 / 3 * C[1, 0] * x1 ** 3 - 1 / 3 * C[1, 0] * x1 * y1 ** 2 + (
                                           1 / 6) * C[1, 0] * x1 * y1 * y2 + (1 / 6) * C[1, 0] * x1 * y2 ** 2 + (
                                           1 / 3) * C[1, 0] * x2 ** 3 - 1 / 6 * C[1, 0] * x2 * y1 ** 2 - 1 / 6 * C[
                                   1, 0] * x2 * y1 * y2 + (1 / 3) * C[1, 0] * x2 * y2 ** 2 + (1 / 2) * C[
                                   1, 1] * x1 ** 2 * y1 / l - 1 / 2 * C[1, 1] * x1 ** 2 * y2 / l - 1 / 2 * C[
                                   1, 1] * x2 ** 2 * y1 / l + (1 / 2) * C[1, 1] * x2 ** 2 * y2 / l + (1 / 2) * C[
                                   1, 1] * y1 ** 3 / l - 1 / 2 * C[1, 1] * y1 ** 2 * y2 / l - 1 / 2 * C[
                                   1, 1] * y1 * y2 ** 2 / l + (1 / 2) * C[1, 1] * y2 ** 3 / l + C[3, 3] * b_element[
                                   0, 2] * b_element[0, 4] * l + C[4, 3] * b_element[0, 2] * b_element[1, 4] * l + (
                                           1 / 2) * C[4, 3] * b_element[0, 2] * b_element[2, 4] * l * x1 + (1 / 2) * C[
                                   4, 3] * b_element[0, 2] * b_element[2, 4] * l * x2 + (1 / 2) * C[4, 3] * b_element[
                                   0, 2] * b_element[3, 4] * l * y1 + (1 / 2) * C[4, 3] * b_element[0, 2] * b_element[
                                   3, 4] * l * y2 + C[4, 3] * b_element[0, 4] * b_element[1, 2] * l + (1 / 2) * C[
                                   4, 3] * b_element[0, 4] * b_element[2, 2] * l * x1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 4] * b_element[2, 2] * l * x2 + (1 / 2) * C[4, 3] * b_element[0, 4] * b_element[
                                   3, 2] * l * y1 + (1 / 2) * C[4, 3] * b_element[0, 4] * b_element[3, 2] * l * y2 + C[
                                   4, 4] * b_element[1, 2] * b_element[1, 4] * l + (1 / 2) * C[4, 4] * b_element[1, 2] * \
                               b_element[2, 4] * l * x1 + (1 / 2) * C[4, 4] * b_element[1, 2] * b_element[
                                   2, 4] * l * x2 + (1 / 2) * C[4, 4] * b_element[1, 2] * b_element[3, 4] * l * y1 + (
                                           1 / 2) * C[4, 4] * b_element[1, 2] * b_element[3, 4] * l * y2 + (1 / 2) * C[
                                   4, 4] * b_element[1, 4] * b_element[2, 2] * l * x1 + (1 / 2) * C[4, 4] * b_element[
                                   1, 4] * b_element[2, 2] * l * x2 + (1 / 2) * C[4, 4] * b_element[1, 4] * b_element[
                                   3, 2] * l * y1 + (1 / 2) * C[4, 4] * b_element[1, 4] * b_element[3, 2] * l * y2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 2] * b_element[2, 4] * l * x1 ** 2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 2] * b_element[2, 4] * l * x1 * x2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 2] * b_element[2, 4] * l * x2 ** 2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 2] * b_element[3, 4] * l * x1 * y1 + (
                                           1 / 6) * C[4, 4] * b_element[2, 2] * b_element[3, 4] * l * x1 * y2 + (
                                           1 / 6) * C[4, 4] * b_element[2, 2] * b_element[3, 4] * l * x2 * y1 + (
                                           1 / 3) * C[4, 4] * b_element[2, 2] * b_element[3, 4] * l * x2 * y2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 4] * b_element[3, 2] * l * x1 * y1 + (
                                           1 / 6) * C[4, 4] * b_element[2, 4] * b_element[3, 2] * l * x1 * y2 + (
                                           1 / 6) * C[4, 4] * b_element[2, 4] * b_element[3, 2] * l * x2 * y1 + (
                                           1 / 3) * C[4, 4] * b_element[2, 4] * b_element[3, 2] * l * x2 * y2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 2] * b_element[3, 4] * l * y1 ** 2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 2] * b_element[3, 4] * l * y1 * y2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 2] * b_element[3, 4] * l * y2 ** 2
            K_bb_half[3, 3] += 4 * C[2, 2] * l + C[3, 3] * b_element[0, 3] ** 2 * l + 2 * C[4, 3] * b_element[0, 3] * \
                               b_element[1, 3] * l + C[4, 3] * b_element[0, 3] * b_element[2, 3] * l * x1 + C[4, 3] * \
                               b_element[0, 3] * b_element[2, 3] * l * x2 + C[4, 3] * b_element[0, 3] * b_element[
                                   3, 3] * l * y1 + C[4, 3] * b_element[0, 3] * b_element[3, 3] * l * y2 + C[4, 4] * \
                               b_element[1, 3] ** 2 * l + C[4, 4] * b_element[1, 3] * b_element[2, 3] * l * x1 + C[
                                   4, 4] * b_element[1, 3] * b_element[2, 3] * l * x2 + C[4, 4] * b_element[1, 3] * \
                               b_element[3, 3] * l * y1 + C[4, 4] * b_element[1, 3] * b_element[3, 3] * l * y2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 3] ** 2 * l * x1 ** 2 + (1 / 3) * C[4, 4] * \
                               b_element[2, 3] ** 2 * l * x1 * x2 + (1 / 3) * C[4, 4] * b_element[
                                   2, 3] ** 2 * l * x2 ** 2 + (2 / 3) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 3] * l * x1 * y1 + (1 / 3) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 3] * l * x1 * y2 + (1 / 3) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 3] * l * x2 * y1 + (2 / 3) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 3] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[3, 3] ** 2 * l * y1 ** 2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 3] ** 2 * l * y1 * y2 + (1 / 3) * C[4, 4] * \
                               b_element[3, 3] ** 2 * l * y2 ** 2
            K_bb_half[3, 4] += -C[2, 0] * l * omega1 - C[2, 0] * l * omega2 + C[2, 1] * x1 ** 2 - C[2, 1] * x2 ** 2 + C[
                2, 1] * y1 ** 2 - C[2, 1] * y2 ** 2 + C[3, 3] * b_element[0, 3] * b_element[0, 4] * l + C[4, 3] * \
                               b_element[0, 3] * b_element[1, 4] * l + (1 / 2) * C[4, 3] * b_element[0, 3] * b_element[
                                   2, 4] * l * x1 + (1 / 2) * C[4, 3] * b_element[0, 3] * b_element[2, 4] * l * x2 + (
                                           1 / 2) * C[4, 3] * b_element[0, 3] * b_element[3, 4] * l * y1 + (1 / 2) * C[
                                   4, 3] * b_element[0, 3] * b_element[3, 4] * l * y2 + C[4, 3] * b_element[0, 4] * \
                               b_element[1, 3] * l + (1 / 2) * C[4, 3] * b_element[0, 4] * b_element[2, 3] * l * x1 + (
                                           1 / 2) * C[4, 3] * b_element[0, 4] * b_element[2, 3] * l * x2 + (1 / 2) * C[
                                   4, 3] * b_element[0, 4] * b_element[3, 3] * l * y1 + (1 / 2) * C[4, 3] * b_element[
                                   0, 4] * b_element[3, 3] * l * y2 + C[4, 4] * b_element[1, 3] * b_element[
                                   1, 4] * l + (1 / 2) * C[4, 4] * b_element[1, 3] * b_element[2, 4] * l * x1 + (
                                           1 / 2) * C[4, 4] * b_element[1, 3] * b_element[2, 4] * l * x2 + (1 / 2) * C[
                                   4, 4] * b_element[1, 3] * b_element[3, 4] * l * y1 + (1 / 2) * C[4, 4] * b_element[
                                   1, 3] * b_element[3, 4] * l * y2 + (1 / 2) * C[4, 4] * b_element[1, 4] * b_element[
                                   2, 3] * l * x1 + (1 / 2) * C[4, 4] * b_element[1, 4] * b_element[2, 3] * l * x2 + (
                                           1 / 2) * C[4, 4] * b_element[1, 4] * b_element[3, 3] * l * y1 + (1 / 2) * C[
                                   4, 4] * b_element[1, 4] * b_element[3, 3] * l * y2 + (1 / 3) * C[4, 4] * b_element[
                                   2, 3] * b_element[2, 4] * l * x1 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 3] * \
                               b_element[2, 4] * l * x1 * x2 + (1 / 3) * C[4, 4] * b_element[2, 3] * b_element[
                                   2, 4] * l * x2 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 4] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 4] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 4] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 3] * b_element[
                                   3, 4] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 3] * l * x1 * y1 + (1 / 6) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 3] * l * x1 * y2 + (1 / 6) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 3] * l * x2 * y1 + (1 / 3) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 3] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[3, 3] * b_element[
                                   3, 4] * l * y1 ** 2 + (1 / 3) * C[4, 4] * b_element[3, 3] * b_element[
                                   3, 4] * l * y1 * y2 + (1 / 3) * C[4, 4] * b_element[3, 3] * b_element[
                                   3, 4] * l * y2 ** 2
            K_bb_half[4, 4] += (1 / 3) * C[0, 0] * l * omega1 ** 2 + (1 / 3) * C[0, 0] * l * omega1 * omega2 + (1 / 3) * \
                               C[0, 0] * l * omega2 ** 2 - 2 / 3 * C[1, 0] * omega1 * x1 ** 2 + (1 / 3) * C[
                                   1, 0] * omega1 * x1 * x2 + (1 / 3) * C[1, 0] * omega1 * x2 ** 2 - 2 / 3 * C[
                                   1, 0] * omega1 * y1 ** 2 + (1 / 3) * C[1, 0] * omega1 * y1 * y2 + (1 / 3) * C[
                                   1, 0] * omega1 * y2 ** 2 - 1 / 3 * C[1, 0] * omega2 * x1 ** 2 - 1 / 3 * C[
                                   1, 0] * omega2 * x1 * x2 + (2 / 3) * C[1, 0] * omega2 * x2 ** 2 - 1 / 3 * C[
                                   1, 0] * omega2 * y1 ** 2 - 1 / 3 * C[1, 0] * omega2 * y1 * y2 + (2 / 3) * C[
                                   1, 0] * omega2 * y2 ** 2 + (1 / 3) * C[1, 1] * x1 ** 4 / l - 1 / 3 * C[
                                   1, 1] * x1 ** 3 * x2 / l + (2 / 3) * C[1, 1] * x1 ** 2 * y1 ** 2 / l - 1 / 3 * C[
                                   1, 1] * x1 ** 2 * y1 * y2 / l - 1 / 3 * C[1, 1] * x1 ** 2 * y2 ** 2 / l - 1 / 3 * C[
                                   1, 1] * x1 * x2 ** 3 / l - 1 / 3 * C[1, 1] * x1 * x2 * y1 ** 2 / l + (2 / 3) * C[
                                   1, 1] * x1 * x2 * y1 * y2 / l - 1 / 3 * C[1, 1] * x1 * x2 * y2 ** 2 / l + (1 / 3) * \
                               C[1, 1] * x2 ** 4 / l - 1 / 3 * C[1, 1] * x2 ** 2 * y1 ** 2 / l - 1 / 3 * C[
                                   1, 1] * x2 ** 2 * y1 * y2 / l + (2 / 3) * C[1, 1] * x2 ** 2 * y2 ** 2 / l + (1 / 3) * \
                               C[1, 1] * y1 ** 4 / l - 1 / 3 * C[1, 1] * y1 ** 3 * y2 / l - 1 / 3 * C[
                                   1, 1] * y1 * y2 ** 3 / l + (1 / 3) * C[1, 1] * y2 ** 4 / l + C[3, 3] * b_element[
                                   0, 4] ** 2 * l + 2 * C[4, 3] * b_element[0, 4] * b_element[1, 4] * l + C[4, 3] * \
                               b_element[0, 4] * b_element[2, 4] * l * x1 + C[4, 3] * b_element[0, 4] * b_element[
                                   2, 4] * l * x2 + C[4, 3] * b_element[0, 4] * b_element[3, 4] * l * y1 + C[4, 3] * \
                               b_element[0, 4] * b_element[3, 4] * l * y2 + C[4, 4] * b_element[1, 4] ** 2 * l + C[
                                   4, 4] * b_element[1, 4] * b_element[2, 4] * l * x1 + C[4, 4] * b_element[1, 4] * \
                               b_element[2, 4] * l * x2 + C[4, 4] * b_element[1, 4] * b_element[3, 4] * l * y1 + C[
                                   4, 4] * b_element[1, 4] * b_element[3, 4] * l * y2 + (1 / 3) * C[4, 4] * b_element[
                                   2, 4] ** 2 * l * x1 ** 2 + (1 / 3) * C[4, 4] * b_element[2, 4] ** 2 * l * x1 * x2 + (
                                           1 / 3) * C[4, 4] * b_element[2, 4] ** 2 * l * x2 ** 2 + (2 / 3) * C[4, 4] * \
                               b_element[2, 4] * b_element[3, 4] * l * x1 * y1 + (1 / 3) * C[4, 4] * b_element[2, 4] * \
                               b_element[3, 4] * l * x1 * y2 + (1 / 3) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 4] * l * x2 * y1 + (2 / 3) * C[4, 4] * b_element[2, 4] * b_element[
                                   3, 4] * l * x2 * y2 + (1 / 3) * C[4, 4] * b_element[3, 4] ** 2 * l * y1 ** 2 + (
                                           1 / 3) * C[4, 4] * b_element[3, 4] ** 2 * l * y1 * y2 + (1 / 3) * C[4, 4] * \
                               b_element[3, 4] ** 2 * l * y2 ** 2

        self._K_bb = symmetrize(K_bb_half)

    def _set_cross_section_matrices_K_vv_and_K_bv(self):
        """
        Set the K_vv and K_bv matrices.
        """
        K_vv = np.zeros((2, 2))
        K_bv = np.zeros((5, 2))

        elements = self._discreet_geometry.elements
        for element in elements:
            l = element.length
            C = element.material.stiffness.K_Jung
            b_element = element.b

            pos1 = element.node1_midsurface_position
            pos2 = element.node2_midsurface_position

            x1 = pos1.x
            x2 = pos2.x
            y1 = pos1.y
            y2 = pos2.y

            f_r_1 = element.f_r_1
            f_r_2 = element.f_r_2
            f_r_3 = element.f_r_3

            f_r_const_111 = f_r_1[0,0]
            f_r_const_112 = f_r_2[0,0]
            f_r_const_113 = f_r_3[0,0]

            f_r_const_121 = f_r_1[0,1]
            f_r_const_122 = f_r_2[0,1]
            f_r_const_123 = f_r_3[0,1]

            f_r_const_211 = f_r_1[1,0]
            f_r_const_212 = f_r_2[1,0]
            f_r_const_213 = f_r_3[1,0]

            f_r_const_221 = f_r_1[1,1]
            f_r_const_222 = f_r_2[1,1]
            f_r_const_223 = f_r_3[1,1]

            K_bv[0, 0] += (1 / 6) * C[3, 3] * b_element[0, 0] * f_r_const_111 * l + (1 / 6) * C[3, 3] * b_element[
                0, 0] * f_r_const_112 * l + (2 / 3) * C[3, 3] * b_element[0, 0] * f_r_const_113 * l + (1 / 6) * C[
                              4, 3] * b_element[0, 0] * f_r_const_211 * l + (1 / 6) * C[4, 3] * b_element[
                              0, 0] * f_r_const_212 * l + (2 / 3) * C[4, 3] * b_element[0, 0] * f_r_const_213 * l + (
                                      1 / 6) * C[4, 3] * b_element[1, 0] * f_r_const_111 * l + (1 / 6) * C[4, 3] * \
                          b_element[1, 0] * f_r_const_112 * l + (2 / 3) * C[4, 3] * b_element[
                              1, 0] * f_r_const_113 * l + (1 / 6) * C[4, 3] * b_element[
                              2, 0] * f_r_const_111 * l * x1 + (1 / 6) * C[4, 3] * b_element[
                              2, 0] * f_r_const_112 * l * x2 + (1 / 3) * C[4, 3] * b_element[
                              2, 0] * f_r_const_113 * l * x1 + (1 / 3) * C[4, 3] * b_element[
                              2, 0] * f_r_const_113 * l * x2 + (1 / 6) * C[4, 3] * b_element[
                              3, 0] * f_r_const_111 * l * y1 + (1 / 6) * C[4, 3] * b_element[
                              3, 0] * f_r_const_112 * l * y2 + (1 / 3) * C[4, 3] * b_element[
                              3, 0] * f_r_const_113 * l * y1 + (1 / 3) * C[4, 3] * b_element[
                              3, 0] * f_r_const_113 * l * y2 + (1 / 6) * C[4, 4] * b_element[
                              1, 0] * f_r_const_211 * l + (1 / 6) * C[4, 4] * b_element[1, 0] * f_r_const_212 * l + (
                                      2 / 3) * C[4, 4] * b_element[1, 0] * f_r_const_213 * l + (1 / 6) * C[4, 4] * \
                          b_element[2, 0] * f_r_const_211 * l * x1 + (1 / 6) * C[4, 4] * b_element[
                              2, 0] * f_r_const_212 * l * x2 + (1 / 3) * C[4, 4] * b_element[
                              2, 0] * f_r_const_213 * l * x1 + (1 / 3) * C[4, 4] * b_element[
                              2, 0] * f_r_const_213 * l * x2 + (1 / 6) * C[4, 4] * b_element[
                              3, 0] * f_r_const_211 * l * y1 + (1 / 6) * C[4, 4] * b_element[
                              3, 0] * f_r_const_212 * l * y2 + (1 / 3) * C[4, 4] * b_element[
                              3, 0] * f_r_const_213 * l * y1 + (1 / 3) * C[4, 4] * b_element[
                              3, 0] * f_r_const_213 * l * y2
            K_bv[0, 1] += (1 / 6) * C[3, 3] * b_element[0, 0] * f_r_const_121 * l + (1 / 6) * C[3, 3] * b_element[
                0, 0] * f_r_const_122 * l + (2 / 3) * C[3, 3] * b_element[0, 0] * f_r_const_123 * l + (1 / 6) * C[
                              4, 3] * b_element[0, 0] * f_r_const_221 * l + (1 / 6) * C[4, 3] * b_element[
                              0, 0] * f_r_const_222 * l + (2 / 3) * C[4, 3] * b_element[0, 0] * f_r_const_223 * l + (
                                      1 / 6) * C[4, 3] * b_element[1, 0] * f_r_const_121 * l + (1 / 6) * C[4, 3] * \
                          b_element[1, 0] * f_r_const_122 * l + (2 / 3) * C[4, 3] * b_element[
                              1, 0] * f_r_const_123 * l + (1 / 6) * C[4, 3] * b_element[
                              2, 0] * f_r_const_121 * l * x1 + (1 / 6) * C[4, 3] * b_element[
                              2, 0] * f_r_const_122 * l * x2 + (1 / 3) * C[4, 3] * b_element[
                              2, 0] * f_r_const_123 * l * x1 + (1 / 3) * C[4, 3] * b_element[
                              2, 0] * f_r_const_123 * l * x2 + (1 / 6) * C[4, 3] * b_element[
                              3, 0] * f_r_const_121 * l * y1 + (1 / 6) * C[4, 3] * b_element[
                              3, 0] * f_r_const_122 * l * y2 + (1 / 3) * C[4, 3] * b_element[
                              3, 0] * f_r_const_123 * l * y1 + (1 / 3) * C[4, 3] * b_element[
                              3, 0] * f_r_const_123 * l * y2 + (1 / 6) * C[4, 4] * b_element[
                              1, 0] * f_r_const_221 * l + (1 / 6) * C[4, 4] * b_element[1, 0] * f_r_const_222 * l + (
                                      2 / 3) * C[4, 4] * b_element[1, 0] * f_r_const_223 * l + (1 / 6) * C[4, 4] * \
                          b_element[2, 0] * f_r_const_221 * l * x1 + (1 / 6) * C[4, 4] * b_element[
                              2, 0] * f_r_const_222 * l * x2 + (1 / 3) * C[4, 4] * b_element[
                              2, 0] * f_r_const_223 * l * x1 + (1 / 3) * C[4, 4] * b_element[
                              2, 0] * f_r_const_223 * l * x2 + (1 / 6) * C[4, 4] * b_element[
                              3, 0] * f_r_const_221 * l * y1 + (1 / 6) * C[4, 4] * b_element[
                              3, 0] * f_r_const_222 * l * y2 + (1 / 3) * C[4, 4] * b_element[
                              3, 0] * f_r_const_223 * l * y1 + (1 / 3) * C[4, 4] * b_element[
                              3, 0] * f_r_const_223 * l * y2
            K_bv[1, 0] += (1 / 6) * C[3, 3] * b_element[0, 1] * f_r_const_111 * l + (1 / 6) * C[3, 3] * b_element[
                0, 1] * f_r_const_112 * l + (2 / 3) * C[3, 3] * b_element[0, 1] * f_r_const_113 * l + (1 / 6) * C[
                              4, 3] * b_element[0, 1] * f_r_const_211 * l + (1 / 6) * C[4, 3] * b_element[
                              0, 1] * f_r_const_212 * l + (2 / 3) * C[4, 3] * b_element[0, 1] * f_r_const_213 * l + (
                                      1 / 6) * C[4, 3] * b_element[1, 1] * f_r_const_111 * l + (1 / 6) * C[4, 3] * \
                          b_element[1, 1] * f_r_const_112 * l + (2 / 3) * C[4, 3] * b_element[
                              1, 1] * f_r_const_113 * l + (1 / 6) * C[4, 3] * b_element[
                              2, 1] * f_r_const_111 * l * x1 + (1 / 6) * C[4, 3] * b_element[
                              2, 1] * f_r_const_112 * l * x2 + (1 / 3) * C[4, 3] * b_element[
                              2, 1] * f_r_const_113 * l * x1 + (1 / 3) * C[4, 3] * b_element[
                              2, 1] * f_r_const_113 * l * x2 + (1 / 6) * C[4, 3] * b_element[
                              3, 1] * f_r_const_111 * l * y1 + (1 / 6) * C[4, 3] * b_element[
                              3, 1] * f_r_const_112 * l * y2 + (1 / 3) * C[4, 3] * b_element[
                              3, 1] * f_r_const_113 * l * y1 + (1 / 3) * C[4, 3] * b_element[
                              3, 1] * f_r_const_113 * l * y2 + (1 / 6) * C[4, 4] * b_element[
                              1, 1] * f_r_const_211 * l + (1 / 6) * C[4, 4] * b_element[1, 1] * f_r_const_212 * l + (
                                      2 / 3) * C[4, 4] * b_element[1, 1] * f_r_const_213 * l + (1 / 6) * C[4, 4] * \
                          b_element[2, 1] * f_r_const_211 * l * x1 + (1 / 6) * C[4, 4] * b_element[
                              2, 1] * f_r_const_212 * l * x2 + (1 / 3) * C[4, 4] * b_element[
                              2, 1] * f_r_const_213 * l * x1 + (1 / 3) * C[4, 4] * b_element[
                              2, 1] * f_r_const_213 * l * x2 + (1 / 6) * C[4, 4] * b_element[
                              3, 1] * f_r_const_211 * l * y1 + (1 / 6) * C[4, 4] * b_element[
                              3, 1] * f_r_const_212 * l * y2 + (1 / 3) * C[4, 4] * b_element[
                              3, 1] * f_r_const_213 * l * y1 + (1 / 3) * C[4, 4] * b_element[
                              3, 1] * f_r_const_213 * l * y2
            K_bv[1, 1] += (1 / 6) * C[3, 3] * b_element[0, 1] * f_r_const_121 * l + (1 / 6) * C[3, 3] * b_element[
                0, 1] * f_r_const_122 * l + (2 / 3) * C[3, 3] * b_element[0, 1] * f_r_const_123 * l + (1 / 6) * C[
                              4, 3] * b_element[0, 1] * f_r_const_221 * l + (1 / 6) * C[4, 3] * b_element[
                              0, 1] * f_r_const_222 * l + (2 / 3) * C[4, 3] * b_element[0, 1] * f_r_const_223 * l + (
                                      1 / 6) * C[4, 3] * b_element[1, 1] * f_r_const_121 * l + (1 / 6) * C[4, 3] * \
                          b_element[1, 1] * f_r_const_122 * l + (2 / 3) * C[4, 3] * b_element[
                              1, 1] * f_r_const_123 * l + (1 / 6) * C[4, 3] * b_element[
                              2, 1] * f_r_const_121 * l * x1 + (1 / 6) * C[4, 3] * b_element[
                              2, 1] * f_r_const_122 * l * x2 + (1 / 3) * C[4, 3] * b_element[
                              2, 1] * f_r_const_123 * l * x1 + (1 / 3) * C[4, 3] * b_element[
                              2, 1] * f_r_const_123 * l * x2 + (1 / 6) * C[4, 3] * b_element[
                              3, 1] * f_r_const_121 * l * y1 + (1 / 6) * C[4, 3] * b_element[
                              3, 1] * f_r_const_122 * l * y2 + (1 / 3) * C[4, 3] * b_element[
                              3, 1] * f_r_const_123 * l * y1 + (1 / 3) * C[4, 3] * b_element[
                              3, 1] * f_r_const_123 * l * y2 + (1 / 6) * C[4, 4] * b_element[
                              1, 1] * f_r_const_221 * l + (1 / 6) * C[4, 4] * b_element[1, 1] * f_r_const_222 * l + (
                                      2 / 3) * C[4, 4] * b_element[1, 1] * f_r_const_223 * l + (1 / 6) * C[4, 4] * \
                          b_element[2, 1] * f_r_const_221 * l * x1 + (1 / 6) * C[4, 4] * b_element[
                              2, 1] * f_r_const_222 * l * x2 + (1 / 3) * C[4, 4] * b_element[
                              2, 1] * f_r_const_223 * l * x1 + (1 / 3) * C[4, 4] * b_element[
                              2, 1] * f_r_const_223 * l * x2 + (1 / 6) * C[4, 4] * b_element[
                              3, 1] * f_r_const_221 * l * y1 + (1 / 6) * C[4, 4] * b_element[
                              3, 1] * f_r_const_222 * l * y2 + (1 / 3) * C[4, 4] * b_element[
                              3, 1] * f_r_const_223 * l * y1 + (1 / 3) * C[4, 4] * b_element[
                              3, 1] * f_r_const_223 * l * y2
            K_bv[2, 0] += (1 / 6) * C[3, 3] * b_element[0, 2] * f_r_const_111 * l + (1 / 6) * C[3, 3] * b_element[
                0, 2] * f_r_const_112 * l + (2 / 3) * C[3, 3] * b_element[0, 2] * f_r_const_113 * l + (1 / 6) * C[
                              4, 3] * b_element[0, 2] * f_r_const_211 * l + (1 / 6) * C[4, 3] * b_element[
                              0, 2] * f_r_const_212 * l + (2 / 3) * C[4, 3] * b_element[0, 2] * f_r_const_213 * l + (
                                      1 / 6) * C[4, 3] * b_element[1, 2] * f_r_const_111 * l + (1 / 6) * C[4, 3] * \
                          b_element[1, 2] * f_r_const_112 * l + (2 / 3) * C[4, 3] * b_element[
                              1, 2] * f_r_const_113 * l + (1 / 6) * C[4, 3] * b_element[
                              2, 2] * f_r_const_111 * l * x1 + (1 / 6) * C[4, 3] * b_element[
                              2, 2] * f_r_const_112 * l * x2 + (1 / 3) * C[4, 3] * b_element[
                              2, 2] * f_r_const_113 * l * x1 + (1 / 3) * C[4, 3] * b_element[
                              2, 2] * f_r_const_113 * l * x2 + (1 / 6) * C[4, 3] * b_element[
                              3, 2] * f_r_const_111 * l * y1 + (1 / 6) * C[4, 3] * b_element[
                              3, 2] * f_r_const_112 * l * y2 + (1 / 3) * C[4, 3] * b_element[
                              3, 2] * f_r_const_113 * l * y1 + (1 / 3) * C[4, 3] * b_element[
                              3, 2] * f_r_const_113 * l * y2 + (1 / 6) * C[4, 4] * b_element[
                              1, 2] * f_r_const_211 * l + (1 / 6) * C[4, 4] * b_element[1, 2] * f_r_const_212 * l + (
                                      2 / 3) * C[4, 4] * b_element[1, 2] * f_r_const_213 * l + (1 / 6) * C[4, 4] * \
                          b_element[2, 2] * f_r_const_211 * l * x1 + (1 / 6) * C[4, 4] * b_element[
                              2, 2] * f_r_const_212 * l * x2 + (1 / 3) * C[4, 4] * b_element[
                              2, 2] * f_r_const_213 * l * x1 + (1 / 3) * C[4, 4] * b_element[
                              2, 2] * f_r_const_213 * l * x2 + (1 / 6) * C[4, 4] * b_element[
                              3, 2] * f_r_const_211 * l * y1 + (1 / 6) * C[4, 4] * b_element[
                              3, 2] * f_r_const_212 * l * y2 + (1 / 3) * C[4, 4] * b_element[
                              3, 2] * f_r_const_213 * l * y1 + (1 / 3) * C[4, 4] * b_element[
                              3, 2] * f_r_const_213 * l * y2
            K_bv[2, 1] += (1 / 6) * C[3, 3] * b_element[0, 2] * f_r_const_121 * l + (1 / 6) * C[3, 3] * b_element[
                0, 2] * f_r_const_122 * l + (2 / 3) * C[3, 3] * b_element[0, 2] * f_r_const_123 * l + (1 / 6) * C[
                              4, 3] * b_element[0, 2] * f_r_const_221 * l + (1 / 6) * C[4, 3] * b_element[
                              0, 2] * f_r_const_222 * l + (2 / 3) * C[4, 3] * b_element[0, 2] * f_r_const_223 * l + (
                                      1 / 6) * C[4, 3] * b_element[1, 2] * f_r_const_121 * l + (1 / 6) * C[4, 3] * \
                          b_element[1, 2] * f_r_const_122 * l + (2 / 3) * C[4, 3] * b_element[
                              1, 2] * f_r_const_123 * l + (1 / 6) * C[4, 3] * b_element[
                              2, 2] * f_r_const_121 * l * x1 + (1 / 6) * C[4, 3] * b_element[
                              2, 2] * f_r_const_122 * l * x2 + (1 / 3) * C[4, 3] * b_element[
                              2, 2] * f_r_const_123 * l * x1 + (1 / 3) * C[4, 3] * b_element[
                              2, 2] * f_r_const_123 * l * x2 + (1 / 6) * C[4, 3] * b_element[
                              3, 2] * f_r_const_121 * l * y1 + (1 / 6) * C[4, 3] * b_element[
                              3, 2] * f_r_const_122 * l * y2 + (1 / 3) * C[4, 3] * b_element[
                              3, 2] * f_r_const_123 * l * y1 + (1 / 3) * C[4, 3] * b_element[
                              3, 2] * f_r_const_123 * l * y2 + (1 / 6) * C[4, 4] * b_element[
                              1, 2] * f_r_const_221 * l + (1 / 6) * C[4, 4] * b_element[1, 2] * f_r_const_222 * l + (
                                      2 / 3) * C[4, 4] * b_element[1, 2] * f_r_const_223 * l + (1 / 6) * C[4, 4] * \
                          b_element[2, 2] * f_r_const_221 * l * x1 + (1 / 6) * C[4, 4] * b_element[
                              2, 2] * f_r_const_222 * l * x2 + (1 / 3) * C[4, 4] * b_element[
                              2, 2] * f_r_const_223 * l * x1 + (1 / 3) * C[4, 4] * b_element[
                              2, 2] * f_r_const_223 * l * x2 + (1 / 6) * C[4, 4] * b_element[
                              3, 2] * f_r_const_221 * l * y1 + (1 / 6) * C[4, 4] * b_element[
                              3, 2] * f_r_const_222 * l * y2 + (1 / 3) * C[4, 4] * b_element[
                              3, 2] * f_r_const_223 * l * y1 + (1 / 3) * C[4, 4] * b_element[
                              3, 2] * f_r_const_223 * l * y2
            K_bv[3, 0] += (1 / 6) * C[3, 3] * b_element[0, 3] * f_r_const_111 * l + (1 / 6) * C[3, 3] * b_element[
                0, 3] * f_r_const_112 * l + (2 / 3) * C[3, 3] * b_element[0, 3] * f_r_const_113 * l + (1 / 6) * C[
                              4, 3] * b_element[0, 3] * f_r_const_211 * l + (1 / 6) * C[4, 3] * b_element[
                              0, 3] * f_r_const_212 * l + (2 / 3) * C[4, 3] * b_element[0, 3] * f_r_const_213 * l + (
                                      1 / 6) * C[4, 3] * b_element[1, 3] * f_r_const_111 * l + (1 / 6) * C[4, 3] * \
                          b_element[1, 3] * f_r_const_112 * l + (2 / 3) * C[4, 3] * b_element[
                              1, 3] * f_r_const_113 * l + (1 / 6) * C[4, 3] * b_element[
                              2, 3] * f_r_const_111 * l * x1 + (1 / 6) * C[4, 3] * b_element[
                              2, 3] * f_r_const_112 * l * x2 + (1 / 3) * C[4, 3] * b_element[
                              2, 3] * f_r_const_113 * l * x1 + (1 / 3) * C[4, 3] * b_element[
                              2, 3] * f_r_const_113 * l * x2 + (1 / 6) * C[4, 3] * b_element[
                              3, 3] * f_r_const_111 * l * y1 + (1 / 6) * C[4, 3] * b_element[
                              3, 3] * f_r_const_112 * l * y2 + (1 / 3) * C[4, 3] * b_element[
                              3, 3] * f_r_const_113 * l * y1 + (1 / 3) * C[4, 3] * b_element[
                              3, 3] * f_r_const_113 * l * y2 + (1 / 6) * C[4, 4] * b_element[
                              1, 3] * f_r_const_211 * l + (1 / 6) * C[4, 4] * b_element[1, 3] * f_r_const_212 * l + (
                                      2 / 3) * C[4, 4] * b_element[1, 3] * f_r_const_213 * l + (1 / 6) * C[4, 4] * \
                          b_element[2, 3] * f_r_const_211 * l * x1 + (1 / 6) * C[4, 4] * b_element[
                              2, 3] * f_r_const_212 * l * x2 + (1 / 3) * C[4, 4] * b_element[
                              2, 3] * f_r_const_213 * l * x1 + (1 / 3) * C[4, 4] * b_element[
                              2, 3] * f_r_const_213 * l * x2 + (1 / 6) * C[4, 4] * b_element[
                              3, 3] * f_r_const_211 * l * y1 + (1 / 6) * C[4, 4] * b_element[
                              3, 3] * f_r_const_212 * l * y2 + (1 / 3) * C[4, 4] * b_element[
                              3, 3] * f_r_const_213 * l * y1 + (1 / 3) * C[4, 4] * b_element[
                              3, 3] * f_r_const_213 * l * y2
            K_bv[3, 1] += (1 / 6) * C[3, 3] * b_element[0, 3] * f_r_const_121 * l + (1 / 6) * C[3, 3] * b_element[
                0, 3] * f_r_const_122 * l + (2 / 3) * C[3, 3] * b_element[0, 3] * f_r_const_123 * l + (1 / 6) * C[
                              4, 3] * b_element[0, 3] * f_r_const_221 * l + (1 / 6) * C[4, 3] * b_element[
                              0, 3] * f_r_const_222 * l + (2 / 3) * C[4, 3] * b_element[0, 3] * f_r_const_223 * l + (
                                      1 / 6) * C[4, 3] * b_element[1, 3] * f_r_const_121 * l + (1 / 6) * C[4, 3] * \
                          b_element[1, 3] * f_r_const_122 * l + (2 / 3) * C[4, 3] * b_element[
                              1, 3] * f_r_const_123 * l + (1 / 6) * C[4, 3] * b_element[
                              2, 3] * f_r_const_121 * l * x1 + (1 / 6) * C[4, 3] * b_element[
                              2, 3] * f_r_const_122 * l * x2 + (1 / 3) * C[4, 3] * b_element[
                              2, 3] * f_r_const_123 * l * x1 + (1 / 3) * C[4, 3] * b_element[
                              2, 3] * f_r_const_123 * l * x2 + (1 / 6) * C[4, 3] * b_element[
                              3, 3] * f_r_const_121 * l * y1 + (1 / 6) * C[4, 3] * b_element[
                              3, 3] * f_r_const_122 * l * y2 + (1 / 3) * C[4, 3] * b_element[
                              3, 3] * f_r_const_123 * l * y1 + (1 / 3) * C[4, 3] * b_element[
                              3, 3] * f_r_const_123 * l * y2 + (1 / 6) * C[4, 4] * b_element[
                              1, 3] * f_r_const_221 * l + (1 / 6) * C[4, 4] * b_element[1, 3] * f_r_const_222 * l + (
                                      2 / 3) * C[4, 4] * b_element[1, 3] * f_r_const_223 * l + (1 / 6) * C[4, 4] * \
                          b_element[2, 3] * f_r_const_221 * l * x1 + (1 / 6) * C[4, 4] * b_element[
                              2, 3] * f_r_const_222 * l * x2 + (1 / 3) * C[4, 4] * b_element[
                              2, 3] * f_r_const_223 * l * x1 + (1 / 3) * C[4, 4] * b_element[
                              2, 3] * f_r_const_223 * l * x2 + (1 / 6) * C[4, 4] * b_element[
                              3, 3] * f_r_const_221 * l * y1 + (1 / 6) * C[4, 4] * b_element[
                              3, 3] * f_r_const_222 * l * y2 + (1 / 3) * C[4, 4] * b_element[
                              3, 3] * f_r_const_223 * l * y1 + (1 / 3) * C[4, 4] * b_element[
                              3, 3] * f_r_const_223 * l * y2
            K_bv[4, 0] += (1 / 6) * C[3, 3] * b_element[0, 4] * f_r_const_111 * l + (1 / 6) * C[3, 3] * b_element[
                0, 4] * f_r_const_112 * l + (2 / 3) * C[3, 3] * b_element[0, 4] * f_r_const_113 * l + (1 / 6) * C[
                              4, 3] * b_element[0, 4] * f_r_const_211 * l + (1 / 6) * C[4, 3] * b_element[
                              0, 4] * f_r_const_212 * l + (2 / 3) * C[4, 3] * b_element[0, 4] * f_r_const_213 * l + (
                                      1 / 6) * C[4, 3] * b_element[1, 4] * f_r_const_111 * l + (1 / 6) * C[4, 3] * \
                          b_element[1, 4] * f_r_const_112 * l + (2 / 3) * C[4, 3] * b_element[
                              1, 4] * f_r_const_113 * l + (1 / 6) * C[4, 3] * b_element[
                              2, 4] * f_r_const_111 * l * x1 + (1 / 6) * C[4, 3] * b_element[
                              2, 4] * f_r_const_112 * l * x2 + (1 / 3) * C[4, 3] * b_element[
                              2, 4] * f_r_const_113 * l * x1 + (1 / 3) * C[4, 3] * b_element[
                              2, 4] * f_r_const_113 * l * x2 + (1 / 6) * C[4, 3] * b_element[
                              3, 4] * f_r_const_111 * l * y1 + (1 / 6) * C[4, 3] * b_element[
                              3, 4] * f_r_const_112 * l * y2 + (1 / 3) * C[4, 3] * b_element[
                              3, 4] * f_r_const_113 * l * y1 + (1 / 3) * C[4, 3] * b_element[
                              3, 4] * f_r_const_113 * l * y2 + (1 / 6) * C[4, 4] * b_element[
                              1, 4] * f_r_const_211 * l + (1 / 6) * C[4, 4] * b_element[1, 4] * f_r_const_212 * l + (
                                      2 / 3) * C[4, 4] * b_element[1, 4] * f_r_const_213 * l + (1 / 6) * C[4, 4] * \
                          b_element[2, 4] * f_r_const_211 * l * x1 + (1 / 6) * C[4, 4] * b_element[
                              2, 4] * f_r_const_212 * l * x2 + (1 / 3) * C[4, 4] * b_element[
                              2, 4] * f_r_const_213 * l * x1 + (1 / 3) * C[4, 4] * b_element[
                              2, 4] * f_r_const_213 * l * x2 + (1 / 6) * C[4, 4] * b_element[
                              3, 4] * f_r_const_211 * l * y1 + (1 / 6) * C[4, 4] * b_element[
                              3, 4] * f_r_const_212 * l * y2 + (1 / 3) * C[4, 4] * b_element[
                              3, 4] * f_r_const_213 * l * y1 + (1 / 3) * C[4, 4] * b_element[
                              3, 4] * f_r_const_213 * l * y2
            K_bv[4, 1] += (1 / 6) * C[3, 3] * b_element[0, 4] * f_r_const_121 * l + (1 / 6) * C[3, 3] * b_element[
                0, 4] * f_r_const_122 * l + (2 / 3) * C[3, 3] * b_element[0, 4] * f_r_const_123 * l + (1 / 6) * C[
                              4, 3] * b_element[0, 4] * f_r_const_221 * l + (1 / 6) * C[4, 3] * b_element[
                              0, 4] * f_r_const_222 * l + (2 / 3) * C[4, 3] * b_element[0, 4] * f_r_const_223 * l + (
                                      1 / 6) * C[4, 3] * b_element[1, 4] * f_r_const_121 * l + (1 / 6) * C[4, 3] * \
                          b_element[1, 4] * f_r_const_122 * l + (2 / 3) * C[4, 3] * b_element[
                              1, 4] * f_r_const_123 * l + (1 / 6) * C[4, 3] * b_element[
                              2, 4] * f_r_const_121 * l * x1 + (1 / 6) * C[4, 3] * b_element[
                              2, 4] * f_r_const_122 * l * x2 + (1 / 3) * C[4, 3] * b_element[
                              2, 4] * f_r_const_123 * l * x1 + (1 / 3) * C[4, 3] * b_element[
                              2, 4] * f_r_const_123 * l * x2 + (1 / 6) * C[4, 3] * b_element[
                              3, 4] * f_r_const_121 * l * y1 + (1 / 6) * C[4, 3] * b_element[
                              3, 4] * f_r_const_122 * l * y2 + (1 / 3) * C[4, 3] * b_element[
                              3, 4] * f_r_const_123 * l * y1 + (1 / 3) * C[4, 3] * b_element[
                              3, 4] * f_r_const_123 * l * y2 + (1 / 6) * C[4, 4] * b_element[
                              1, 4] * f_r_const_221 * l + (1 / 6) * C[4, 4] * b_element[1, 4] * f_r_const_222 * l + (
                                      2 / 3) * C[4, 4] * b_element[1, 4] * f_r_const_223 * l + (1 / 6) * C[4, 4] * \
                          b_element[2, 4] * f_r_const_221 * l * x1 + (1 / 6) * C[4, 4] * b_element[
                              2, 4] * f_r_const_222 * l * x2 + (1 / 3) * C[4, 4] * b_element[
                              2, 4] * f_r_const_223 * l * x1 + (1 / 3) * C[4, 4] * b_element[
                              2, 4] * f_r_const_223 * l * x2 + (1 / 6) * C[4, 4] * b_element[
                              3, 4] * f_r_const_221 * l * y1 + (1 / 6) * C[4, 4] * b_element[
                              3, 4] * f_r_const_222 * l * y2 + (1 / 3) * C[4, 4] * b_element[
                              3, 4] * f_r_const_223 * l * y1 + (1 / 3) * C[4, 4] * b_element[
                              3, 4] * f_r_const_223 * l * y2

            K_vv[0, 0] += (2 / 15) * C[3, 3] * f_r_const_111 ** 2 * l - 1 / 15 * C[
                3, 3] * f_r_const_111 * f_r_const_112 * l + (2 / 15) * C[3, 3] * f_r_const_111 * f_r_const_113 * l + (
                                      2 / 15) * C[3, 3] * f_r_const_112 ** 2 * l + (2 / 15) * C[
                              3, 3] * f_r_const_112 * f_r_const_113 * l + (8 / 15) * C[
                              3, 3] * f_r_const_113 ** 2 * l + (4 / 15) * C[
                              4, 3] * f_r_const_111 * f_r_const_211 * l - 1 / 15 * C[
                              4, 3] * f_r_const_111 * f_r_const_212 * l + (2 / 15) * C[
                              4, 3] * f_r_const_111 * f_r_const_213 * l - 1 / 15 * C[
                              4, 3] * f_r_const_112 * f_r_const_211 * l + (4 / 15) * C[
                              4, 3] * f_r_const_112 * f_r_const_212 * l + (2 / 15) * C[
                              4, 3] * f_r_const_112 * f_r_const_213 * l + (2 / 15) * C[
                              4, 3] * f_r_const_113 * f_r_const_211 * l + (2 / 15) * C[
                              4, 3] * f_r_const_113 * f_r_const_212 * l + (16 / 15) * C[
                              4, 3] * f_r_const_113 * f_r_const_213 * l + (2 / 15) * C[
                              4, 4] * f_r_const_211 ** 2 * l - 1 / 15 * C[4, 4] * f_r_const_211 * f_r_const_212 * l + (
                                      2 / 15) * C[4, 4] * f_r_const_211 * f_r_const_213 * l + (2 / 15) * C[
                              4, 4] * f_r_const_212 ** 2 * l + (2 / 15) * C[
                              4, 4] * f_r_const_212 * f_r_const_213 * l + (8 / 15) * C[4, 4] * f_r_const_213 ** 2 * l
            K_vv[0, 1] += (2 / 15) * C[3, 3] * f_r_const_111 * f_r_const_121 * l - 1 / 30 * C[
                3, 3] * f_r_const_111 * f_r_const_122 * l + (1 / 15) * C[
                              3, 3] * f_r_const_111 * f_r_const_123 * l - 1 / 30 * C[
                              3, 3] * f_r_const_112 * f_r_const_121 * l + (2 / 15) * C[
                              3, 3] * f_r_const_112 * f_r_const_122 * l + (1 / 15) * C[
                              3, 3] * f_r_const_112 * f_r_const_123 * l + (1 / 15) * C[
                              3, 3] * f_r_const_113 * f_r_const_121 * l + (1 / 15) * C[
                              3, 3] * f_r_const_113 * f_r_const_122 * l + (8 / 15) * C[
                              3, 3] * f_r_const_113 * f_r_const_123 * l + (2 / 15) * C[
                              4, 3] * f_r_const_111 * f_r_const_221 * l - 1 / 30 * C[
                              4, 3] * f_r_const_111 * f_r_const_222 * l + (1 / 15) * C[
                              4, 3] * f_r_const_111 * f_r_const_223 * l - 1 / 30 * C[
                              4, 3] * f_r_const_112 * f_r_const_221 * l + (2 / 15) * C[
                              4, 3] * f_r_const_112 * f_r_const_222 * l + (1 / 15) * C[
                              4, 3] * f_r_const_112 * f_r_const_223 * l + (1 / 15) * C[
                              4, 3] * f_r_const_113 * f_r_const_221 * l + (1 / 15) * C[
                              4, 3] * f_r_const_113 * f_r_const_222 * l + (8 / 15) * C[
                              4, 3] * f_r_const_113 * f_r_const_223 * l + (2 / 15) * C[
                              4, 3] * f_r_const_121 * f_r_const_211 * l - 1 / 30 * C[
                              4, 3] * f_r_const_121 * f_r_const_212 * l + (1 / 15) * C[
                              4, 3] * f_r_const_121 * f_r_const_213 * l - 1 / 30 * C[
                              4, 3] * f_r_const_122 * f_r_const_211 * l + (2 / 15) * C[
                              4, 3] * f_r_const_122 * f_r_const_212 * l + (1 / 15) * C[
                              4, 3] * f_r_const_122 * f_r_const_213 * l + (1 / 15) * C[
                              4, 3] * f_r_const_123 * f_r_const_211 * l + (1 / 15) * C[
                              4, 3] * f_r_const_123 * f_r_const_212 * l + (8 / 15) * C[
                              4, 3] * f_r_const_123 * f_r_const_213 * l + (2 / 15) * C[
                              4, 4] * f_r_const_211 * f_r_const_221 * l - 1 / 30 * C[
                              4, 4] * f_r_const_211 * f_r_const_222 * l + (1 / 15) * C[
                              4, 4] * f_r_const_211 * f_r_const_223 * l - 1 / 30 * C[
                              4, 4] * f_r_const_212 * f_r_const_221 * l + (2 / 15) * C[
                              4, 4] * f_r_const_212 * f_r_const_222 * l + (1 / 15) * C[
                              4, 4] * f_r_const_212 * f_r_const_223 * l + (1 / 15) * C[
                              4, 4] * f_r_const_213 * f_r_const_221 * l + (1 / 15) * C[
                              4, 4] * f_r_const_213 * f_r_const_222 * l + (8 / 15) * C[
                              4, 4] * f_r_const_213 * f_r_const_223 * l
            K_vv[1, 0] += (2 / 15) * C[3, 3] * f_r_const_111 * f_r_const_121 * l - 1 / 30 * C[
                3, 3] * f_r_const_111 * f_r_const_122 * l + (1 / 15) * C[
                              3, 3] * f_r_const_111 * f_r_const_123 * l - 1 / 30 * C[
                              3, 3] * f_r_const_112 * f_r_const_121 * l + (2 / 15) * C[
                              3, 3] * f_r_const_112 * f_r_const_122 * l + (1 / 15) * C[
                              3, 3] * f_r_const_112 * f_r_const_123 * l + (1 / 15) * C[
                              3, 3] * f_r_const_113 * f_r_const_121 * l + (1 / 15) * C[
                              3, 3] * f_r_const_113 * f_r_const_122 * l + (8 / 15) * C[
                              3, 3] * f_r_const_113 * f_r_const_123 * l + (2 / 15) * C[
                              4, 3] * f_r_const_111 * f_r_const_221 * l - 1 / 30 * C[
                              4, 3] * f_r_const_111 * f_r_const_222 * l + (1 / 15) * C[
                              4, 3] * f_r_const_111 * f_r_const_223 * l - 1 / 30 * C[
                              4, 3] * f_r_const_112 * f_r_const_221 * l + (2 / 15) * C[
                              4, 3] * f_r_const_112 * f_r_const_222 * l + (1 / 15) * C[
                              4, 3] * f_r_const_112 * f_r_const_223 * l + (1 / 15) * C[
                              4, 3] * f_r_const_113 * f_r_const_221 * l + (1 / 15) * C[
                              4, 3] * f_r_const_113 * f_r_const_222 * l + (8 / 15) * C[
                              4, 3] * f_r_const_113 * f_r_const_223 * l + (2 / 15) * C[
                              4, 3] * f_r_const_121 * f_r_const_211 * l - 1 / 30 * C[
                              4, 3] * f_r_const_121 * f_r_const_212 * l + (1 / 15) * C[
                              4, 3] * f_r_const_121 * f_r_const_213 * l - 1 / 30 * C[
                              4, 3] * f_r_const_122 * f_r_const_211 * l + (2 / 15) * C[
                              4, 3] * f_r_const_122 * f_r_const_212 * l + (1 / 15) * C[
                              4, 3] * f_r_const_122 * f_r_const_213 * l + (1 / 15) * C[
                              4, 3] * f_r_const_123 * f_r_const_211 * l + (1 / 15) * C[
                              4, 3] * f_r_const_123 * f_r_const_212 * l + (8 / 15) * C[
                              4, 3] * f_r_const_123 * f_r_const_213 * l + (2 / 15) * C[
                              4, 4] * f_r_const_211 * f_r_const_221 * l - 1 / 30 * C[
                              4, 4] * f_r_const_211 * f_r_const_222 * l + (1 / 15) * C[
                              4, 4] * f_r_const_211 * f_r_const_223 * l - 1 / 30 * C[
                              4, 4] * f_r_const_212 * f_r_const_221 * l + (2 / 15) * C[
                              4, 4] * f_r_const_212 * f_r_const_222 * l + (1 / 15) * C[
                              4, 4] * f_r_const_212 * f_r_const_223 * l + (1 / 15) * C[
                              4, 4] * f_r_const_213 * f_r_const_221 * l + (1 / 15) * C[
                              4, 4] * f_r_const_213 * f_r_const_222 * l + (8 / 15) * C[
                              4, 4] * f_r_const_213 * f_r_const_223 * l
            K_vv[1, 1] += (2 / 15) * C[3, 3] * f_r_const_121 ** 2 * l - 1 / 15 * C[
                3, 3] * f_r_const_121 * f_r_const_122 * l + (2 / 15) * C[3, 3] * f_r_const_121 * f_r_const_123 * l + (
                                      2 / 15) * C[3, 3] * f_r_const_122 ** 2 * l + (2 / 15) * C[
                              3, 3] * f_r_const_122 * f_r_const_123 * l + (8 / 15) * C[
                              3, 3] * f_r_const_123 ** 2 * l + (4 / 15) * C[
                              4, 3] * f_r_const_121 * f_r_const_221 * l - 1 / 15 * C[
                              4, 3] * f_r_const_121 * f_r_const_222 * l + (2 / 15) * C[
                              4, 3] * f_r_const_121 * f_r_const_223 * l - 1 / 15 * C[
                              4, 3] * f_r_const_122 * f_r_const_221 * l + (4 / 15) * C[
                              4, 3] * f_r_const_122 * f_r_const_222 * l + (2 / 15) * C[
                              4, 3] * f_r_const_122 * f_r_const_223 * l + (2 / 15) * C[
                              4, 3] * f_r_const_123 * f_r_const_221 * l + (2 / 15) * C[
                              4, 3] * f_r_const_123 * f_r_const_222 * l + (16 / 15) * C[
                              4, 3] * f_r_const_123 * f_r_const_223 * l + (2 / 15) * C[
                              4, 4] * f_r_const_221 ** 2 * l - 1 / 15 * C[4, 4] * f_r_const_221 * f_r_const_222 * l + (
                                      2 / 15) * C[4, 4] * f_r_const_221 * f_r_const_223 * l + (2 / 15) * C[
                              4, 4] * f_r_const_222 ** 2 * l + (2 / 15) * C[
                              4, 4] * f_r_const_222 * f_r_const_223 * l + (8 / 15) * C[4, 4] * f_r_const_223 ** 2 * l

        self._K_vv = K_vv
        self._K_bv = K_bv

    def _set_cross_section_matrix_p(self):
        """
        Set the shear correction matrix p.
        """
        p_v = np.zeros((2, 2))
        p_q = np.zeros((2, 7))

        elements = self._discreet_geometry.elements
        for element in elements:
            l = element.length
            C = element.material.stiffness.K_Jung
            b_element = element.b

            pos1 = element.node1_midsurface_position
            pos2 = element.node2_midsurface_position

            omega1 = element.node1.integral_values['int_rtorsional_ds']
            omega2 = element.node2.integral_values['int_rtorsional_ds']

            x1 = pos1.x
            x2 = pos2.x
            y1 = pos1.y
            y2 = pos2.y

            f_r_1 = element.f_r_1
            f_r_2 = element.f_r_2
            f_r_3 = element.f_r_3

            f_r_const_111 = f_r_1[0, 0]
            f_r_const_112 = f_r_2[0, 0]
            f_r_const_113 = f_r_3[0, 0]

            f_r_const_121 = f_r_1[0, 1]
            f_r_const_122 = f_r_2[0, 1]
            f_r_const_123 = f_r_3[0, 1]

            f_r_const_211 = f_r_1[1, 0]
            f_r_const_212 = f_r_2[1, 0]
            f_r_const_213 = f_r_3[1, 0]

            f_r_const_221 = f_r_1[1, 1]
            f_r_const_222 = f_r_2[1, 1]
            f_r_const_223 = f_r_3[1, 1]

            p_v[0, 0] += 0.0666666666666664 * C[3, 3] * f_r_const_111 ** 2 * l - 0.0333333333333332 * C[
                3, 3] * f_r_const_111 * f_r_const_112 * l + 0.0666666666666664 * C[
                             3, 3] * f_r_const_111 * f_r_const_113 * l + 0.0666666666666667 * C[
                             3, 3] * f_r_const_112 ** 2 * l + 0.0666666666666664 * C[
                             3, 3] * f_r_const_112 * f_r_const_113 * l + 0.266666666666667 * C[
                             3, 3] * f_r_const_113 ** 2 * l + 0.0666666666666664 * C[
                             4, 3] * f_r_const_111 * f_r_const_211 * l - 0.0166666666666666 * C[
                             4, 3] * f_r_const_111 * f_r_const_212 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_111 * f_r_const_213 * l - 0.0166666666666666 * C[
                             4, 3] * f_r_const_112 * f_r_const_211 * l + 0.0666666666666667 * C[
                             4, 3] * f_r_const_112 * f_r_const_212 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_112 * f_r_const_213 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_113 * f_r_const_211 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_113 * f_r_const_212 * l + 0.266666666666667 * C[
                             4, 3] * f_r_const_113 * f_r_const_213 * l
            p_v[0, 1] += 0.0666666666666664 * C[3, 3] * f_r_const_111 * f_r_const_121 * l - 0.0166666666666666 * C[
                3, 3] * f_r_const_111 * f_r_const_122 * l + 0.0333333333333332 * C[
                             3, 3] * f_r_const_111 * f_r_const_123 * l - 0.0166666666666666 * C[
                             3, 3] * f_r_const_112 * f_r_const_121 * l + 0.0666666666666667 * C[
                             3, 3] * f_r_const_112 * f_r_const_122 * l + 0.0333333333333332 * C[
                             3, 3] * f_r_const_112 * f_r_const_123 * l + 0.0333333333333332 * C[
                             3, 3] * f_r_const_113 * f_r_const_121 * l + 0.0333333333333332 * C[
                             3, 3] * f_r_const_113 * f_r_const_122 * l + 0.266666666666667 * C[
                             3, 3] * f_r_const_113 * f_r_const_123 * l + 0.0666666666666664 * C[
                             4, 3] * f_r_const_111 * f_r_const_221 * l - 0.0166666666666666 * C[
                             4, 3] * f_r_const_111 * f_r_const_222 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_111 * f_r_const_223 * l - 0.0166666666666666 * C[
                             4, 3] * f_r_const_112 * f_r_const_221 * l + 0.0666666666666667 * C[
                             4, 3] * f_r_const_112 * f_r_const_222 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_112 * f_r_const_223 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_113 * f_r_const_221 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_113 * f_r_const_222 * l + 0.266666666666667 * C[
                             4, 3] * f_r_const_113 * f_r_const_223 * l
            p_v[1, 0] += 0.0666666666666664 * C[3, 3] * f_r_const_111 * f_r_const_121 * l - 0.0166666666666666 * C[
                3, 3] * f_r_const_111 * f_r_const_122 * l + 0.0333333333333332 * C[
                             3, 3] * f_r_const_111 * f_r_const_123 * l - 0.0166666666666666 * C[
                             3, 3] * f_r_const_112 * f_r_const_121 * l + 0.0666666666666667 * C[
                             3, 3] * f_r_const_112 * f_r_const_122 * l + 0.0333333333333332 * C[
                             3, 3] * f_r_const_112 * f_r_const_123 * l + 0.0333333333333332 * C[
                             3, 3] * f_r_const_113 * f_r_const_121 * l + 0.0333333333333332 * C[
                             3, 3] * f_r_const_113 * f_r_const_122 * l + 0.266666666666667 * C[
                             3, 3] * f_r_const_113 * f_r_const_123 * l + 0.0666666666666664 * C[
                             4, 3] * f_r_const_121 * f_r_const_211 * l - 0.0166666666666666 * C[
                             4, 3] * f_r_const_121 * f_r_const_212 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_121 * f_r_const_213 * l - 0.0166666666666666 * C[
                             4, 3] * f_r_const_122 * f_r_const_211 * l + 0.0666666666666667 * C[
                             4, 3] * f_r_const_122 * f_r_const_212 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_122 * f_r_const_213 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_123 * f_r_const_211 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_123 * f_r_const_212 * l + 0.266666666666667 * C[
                             4, 3] * f_r_const_123 * f_r_const_213 * l
            p_v[1, 1] += 0.0666666666666664 * C[3, 3] * f_r_const_121 ** 2 * l - 0.0333333333333332 * C[
                3, 3] * f_r_const_121 * f_r_const_122 * l + 0.0666666666666664 * C[
                             3, 3] * f_r_const_121 * f_r_const_123 * l + 0.0666666666666667 * C[
                             3, 3] * f_r_const_122 ** 2 * l + 0.0666666666666664 * C[
                             3, 3] * f_r_const_122 * f_r_const_123 * l + 0.266666666666667 * C[
                             3, 3] * f_r_const_123 ** 2 * l + 0.0666666666666664 * C[
                             4, 3] * f_r_const_121 * f_r_const_221 * l - 0.0166666666666666 * C[
                             4, 3] * f_r_const_121 * f_r_const_222 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_121 * f_r_const_223 * l - 0.0166666666666666 * C[
                             4, 3] * f_r_const_122 * f_r_const_221 * l + 0.0666666666666667 * C[
                             4, 3] * f_r_const_122 * f_r_const_222 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_122 * f_r_const_223 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_123 * f_r_const_221 * l + 0.0333333333333332 * C[
                             4, 3] * f_r_const_123 * f_r_const_222 * l + 0.266666666666667 * C[
                             4, 3] * f_r_const_123 * f_r_const_223 * l

            p_q[0, 0] += 0.0833333333333333 * C[3, 0] * f_r_const_111 * l + 0.0833333333333333 * C[
                3, 0] * f_r_const_112 * l + 0.333333333333333 * C[3, 0] * f_r_const_113 * l + 0.0833333333333333 * C[
                             3, 3] * b_element[0, 0] * f_r_const_111 * l + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 0] * f_r_const_112 * l + 0.333333333333333 * C[3, 3] * b_element[
                             0, 0] * f_r_const_113 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 0] * f_r_const_111 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 0] * f_r_const_112 * l + 0.333333333333333 * C[4, 3] * b_element[
                             1, 0] * f_r_const_113 * l + 0.0833333333333334 * C[4, 3] * b_element[
                             2, 0] * f_r_const_111 * l * x1 + 0.0833333333333333 * C[4, 3] * b_element[
                             2, 0] * f_r_const_112 * l * x2 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 0] * f_r_const_113 * l * x1 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 0] * f_r_const_113 * l * x2 + 0.0833333333333334 * C[4, 3] * b_element[
                             3, 0] * f_r_const_111 * l * y1 + 0.0833333333333333 * C[4, 3] * b_element[
                             3, 0] * f_r_const_112 * l * y2 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 0] * f_r_const_113 * l * y1 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 0] * f_r_const_113 * l * y2
            p_q[0, 1] += -0.0833333333333333 * C[1, 3] * f_r_const_111 * x1 + 0.0833333333333333 * C[
                1, 3] * f_r_const_111 * x2 - 0.0833333333333333 * C[1, 3] * f_r_const_112 * x1 + 0.0833333333333333 * C[
                             1, 3] * f_r_const_112 * x2 - 0.333333333333333 * C[
                             1, 3] * f_r_const_113 * x1 + 0.333333333333333 * C[
                             1, 3] * f_r_const_113 * x2 + 0.0833333333333335 * C[
                             3, 0] * f_r_const_111 * l * y1 + 0.0833333333333333 * C[
                             3, 0] * f_r_const_112 * l * y2 + 0.166666666666667 * C[
                             3, 0] * f_r_const_113 * l * y1 + 0.166666666666667 * C[
                             3, 0] * f_r_const_113 * l * y2 + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 1] * f_r_const_111 * l + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 1] * f_r_const_112 * l + 0.333333333333333 * C[3, 3] * b_element[
                             0, 1] * f_r_const_113 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 1] * f_r_const_111 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 1] * f_r_const_112 * l + 0.333333333333333 * C[4, 3] * b_element[
                             1, 1] * f_r_const_113 * l + 0.0833333333333334 * C[4, 3] * b_element[
                             2, 1] * f_r_const_111 * l * x1 + 0.0833333333333333 * C[4, 3] * b_element[
                             2, 1] * f_r_const_112 * l * x2 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 1] * f_r_const_113 * l * x1 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 1] * f_r_const_113 * l * x2 + 0.0833333333333334 * C[4, 3] * b_element[
                             3, 1] * f_r_const_111 * l * y1 + 0.0833333333333333 * C[4, 3] * b_element[
                             3, 1] * f_r_const_112 * l * y2 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 1] * f_r_const_113 * l * y1 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 1] * f_r_const_113 * l * y2
            p_q[0, 2] += 0.0833333333333334 * C[0, 3] * f_r_const_111 * l * x1 + 0.0833333333333333 * C[
                0, 3] * f_r_const_112 * l * x2 + 0.166666666666667 * C[
                             0, 3] * f_r_const_113 * l * x1 + 0.166666666666667 * C[
                             0, 3] * f_r_const_113 * l * x2 - 0.0833333333333333 * C[
                             1, 3] * f_r_const_111 * y1 + 0.0833333333333333 * C[
                             1, 3] * f_r_const_111 * y2 - 0.0833333333333333 * C[
                             1, 3] * f_r_const_112 * y1 + 0.0833333333333333 * C[
                             1, 3] * f_r_const_112 * y2 - 0.333333333333333 * C[
                             1, 3] * f_r_const_113 * y1 + 0.333333333333333 * C[
                             1, 3] * f_r_const_113 * y2 + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 2] * f_r_const_111 * l + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 2] * f_r_const_112 * l + 0.333333333333333 * C[3, 3] * b_element[
                             0, 2] * f_r_const_113 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 2] * f_r_const_111 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 2] * f_r_const_112 * l + 0.333333333333333 * C[4, 3] * b_element[
                             1, 2] * f_r_const_113 * l + 0.0833333333333334 * C[4, 3] * b_element[
                             2, 2] * f_r_const_111 * l * x1 + 0.0833333333333333 * C[4, 3] * b_element[
                             2, 2] * f_r_const_112 * l * x2 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 2] * f_r_const_113 * l * x1 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 2] * f_r_const_113 * l * x2 + 0.0833333333333334 * C[4, 3] * b_element[
                             3, 2] * f_r_const_111 * l * y1 + 0.0833333333333333 * C[4, 3] * b_element[
                             3, 2] * f_r_const_112 * l * y2 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 2] * f_r_const_113 * l * y1 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 2] * f_r_const_113 * l * y2
            p_q[0, 3] += 0.166666666666667 * C[3, 2] * f_r_const_111 * l + 0.166666666666667 * C[
                3, 2] * f_r_const_112 * l + 0.666666666666667 * C[3, 2] * f_r_const_113 * l + 0.0833333333333333 * C[
                             3, 3] * b_element[0, 3] * f_r_const_111 * l + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 3] * f_r_const_112 * l + 0.333333333333333 * C[3, 3] * b_element[
                             0, 3] * f_r_const_113 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 3] * f_r_const_111 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 3] * f_r_const_112 * l + 0.333333333333333 * C[4, 3] * b_element[
                             1, 3] * f_r_const_113 * l + 0.0833333333333334 * C[4, 3] * b_element[
                             2, 3] * f_r_const_111 * l * x1 + 0.0833333333333333 * C[4, 3] * b_element[
                             2, 3] * f_r_const_112 * l * x2 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 3] * f_r_const_113 * l * x1 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 3] * f_r_const_113 * l * x2 + 0.0833333333333334 * C[4, 3] * b_element[
                             3, 3] * f_r_const_111 * l * y1 + 0.0833333333333333 * C[4, 3] * b_element[
                             3, 3] * f_r_const_112 * l * y2 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 3] * f_r_const_113 * l * y1 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 3] * f_r_const_113 * l * y2 + 0.0833333333333333 * f_r_const_111 * l * (
                                     -omega1 / l + omega2 / l) - 0.0833333333333333 * f_r_const_111 * x1 * y2 + 0.0833333333333333 * f_r_const_111 * x2 * y1 + 0.0833333333333333 * f_r_const_112 * l * (
                                     -omega1 / l + omega2 / l) - 0.0833333333333333 * f_r_const_112 * x1 * y2 + 0.0833333333333333 * f_r_const_112 * x2 * y1 + 0.333333333333333 * f_r_const_113 * l * (
                                     -omega1 / l + omega2 / l) - 0.333333333333333 * f_r_const_113 * x1 * y2 + 0.333333333333333 * f_r_const_113 * x2 * y1
            p_q[0, 4] += 0.0833333333333334 * C[0, 3] * f_r_const_111 * l * omega1 + 0.0833333333333333 * C[
                0, 3] * f_r_const_112 * l * omega2 + 0.166666666666667 * C[
                             0, 3] * f_r_const_113 * l * omega1 + 0.166666666666667 * C[
                             0, 3] * f_r_const_113 * l * omega2 + 0.0833333333333335 * C[
                             3, 1] * f_r_const_111 * x1 ** 2 - 0.0833333333333333 * C[
                             3, 1] * f_r_const_111 * x1 * x2 + 0.0833333333333335 * C[
                             3, 1] * f_r_const_111 * y1 ** 2 - 0.0833333333333333 * C[
                             3, 1] * f_r_const_111 * y1 * y2 + 0.0833333333333334 * C[
                             3, 1] * f_r_const_112 * x1 * x2 - 0.0833333333333333 * C[
                             3, 1] * f_r_const_112 * x2 ** 2 + 0.0833333333333334 * C[
                             3, 1] * f_r_const_112 * y1 * y2 - 0.0833333333333333 * C[
                             3, 1] * f_r_const_112 * y2 ** 2 + 0.166666666666667 * C[
                             3, 1] * f_r_const_113 * x1 ** 2 - 0.166666666666667 * C[
                             3, 1] * f_r_const_113 * x2 ** 2 + 0.166666666666667 * C[
                             3, 1] * f_r_const_113 * y1 ** 2 - 0.166666666666667 * C[
                             3, 1] * f_r_const_113 * y2 ** 2 + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 4] * f_r_const_111 * l + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 4] * f_r_const_112 * l + 0.333333333333333 * C[3, 3] * b_element[
                             0, 4] * f_r_const_113 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 4] * f_r_const_111 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 4] * f_r_const_112 * l + 0.333333333333333 * C[4, 3] * b_element[
                             1, 4] * f_r_const_113 * l + 0.0833333333333334 * C[4, 3] * b_element[
                             2, 4] * f_r_const_111 * l * x1 + 0.0833333333333333 * C[4, 3] * b_element[
                             2, 4] * f_r_const_112 * l * x2 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 4] * f_r_const_113 * l * x1 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 4] * f_r_const_113 * l * x2 + 0.0833333333333334 * C[4, 3] * b_element[
                             3, 4] * f_r_const_111 * l * y1 + 0.0833333333333333 * C[4, 3] * b_element[
                             3, 4] * f_r_const_112 * l * y2 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 4] * f_r_const_113 * l * y1 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 4] * f_r_const_113 * l * y2
            p_q[
                0, 5] += 0.0833333333333333 * f_r_const_111 * x1 - 0.0833333333333333 * f_r_const_111 * x2 + 0.0833333333333333 * f_r_const_112 * x1 - 0.0833333333333333 * f_r_const_112 * x2 + 0.333333333333333 * f_r_const_113 * x1 - 0.333333333333333 * f_r_const_113 * x2
            p_q[
                0, 6] += 0.0833333333333333 * f_r_const_111 * y1 - 0.0833333333333333 * f_r_const_111 * y2 + 0.0833333333333333 * f_r_const_112 * y1 - 0.0833333333333333 * f_r_const_112 * y2 + 0.333333333333333 * f_r_const_113 * y1 - 0.333333333333333 * f_r_const_113 * y2
            p_q[1, 0] += 0.0833333333333333 * C[3, 0] * f_r_const_121 * l + 0.0833333333333333 * C[
                3, 0] * f_r_const_122 * l + 0.333333333333333 * C[3, 0] * f_r_const_123 * l + 0.0833333333333333 * C[
                             3, 3] * b_element[0, 0] * f_r_const_121 * l + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 0] * f_r_const_122 * l + 0.333333333333333 * C[3, 3] * b_element[
                             0, 0] * f_r_const_123 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 0] * f_r_const_121 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 0] * f_r_const_122 * l + 0.333333333333333 * C[4, 3] * b_element[
                             1, 0] * f_r_const_123 * l + 0.0833333333333334 * C[4, 3] * b_element[
                             2, 0] * f_r_const_121 * l * x1 + 0.0833333333333333 * C[4, 3] * b_element[
                             2, 0] * f_r_const_122 * l * x2 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 0] * f_r_const_123 * l * x1 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 0] * f_r_const_123 * l * x2 + 0.0833333333333334 * C[4, 3] * b_element[
                             3, 0] * f_r_const_121 * l * y1 + 0.0833333333333333 * C[4, 3] * b_element[
                             3, 0] * f_r_const_122 * l * y2 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 0] * f_r_const_123 * l * y1 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 0] * f_r_const_123 * l * y2
            p_q[1, 1] += -0.0833333333333333 * C[1, 3] * f_r_const_121 * x1 + 0.0833333333333333 * C[
                1, 3] * f_r_const_121 * x2 - 0.0833333333333333 * C[1, 3] * f_r_const_122 * x1 + 0.0833333333333333 * C[
                             1, 3] * f_r_const_122 * x2 - 0.333333333333333 * C[
                             1, 3] * f_r_const_123 * x1 + 0.333333333333333 * C[
                             1, 3] * f_r_const_123 * x2 + 0.0833333333333335 * C[
                             3, 0] * f_r_const_121 * l * y1 + 0.0833333333333333 * C[
                             3, 0] * f_r_const_122 * l * y2 + 0.166666666666667 * C[
                             3, 0] * f_r_const_123 * l * y1 + 0.166666666666667 * C[
                             3, 0] * f_r_const_123 * l * y2 + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 1] * f_r_const_121 * l + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 1] * f_r_const_122 * l + 0.333333333333333 * C[3, 3] * b_element[
                             0, 1] * f_r_const_123 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 1] * f_r_const_121 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 1] * f_r_const_122 * l + 0.333333333333333 * C[4, 3] * b_element[
                             1, 1] * f_r_const_123 * l + 0.0833333333333334 * C[4, 3] * b_element[
                             2, 1] * f_r_const_121 * l * x1 + 0.0833333333333333 * C[4, 3] * b_element[
                             2, 1] * f_r_const_122 * l * x2 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 1] * f_r_const_123 * l * x1 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 1] * f_r_const_123 * l * x2 + 0.0833333333333334 * C[4, 3] * b_element[
                             3, 1] * f_r_const_121 * l * y1 + 0.0833333333333333 * C[4, 3] * b_element[
                             3, 1] * f_r_const_122 * l * y2 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 1] * f_r_const_123 * l * y1 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 1] * f_r_const_123 * l * y2
            p_q[1, 2] += 0.0833333333333334 * C[0, 3] * f_r_const_121 * l * x1 + 0.0833333333333333 * C[
                0, 3] * f_r_const_122 * l * x2 + 0.166666666666667 * C[
                             0, 3] * f_r_const_123 * l * x1 + 0.166666666666667 * C[
                             0, 3] * f_r_const_123 * l * x2 - 0.0833333333333333 * C[
                             1, 3] * f_r_const_121 * y1 + 0.0833333333333333 * C[
                             1, 3] * f_r_const_121 * y2 - 0.0833333333333333 * C[
                             1, 3] * f_r_const_122 * y1 + 0.0833333333333333 * C[
                             1, 3] * f_r_const_122 * y2 - 0.333333333333333 * C[
                             1, 3] * f_r_const_123 * y1 + 0.333333333333333 * C[
                             1, 3] * f_r_const_123 * y2 + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 2] * f_r_const_121 * l + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 2] * f_r_const_122 * l + 0.333333333333333 * C[3, 3] * b_element[
                             0, 2] * f_r_const_123 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 2] * f_r_const_121 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 2] * f_r_const_122 * l + 0.333333333333333 * C[4, 3] * b_element[
                             1, 2] * f_r_const_123 * l + 0.0833333333333334 * C[4, 3] * b_element[
                             2, 2] * f_r_const_121 * l * x1 + 0.0833333333333333 * C[4, 3] * b_element[
                             2, 2] * f_r_const_122 * l * x2 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 2] * f_r_const_123 * l * x1 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 2] * f_r_const_123 * l * x2 + 0.0833333333333334 * C[4, 3] * b_element[
                             3, 2] * f_r_const_121 * l * y1 + 0.0833333333333333 * C[4, 3] * b_element[
                             3, 2] * f_r_const_122 * l * y2 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 2] * f_r_const_123 * l * y1 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 2] * f_r_const_123 * l * y2
            p_q[1, 3] += 0.166666666666667 * C[3, 2] * f_r_const_121 * l + 0.166666666666667 * C[
                3, 2] * f_r_const_122 * l + 0.666666666666667 * C[3, 2] * f_r_const_123 * l + 0.0833333333333333 * C[
                             3, 3] * b_element[0, 3] * f_r_const_121 * l + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 3] * f_r_const_122 * l + 0.333333333333333 * C[3, 3] * b_element[
                             0, 3] * f_r_const_123 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 3] * f_r_const_121 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 3] * f_r_const_122 * l + 0.333333333333333 * C[4, 3] * b_element[
                             1, 3] * f_r_const_123 * l + 0.0833333333333334 * C[4, 3] * b_element[
                             2, 3] * f_r_const_121 * l * x1 + 0.0833333333333333 * C[4, 3] * b_element[
                             2, 3] * f_r_const_122 * l * x2 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 3] * f_r_const_123 * l * x1 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 3] * f_r_const_123 * l * x2 + 0.0833333333333334 * C[4, 3] * b_element[
                             3, 3] * f_r_const_121 * l * y1 + 0.0833333333333333 * C[4, 3] * b_element[
                             3, 3] * f_r_const_122 * l * y2 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 3] * f_r_const_123 * l * y1 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 3] * f_r_const_123 * l * y2 + 0.0833333333333333 * f_r_const_121 * l * (
                                     -omega1 / l + omega2 / l) - 0.0833333333333333 * f_r_const_121 * x1 * y2 + 0.0833333333333333 * f_r_const_121 * x2 * y1 + 0.0833333333333333 * f_r_const_122 * l * (
                                     -omega1 / l + omega2 / l) - 0.0833333333333333 * f_r_const_122 * x1 * y2 + 0.0833333333333333 * f_r_const_122 * x2 * y1 + 0.333333333333333 * f_r_const_123 * l * (
                                     -omega1 / l + omega2 / l) - 0.333333333333333 * f_r_const_123 * x1 * y2 + 0.333333333333333 * f_r_const_123 * x2 * y1
            p_q[1, 4] += 0.0833333333333334 * C[0, 3] * f_r_const_121 * l * omega1 + 0.0833333333333333 * C[
                0, 3] * f_r_const_122 * l * omega2 + 0.166666666666667 * C[
                             0, 3] * f_r_const_123 * l * omega1 + 0.166666666666667 * C[
                             0, 3] * f_r_const_123 * l * omega2 + 0.0833333333333335 * C[
                             3, 1] * f_r_const_121 * x1 ** 2 - 0.0833333333333333 * C[
                             3, 1] * f_r_const_121 * x1 * x2 + 0.0833333333333335 * C[
                             3, 1] * f_r_const_121 * y1 ** 2 - 0.0833333333333333 * C[
                             3, 1] * f_r_const_121 * y1 * y2 + 0.0833333333333334 * C[
                             3, 1] * f_r_const_122 * x1 * x2 - 0.0833333333333333 * C[
                             3, 1] * f_r_const_122 * x2 ** 2 + 0.0833333333333334 * C[
                             3, 1] * f_r_const_122 * y1 * y2 - 0.0833333333333333 * C[
                             3, 1] * f_r_const_122 * y2 ** 2 + 0.166666666666667 * C[
                             3, 1] * f_r_const_123 * x1 ** 2 - 0.166666666666667 * C[
                             3, 1] * f_r_const_123 * x2 ** 2 + 0.166666666666667 * C[
                             3, 1] * f_r_const_123 * y1 ** 2 - 0.166666666666667 * C[
                             3, 1] * f_r_const_123 * y2 ** 2 + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 4] * f_r_const_121 * l + 0.0833333333333333 * C[3, 3] * b_element[
                             0, 4] * f_r_const_122 * l + 0.333333333333333 * C[3, 3] * b_element[
                             0, 4] * f_r_const_123 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 4] * f_r_const_121 * l + 0.0833333333333333 * C[4, 3] * b_element[
                             1, 4] * f_r_const_122 * l + 0.333333333333333 * C[4, 3] * b_element[
                             1, 4] * f_r_const_123 * l + 0.0833333333333334 * C[4, 3] * b_element[
                             2, 4] * f_r_const_121 * l * x1 + 0.0833333333333333 * C[4, 3] * b_element[
                             2, 4] * f_r_const_122 * l * x2 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 4] * f_r_const_123 * l * x1 + 0.166666666666667 * C[4, 3] * b_element[
                             2, 4] * f_r_const_123 * l * x2 + 0.0833333333333334 * C[4, 3] * b_element[
                             3, 4] * f_r_const_121 * l * y1 + 0.0833333333333333 * C[4, 3] * b_element[
                             3, 4] * f_r_const_122 * l * y2 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 4] * f_r_const_123 * l * y1 + 0.166666666666667 * C[4, 3] * b_element[
                             3, 4] * f_r_const_123 * l * y2
            p_q[
                1, 5] += 0.0833333333333333 * f_r_const_121 * x1 - 0.0833333333333333 * f_r_const_121 * x2 + 0.0833333333333333 * f_r_const_122 * x1 - 0.0833333333333333 * f_r_const_122 * x2 + 0.333333333333333 * f_r_const_123 * x1 - 0.333333333333333 * f_r_const_123 * x2
            p_q[
                1, 6] += 0.0833333333333333 * f_r_const_121 * y1 - 0.0833333333333333 * f_r_const_121 * y2 + 0.0833333333333333 * f_r_const_122 * y1 - 0.0833333333333333 * f_r_const_122 * y2 + 0.333333333333333 * f_r_const_123 * y1 - 0.333333333333333 * f_r_const_123 * y2

        self._p_v = p_v
        self._p_q = p_q
        self._p = -np.linalg.solve(p_v, p_q)

    def _set_element_f_r_matrices(self):
        """
        Set the f_r matrices to the elements.
        """
        K_bb_inv = self._K_bb_inv

        elements = self._discreet_geometry.elements
        for element in elements:
            f_r_1 = np.zeros((2, 2))
            f_r_2 = np.zeros((2, 2))
            f_r_3 = np.zeros((2, 2))

            B_element = element.B

            pos1 = element.node1_midsurface_position
            pos2 = element.node2_midsurface_position

            x1 = pos1.x
            x2 = pos2.x
            y1 = pos1.y
            y2 = pos2.y

            int_A11_ds1 = element.integral_values_0['int_A11_ds']
            int_A11_ds2 = element.integral_values_l['int_A11_ds']
            int_B16_ds1 = element.integral_values_0['int_B16_ds']
            int_B16_ds2 = element.integral_values_l['int_B16_ds']
            int_D16_ds1 = element.integral_values_0['int_D16_ds']
            int_D16_ds2 = element.integral_values_l['int_D16_ds']
            int_A11_x_ds1 = element.integral_values_0['int_A11_x_ds']
            int_A11_x_ds2 = element.integral_values_l['int_A11_x_ds']
            int_A11_y_ds1 = element.integral_values_0['int_A11_y_ds']
            int_A11_y_ds2 = element.integral_values_l['int_A11_y_ds']
            int_A11_omega_ds1 = element.integral_values_0['int_A11_omega_ds']
            int_A11_omega_ds2 = element.integral_values_l['int_A11_omega_ds']
            int_B16_x_ds1 = element.integral_values_0['int_B16_x_ds']
            int_B16_x_ds2 = element.integral_values_l['int_B16_x_ds']
            int_B16_y_ds1 = element.integral_values_0['int_B16_y_ds']
            int_B16_y_ds2 = element.integral_values_l['int_B16_y_ds']
            int_B16_omega_ds1 = element.integral_values_0['int_B16_omega_ds']
            int_B16_omega_ds2 = element.integral_values_l['int_B16_omega_ds']
            int_A11_x_ds3 = element.integral_values_l_half['int_A11_x_ds']
            int_A11_y_ds3 = element.integral_values_l_half['int_A11_y_ds']
            int_A11_omega_ds3 = element.integral_values_l_half['int_A11_omega_ds']
            int_B16_x_ds3 = element.integral_values_l_half['int_B16_x_ds']
            int_B16_y_ds3 = element.integral_values_l_half['int_B16_y_ds']
            int_B16_omega_ds3 = element.integral_values_l_half['int_B16_omega_ds']

            f_r_1[0, 0] = B_element[0, 0] * K_bb_inv[0, 2] + B_element[0, 1] * K_bb_inv[1, 2] + B_element[0, 2] * \
                          K_bb_inv[2, 2] + B_element[0, 3] * K_bb_inv[3, 2] + B_element[0, 4] * K_bb_inv[4, 2] - \
                          K_bb_inv[0, 2] * int_A11_ds1 - K_bb_inv[1, 2] * int_A11_y_ds1 + K_bb_inv[
                              2, 2] * int_A11_x_ds1 - 2 * K_bb_inv[3, 2] * int_B16_ds1 + K_bb_inv[
                              4, 2] * int_A11_omega_ds1
            f_r_1[0, 1] = -B_element[0, 0] * K_bb_inv[0, 1] - B_element[0, 1] * K_bb_inv[1, 1] - B_element[0, 2] * \
                          K_bb_inv[2, 1] - B_element[0, 3] * K_bb_inv[3, 1] - B_element[0, 4] * K_bb_inv[4, 1] + \
                          K_bb_inv[0, 1] * int_A11_ds1 + K_bb_inv[1, 1] * int_A11_y_ds1 - K_bb_inv[
                              2, 1] * int_A11_x_ds1 + 2 * K_bb_inv[3, 1] * int_B16_ds1 - K_bb_inv[
                              4, 1] * int_A11_omega_ds1
            f_r_1[1, 0] = B_element[1, 0] * K_bb_inv[0, 2] + B_element[1, 1] * K_bb_inv[1, 2] + B_element[1, 2] * \
                          K_bb_inv[2, 2] + B_element[1, 3] * K_bb_inv[3, 2] + B_element[1, 4] * K_bb_inv[4, 2] + \
                          B_element[2, 0] * K_bb_inv[0, 2] * x1 + B_element[2, 1] * K_bb_inv[1, 2] * x1 + B_element[
                              2, 2] * K_bb_inv[2, 2] * x1 + B_element[2, 3] * K_bb_inv[3, 2] * x1 + B_element[2, 4] * \
                          K_bb_inv[4, 2] * x1 + B_element[3, 0] * K_bb_inv[0, 2] * y1 + B_element[3, 1] * K_bb_inv[
                              1, 2] * y1 + B_element[3, 2] * K_bb_inv[2, 2] * y1 + B_element[3, 3] * K_bb_inv[
                              3, 2] * y1 + B_element[3, 4] * K_bb_inv[4, 2] * y1 - K_bb_inv[0, 2] * int_B16_ds1 - \
                          K_bb_inv[1, 2] * int_B16_y_ds1 + K_bb_inv[2, 2] * int_B16_x_ds1 - 2 * K_bb_inv[
                              3, 2] * int_D16_ds1 + K_bb_inv[4, 2] * int_B16_omega_ds1
            f_r_1[1, 1] = -B_element[1, 0] * K_bb_inv[0, 1] - B_element[1, 1] * K_bb_inv[1, 1] - B_element[1, 2] * \
                          K_bb_inv[2, 1] - B_element[1, 3] * K_bb_inv[3, 1] - B_element[1, 4] * K_bb_inv[4, 1] - \
                          B_element[2, 0] * K_bb_inv[0, 1] * x1 - B_element[2, 1] * K_bb_inv[1, 1] * x1 - B_element[
                              2, 2] * K_bb_inv[2, 1] * x1 - B_element[2, 3] * K_bb_inv[3, 1] * x1 - B_element[2, 4] * \
                          K_bb_inv[4, 1] * x1 - B_element[3, 0] * K_bb_inv[0, 1] * y1 - B_element[3, 1] * K_bb_inv[
                              1, 1] * y1 - B_element[3, 2] * K_bb_inv[2, 1] * y1 - B_element[3, 3] * K_bb_inv[
                              3, 1] * y1 - B_element[3, 4] * K_bb_inv[4, 1] * y1 + K_bb_inv[0, 1] * int_B16_ds1 + \
                          K_bb_inv[1, 1] * int_B16_y_ds1 - K_bb_inv[2, 1] * int_B16_x_ds1 + 2 * K_bb_inv[
                              3, 1] * int_D16_ds1 - K_bb_inv[4, 1] * int_B16_omega_ds1

            f_r_2[0, 0] = B_element[0, 0] * K_bb_inv[0, 2] + B_element[0, 1] * K_bb_inv[1, 2] + B_element[0, 2] * \
                          K_bb_inv[2, 2] + B_element[0, 3] * K_bb_inv[3, 2] + B_element[0, 4] * K_bb_inv[4, 2] - \
                          K_bb_inv[0, 2] * int_A11_ds2 - K_bb_inv[1, 2] * int_A11_y_ds2 + K_bb_inv[
                              2, 2] * int_A11_x_ds2 - 2 * K_bb_inv[3, 2] * int_B16_ds2 + K_bb_inv[
                              4, 2] * int_A11_omega_ds2
            f_r_2[0, 1] = -B_element[0, 0] * K_bb_inv[0, 1] - B_element[0, 1] * K_bb_inv[1, 1] - B_element[0, 2] * \
                          K_bb_inv[2, 1] - B_element[0, 3] * K_bb_inv[3, 1] - B_element[0, 4] * K_bb_inv[4, 1] + \
                          K_bb_inv[0, 1] * int_A11_ds2 + K_bb_inv[1, 1] * int_A11_y_ds2 - K_bb_inv[
                              2, 1] * int_A11_x_ds2 + 2 * K_bb_inv[3, 1] * int_B16_ds2 - K_bb_inv[
                              4, 1] * int_A11_omega_ds2
            f_r_2[1, 0] = B_element[1, 0] * K_bb_inv[0, 2] + B_element[1, 1] * K_bb_inv[1, 2] + B_element[1, 2] * \
                          K_bb_inv[2, 2] + B_element[1, 3] * K_bb_inv[3, 2] + B_element[1, 4] * K_bb_inv[4, 2] + \
                          B_element[2, 0] * K_bb_inv[0, 2] * x2 + B_element[2, 1] * K_bb_inv[1, 2] * x2 + B_element[
                              2, 2] * K_bb_inv[2, 2] * x2 + B_element[2, 3] * K_bb_inv[3, 2] * x2 + B_element[2, 4] * \
                          K_bb_inv[4, 2] * x2 + B_element[3, 0] * K_bb_inv[0, 2] * y2 + B_element[3, 1] * K_bb_inv[
                              1, 2] * y2 + B_element[3, 2] * K_bb_inv[2, 2] * y2 + B_element[3, 3] * K_bb_inv[
                              3, 2] * y2 + B_element[3, 4] * K_bb_inv[4, 2] * y2 - K_bb_inv[0, 2] * int_B16_ds2 - \
                          K_bb_inv[1, 2] * int_B16_y_ds2 + K_bb_inv[2, 2] * int_B16_x_ds2 - 2 * K_bb_inv[
                              3, 2] * int_D16_ds2 + K_bb_inv[4, 2] * int_B16_omega_ds2
            f_r_2[1, 1] = -B_element[1, 0] * K_bb_inv[0, 1] - B_element[1, 1] * K_bb_inv[1, 1] - B_element[1, 2] * \
                          K_bb_inv[2, 1] - B_element[1, 3] * K_bb_inv[3, 1] - B_element[1, 4] * K_bb_inv[4, 1] - \
                          B_element[2, 0] * K_bb_inv[0, 1] * x2 - B_element[2, 1] * K_bb_inv[1, 1] * x2 - B_element[
                              2, 2] * K_bb_inv[2, 1] * x2 - B_element[2, 3] * K_bb_inv[3, 1] * x2 - B_element[2, 4] * \
                          K_bb_inv[4, 1] * x2 - B_element[3, 0] * K_bb_inv[0, 1] * y2 - B_element[3, 1] * K_bb_inv[
                              1, 1] * y2 - B_element[3, 2] * K_bb_inv[2, 1] * y2 - B_element[3, 3] * K_bb_inv[
                              3, 1] * y2 - B_element[3, 4] * K_bb_inv[4, 1] * y2 + K_bb_inv[0, 1] * int_B16_ds2 + \
                          K_bb_inv[1, 1] * int_B16_y_ds2 - K_bb_inv[2, 1] * int_B16_x_ds2 + 2 * K_bb_inv[
                              3, 1] * int_D16_ds2 - K_bb_inv[4, 1] * int_B16_omega_ds2

            f_r_3[0, 0] = B_element[0, 0] * K_bb_inv[0, 2] + B_element[0, 1] * K_bb_inv[1, 2] + B_element[0, 2] * \
                          K_bb_inv[2, 2] + B_element[0, 3] * K_bb_inv[3, 2] + B_element[0, 4] * K_bb_inv[4, 2] - 1 / 2 * \
                          K_bb_inv[0, 2] * int_A11_ds1 - 1 / 2 * K_bb_inv[0, 2] * int_A11_ds2 - K_bb_inv[
                              1, 2] * int_A11_y_ds3 + K_bb_inv[2, 2] * int_A11_x_ds3 - K_bb_inv[3, 2] * int_B16_ds1 - \
                          K_bb_inv[3, 2] * int_B16_ds2 + K_bb_inv[4, 2] * int_A11_omega_ds3
            f_r_3[0, 1] = -B_element[0, 0] * K_bb_inv[0, 1] - B_element[0, 1] * K_bb_inv[1, 1] - B_element[0, 2] * \
                          K_bb_inv[2, 1] - B_element[0, 3] * K_bb_inv[3, 1] - B_element[0, 4] * K_bb_inv[4, 1] + (
                                      1 / 2) * K_bb_inv[0, 1] * int_A11_ds1 + (1 / 2) * K_bb_inv[0, 1] * int_A11_ds2 + \
                          K_bb_inv[1, 1] * int_A11_y_ds3 - K_bb_inv[2, 1] * int_A11_x_ds3 + K_bb_inv[
                              3, 1] * int_B16_ds1 + K_bb_inv[3, 1] * int_B16_ds2 - K_bb_inv[4, 1] * int_A11_omega_ds3
            f_r_3[1, 0] = B_element[1, 0] * K_bb_inv[0, 2] + B_element[1, 1] * K_bb_inv[1, 2] + B_element[1, 2] * \
                          K_bb_inv[2, 2] + B_element[1, 3] * K_bb_inv[3, 2] + B_element[1, 4] * K_bb_inv[4, 2] + (
                                      1 / 2) * B_element[2, 0] * K_bb_inv[0, 2] * x1 + (1 / 2) * B_element[2, 0] * \
                          K_bb_inv[0, 2] * x2 + (1 / 2) * B_element[2, 1] * K_bb_inv[1, 2] * x1 + (1 / 2) * B_element[
                              2, 1] * K_bb_inv[1, 2] * x2 + (1 / 2) * B_element[2, 2] * K_bb_inv[2, 2] * x1 + (1 / 2) * \
                          B_element[2, 2] * K_bb_inv[2, 2] * x2 + (1 / 2) * B_element[2, 3] * K_bb_inv[3, 2] * x1 + (
                                      1 / 2) * B_element[2, 3] * K_bb_inv[3, 2] * x2 + (1 / 2) * B_element[2, 4] * \
                          K_bb_inv[4, 2] * x1 + (1 / 2) * B_element[2, 4] * K_bb_inv[4, 2] * x2 + (1 / 2) * B_element[
                              3, 0] * K_bb_inv[0, 2] * y1 + (1 / 2) * B_element[3, 0] * K_bb_inv[0, 2] * y2 + (1 / 2) * \
                          B_element[3, 1] * K_bb_inv[1, 2] * y1 + (1 / 2) * B_element[3, 1] * K_bb_inv[1, 2] * y2 + (
                                      1 / 2) * B_element[3, 2] * K_bb_inv[2, 2] * y1 + (1 / 2) * B_element[3, 2] * \
                          K_bb_inv[2, 2] * y2 + (1 / 2) * B_element[3, 3] * K_bb_inv[3, 2] * y1 + (1 / 2) * B_element[
                              3, 3] * K_bb_inv[3, 2] * y2 + (1 / 2) * B_element[3, 4] * K_bb_inv[4, 2] * y1 + (1 / 2) * \
                          B_element[3, 4] * K_bb_inv[4, 2] * y2 - 1 / 2 * K_bb_inv[0, 2] * int_B16_ds1 - 1 / 2 * \
                          K_bb_inv[0, 2] * int_B16_ds2 - K_bb_inv[1, 2] * int_B16_y_ds3 + K_bb_inv[
                              2, 2] * int_B16_x_ds3 - K_bb_inv[3, 2] * int_D16_ds1 - K_bb_inv[3, 2] * int_D16_ds2 + \
                          K_bb_inv[4, 2] * int_B16_omega_ds3
            f_r_3[1, 1] = -B_element[1, 0] * K_bb_inv[0, 1] - B_element[1, 1] * K_bb_inv[1, 1] - B_element[1, 2] * \
                          K_bb_inv[2, 1] - B_element[1, 3] * K_bb_inv[3, 1] - B_element[1, 4] * K_bb_inv[4, 1] - 1 / 2 * \
                          B_element[2, 0] * K_bb_inv[0, 1] * x1 - 1 / 2 * B_element[2, 0] * K_bb_inv[
                              0, 1] * x2 - 1 / 2 * B_element[2, 1] * K_bb_inv[1, 1] * x1 - 1 / 2 * B_element[2, 1] * \
                          K_bb_inv[1, 1] * x2 - 1 / 2 * B_element[2, 2] * K_bb_inv[2, 1] * x1 - 1 / 2 * B_element[
                              2, 2] * K_bb_inv[2, 1] * x2 - 1 / 2 * B_element[2, 3] * K_bb_inv[3, 1] * x1 - 1 / 2 * \
                          B_element[2, 3] * K_bb_inv[3, 1] * x2 - 1 / 2 * B_element[2, 4] * K_bb_inv[
                              4, 1] * x1 - 1 / 2 * B_element[2, 4] * K_bb_inv[4, 1] * x2 - 1 / 2 * B_element[3, 0] * \
                          K_bb_inv[0, 1] * y1 - 1 / 2 * B_element[3, 0] * K_bb_inv[0, 1] * y2 - 1 / 2 * B_element[
                              3, 1] * K_bb_inv[1, 1] * y1 - 1 / 2 * B_element[3, 1] * K_bb_inv[1, 1] * y2 - 1 / 2 * \
                          B_element[3, 2] * K_bb_inv[2, 1] * y1 - 1 / 2 * B_element[3, 2] * K_bb_inv[
                              2, 1] * y2 - 1 / 2 * B_element[3, 3] * K_bb_inv[3, 1] * y1 - 1 / 2 * B_element[3, 3] * \
                          K_bb_inv[3, 1] * y2 - 1 / 2 * B_element[3, 4] * K_bb_inv[4, 1] * y1 - 1 / 2 * B_element[
                              3, 4] * K_bb_inv[4, 1] * y2 + (1 / 2) * K_bb_inv[0, 1] * int_B16_ds1 + (1 / 2) * K_bb_inv[
                              0, 1] * int_B16_ds2 + K_bb_inv[1, 1] * int_B16_y_ds3 - K_bb_inv[2, 1] * int_B16_x_ds3 + \
                          K_bb_inv[3, 1] * int_D16_ds1 + K_bb_inv[3, 1] * int_D16_ds2 - K_bb_inv[
                              4, 1] * int_B16_omega_ds3

            element.f_r_1 = f_r_1
            element.f_r_2 = f_r_2
            element.f_r_3 = f_r_3

    def calc_displacements(self, internal_loads):
        """
        Calculate the cross section displacements.

        Parameters
        ----------
        internal_loads: ClassicCrossSectionLoadsWithBimoment
            Cross section internal loads.

        Returns
        -------
        TimoschenkoWithRestrainedWarpingDisplacements
            Displacements of the cross section.
        """
        self._update_if_required()
        load_vector = np.array(internal_loads.forces.tolist() + internal_loads.moments.tolist() + [internal_loads.bimoment])
        displacements = np.dot(self._compliance_matrix, load_vector).flatten()
        return TimoschenkoWithRestrainedWarpingDisplacements(Vector(displacements[0:3]), Vector(displacements[3:6]), displacements[6])

    def calc_element_load_state(self, element, displacements):
        """
        Calculate the element load state (strain and stress) as function of the element contour coordinate.

        Parameters
        ----------
        element: IElement
            The element.
        displacements: TimoschenkoWithRestrainedWarpingDisplacements
            Displacements of the cross section.

        Returns
        -------
        CompositeLoadState
            The load states of the discreet elements of the cross section as function of the element contour coordinate.
        """
        self._update_if_required()

        l = element.length
        C = element.material.stiffness.K_Jung
        b_element = element.b

        pos1 = element.node1_midsurface_position
        pos2 = element.node2_midsurface_position

        omega1 = element.node1.integral_values['int_rtorsional_ds']
        omega2 = element.node2.integral_values['int_rtorsional_ds']

        x1 = pos1.x
        x2 = pos2.x
        y1 = pos1.y
        y2 = pos2.y

        f_r_1 = element.f_r_1
        f_r_2 = element.f_r_2
        f_r_3 = element.f_r_3

        f_r_const_111 = f_r_1[0, 0]
        f_r_const_112 = f_r_2[0, 0]
        f_r_const_113 = f_r_3[0, 0]

        f_r_const_121 = f_r_1[0, 1]
        f_r_const_122 = f_r_2[0, 1]
        f_r_const_123 = f_r_3[0, 1]

        f_r_const_211 = f_r_1[1, 0]
        f_r_const_212 = f_r_2[1, 0]
        f_r_const_213 = f_r_3[1, 0]

        f_r_const_221 = f_r_1[1, 1]
        f_r_const_222 = f_r_2[1, 1]
        f_r_const_223 = f_r_3[1, 1]

        # Cross section displacements
        gamma_xz = displacements.strain[0]
        gamma_yz = displacements.strain[1]
        w_p_d = displacements.strain[2]
        Theta_x_d = displacements.curvature[0]
        Theta_y_d = displacements.curvature[1]
        phi_d = displacements.curvature[2]
        phi_dd = displacements.twisting_derivation

        # TODO: Berechnung von v_s nur einmal pro Lastfall ausführen
        q_cs = np.array([w_p_d, Theta_x_d, Theta_y_d, phi_d, phi_dd, gamma_xz, gamma_yz])
        v_s = self._p @ q_cs

        V_x_additional = v_s[0]
        V_y_additional = v_s[1]

        # Element displacements
        def epsilon_zz(s):
            return (Theta_x_d*(l*y1 - s*(y1 - y2)) - Theta_y_d*(l*x1 - s*(x1 - x2)) + l*w_p_d - phi_dd*(l*omega1 - s*(omega1 - omega2)))/l

        def kappa_zz(s):
            return (l*(Theta_x_d*(x1 - x2) + Theta_y_d*(y1 - y2)) + phi_dd*((x1 - x2)*(l*x1 - s*(x1 - x2)) + (y1 - y2)*(l*y1 + s*(-y1 + y2))))/l**2

        def kappa_zs(s):
            return 2*phi_d

        def N_zs(s):
            return (V_x_additional*(f_r_const_111*l**2 - l*s*(3*f_r_const_111 + f_r_const_112 - 4*f_r_const_113) + 2*s**2*(f_r_const_111 + f_r_const_112 - 2*f_r_const_113)) + V_y_additional*(f_r_const_121*l**2 - l*s*(3*f_r_const_121 + f_r_const_122 - 4*f_r_const_123) + 2*s**2*(f_r_const_121 + f_r_const_122 - 2*f_r_const_123)) + l**2*(Theta_x_d*b_element[0,1] + Theta_y_d*b_element[0,2] + b_element[0,0]*w_p_d + b_element[0,3]*phi_d + b_element[0,4]*phi_dd))/l**2

        def M_ss(s):
            return (V_x_additional*(f_r_const_211*l**2 - l*s*(3*f_r_const_211 + f_r_const_212 - 4*f_r_const_213) + 2*s**2*(f_r_const_211 + f_r_const_212 - 2*f_r_const_213)) + V_y_additional*(f_r_const_221*l**2 - l*s*(3*f_r_const_221 + f_r_const_222 - 4*f_r_const_223) + 2*s**2*(f_r_const_221 + f_r_const_222 - 2*f_r_const_223)) + l*(Theta_x_d*(b_element[1,1]*l + b_element[2,1]*(l*x1 - s*(x1 - x2)) + b_element[3,1]*(l*y1 - s*(y1 - y2))) + Theta_y_d*(b_element[1,2]*l + b_element[2,2]*(l*x1 - s*(x1 - x2)) + b_element[3,2]*(l*y1 - s*(y1 - y2))) + phi_d*(b_element[1,3]*l + b_element[2,3]*(l*x1 - s*(x1 - x2)) + b_element[3,3]*(l*y1 - s*(y1 - y2))) + phi_dd*(b_element[1,4]*l + b_element[2,4]*(l*x1 - s*(x1 - x2)) + b_element[3,4]*(l*y1 - s*(y1 - y2))) + w_p_d*(b_element[1,0]*l + b_element[2,0]*(l*x1 - s*(x1 - x2)) + b_element[3,0]*(l*y1 - s*(y1 - y2)))))/l**2

        #def gamma_zn(s): # Only reactive displacement with first order shear deformation theory
        #    return (-gamma_xz*(y1 - y2) + gamma_yz*(x1 - x2))/l

        # Stress state: material laws
        def N_zz(s): return C[0,0]*epsilon_zz(s) + C[0,3]*N_zs(s) + C[0,4]*M_ss(s) + C[1,0]*kappa_zz(s) + C[2,0]*kappa_zs(s)

        def M_zz(s): return C[1,0]*epsilon_zz(s) + C[1,1]*kappa_zz(s) + C[1,3]*N_zs(s) + C[1,4]*M_ss(s) + C[2,1]*kappa_zs(s)

        def M_zs(s): return C[2,0]*epsilon_zz(s) + C[2,1]*kappa_zz(s) + C[2,2]*kappa_zs(s) + C[2,3]*N_zs(s) + C[2,4]*M_ss(s)

        def gamma_zs(s): return C[3,0]*epsilon_zz(s) + C[3,1]*kappa_zz(s) + C[3,2]*kappa_zs(s) + C[3,3]*N_zs(s) + C[4,3]*M_ss(s)

        def kappa_ss(s): return C[4,0]*epsilon_zz(s) + C[4,1]*kappa_zz(s) + C[4,2]*kappa_zs(s) + C[4,3]*N_zs(s) + C[4,4]*M_ss(s)

        #def N_zn(s): return C[5,5]*gamma_zn(s)

        #def epsilon_ss(s): return C[6,0]*epsilon_zz(s) + C[6,1]*kappa_zz(s) + C[6,2]*kappa_zs(s) + C[6,3]*N_zs(s) + C[6,4]*M_ss(s)

        #def gamma_sn(s): return C[7,5]*gamma_zn(s)

        # Load state
        strain_state = {'epsilon_zz': lambda s: element.get_function_with_bounds(epsilon_zz, s),
                        'kappa_zz': lambda s: element.get_function_with_bounds(kappa_zz, s),
                        'kappa_zs': lambda s: element.get_function_with_bounds(kappa_zs, s),
                        'gamma_zs': lambda s: element.get_function_with_bounds(gamma_zs, s),
                        'kappa_ss': lambda s: element.get_function_with_bounds(kappa_ss, s)}#,
                        #'gamma_zn': lambda s: element.get_function_with_bounds(gamma_zn, s),
                        #'epsilon_ss': lambda s: element.get_function_with_bounds(epsilon_ss, s),
                        #'gamma_sn': lambda s: element.get_function_with_bounds(gamma_sn, s)}

        stress_state = {'N_zz': lambda s: element.get_function_with_bounds(N_zz, s),
                        'M_zz': lambda s: element.get_function_with_bounds(M_zz, s),
                        'M_zs': lambda s: element.get_function_with_bounds(M_zs, s),
                        'N_zs': lambda s: element.get_function_with_bounds(N_zs, s),
                        'M_ss': lambda s: element.get_function_with_bounds(M_ss, s)}#,
                        #'N_zn': lambda s: element.get_function_with_bounds(N_zn, s)}

        return ElementLoadState(strain_state, stress_state)

    @staticmethod
    def _d(element, displacements, v_s, s):
        l = element.length
        #C = element.material.stiffness.K_Jung
        b_element = element.b

        pos1 = element.node1_midsurface_position
        pos2 = element.node2_midsurface_position

        omega1 = element.node1.integral_values['int_rtorsional_ds']
        omega2 = element.node2.integral_values['int_rtorsional_ds']

        x1 = pos1.x
        x2 = pos2.x
        y1 = pos1.y
        y2 = pos2.y

        f_r_1 = element.f_r_1
        f_r_2 = element.f_r_2
        f_r_3 = element.f_r_3

        f_r_const_111 = f_r_1[0, 0]
        f_r_const_112 = f_r_2[0, 0]
        f_r_const_113 = f_r_3[0, 0]

        f_r_const_121 = f_r_1[0, 1]
        f_r_const_122 = f_r_2[0, 1]
        f_r_const_123 = f_r_3[0, 1]

        f_r_const_211 = f_r_1[1, 0]
        f_r_const_212 = f_r_2[1, 0]
        f_r_const_213 = f_r_3[1, 0]

        f_r_const_221 = f_r_1[1, 1]
        f_r_const_222 = f_r_2[1, 1]
        f_r_const_223 = f_r_3[1, 1]

        # Cross section displacements
        #gamma_xz = displacements.strain[0]
        #gamma_yz = displacements.strain[1]
        w_p_d = displacements.strain[2]
        Theta_x_d = displacements.curvature[0]
        Theta_y_d = displacements.curvature[1]
        phi_d = displacements.curvature[2]
        phi_dd = displacements.twisting_derivation

        V_x_additional = v_s[0]
        V_y_additional = v_s[1]

        d = np.zeros((5, 1))


        d[0, 0] = (Theta_x_d * (l * y1 - s * (y1 - y2)) - Theta_y_d * (l * x1 - s * (x1 - x2)) + l * w_p_d - phi_dd * (
                    l * omega1 - s * (omega1 - omega2))) / l
        d[1, 0] = (l * (Theta_x_d * (x1 - x2) + Theta_y_d * (y1 - y2)) + phi_dd * (
                    (x1 - x2) * (l * x1 - s * (x1 - x2)) + (y1 - y2) * (l * y1 + s * (-y1 + y2)))) / l ** 2
        d[2, 0] = 2 * phi_d
        d[3, 0] = (V_x_additional * (f_r_const_111 * l ** 2 - l * s * (
                    3 * f_r_const_111 + f_r_const_112 - 4 * f_r_const_113) + 2 * s ** 2 * (
                                                 f_r_const_111 + f_r_const_112 - 2 * f_r_const_113)) + V_y_additional * (
                               f_r_const_121 * l ** 2 - l * s * (
                                   3 * f_r_const_121 + f_r_const_122 - 4 * f_r_const_123) + 2 * s ** 2 * (
                                           f_r_const_121 + f_r_const_122 - 2 * f_r_const_123)) + l ** 2 * (
                               Theta_x_d * b_element[0, 1] + Theta_y_d * b_element[0, 2] + b_element[0, 0] * w_p_d +
                               b_element[0, 3] * phi_d + b_element[0, 4] * phi_dd)) / l ** 2
        d[4, 0] = (V_x_additional * (f_r_const_211 * l ** 2 - l * s * (
                    3 * f_r_const_211 + f_r_const_212 - 4 * f_r_const_213) + 2 * s ** 2 * (
                                                 f_r_const_211 + f_r_const_212 - 2 * f_r_const_213)) + V_y_additional * (
                               f_r_const_221 * l ** 2 - l * s * (
                                   3 * f_r_const_221 + f_r_const_222 - 4 * f_r_const_223) + 2 * s ** 2 * (
                                           f_r_const_221 + f_r_const_222 - 2 * f_r_const_223)) + l * (Theta_x_d * (
                    b_element[1, 1] * l + b_element[2, 1] * (l * x1 - s * (x1 - x2)) + b_element[3, 1] * (
                        l * y1 - s * (y1 - y2))) + Theta_y_d * (b_element[1, 2] * l + b_element[2, 2] * (
                    l * x1 - s * (x1 - x2)) + b_element[3, 2] * (l * y1 - s * (y1 - y2))) + phi_d * (b_element[
                                                                                                         1, 3] * l +
                                                                                                     b_element[2, 3] * (
                                                                                                                 l * x1 - s * (
                                                                                                                     x1 - x2)) +
                                                                                                     b_element[3, 3] * (
                                                                                                                 l * y1 - s * (
                                                                                                                     y1 - y2))) + phi_dd * (
                                                                                                                  b_element[
                                                                                                                      1, 4] * l +
                                                                                                                  b_element[
                                                                                                                      2, 4] * (
                                                                                                                              l * x1 - s * (
                                                                                                                                  x1 - x2)) +
                                                                                                                  b_element[
                                                                                                                      3, 4] * (
                                                                                                                              l * y1 - s * (
                                                                                                                                  y1 - y2))) + w_p_d * (
                                                                                                                  b_element[
                                                                                                                      1, 0] * l +
                                                                                                                  b_element[
                                                                                                                      2, 0] * (
                                                                                                                              l * x1 - s * (
                                                                                                                                  x1 - x2)) +
                                                                                                                  b_element[
                                                                                                                      3, 0] * (
                                                                                                                              l * y1 - s * (
                                                                                                                                  y1 - y2))))) / l ** 2



        return d

    @staticmethod
    def _t_from_d(C, d_const):
        return C[0:5, 0:5] @ d_const

    @staticmethod
    def strain_stress_vectors_to_load_state(strain, stress):
        strain_state = {'epsilon_zz': strain[0],
                        'kappa_zz': strain[1],
                        'kappa_zs': strain[2],
                        'gamma_zs': stress[3],
                        'kappa_ss': stress[4]}

        stress_state = {'N_zz': stress[0],
                        'M_zz': stress[1],
                        'M_zs': stress[2],
                        'N_zs': strain[3],
                        'M_ss': strain[4]}

        return ElementLoadState(strain_state, stress_state)

    def calc_element_min_max_load_state(self, element, displacements, **kwargs):
        """
        Calculate the minimum and maximum element load states (strain and stress).

        Parameters
        ----------
        element: IElement
            The element.
        displacements: ICrossSectionDisplacements
            Displacements of the cross section.

        Returns
        -------
        (IElementLoadState, IElementLoadState)
            The minimum and maximum load states of the discreet elements of the cross section.
        """
        self._update_if_required()

        # simple method: evaluate load states at s=0, s=l/, s=l
        # extended method: evaluate load states at s=0, s=l and the analytical extrema between [0, l]
        simple_method = True # TODO: performance?

        if simple_method:
            l = element.length
            C = element.material.stiffness.K_Jung
            b_element = element.b

            pos1 = element.node1_midsurface_position
            pos2 = element.node2_midsurface_position

            omega1 = element.node1.integral_values['int_rtorsional_ds']
            omega2 = element.node2.integral_values['int_rtorsional_ds']

            x1 = pos1.x
            x2 = pos2.x
            y1 = pos1.y
            y2 = pos2.y

            f_r_1 = element.f_r_1
            f_r_2 = element.f_r_2
            f_r_3 = element.f_r_3

            f_r_const_111 = f_r_1[0, 0]
            f_r_const_112 = f_r_2[0, 0]
            f_r_const_113 = f_r_3[0, 0]

            f_r_const_121 = f_r_1[0, 1]
            f_r_const_122 = f_r_2[0, 1]
            f_r_const_123 = f_r_3[0, 1]

            f_r_const_211 = f_r_1[1, 0]
            f_r_const_212 = f_r_2[1, 0]
            f_r_const_213 = f_r_3[1, 0]

            f_r_const_221 = f_r_1[1, 1]
            f_r_const_222 = f_r_2[1, 1]
            f_r_const_223 = f_r_3[1, 1]

            # Cross section displacements
            gamma_xz = displacements.strain[0]
            gamma_yz = displacements.strain[1]
            w_p_d = displacements.strain[2]
            Theta_x_d = displacements.curvature[0]
            Theta_y_d = displacements.curvature[1]
            phi_d = displacements.curvature[2]
            phi_dd = displacements.twisting_derivation

            # TODO: Berechnung von v_s nur einmal pro Lastfall ausführen
            q_cs = np.array([w_p_d, Theta_x_d, Theta_y_d, phi_d, phi_dd, gamma_xz, gamma_yz])
            v_s = self._p @ q_cs

            V_x_additional = v_s[0]
            V_y_additional = v_s[1]

            # Element strains
            d_ex_0 = JungCrossSectionProcessor._d(element, displacements, v_s, 0)
            d_ex_l = JungCrossSectionProcessor._d(element, displacements, v_s, l)
            d_ex_l2 = JungCrossSectionProcessor._d(element, displacements, v_s, l/2)

            # Element stresses
            t_ex_0 = JungCrossSectionProcessor._t_from_d(C, d_ex_0)
            t_ex_l = JungCrossSectionProcessor._t_from_d(C, d_ex_l)
            t_ex_l2 = JungCrossSectionProcessor._t_from_d(C, d_ex_l2)

            min_strain = np.nanmin(np.hstack([d_ex_0, d_ex_l, d_ex_l2]), axis=1)
            max_strain = np.nanmax(np.hstack([d_ex_0, d_ex_l, d_ex_l2]), axis=1)

            min_stress = np.nanmin(np.hstack([t_ex_0, t_ex_l, t_ex_l2]), axis=1)
            max_stress = np.nanmax(np.hstack([t_ex_0, t_ex_l, t_ex_l2]), axis=1)


        else:
            # TODO: auf Rand-Extrema checken (an den Element Grenzen)
            l = element.length
            C = element.material.stiffness.K_Jung
            b_element = element.b

            pos1 = element.node1_midsurface_position
            pos2 = element.node2_midsurface_position

            omega1 = element.node1.integral_values['int_rtorsional_ds']
            omega2 = element.node2.integral_values['int_rtorsional_ds']

            x1 = pos1.x
            x2 = pos2.x
            y1 = pos1.y
            y2 = pos2.y

            f_r_1 = element.f_r_1
            f_r_2 = element.f_r_2
            f_r_3 = element.f_r_3

            f_r_const_111 = f_r_1[0, 0]
            f_r_const_112 = f_r_2[0, 0]
            f_r_const_113 = f_r_3[0, 0]

            f_r_const_121 = f_r_1[0, 1]
            f_r_const_122 = f_r_2[0, 1]
            f_r_const_123 = f_r_3[0, 1]

            f_r_const_211 = f_r_1[1, 0]
            f_r_const_212 = f_r_2[1, 0]
            f_r_const_213 = f_r_3[1, 0]

            f_r_const_221 = f_r_1[1, 1]
            f_r_const_222 = f_r_2[1, 1]
            f_r_const_223 = f_r_3[1, 1]

            # Cross section displacements
            gamma_xz = displacements.strain[0]
            gamma_yz = displacements.strain[1]
            w_p_d = displacements.strain[2]
            Theta_x_d = displacements.curvature[0]
            Theta_y_d = displacements.curvature[1]
            phi_d = displacements.curvature[2]
            phi_dd = displacements.twisting_derivation

            # TODO: Berechnung von v_s nur einmal pro Lastfall ausführen
            q_cs = np.array([w_p_d, Theta_x_d, Theta_y_d, phi_d, phi_dd, gamma_xz, gamma_yz])
            v_s = self._p @ q_cs

            V_x_additional = v_s[0]
            V_y_additional = v_s[1]

            # Element strains
            d_ex_0 = JungCrossSectionProcessor._d(element, displacements, v_s, 0)
            d_ex_l = JungCrossSectionProcessor._d(element, displacements, v_s, l)
            s_d = np.zeros((5, 1))
            # s_d_A = np.zeros((2, 2))
            # s_d_b = np.zeros((2, 1))
            d_ex_d = np.zeros((5, 1))

            s_d[0, 0] = float('nan')
            s_d[1, 0] = float('nan')
            s_d[2, 0] = float('nan')
            s_d[3, 0] = (1 / 4) * l * (
                        3 * V_x_additional * f_r_const_111 + V_x_additional * f_r_const_112 - 4 * V_x_additional * f_r_const_113 + 3 * V_y_additional * f_r_const_121 + V_y_additional * f_r_const_122 - 4 * V_y_additional * f_r_const_123) / (
                                    V_x_additional * f_r_const_111 + V_x_additional * f_r_const_112 - 2 * V_x_additional * f_r_const_113 + V_y_additional * f_r_const_121 + V_y_additional * f_r_const_122 - 2 * V_y_additional * f_r_const_123)
            s_d[4, 0] = (1 / 4) * l * (
                        Theta_x_d * b_element[2, 1] * x1 - Theta_x_d * b_element[2, 1] * x2 + Theta_x_d * b_element[
                    3, 1] * y1 - Theta_x_d * b_element[3, 1] * y2 + Theta_y_d * b_element[2, 2] * x1 - Theta_y_d *
                        b_element[2, 2] * x2 + Theta_y_d * b_element[3, 2] * y1 - Theta_y_d * b_element[
                            3, 2] * y2 + 3 * V_x_additional * f_r_const_211 + V_x_additional * f_r_const_212 - 4 * V_x_additional * f_r_const_213 + 3 * V_y_additional * f_r_const_221 + V_y_additional * f_r_const_222 - 4 * V_y_additional * f_r_const_223 +
                        b_element[2, 0] * w_p_d * x1 - b_element[2, 0] * w_p_d * x2 + b_element[2, 3] * phi_d * x1 -
                        b_element[2, 3] * phi_d * x2 + b_element[2, 4] * phi_dd * x1 - b_element[2, 4] * phi_dd * x2 +
                        b_element[3, 0] * w_p_d * y1 - b_element[3, 0] * w_p_d * y2 + b_element[3, 3] * phi_d * y1 -
                        b_element[3, 3] * phi_d * y2 + b_element[3, 4] * phi_dd * y1 - b_element[3, 4] * phi_dd * y2) / (
                                    V_x_additional * f_r_const_211 + V_x_additional * f_r_const_212 - 2 * V_x_additional * f_r_const_213 + V_y_additional * f_r_const_221 + V_y_additional * f_r_const_222 - 2 * V_y_additional * f_r_const_223)


            # s_d in element bounds
            s_d[np.bitwise_and(~np.isnan(s_d), s_d < 0)] = 0
            s_d[np.bitwise_and(~np.isnan(s_d), s_d > l)] = l


            d_ex_d[0, 0] = float('nan')
            d_ex_d[1, 0] = float('nan')
            d_ex_d[2, 0] = float('nan')
            d_ex_d[3, 0] = (V_x_additional * (
                        f_r_const_111 * l ** 2 - l * s_d[3, 0] * (3 * f_r_const_111 + f_r_const_112 - 4 * f_r_const_113) + 2 * s_d[
                    3, 0] ** 2 * (f_r_const_111 + f_r_const_112 - 2 * f_r_const_113)) + V_y_additional * (
                                        f_r_const_121 * l ** 2 - l * s_d[3, 0] * (
                                            3 * f_r_const_121 + f_r_const_122 - 4 * f_r_const_123) + 2 * s_d[3, 0] ** 2 * (
                                                    f_r_const_121 + f_r_const_122 - 2 * f_r_const_123)) + l ** 2 * (
                                        Theta_x_d * b_element[0, 1] + Theta_y_d * b_element[0, 2] + b_element[0, 0] * w_p_d +
                                        b_element[0, 3] * phi_d + b_element[0, 4] * phi_dd)) / l ** 2
            d_ex_d[4, 0] = (V_x_additional * (
                        f_r_const_211 * l ** 2 - l * s_d[4, 0] * (3 * f_r_const_211 + f_r_const_212 - 4 * f_r_const_213) + 2 * s_d[
                    4, 0] ** 2 * (f_r_const_211 + f_r_const_212 - 2 * f_r_const_213)) + V_y_additional * (
                                        f_r_const_221 * l ** 2 - l * s_d[4, 0] * (
                                            3 * f_r_const_221 + f_r_const_222 - 4 * f_r_const_223) + 2 * s_d[4, 0] ** 2 * (
                                                    f_r_const_221 + f_r_const_222 - 2 * f_r_const_223)) + l * (Theta_x_d * (
                        b_element[1, 1] * l + b_element[2, 1] * (l * x1 - s_d[4, 0] * (x1 - x2)) + b_element[3, 1] * (
                            l * y1 - s_d[4, 0] * (y1 - y2))) + Theta_y_d * (b_element[1, 2] * l + b_element[2, 2] * (
                        l * x1 - s_d[4, 0] * (x1 - x2)) + b_element[3, 2] * (l * y1 - s_d[4, 0] * (y1 - y2))) + phi_d * (b_element[
                                                                                                                             1, 3] * l +
                                                                                                                         b_element[
                                                                                                                             2, 3] * (
                                                                                                                                     l * x1 -
                                                                                                                                     s_d[
                                                                                                                                         4, 0] * (
                                                                                                                                                 x1 - x2)) +
                                                                                                                         b_element[
                                                                                                                             3, 3] * (
                                                                                                                                     l * y1 -
                                                                                                                                     s_d[
                                                                                                                                         4, 0] * (
                                                                                                                                                 y1 - y2))) + phi_dd * (
                                                                                                                           b_element[
                                                                                                                               1, 4] * l +
                                                                                                                           b_element[
                                                                                                                               2, 4] * (
                                                                                                                                       l * x1 -
                                                                                                                                       s_d[
                                                                                                                                           4, 0] * (
                                                                                                                                                   x1 - x2)) +
                                                                                                                           b_element[
                                                                                                                               3, 4] * (
                                                                                                                                       l * y1 -
                                                                                                                                       s_d[
                                                                                                                                           4, 0] * (
                                                                                                                                                   y1 - y2))) + w_p_d * (
                                                                                                                           b_element[
                                                                                                                               1, 0] * l +
                                                                                                                           b_element[
                                                                                                                               2, 0] * (
                                                                                                                                       l * x1 -
                                                                                                                                       s_d[
                                                                                                                                           4, 0] * (
                                                                                                                                                   x1 - x2)) +
                                                                                                                           b_element[
                                                                                                                               3, 0] * (
                                                                                                                                       l * y1 -
                                                                                                                                       s_d[
                                                                                                                                           4, 0] * (
                                                                                                                                                   y1 - y2))))) / l ** 2


            # Element stresses
            t_ex_0 = JungCrossSectionProcessor._t_from_d(C, d_ex_0)
            t_ex_l = JungCrossSectionProcessor._t_from_d(C, d_ex_l)
            # s_t_A = np.zeros((5, 5))
            s_t = np.zeros((5, 1))


            s_t[0, 0] = (1 / 4) * (
                        C[0, 0] * Theta_x_d * l * y1 - C[0, 0] * Theta_x_d * l * y2 - C[0, 0] * Theta_y_d * l * x1 + C[
                    0, 0] * Theta_y_d * l * x2 - C[0, 0] * l * omega1 * phi_dd + C[0, 0] * l * omega2 * phi_dd + 3 * C[
                            0, 3] * V_x_additional * f_r_const_111 * l + C[
                            0, 3] * V_x_additional * f_r_const_112 * l - 4 * C[
                            0, 3] * V_x_additional * f_r_const_113 * l + 3 * C[
                            0, 3] * V_y_additional * f_r_const_121 * l + C[
                            0, 3] * V_y_additional * f_r_const_122 * l - 4 * C[
                            0, 3] * V_y_additional * f_r_const_123 * l + C[0, 4] * Theta_x_d * b_element[
                            2, 1] * l * x1 - C[0, 4] * Theta_x_d * b_element[2, 1] * l * x2 + C[0, 4] * Theta_x_d *
                        b_element[3, 1] * l * y1 - C[0, 4] * Theta_x_d * b_element[3, 1] * l * y2 + C[
                            0, 4] * Theta_y_d * b_element[2, 2] * l * x1 - C[0, 4] * Theta_y_d * b_element[
                            2, 2] * l * x2 + C[0, 4] * Theta_y_d * b_element[3, 2] * l * y1 - C[0, 4] * Theta_y_d *
                        b_element[3, 2] * l * y2 + 3 * C[0, 4] * V_x_additional * f_r_const_211 * l + C[
                            0, 4] * V_x_additional * f_r_const_212 * l - 4 * C[
                            0, 4] * V_x_additional * f_r_const_213 * l + 3 * C[
                            0, 4] * V_y_additional * f_r_const_221 * l + C[
                            0, 4] * V_y_additional * f_r_const_222 * l - 4 * C[
                            0, 4] * V_y_additional * f_r_const_223 * l + C[0, 4] * b_element[2, 0] * l * w_p_d * x1 - C[
                            0, 4] * b_element[2, 0] * l * w_p_d * x2 + C[0, 4] * b_element[2, 3] * l * phi_d * x1 - C[
                            0, 4] * b_element[2, 3] * l * phi_d * x2 + C[0, 4] * b_element[2, 4] * l * phi_dd * x1 - C[
                            0, 4] * b_element[2, 4] * l * phi_dd * x2 + C[0, 4] * b_element[3, 0] * l * w_p_d * y1 - C[
                            0, 4] * b_element[3, 0] * l * w_p_d * y2 + C[0, 4] * b_element[3, 3] * l * phi_d * y1 - C[
                            0, 4] * b_element[3, 3] * l * phi_d * y2 + C[0, 4] * b_element[3, 4] * l * phi_dd * y1 - C[
                            0, 4] * b_element[3, 4] * l * phi_dd * y2 + C[1, 0] * phi_dd * x1 ** 2 - 2 * C[
                            1, 0] * phi_dd * x1 * x2 + C[1, 0] * phi_dd * x2 ** 2 + C[1, 0] * phi_dd * y1 ** 2 - 2 * C[
                            1, 0] * phi_dd * y1 * y2 + C[1, 0] * phi_dd * y2 ** 2) / (
                                    C[0, 3] * V_x_additional * f_r_const_111 + C[
                                0, 3] * V_x_additional * f_r_const_112 - 2 * C[0, 3] * V_x_additional * f_r_const_113 +
                                    C[0, 3] * V_y_additional * f_r_const_121 + C[
                                        0, 3] * V_y_additional * f_r_const_122 - 2 * C[
                                        0, 3] * V_y_additional * f_r_const_123 + C[
                                        0, 4] * V_x_additional * f_r_const_211 + C[
                                        0, 4] * V_x_additional * f_r_const_212 - 2 * C[
                                        0, 4] * V_x_additional * f_r_const_213 + C[
                                        0, 4] * V_y_additional * f_r_const_221 + C[
                                        0, 4] * V_y_additional * f_r_const_222 - 2 * C[
                                        0, 4] * V_y_additional * f_r_const_223)
            s_t[1, 0] = (1 / 4) * (
                        C[1, 0] * Theta_x_d * l * y1 - C[1, 0] * Theta_x_d * l * y2 - C[1, 0] * Theta_y_d * l * x1 + C[
                    1, 0] * Theta_y_d * l * x2 - C[1, 0] * l * omega1 * phi_dd + C[1, 0] * l * omega2 * phi_dd + C[
                            1, 1] * phi_dd * x1 ** 2 - 2 * C[1, 1] * phi_dd * x1 * x2 + C[1, 1] * phi_dd * x2 ** 2 + C[
                            1, 1] * phi_dd * y1 ** 2 - 2 * C[1, 1] * phi_dd * y1 * y2 + C[1, 1] * phi_dd * y2 ** 2 + 3 *
                        C[1, 3] * V_x_additional * f_r_const_111 * l + C[
                            1, 3] * V_x_additional * f_r_const_112 * l - 4 * C[
                            1, 3] * V_x_additional * f_r_const_113 * l + 3 * C[
                            1, 3] * V_y_additional * f_r_const_121 * l + C[
                            1, 3] * V_y_additional * f_r_const_122 * l - 4 * C[
                            1, 3] * V_y_additional * f_r_const_123 * l + C[1, 4] * Theta_x_d * b_element[
                            2, 1] * l * x1 - C[1, 4] * Theta_x_d * b_element[2, 1] * l * x2 + C[1, 4] * Theta_x_d *
                        b_element[3, 1] * l * y1 - C[1, 4] * Theta_x_d * b_element[3, 1] * l * y2 + C[
                            1, 4] * Theta_y_d * b_element[2, 2] * l * x1 - C[1, 4] * Theta_y_d * b_element[
                            2, 2] * l * x2 + C[1, 4] * Theta_y_d * b_element[3, 2] * l * y1 - C[1, 4] * Theta_y_d *
                        b_element[3, 2] * l * y2 + 3 * C[1, 4] * V_x_additional * f_r_const_211 * l + C[
                            1, 4] * V_x_additional * f_r_const_212 * l - 4 * C[
                            1, 4] * V_x_additional * f_r_const_213 * l + 3 * C[
                            1, 4] * V_y_additional * f_r_const_221 * l + C[
                            1, 4] * V_y_additional * f_r_const_222 * l - 4 * C[
                            1, 4] * V_y_additional * f_r_const_223 * l + C[1, 4] * b_element[2, 0] * l * w_p_d * x1 - C[
                            1, 4] * b_element[2, 0] * l * w_p_d * x2 + C[1, 4] * b_element[2, 3] * l * phi_d * x1 - C[
                            1, 4] * b_element[2, 3] * l * phi_d * x2 + C[1, 4] * b_element[2, 4] * l * phi_dd * x1 - C[
                            1, 4] * b_element[2, 4] * l * phi_dd * x2 + C[1, 4] * b_element[3, 0] * l * w_p_d * y1 - C[
                            1, 4] * b_element[3, 0] * l * w_p_d * y2 + C[1, 4] * b_element[3, 3] * l * phi_d * y1 - C[
                            1, 4] * b_element[3, 3] * l * phi_d * y2 + C[1, 4] * b_element[3, 4] * l * phi_dd * y1 - C[
                            1, 4] * b_element[3, 4] * l * phi_dd * y2) / (C[1, 3] * V_x_additional * f_r_const_111 + C[
                1, 3] * V_x_additional * f_r_const_112 - 2 * C[1, 3] * V_x_additional * f_r_const_113 + C[
                                                                              1, 3] * V_y_additional * f_r_const_121 +
                                                                          C[1, 3] * V_y_additional * f_r_const_122 - 2 *
                                                                          C[1, 3] * V_y_additional * f_r_const_123 + C[
                                                                              1, 4] * V_x_additional * f_r_const_211 +
                                                                          C[1, 4] * V_x_additional * f_r_const_212 - 2 *
                                                                          C[1, 4] * V_x_additional * f_r_const_213 + C[
                                                                              1, 4] * V_y_additional * f_r_const_221 +
                                                                          C[1, 4] * V_y_additional * f_r_const_222 - 2 *
                                                                          C[1, 4] * V_y_additional * f_r_const_223)
            s_t[2, 0] = (1 / 4) * (
                        C[2, 0] * Theta_x_d * l * y1 - C[2, 0] * Theta_x_d * l * y2 - C[2, 0] * Theta_y_d * l * x1 + C[
                    2, 0] * Theta_y_d * l * x2 - C[2, 0] * l * omega1 * phi_dd + C[2, 0] * l * omega2 * phi_dd + C[
                            2, 1] * phi_dd * x1 ** 2 - 2 * C[2, 1] * phi_dd * x1 * x2 + C[2, 1] * phi_dd * x2 ** 2 + C[
                            2, 1] * phi_dd * y1 ** 2 - 2 * C[2, 1] * phi_dd * y1 * y2 + C[2, 1] * phi_dd * y2 ** 2 + 3 *
                        C[2, 3] * V_x_additional * f_r_const_111 * l + C[
                            2, 3] * V_x_additional * f_r_const_112 * l - 4 * C[
                            2, 3] * V_x_additional * f_r_const_113 * l + 3 * C[
                            2, 3] * V_y_additional * f_r_const_121 * l + C[
                            2, 3] * V_y_additional * f_r_const_122 * l - 4 * C[
                            2, 3] * V_y_additional * f_r_const_123 * l + C[2, 4] * Theta_x_d * b_element[
                            2, 1] * l * x1 - C[2, 4] * Theta_x_d * b_element[2, 1] * l * x2 + C[2, 4] * Theta_x_d *
                        b_element[3, 1] * l * y1 - C[2, 4] * Theta_x_d * b_element[3, 1] * l * y2 + C[
                            2, 4] * Theta_y_d * b_element[2, 2] * l * x1 - C[2, 4] * Theta_y_d * b_element[
                            2, 2] * l * x2 + C[2, 4] * Theta_y_d * b_element[3, 2] * l * y1 - C[2, 4] * Theta_y_d *
                        b_element[3, 2] * l * y2 + 3 * C[2, 4] * V_x_additional * f_r_const_211 * l + C[
                            2, 4] * V_x_additional * f_r_const_212 * l - 4 * C[
                            2, 4] * V_x_additional * f_r_const_213 * l + 3 * C[
                            2, 4] * V_y_additional * f_r_const_221 * l + C[
                            2, 4] * V_y_additional * f_r_const_222 * l - 4 * C[
                            2, 4] * V_y_additional * f_r_const_223 * l + C[2, 4] * b_element[2, 0] * l * w_p_d * x1 - C[
                            2, 4] * b_element[2, 0] * l * w_p_d * x2 + C[2, 4] * b_element[2, 3] * l * phi_d * x1 - C[
                            2, 4] * b_element[2, 3] * l * phi_d * x2 + C[2, 4] * b_element[2, 4] * l * phi_dd * x1 - C[
                            2, 4] * b_element[2, 4] * l * phi_dd * x2 + C[2, 4] * b_element[3, 0] * l * w_p_d * y1 - C[
                            2, 4] * b_element[3, 0] * l * w_p_d * y2 + C[2, 4] * b_element[3, 3] * l * phi_d * y1 - C[
                            2, 4] * b_element[3, 3] * l * phi_d * y2 + C[2, 4] * b_element[3, 4] * l * phi_dd * y1 - C[
                            2, 4] * b_element[3, 4] * l * phi_dd * y2) / (C[2, 3] * V_x_additional * f_r_const_111 + C[
                2, 3] * V_x_additional * f_r_const_112 - 2 * C[2, 3] * V_x_additional * f_r_const_113 + C[
                                                                              2, 3] * V_y_additional * f_r_const_121 +
                                                                          C[2, 3] * V_y_additional * f_r_const_122 - 2 *
                                                                          C[2, 3] * V_y_additional * f_r_const_123 + C[
                                                                              2, 4] * V_x_additional * f_r_const_211 +
                                                                          C[2, 4] * V_x_additional * f_r_const_212 - 2 *
                                                                          C[2, 4] * V_x_additional * f_r_const_213 + C[
                                                                              2, 4] * V_y_additional * f_r_const_221 +
                                                                          C[2, 4] * V_y_additional * f_r_const_222 - 2 *
                                                                          C[2, 4] * V_y_additional * f_r_const_223)
            s_t[3, 0] = (1 / 4) * (
                        C[3, 0] * Theta_x_d * l * y1 - C[3, 0] * Theta_x_d * l * y2 - C[3, 0] * Theta_y_d * l * x1 + C[
                    3, 0] * Theta_y_d * l * x2 - C[3, 0] * l * omega1 * phi_dd + C[3, 0] * l * omega2 * phi_dd + C[
                            3, 1] * phi_dd * x1 ** 2 - 2 * C[3, 1] * phi_dd * x1 * x2 + C[3, 1] * phi_dd * x2 ** 2 + C[
                            3, 1] * phi_dd * y1 ** 2 - 2 * C[3, 1] * phi_dd * y1 * y2 + C[3, 1] * phi_dd * y2 ** 2 + 3 *
                        C[3, 3] * V_x_additional * f_r_const_111 * l + C[
                            3, 3] * V_x_additional * f_r_const_112 * l - 4 * C[
                            3, 3] * V_x_additional * f_r_const_113 * l + 3 * C[
                            3, 3] * V_y_additional * f_r_const_121 * l + C[
                            3, 3] * V_y_additional * f_r_const_122 * l - 4 * C[
                            3, 3] * V_y_additional * f_r_const_123 * l + C[4, 3] * Theta_x_d * b_element[
                            2, 1] * l * x1 - C[4, 3] * Theta_x_d * b_element[2, 1] * l * x2 + C[4, 3] * Theta_x_d *
                        b_element[3, 1] * l * y1 - C[4, 3] * Theta_x_d * b_element[3, 1] * l * y2 + C[
                            4, 3] * Theta_y_d * b_element[2, 2] * l * x1 - C[4, 3] * Theta_y_d * b_element[
                            2, 2] * l * x2 + C[4, 3] * Theta_y_d * b_element[3, 2] * l * y1 - C[4, 3] * Theta_y_d *
                        b_element[3, 2] * l * y2 + 3 * C[4, 3] * V_x_additional * f_r_const_211 * l + C[
                            4, 3] * V_x_additional * f_r_const_212 * l - 4 * C[
                            4, 3] * V_x_additional * f_r_const_213 * l + 3 * C[
                            4, 3] * V_y_additional * f_r_const_221 * l + C[
                            4, 3] * V_y_additional * f_r_const_222 * l - 4 * C[
                            4, 3] * V_y_additional * f_r_const_223 * l + C[4, 3] * b_element[2, 0] * l * w_p_d * x1 - C[
                            4, 3] * b_element[2, 0] * l * w_p_d * x2 + C[4, 3] * b_element[2, 3] * l * phi_d * x1 - C[
                            4, 3] * b_element[2, 3] * l * phi_d * x2 + C[4, 3] * b_element[2, 4] * l * phi_dd * x1 - C[
                            4, 3] * b_element[2, 4] * l * phi_dd * x2 + C[4, 3] * b_element[3, 0] * l * w_p_d * y1 - C[
                            4, 3] * b_element[3, 0] * l * w_p_d * y2 + C[4, 3] * b_element[3, 3] * l * phi_d * y1 - C[
                            4, 3] * b_element[3, 3] * l * phi_d * y2 + C[4, 3] * b_element[3, 4] * l * phi_dd * y1 - C[
                            4, 3] * b_element[3, 4] * l * phi_dd * y2) / (C[3, 3] * V_x_additional * f_r_const_111 + C[
                3, 3] * V_x_additional * f_r_const_112 - 2 * C[3, 3] * V_x_additional * f_r_const_113 + C[
                                                                              3, 3] * V_y_additional * f_r_const_121 +
                                                                          C[3, 3] * V_y_additional * f_r_const_122 - 2 *
                                                                          C[3, 3] * V_y_additional * f_r_const_123 + C[
                                                                              4, 3] * V_x_additional * f_r_const_211 +
                                                                          C[4, 3] * V_x_additional * f_r_const_212 - 2 *
                                                                          C[4, 3] * V_x_additional * f_r_const_213 + C[
                                                                              4, 3] * V_y_additional * f_r_const_221 +
                                                                          C[4, 3] * V_y_additional * f_r_const_222 - 2 *
                                                                          C[4, 3] * V_y_additional * f_r_const_223)
            s_t[4, 0] = (1 / 4) * (
                        C[4, 0] * Theta_x_d * l * y1 - C[4, 0] * Theta_x_d * l * y2 - C[4, 0] * Theta_y_d * l * x1 + C[
                    4, 0] * Theta_y_d * l * x2 - C[4, 0] * l * omega1 * phi_dd + C[4, 0] * l * omega2 * phi_dd + C[
                            4, 1] * phi_dd * x1 ** 2 - 2 * C[4, 1] * phi_dd * x1 * x2 + C[4, 1] * phi_dd * x2 ** 2 + C[
                            4, 1] * phi_dd * y1 ** 2 - 2 * C[4, 1] * phi_dd * y1 * y2 + C[4, 1] * phi_dd * y2 ** 2 + 3 *
                        C[4, 3] * V_x_additional * f_r_const_111 * l + C[
                            4, 3] * V_x_additional * f_r_const_112 * l - 4 * C[
                            4, 3] * V_x_additional * f_r_const_113 * l + 3 * C[
                            4, 3] * V_y_additional * f_r_const_121 * l + C[
                            4, 3] * V_y_additional * f_r_const_122 * l - 4 * C[
                            4, 3] * V_y_additional * f_r_const_123 * l + C[4, 4] * Theta_x_d * b_element[
                            2, 1] * l * x1 - C[4, 4] * Theta_x_d * b_element[2, 1] * l * x2 + C[4, 4] * Theta_x_d *
                        b_element[3, 1] * l * y1 - C[4, 4] * Theta_x_d * b_element[3, 1] * l * y2 + C[
                            4, 4] * Theta_y_d * b_element[2, 2] * l * x1 - C[4, 4] * Theta_y_d * b_element[
                            2, 2] * l * x2 + C[4, 4] * Theta_y_d * b_element[3, 2] * l * y1 - C[4, 4] * Theta_y_d *
                        b_element[3, 2] * l * y2 + 3 * C[4, 4] * V_x_additional * f_r_const_211 * l + C[
                            4, 4] * V_x_additional * f_r_const_212 * l - 4 * C[
                            4, 4] * V_x_additional * f_r_const_213 * l + 3 * C[
                            4, 4] * V_y_additional * f_r_const_221 * l + C[
                            4, 4] * V_y_additional * f_r_const_222 * l - 4 * C[
                            4, 4] * V_y_additional * f_r_const_223 * l + C[4, 4] * b_element[2, 0] * l * w_p_d * x1 - C[
                            4, 4] * b_element[2, 0] * l * w_p_d * x2 + C[4, 4] * b_element[2, 3] * l * phi_d * x1 - C[
                            4, 4] * b_element[2, 3] * l * phi_d * x2 + C[4, 4] * b_element[2, 4] * l * phi_dd * x1 - C[
                            4, 4] * b_element[2, 4] * l * phi_dd * x2 + C[4, 4] * b_element[3, 0] * l * w_p_d * y1 - C[
                            4, 4] * b_element[3, 0] * l * w_p_d * y2 + C[4, 4] * b_element[3, 3] * l * phi_d * y1 - C[
                            4, 4] * b_element[3, 3] * l * phi_d * y2 + C[4, 4] * b_element[3, 4] * l * phi_dd * y1 - C[
                            4, 4] * b_element[3, 4] * l * phi_dd * y2) / (C[4, 3] * V_x_additional * f_r_const_111 + C[
                4, 3] * V_x_additional * f_r_const_112 - 2 * C[4, 3] * V_x_additional * f_r_const_113 + C[
                                                                              4, 3] * V_y_additional * f_r_const_121 +
                                                                          C[4, 3] * V_y_additional * f_r_const_122 - 2 *
                                                                          C[4, 3] * V_y_additional * f_r_const_123 + C[
                                                                              4, 4] * V_x_additional * f_r_const_211 +
                                                                          C[4, 4] * V_x_additional * f_r_const_212 - 2 *
                                                                          C[4, 4] * V_x_additional * f_r_const_213 + C[
                                                                              4, 4] * V_y_additional * f_r_const_221 +
                                                                          C[4, 4] * V_y_additional * f_r_const_222 - 2 *
                                                                          C[4, 4] * V_y_additional * f_r_const_223)



            #s_t = np.linalg.solve(s_t_A, s_t_b)
            t_ex_d = np.zeros((5, 1))
            for i, s_i in enumerate(s_t):
                if not np.isnan(s_i) and 0 < s_i < l:
                    d_i = JungCrossSectionProcessor._d(element, displacements, v_s, s_i)
                    t_i = JungCrossSectionProcessor._t_from_d(C, d_i)
                    t_ex_d[i, 0] = t_i[i]

            min_strain = np.nanmin(np.hstack([d_ex_0, d_ex_l, d_ex_d]), axis=1)
            max_strain = np.nanmax(np.hstack([d_ex_0, d_ex_l, d_ex_d]), axis=1)

            min_stress = np.nanmin(np.hstack([t_ex_0, t_ex_l, t_ex_d]), axis=1)
            max_stress = np.nanmax(np.hstack([t_ex_0, t_ex_l, t_ex_d]), axis=1)


        min_load_state = JungCrossSectionProcessor.strain_stress_vectors_to_load_state(min_strain, min_stress)
        max_load_state = JungCrossSectionProcessor.strain_stress_vectors_to_load_state(max_strain, max_stress)

        # min_strain = np.hstack([d_ex_0, d_ex_l, d_ex_d]).nanmin(axis=1)
        # max_strain = np.hstack([d_ex_0, d_ex_l, d_ex_d]).nanmax(axis=1)
        #
        # min_stress = np.hstack([t_ex_0, t_ex_l, t_ex_d]).nanmin(axis=1)
        # max_stress = np.hstack([t_ex_0, t_ex_l, t_ex_d]).nanmax(axis=1)

        # Load state
        #STRAIN_NAMES = ['epsilon_zz', 'kappa_zz', 'kappa_zs', 'gamma_zs', 'kappa_ss']
        #STRESS_NAMES = ['N_zz', 'M_zz', 'M_zs', 'N_zs', 'M_ss']

        #
        # # Validation
        # load_state_functions = self.calc_element_load_state(element, displacements)
        #
        # def calc_load_state(load_state_functions, s):
        #     new_strain_state = {key: val(s) for key, val in load_state_functions.strain_state.items()}
        #     new_stress_state = {key: val(s) for key, val in load_state_functions.stress_state.items()}
        #     return ElementLoadState(new_strain_state, new_stress_state)
        #
        # ex_0_ref = calc_load_state(load_state_functions, 0)
        # ex_l_ref = calc_load_state(load_state_functions, l)
        # ex_l2_ref = calc_load_state(load_state_functions, l/2)

        # strain_dict_min = {}
        # for state_key, stress_from_strain_func in load_state_functions.strain_state.items():
        #     stress = min([stress_from_strain_func(0),
        #                   stress_from_strain_func(l / 2),
        #                   stress_from_strain_func(l)])#, key=abs)  # TODO: what ist abs key?
        #     strain_dict_min[state_key] = stress
        # stress_dict_min = {}
        # for state_key, stress_from_strain_func in load_state_functions.stress_state.items():
        #     stress = min([stress_from_strain_func(0),
        #                   stress_from_strain_func(l / 2),
        #                   stress_from_strain_func(l)])#, key=abs)  # TODO: what ist abs key?
        #     stress_dict_min[state_key] = stress
        #
        # strain_dict_max = {}
        # for state_key, stress_from_strain_func in load_state_functions.strain_state.items():
        #     stress = max([stress_from_strain_func(0),
        #                   stress_from_strain_func(l / 2),
        #                   stress_from_strain_func(l)])#, key=abs)  # TODO: what ist abs key?
        #     strain_dict_max[state_key] = stress
        # stress_dict_max = {}
        # for state_key, stress_from_strain_func in load_state_functions.stress_state.items():
        #     stress = max([stress_from_strain_func(0),
        #                   stress_from_strain_func(l / 2),
        #                   stress_from_strain_func(l)])#, key=abs)  # TODO: what ist abs key?
        #     stress_dict_max[state_key] = stress


        # min_strain_ref = np.nanmin(np.vstack([list(ex_0_ref.strain_state.values()), list(ex_l_ref.strain_state.values()), list(ex_l2_ref.strain_state.values())]).T, axis=1)
        # max_strain_ref = np.nanmax(np.vstack([list(ex_0_ref.strain_state.values()), list(ex_l_ref.strain_state.values()), list(ex_l2_ref.strain_state.values())]).T, axis=1)
        #
        # min_stress_ref = np.nanmin(np.vstack([list(ex_0_ref.stress_state.values()), list(ex_l_ref.stress_state.values()), list(ex_l2_ref.stress_state.values())]).T, axis=1)
        # max_stress_ref = np.nanmax(np.vstack([list(ex_0_ref.stress_state.values()), list(ex_l_ref.stress_state.values()), list(ex_l2_ref.stress_state.values())]).T, axis=1)

        # if not np.all(np.isclose(list(min_load_state.strain_state.values()), min_strain_ref, rtol=1e-1)):
        #     log.warning('nich tgut')
        # if not np.all(np.isclose(list(max_load_state.strain_state.values()), max_strain_ref, rtol=1e-1)):
        #     log.warning('nich tgut')
        # if not np.all(np.isclose(list(min_load_state.stress_state.values()), min_stress_ref, rtol=1e-1)):
        #     log.warning('nich tgut')
        # if not np.all(np.isclose(list(max_load_state.stress_state.values()), max_stress_ref, rtol=1e-1)):
        #     log.warning('nich tgut')

        # assert np.all(np.isclose(list(min_load_state.strain_state.values()), min_strain_ref, rtol=1e-2))
        # assert np.all(np.isclose(list(max_load_state.strain_state.values()), max_strain_ref, rtol=1e-2))
        # assert np.all(np.isclose(list(min_load_state.stress_state.values()), min_stress_ref, rtol=1e-2))
        # assert np.all(np.isclose(list(max_load_state.stress_state.values()), max_stress_ref, rtol=1e-2))

        return min_load_state, max_load_state#ElementLoadState(strain_dict_min, stress_dict_min), ElementLoadState(strain_dict_max, stress_dict_max)#min_load_state, max_load_state