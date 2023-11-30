"""
.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
from copy import copy
from typing import Optional

import networkx as nx
import numpy as np

from PreDoCS.CrossSectionAnalysis.Interfaces import IElement, INode
from PreDoCS.util.Logging import get_module_logger
from PreDoCS.util.MinimalCycleBasis import MinimalCycleBasis
from PreDoCS.util.util import normal_vector_2d, get_polygon_area
from PreDoCS.util.vector import Vector

log = get_module_logger(__name__)


class DiscreetCrossSectionGeometry(object):
    """
    A discreet geometry description of a cross section build of IElement.
    
    Attributes
    ----------
    _graph: networkx.Graph
        The graph describing the structure buildup.
    _cells: list(Cell)
        List of all cells of the discreet geometry.
    _segments: list(Segment)
        List of all segments of the discreet geometry.
    _update_required: bool
        True, if a new calculation is required.
    
    Constants
    ---------
    _ELEMENT_EDGE_NAME: str
        The name of the element attribute of a graph edge. 
    """
    
    _ELEMENT_EDGE_NAME = 'element'

    def __init__(self):
        """
        Constructor.
        """
        self._graph = nx.Graph()
        self._update_required = False
    
    def copy(self):
        """
        Returns a copy of the discreet geometry.
        
        Returns
        -------
        DiscreetCrossSectionGeometry
            The new discreet geometry.
        """
        discreet_geometry = DiscreetCrossSectionGeometry()
        discreet_geometry._graph = self._graph.copy()
        discreet_geometry._update_required = True
        return discreet_geometry
    
    @property
    def cells(self) -> list['DiscreetCrossSectionGeometry.Cell']:
        """list(Cell): List of all cells of the discreet geometry."""
        self._update_if_required()
        return self._cells
    
    def _update_if_required(self):
        """
        Update the cached values.
        """
        if self._update_required:
            self._update_required = False

            # # DEBUG
            # import matplotlib.pyplot as plt
            # plt.figure()
            # nx.draw(self._graph)
            # plt.savefig('planar_graph.png')
            # plt.close()

            # Check for id duplicates
            node_hashs = [hash(n) for n in self.nodes]
            assert(len(node_hashs) == len(set(node_hashs)))
            element_ids = [e.id for e in self.elements]
            assert(len(element_ids) == len(set(element_ids)))
            component_ids = [s.id for s in self.components]
            assert(len(component_ids) == len(set(component_ids)))
            
            self._segments = self._get_segments()
            segment_ids = [s.id for s in self.segments]
            assert(len(segment_ids) == len(set(segment_ids)))

            self._cells = self._get_cells()
            for cell in self._cells:
                cell.set_segments()
            
    @property
    def elements(self) -> list['DiscreetCrossSectionGeometry.Element']:
        """list(IElement): List of all elements of the cross section discreet geometry."""
        edges = self._graph.edges(data=True)
        res = [data[DiscreetCrossSectionGeometry._ELEMENT_EDGE_NAME] for (node1, node2, data) in edges]
        return sorted(res, key=lambda e: e.id)
    
    def add_element(self, element):
        """
        Adds an element to the discreet cross section.
        
        Parameters
        ----------
        element: IElement
            The element.
        """
        self._graph.add_edge(element.node1, element.node2, **{DiscreetCrossSectionGeometry._ELEMENT_EDGE_NAME: element})
        self._update_required = True
        
    def add_elements(self, elements):
        """
        Adds elements to the discreet cross section.
        
        Parameters
        ----------
        elements: list( IElement)
            The elements added between the given nodes.
        """
        for element in elements:
            self.add_element(element)
        self._update_required = True
    
    @property
    def nodes(self) -> list['DiscreetCrossSectionGeometry.Node']:
        """
        list(INode):
           List of all nodes of the discreet cross section.
        """
        return sorted(self._graph.nodes(), key=lambda n: n.id)
    
    @property
    def components(self) -> list['DiscreetCrossSectionGeometry.Component']:
        """
        list(Component):
           List of all components of the discreet cross section.
        """
        return sorted({element.component for element in self.elements}, key=lambda c: c.id)
    
    @property
    def segment_border_nodes(self) -> list['DiscreetCrossSectionGeometry.Node']:
        """
        list(INode):
           List of all nodes that are border nodes of a segment.
        """
        self._update_if_required()
        return sorted(
            {segment.node1 for segment in self._segments} | {segment.node2 for segment in self._segments},
            key=lambda n: n.id
        )

    @property
    def segments(self) -> list['DiscreetCrossSectionGeometry.Segment']:
        """
        list(Segment):
            List of all segments of the cross section discreet geometry.
        """
        self._update_if_required()
        return sorted(self._segments, key=lambda s: s.id)
    
    def get_element_from_nodes(self, node1, node2) -> Optional['DiscreetCrossSectionGeometry.Element']:
        """
        Returns the element between the given nodes.
        
        Parameters
        ----------
        node1: INode
            First node of the element.
        node2: INode
            Second node of the element.

        Returns
        -------
        IElement
            Element between the nodes if available, otherwise None.
        """
        data = self._graph.get_edge_data(node1, node2)
        if data:
            return data[DiscreetCrossSectionGeometry._ELEMENT_EDGE_NAME]
        else:
            return None

    def get_neighbor_nodes(self, node) -> list['DiscreetCrossSectionGeometry.Node']:
        """
        Returns the neighbor nodes of a node.
        
        Parameters
        ----------
        node: INode
            The node.
        
        Returns
        -------
        list(INode)
            Neighbor nodes of the node, empty list if no neighbor nodes available.
        """
        return sorted(self._graph.neighbors(node), key=lambda n: n.id)
    
    def get_adjacent_elements(self, node) -> list['DiscreetCrossSectionGeometry.Element']:
        """
        Returns the adjacent elements of a node.
        
        Parameters
        ----------
        node: INode
            The node.
        
        Returns
        -------
        list(IElement)
            Adjacent elements of the node, empty list if no adjacent elements available.
        """
        return sorted(
            [self.get_element_from_nodes(neighbor, node) for neighbor in self.get_neighbor_nodes(node)],
            key=lambda e: e.id
        )
    
    def get_shortest_path(self, start_node, end_node) -> list['DiscreetCrossSectionGeometry.Node']:
        """
        Returns the shortest path between start and end node.
        
        Parameters
        ----------
        start_node: INode
            The start node.
        end_node: INode
            The end node.
        
        Returns
        -------
        list(INode)
            Shortest path.
        """
        return nx.shortest_path(self._graph, start_node, end_node)

    @staticmethod
    def get_common_node_from_elements(element1, element2) -> 'DiscreetCrossSectionGeometry.Node':
        """
        Returns the common node of the elements.
            
        Parameters
        ----------
        element1: IElement
            The first element.
        element2: IElement
            The second element.
            
        Returns
        -------
        INode
            The common node.
            
        Raises
        ------
        KeyError
            Thrown, if the elements do not have a common node.
        """
        return ({element1.node1, element1.node2} & {element2.node1, element2.node2}).pop()
    
    @staticmethod
    def get_common_node_from_segments(segment1, segment2) -> 'DiscreetCrossSectionGeometry.Node':
        """
        Returns the common node of the segments.
            
        Parameters
        ----------
        segment1: Segment
            The first segment.
        segment2: Segment
            The second segment.
            
        Returns
        -------
        INode
            The common node.
            
        Raises
        ------
        KeyError
            Thrown, if the segments do not have a common node.
        """
        return ({segment1.node1, segment1.node2} & {segment2.node1, segment2.node2}).pop()

    @staticmethod
    def is_element_in_direction_of_elements(element, elements) -> bool:
        """
        Returns True, if the element orientation is equal to the direction of the elements.
        
        Parameters
        ----------
        element: IElement
            The element.
        elements: list(IElement)
            The list of elements.
        
        Returns
        -------
        bool
            True, if the element orientation is equal to the direction of the elements.
        """
        assert(len(elements) > 0)
        
        if len(elements) == 1:
            return True
        
        if element == elements[-1]:
            # Element is last element of the list
            common_node = DiscreetCrossSectionGeometry.get_common_node_from_elements(element, elements[-2])
            if common_node == element.node1:
                return True
            else:
                return False
        else:
            next_element = elements[elements.index(element)+1]
            common_node = DiscreetCrossSectionGeometry.get_common_node_from_elements(element, next_element)
            if common_node == element.node2:
                return True
            else:
                return False

    @staticmethod
    def is_segment_in_direction_of_cell(segment, cell) -> bool:
        """
        Returns True, if the segment orientation is equal to circulating direction of the cell.
        
        Parameters
        ----------
        segment: Segment
            The segment.
        cell: Cell
            The cell.
        
        Returns
        -------
        bool
            True, if the segment orientation is equal to circulating direction of the cell.
        """
        first_element = segment.elements[0]
        first_element_in_direction_of_segment = DiscreetCrossSectionGeometry.is_element_in_direction_of_segment(first_element, segment)
        first_element_in_direction_of_cell = DiscreetCrossSectionGeometry.is_element_in_direction_of_elements(first_element, cell.elements)
        return first_element_in_direction_of_segment == first_element_in_direction_of_cell

    @staticmethod
    def is_element_in_direction_of_segment(element, segment) -> bool:
        """
        Returns, if the element orientation is equal to the direction of the segment.
        
        Parameters
        ----------
        element: Element
            The element.
        segment: Segment
            The segment.
        
        Returns
        -------
        bool
            True, if the element orientation is equal to the direction of the segment.
        """
        return DiscreetCrossSectionGeometry.is_element_in_direction_of_elements(element, segment.elements)
    
    def _get_cells(self) -> list['DiscreetCrossSectionGeometry.Cell']:
        """
        Returns all cells of the cross section.
        
        Returns
        -------
        list(Cell)
            List of all cells of the cross section.
        """
        # Convert to planar graph
        planar_graph = nx.Graph()
        dict_nodes_vertices = {}  # INode: Vertex
        dict_vertex_id_node = {}  # int: INode
        nodes = self.nodes
        for node in nodes:
            vertex = MinimalCycleBasis.Vertex(node.position)
            dict_nodes_vertices[node] = vertex
            dict_vertex_id_node[vertex.id] = node
            planar_graph.add_node(vertex)
        
        for (n1, n2, data) in self._graph.edges(data=True):
            planar_graph.add_edge(dict_nodes_vertices[n1], dict_nodes_vertices[n2], element=data)

        mcb = MinimalCycleBasis(planar_graph)
        if not len(mcb.get_forest()) == 1:
            raise RuntimeError('The cross section has to made up of one connected part')
        
        # Find faces
        faces = mcb.get_faces()
        if len(faces) < 1:
            raise RuntimeError('A cross section has to the made of at least one closed geometry')
       
        # Convert to cells
        cells = []
        for face in faces:
            face.pop()
            nodes = []
            for vertex in face:
                nodes.append(dict_vertex_id_node[vertex.id])
            cells.append(DiscreetCrossSectionGeometry.Cell(nodes, self))
        cells = sorted(cells, key=lambda c: c.position.length)  # Sort cells

        return cells

    def _get_new_node_id(self) -> int:
        """Returns ID for new node."""
        node_id = 0
        for n in self.nodes:
            if n.id >= node_id:
                node_id = n.id + 1
        return node_id
    
    def cut_discreet_geometry(self, cut_node, other):
        """
        Cuts the discreet geometry at the given cut node at the element between cut_node an other.
        
        Parameters
        ----------
        cut_node: INode
            The cut node.
        other: INode
            The other node.
        """
        # Check if cut node is segment border node
        if cut_node not in self.segment_border_nodes:
            raise RuntimeError('Cut node has to be an border node from an segment')
        
        # Cut discreet geometry
        clone = copy(cut_node)
        clone._id = self._get_new_node_id()

        data = self._graph.get_edge_data(cut_node, other)[DiscreetCrossSectionGeometry._ELEMENT_EDGE_NAME]
        self._graph.remove_edge(cut_node, other)
        self._graph.add_edge(other, clone, **{DiscreetCrossSectionGeometry._ELEMENT_EDGE_NAME: data})
        self._update_required = True
    
    def _get_segments(self) -> list['DiscreetCrossSectionGeometry.Segment']:
        """
        Returns the segments of the discreet geometry. A segment is a part of the contour without branch nodes and
        is contained by only one component.
        
        Returns
        -------
        list(Segment)
            List of all segments of the discreet geometry.
        """
        # # DEBUG
        # from matplotlib import pyplot as plt
        # log.debug('_get_segments')
        # plt.figure()
        # # pos = nx.planar_layout(self._graph)
        # # pos = nx.kamada_kawai_layout(self._graph, dist={(e.node1, e.node2): e.length for e in self.elements})
        # # pos = nx.spring_layout(self._graph, iterations=10, seed=227)
        # nx.draw_networkx(
        #     self._graph,
        #     #pos,
        #     node_size=5,
        #     alpha=0.4,
        #     edge_color="r",
        #     font_size=10,
        #     with_labels=True,
        #     labels={n: n.id for n in self.nodes}
        # )
        # #ax = plt.gca()
        # #ax.margins(0.08)
        # plt.show()

        # nx.draw(self._graph) # DEBUG
        segments_elements = []
        elements_used = []
        start_nodes = sorted([n for n in self.nodes if len(list(self.get_neighbor_nodes(n))) > 2], key=lambda n: n.id) + \
                      sorted([n for n in self.nodes if len(list(self.get_neighbor_nodes(n))) == 1], key=lambda n: n.id)
        
        # Only one cell
        if len(start_nodes) == 0:
            start_nodes = [self.nodes[0]]
        
        for branch_node in start_nodes:
            # log.debug(f'start at branch node {branch_node.id}')
            for neighbor_node in self.get_neighbor_nodes(branch_node):
                # log.debug(f'go to neighbor node {neighbor_node.id}')
                element = self.get_element_from_nodes(branch_node, neighbor_node)
                if element not in elements_used:
                    prev_node = branch_node
                    current_node = neighbor_node
                    segment = [element]
                    elements_used.append(element)
                    while True:
                        if current_node in start_nodes:
                            # Reached next branch or end node
                            segments_elements.append(segment)
                            # log.debug(f'segment finished at node {current_node.id}')
                            break
                        else:
                            next_nodes = set(self.get_neighbor_nodes(current_node)) - {prev_node}
                            assert len(next_nodes) == 1
                            next_node = next_nodes.pop()#sorted(next_nodes, key=lambda n: n.id)[0]
                            next_element = self.get_element_from_nodes(current_node, next_node)
                            if element.component == next_element.component:
                                segment.append(next_element)
                            else:
                                segments_elements.append(segment)
                                segment = [next_element]
                            prev_node = current_node
                            current_node = next_node
                            element = next_element
                            elements_used.append(next_element)

        # if len(elements_used) != len(self.elements):
        #     log.debug(f'invalid: {set(self.elements) - set(elements_used)}')
        assert len(elements_used) == len(self.elements)

        segment_id = 1
        segments = []
        for elements in segments_elements:
            segment = DiscreetCrossSectionGeometry.Segment(segment_id, elements)
            segment_id += 1
            segments.append(segment)
            for element in elements:
                element.segment = segment
        return segments
    
    class Node(INode):
        """
        A node of a discreet cross section. The node has no exact position and is used to describe the connection
        of the elements.
        
        Attributes
        ----------
        _id: int
            Id of the node.
        _position: Vector
            Two-dimensional position of the node in the discreet cross section;
            in line with the elastic axis of the element.
        """
        
        def __init__(self, node_id, position):
            """
            Constructor.
            
            Parameters
            ----------
            position: Vector
                Two-dimensional position of the node in the discreet cross section;
                in line with the elastic axis of the element.
            """
            assert(len(position) == 2)  # Two-dimensional vector
            self._id = node_id
            self._position = position
        
        def __hash__(self):
            """
            Returns
            -------
            int
                Returns a unique hash for the node.
            """
            return self._id
        
        def __repr__(self):
            return '<DiscreetCrossSectionGeometry.Node id:{} position:({}; {})>'.\
                format(self._id, self._position.x, self._position.y)
        
        @property
        def id(self):
            """int: Returns the id of the node."""
            return self._id
        
        def __eq__(self, other):
            """
            Overrides the '=='-operator. Compares the id's of the nodes.
            
            Returns
            -------
            bool
                True, the id's of self and other are equal.
        
            Raises
            ------
            TypeError
                If other is not an instance of Node.
            """
            if isinstance(other, DiscreetCrossSectionGeometry.Node):
                return self._id == other._id
            else:
                raise TypeError()
            
        @property
        def position(self):
            """
            Vector:
                Two-dimensional position of the node in the discreet cross section;
                in line with the elastic axis of the element.
            """
            return self._position
        
        @position.setter
        def position(self, value):
            self._position = value

    class Element(IElement):
        """
        A discreet element of a cross section. The element is is made up of one material.
        Two nodes determine the orientation of an element. The nodes are in line with the elastic axis of the element.
        
        Coordinate system:
            * Length-direction (s): connection vector from the position of the first node
                to the position of the second node.
            * Depth-direction (z): The same as the cross section depth-direction (z).
            * Thickness-direction (n): perpendicular to length- and depth-direction.
        
        Attributes
        ----------
        _id: int
            Id of the element.
        _node1: INode
            First node of the element.
        _node2: INode
            Second node of the element.
        _component: Component
            Component, the element belongs to.
        _segment: Segment
            Segment, the element belongs to.
        """
        def __init__(self, element_id, node1, node2, component):
            """
            Constructor.
            
            Parameters
            ----------
            node1: INode
                First node of the element.
            node2: INode
                Second node of the element.
            component: Component
                Component, the element belongs to.

            Raises
            ------
            AssertionError
                Dimension of positions does not equal two.
            """
            assert(not (node1 == node2))
            assert(not ((node1.position - node2.position).length == 0))  # Element must have a length
            self._id = element_id
            self._node1 = node1
            self._node2 = node2
            self._component = component
            self._segment = None

        def __hash__(self):
            """
            Returns
            -------
            int
                Returns a unique hash for the element.
            """
            return self._id
        
        def __repr__(self):
            return '<DiscreetCrossSectionGeometry.Element id:{} position:({}; {})>'.\
                format(self._id, self.position.x, self.position.y)
        
        def __eq__(self, other):
            """
            Overrides the '=='-operator. Compares the id's of the elements.
            
            Returns
            -------
            bool
                True, the id's of self and other are equal.
        
            Raises
            ------
            TypeError
                If other is not an instance of Element.
            """
            if isinstance(other, DiscreetCrossSectionGeometry.Element):
                return self._id == other._id
            else:
                raise TypeError()
        
        @property
        def id(self):
            """int: Returns the id of the element."""
            return self._id

        @property
        def node1(self):
            """INode: Returns the first node of the element."""
            return self._node1
        
        @property
        def node2(self):
            """INode: Returns the second node of the element."""
            return self._node2
        
        @property
        def node1_midsurface_position(self):
            """
            Vector:
                Returns position of the first node of the element on the element midsurface.
            """
            return self.node1.position + self.thickness_vector * self.component.midsurface_offset
        
        @property
        def node2_midsurface_position(self):
            """
            Vector:
                Returns position of the second node of the element on the element midsurface.
            """
            return self.node2.position + self.thickness_vector * self.component.midsurface_offset
        
        @property
        def position(self):
            """Vector: Mean position of the element, on the reference axis."""
            return self.node1.position + self.length_vector / 2.
        
        @property
        def midsurface_position(self):
            """Vector: Mean position of the element, on the midsurface."""
            return self.node1_midsurface_position + self.length_vector / 2.
        
        @property
        def angle_in_cross_section(self):
            """float: Returns the angle of the element in RAD in the cross section plane."""
            return self.length_vector.angle_in_plane
        
        @property
        def length_vector(self):
            """
            Vector:
                Returns the vector in length-direction of the element.
                The length of the vector equals the length of the element.
            """
            return self.node2.position - self.node1.position
        
        @property
        def length(self):
            """float: Length of the element."""
            return np.linalg.norm(self.length_vector)
        
        @property
        def thickness_vector(self):
            """
            Vector:
                Returns the vector in thickness-direction of the element.
                The length of the vector equals the thickness of the element.
            """
            return normal_vector_2d(self.length_vector).normalised * self.thickness
        
        @property
        def thickness(self):
            """float: Thickness of the element."""
            return self.material.thickness
    
        @property
        def area(self):
            """float: Area of the element."""
            return self.length * self.thickness

        @property
        def dx_ds(self):
            """float: X-slope of the element."""
            return self.length_vector.x / self.length

        @property
        def dy_ds(self):
            """float: Y-slope of the element."""
            return self.length_vector.y / self.length

        @property
        def component(self):
            """Component: Component, the element belongs to."""
            return self._component
        
        @property
        def segment(self):
            """Segment: Segment, the element belongs to."""
            return self._segment

        @segment.setter
        def segment(self, value):
            self._segment = value
        
        @property
        def material(self):
            """IMaterial: Material of the element."""
            return self.component.material

        def get_function_with_bounds(self, function_without_bounds, s):
            """
            Checks for the given function, if the contur coordinate is in the bound of the element.
            Returns the value of the function at the given contour coordinate value.

            Parameters
            ----------
            function_without_bounds: function(float)
                The function.
            s: float
                The contour coordinate value.

            Returns
            -------
            float
                Value of the function at the given contour coordinate value.
            """
            assert s >= 0
            assert s <= self.length + 1e-8 # TODO: remove  + 1e-8 (tolerance)
            return function_without_bounds(s)
    
    class Component(object):
        """
        A component is a continuous part of the contour build of one material.
        A component can contain branch nodes, in contrast to a segment.
        
        Attributes
        ----------
        _id: int
            Id of the component.
        _material: IMaterial
            Material of the component.
        _midsurface_offset: float
            The midsurface offset defines the distance in normal direction of the contur (as a fraction of the element thickness)
            from the reference surface (connecting the nodes of the element) to the midsurface of the contur.
            The value is from -0.5 to +0.5. 0 means that reference surface and the midsurface are indentical.
        _assembly: Assembly
            The Assembly, the component belongs to.
        _material_region: AssemblyMaterialRegion
            The material region, the component belongs to.
        """
        def __init__(self, component_id, material, midsurface_offset=0.0):
            """
            Constructor.
            
            Parameters
            ----------
            component_id: int
                Id of the component.
            material: IMaterial
                Material of the component.
            midsurface_offset: float
                The midsurface offset defines the distance in normal direction of the contur (as a fraction of the element thickness)
                from the reference surface (connecting the nodes of the element) to the midsurface of the contur.
                The value is from -0.5 to +0.5. 0 means that reference surface and the midsurface are indentical.
            """
            assert(-0.5 <= midsurface_offset <= 0.5)
            self._id = component_id
            self._material = material
            self._midsurface_offset = midsurface_offset
            self._assembly = None
            self._material_region = None
        
        def __hash__(self):
            """
            Returns
            -------
            int
                Returns a unique hash for the component.
            """
            return self._id
        
        def __repr__(self):
            return '<DiscreetCrossSectionGeometry.Component id:{}>'.format(self._id)
        
        @property
        def id(self):
            """int: Returns the id of the component."""
            return self._id
        
        @property
        def material(self):
            """IMaterial: Material of the component."""
            return self._material

        @material.setter
        def material(self, material):
            self._material = material
        
        def __eq__(self, other):
            """
            Overrides the '=='-operator. Compares the id's of the components.
            
            Returns
            -------
            bool
                True, the id's of self and other are equal.
        
            Raises
            ------
            TypeError
                If other is not an instance of Component.
            """
            if isinstance(other, DiscreetCrossSectionGeometry.Component):
                return self._id == other._id
            else:
                raise TypeError()

        @property
        def midsurface_offset(self):
            """
            float:
                The midsurface offset defines the distance in normal direction of the contur (as a fraction of the element thickness)
                from the reference surface (connecting the nodes of the element) to the midsurface of the contur.
                The value is from -0.5 to +0.5. 0 means that reference surface and the midsurface are indentical.
            """
            return self._midsurface_offset

        @property
        def assembly(self):
            """Assembly: The Assembly, the component belongs to."""
            return self._assembly

        @assembly.setter
        def assembly(self, value):
            self._assembly = value

        @property
        def material_region(self):
            """AssemblyMaterialRegion: The material region, the component belongs to."""
            return self._material_region

        @material_region.setter
        def material_region(self, value):
            self._material_region = value

    class Segment(object):
        """
        A segment is a part of the contour without branch nodes, kinks and made of one material
        (belongs to only one component). Segment direction is from node 1 to node 2.
        
        Attributes
        ----------
        _id: int
            Id of the segment.
        _elements: list(IElement)
            List of elements of the segment, sorted from node1 to node2.
        _node1: INode
            First node of the segment.
        _node2: INode
            Second node of the segment.
        _length: float
            Length of the segment.
        """
        def __init__(self, segment_id, elements):
            """
            Constructor.
            
            Parameters
            ----------
            segment_id: int
                Id of the segment.
            elements: list(IElement)
                List of elements of the segment, sorted from node1 to node2.
            """
            assert(len(elements) > 0)
            self._id = segment_id
            self.elements = elements

        def __hash__(self):
            """
            Returns
            -------
            int
                Returns a unique hash for the segment.
            """
            return self._id

        def __repr__(self):
            return '<DiscreetCrossSectionGeometry.Segment id:{}>'.format(self._id)

        @property
        def id(self):
            """int: Returns the id of the segment."""
            return self._id

        def __eq__(self, other):
            """
            Overrides the '=='-operator. Compares the id's of the segments.

            Returns
            -------
            bool
                True, the id's of self and other are equal.

            Raises
            ------
            TypeError
                If other is not an instance of Segment.
            """
            if isinstance(other, DiscreetCrossSectionGeometry.Segment):
                return self._id == other._id
            else:
                raise TypeError()

        @property
        def elements(self):
            """list(IElement): List of elements of the segment, sorted."""
            return self._elements

        @elements.setter
        def elements(self, elements):
            """list(IElement): List of elements of the segment, sorted."""
            self._elements = elements
            # Get border nodes
            if len(elements) == 1:
                self._node1 = elements[0].node1
                self._node2 = elements[0].node2
            elif len(elements) > 1:
                self._node1 = ({elements[0].node1, elements[0].node2} - {elements[1].node1, elements[1].node2}).pop()
                self._node2 = (
                            {elements[-1].node1, elements[-1].node2} - {elements[-2].node1, elements[-2].node2}).pop()

            self._length = sum(element.length for element in self._elements)

        @property
        def node1(self):
            """INode: First node of the segment."""
            return self._node1
        
        @property
        def node2(self):
            """INode: Second node of the segment."""
            return self._node2
        
        @property
        def length(self):
            """float: Length of the segment."""
            return self._length
        
        @property
        def component(self):
            """Component: Component of the segment."""
            return self._elements[0].component

        @property
        def material(self):
            """IMaterial: Material of the segment."""
            return self.component.material

    class Cell(object):
        """
        The class represents a closed cell of a cross section. Furthermore, the cell can be cutted.

        Attributes
        ----------
        _elements: list(IElement)
            Elements of the cell, sorted.
        _segments: list(Segment)
            Segments of the cell, not sorted.
        _nodes: list(INode)
            Nodes of the cell, sorted.
        _cut_node: INode
            Cut node.
        """
    
        def __init__(self, nodes, discreet_geometry):
            """
            Constructor.
            
            Parameters
            ----------
            nodes: list(INode)
                Sorted list of the node of the cell.
            discreet_geometry: IDiscreetDiscreetCrossSectionGeometry
                Discreet cross section discreet geometry containing the cell.
            """
            self._cut_node = None
            self._nodes = sorted(nodes, key=lambda n: n.id)
            self._elements = []
            self._segments = []
            prev_node = nodes[-1]
            for node in nodes:
                self._elements.append(discreet_geometry.get_element_from_nodes(prev_node, node))
                prev_node = node
            self._area = self._get_area()
            
        @property
        def nodes(self):
            """list(INode): nodes of the cell, sorted."""
            return self._nodes
         
        @property
        def elements(self):
            """list(IElement): Elements of the cell, sorted."""
            return self._elements
         
        @property
        def segments(self):
            """list(Segment): Segments of the cell, not sorted."""
            return self._segments
        
        @property
        def is_cutted(self):
            """bool: True, if the cell is cutted and has a cut node."""
            return self._cut_node is not None
        
        @property
        def cut_node(self):
            """INode: Cut node."""
            return self._cut_node
        
        @cut_node.setter
        def cut_node(self, value):
            self._cut_node = value
        
        @property
        def area(self):
            """float: Enclosed area of the cell."""
            return self._area

        @property
        def position(self) -> Vector:
            """Vector: Mean position of the cell."""
            return Vector(np.mean([n.position for n in self.nodes], axis=0))

        def _get_midsurface_position_from_node(self, node):
            """
            Returns the midsurface position of the given node.

            Parameters
            ----------
            INode
                The node.

            Returns
            -------
            Vector
                The midsurface position of the node.
            """
            positions = []
            for e in self._elements:
                if node == e.node1:
                    positions.append(e.node1_midsurface_position)
                elif node == e.node2:
                    positions.append(e.node2_midsurface_position)
            num_positions = len(positions)
            return Vector([sum(p.x for p in positions) / num_positions,
                           sum(p.y for p in positions) / num_positions])

        def _get_area(self):
            """
            Calculates the enclosed area of the cell.
            
            Returns
            -------
            float
                Enclosed area of the cell.
            """
            # TODO: actually the nodes from the midsurface should be used.
            #  But when using them, the torsional function calculation and the warping calculation fails.
            #midsurface_node_positions = [self._get_midsurface_position_from_node(node) for node in self._nodes]
            #x = [p.x for p in midsurface_node_positions]
            #y = [p.y for p in midsurface_node_positions]

            x = [node.position.x for node in self._nodes]
            y = [node.position.y for node in self._nodes]
            return get_polygon_area(x, y)
        
        def set_segments(self):
            """
            Sets the segments of the cell.
            """
            all_segments = {e.segment for e in self._elements}
            segments = []
            cell_element_set = set(self._elements)
            for segment in all_segments:
                segment_element_set = set(segment.elements)
                if segment_element_set.issubset(cell_element_set):
                    # Segments in cell
                    segments.append(segment)
                elif len(segment_element_set.intersection(cell_element_set)) > 0:
                    raise RuntimeError('It is not possible that a part of a segment belongs to a cell')
            self._segments = sorted(segments, key=lambda s: s.id)
