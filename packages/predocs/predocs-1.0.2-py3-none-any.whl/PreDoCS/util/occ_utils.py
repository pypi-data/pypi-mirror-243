"""
This module contains helping function for the work with OpenCASCADE.

.. codeauthor:: Daniel Hardt <daniel@daniel-hardt.de>
.. codeauthor:: Edgar Werthen <Edgar.Werthen@dlr.de>
"""
#   Copyright (c): 2023 Deutsches Zentrum fuer Luft- und Raumfahrt (DLR, German Aerospace Center) <www.dlr.de>. All rights reserved.
from PreDoCS.util.Logging import get_module_logger

log = get_module_logger(__name__)

try:
    from lightworks.cad.occ_utils import *

except ImportError:
    log.info('Modul lightworks.cad.occ_utils not found. Use PreDoCS OCC utils.')

    from typing import List, Union
    from random import random

    import numpy as np
    import pandas as pd
    from OCC.Core.Approx import Approx_Curve3d
    from OCC.Core.BRep import BRep_Tool
    from OCC.Core.BRepAdaptor import BRepAdaptor_HCompCurve, BRepAdaptor_CompCurve, BRepAdaptor_HCurve, BRepAdaptor_Curve, \
        BRepAdaptor_Surface
    from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Section
    from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeEdge, BRepBuilderAPI_Transform, \
        BRepBuilderAPI_MakeFace
    from OCC.Core.BRepFeat import BRepFeat_SplitShape
    from OCC.Core.BRepGProp import brepgprop_SurfaceProperties
    from OCC.Core.BRepLProp import BRepLProp_SLProps
    from OCC.Core.GCPnts import GCPnts_AbscissaPoint, GCPnts_AbscissaPoint_Length
    from OCC.Core.GProp import GProp_GProps
    from OCC.Core.Geom import Geom_Plane, Geom_Line
    from OCC.Core.GeomAPI import GeomAPI_ProjectPointOnCurve, GeomAPI_IntCS, GeomAPI_ProjectPointOnSurf
    from OCC.Core.GeomAbs import GeomAbs_C2, GeomAbs_C1, GeomAbs_C0
    from OCC.Core.GeomAdaptor import GeomAdaptor_Curve
    from OCC.Core.ShapeAnalysis import ShapeAnalysis_Surface
    from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_VERTEX, TopAbs_FACE, TopAbs_ShapeEnum
    from OCC.Core.TopExp import TopExp_Explorer
    from OCC.Core.TopoDS import topods, TopoDS_Face, TopoDS_Iterator, TopoDS_Shape, TopoDS_Shell, TopoDS_Compound, \
        TopoDS_Wire
    from OCC.Core.gp import gp_Vec, gp_Pln, gp_Pnt, gp_Dir
    from OCC.Display.OCCViewer import rgb_color as color

    from PreDoCS.util.vector import Vector


    def edge_from_points(start_point, end_point):
        """
        Returns a edge from two points.

        Parameters
        ----------
        start_point: Vector
            Start point.
        end_point: Vector
            End point.

        Returns
        -------
        OCC.TopoDS.TopoDS_Edge
            The edge.
        """
        return BRepBuilderAPI_MakeEdge(gp_Pnt(start_point.x, start_point.y, start_point.z if len(start_point) > 2 else 0),
                                       gp_Pnt(end_point.x, end_point.y, end_point.z if len(end_point) > 2 else 0)).Edge()


    def point_list_to_wire(point_list, closed_wire=False):
        """
        Returns a wire from a point list.

        Parameters
        ----------
        point_list: list(Vector)
            List of points. If the vectors are two elements in size, 0 is added as the z-element.
        closed_wire: bool (default: False)
            True for closed wire, False for open wire.

        Returns
        -------
        OCC.TopoDS.TopoDS_Wire
            The wire.
        """
        point_list = [Vector([p.x, p.y, 0]) if len(p) == 2 else p for p in point_list]
        builder = BRepBuilderAPI_MakeWire()
        for i_edge in range((len(point_list) - 1)):
            p1 = point_list[i_edge]
            p2 = point_list[i_edge + 1]
            builder.Add(edge_from_points(p1, p2))
        if closed_wire:
            builder.Add(edge_from_points(point_list[-1], point_list[0]))
        return builder.Wire()


    def plane_to_face(plane: gp_Pln) -> TopoDS_Face:
        """
        Converts a plane into a face.

        Parameters
        ----------
        plane: gp_Pln
            The plane.

        Returns
        -------
        TopoDS_Face
            Converted face from plane.
        """
        return BRepBuilderAPI_MakeFace(plane).Face()


    def get_intersection_wire(geometry1, geometry2):
        """
        Returns the intersection wire from the two geometries.

        Parameters
        ----------
        geometry1: OCC.TopoDS.TopoDS_Shape
            The first geometry.
        geometry2: OCC.TopoDS.TopoDS_Shape
            The second geometry.

        Returns
        -------
        OCC.TopoDS.TopoDS_Wire
            The intersection wire.
        """
        assert isinstance(geometry1, TopoDS_Shape)
        assert isinstance(geometry2, TopoDS_Shape) or isinstance(geometry2, gp_Pln)
        section = BRepAlgoAPI_Section(geometry1, geometry2, False)
        section.ComputePCurveOn1(True)
        section.Approximation(True)
        section.Build()

        intersection_shape = section.Shape()

        wire_builder = BRepBuilderAPI_MakeWire()
        edge_explorer = TopExp_Explorer(intersection_shape, TopAbs_EDGE)
        has_intersection = False
        while edge_explorer.More():
            has_intersection = True
            wire_builder.Add(topods.Edge(edge_explorer.Current()))
            edge_explorer.Next()

        if has_intersection:
            wire_builder.Build()
            if wire_builder.IsDone():
                return wire_builder.Wire()
            else:
                # # DEBUG
                # from OCC.Display.SimpleGui import init_display
                # from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
                # from OCC.Core.BRepTools import breptools_Write
                # from OCC.Display.OCCViewer import rgb_color as color
                #
                # display, start_display, add_menu, add_function_to_menu = init_display()
                # plane = BRepBuilderAPI_MakeFace(geometry2, -10, 10, -10, 10)
                # display.DisplayShape(geometry1, update=True, color=color(1, 0, 0))
                # display.DisplayShape(plane.Face(), update=True, color=color(0, 1, 0))
                # display.FitAll()
                # start_display()
                # display, start_display, add_menu, add_function_to_menu = init_display()
                # edge_explorer.ReInit()
                # i = 0
                # while edge_explorer.More():
                #     shape = edge_explorer.Current()
                #     breptools_Write(topods.Edge(shape), 'shape_{}.brep'.format(i))
                #     display.DisplayShape(shape, update=True)
                #     edge_explorer.Next()
                #     i += 1
                # display.FitAll()
                # start_display()
                raise RuntimeError('get_intersection_wire() BRepBuilderAPI_WireError {}'.format(wire_builder.Error()))
        else:
            return None


    def vertex_to_vector(vertex):
        """
        Converts an OpenCASCADE Vertex to a PreDoCS Vector.

        Parameters
        ----------
        vertex: OCC.TopoDS.TopoDS_Vertex
            The vertex.

        Returns
        -------
        Vector
            The vector.
        """
        return point_to_vector(BRep_Tool.Pnt(vertex))


    def point_to_vector(point):
        """
        Converts an OpenCASCADE Point to a PreDoCS Vector.

        Parameters
        ----------
        point: OCC.gp.gp_Pnt
            The point.

        Returns
        -------
        Vector
            The vector.
        """
        return Vector([point.X(), point.Y(), point.Z()])


    def vector_to_point(vector):
        """
        Converts a PreDoCS Vector to an OpenCASCADE Point.

        Parameters
        ----------
        vector: Vector
            The vector.

        Returns
        -------
        point: OCC.gp.gp_Pnt
            The point.
        """
        return gp_Pnt(vector.x, vector.y, vector.z)


    def vector_to_occ_vector(vector):
        """
        Converts a PreDoCS Vector to an OpenCASCADE Vector.

        Parameters
        ----------
        Vector
            The vector.

        Returns
        -------
        point: OCC.gp.gp_Vec
            The point.
        """
        return gp_Vec(vector.x, vector.y, vector.z)


    def get_intersection_points(geometry1, geometry2):
        """
        Returns the intersection points from the two geometries.

        Parameters
        ----------
        geometry1: OCC.TopoDS.TopoDS_Shape
            The first geometry.
        geometry2: OCC.TopoDS.TopoDS_Shape
            The second geometry.

        Returns
        -------
        list(Vector)
            The intersection points.
        """
        section = BRepAlgoAPI_Section(geometry1, geometry2, False)
        # section.ComputePCurveOn1(True)
        section.Approximation(True)
        section.Build()
        result_shape = section.Shape()
        return get_shape_vertices(result_shape)


    def get_shape_vertices(shape, with_boundary_vertices=True, only_forward: bool = False) -> List[Vector]:
        """
        Returns the vertices of the shape.

        Parameters
        ----------
        shape: OCC.TopoDS.TopoDS_Shape
            The shape.
        with_boundary_vertices: bool (default: True)
            False, if the first and the last vertices should be deleted.

        Returns
        -------
        list(Vector)
            The points.
        """
        vertex_explorer = TopExp_Explorer(shape, TopAbs_VERTEX)
        vertices = []
        is_wire = isinstance(shape, TopoDS_Wire)
        while vertex_explorer.More():
            # consider only vertices with Orientation TopAbs_FORWARD (=0)
            if not only_forward or (not vertex_explorer.Current().Orientation() or is_wire):
                vertices.append(topods.Vertex(vertex_explorer.Current()))
            vertex_explorer.Next()

        if not with_boundary_vertices:
            del vertices[0]
            del vertices[-1]

        return [vertex_to_vector(v) for v in vertices]


    def get_shape_vertices_forward(shape, with_boundary_vertices=True) -> List[Vector]:
        """
        Returns the vertices of the shape.

        Parameters
        ----------
        shape: OCC.TopoDS.TopoDS_Shape
            The shape.
        with_boundary_vertices: bool (default: True)
            False, if the first and the last vertices should be deleted.

        Returns
        -------
        list(Vector)
            The points.
        """
        return get_shape_vertices(shape, with_boundary_vertices=with_boundary_vertices, only_forward=True)


    def get_wire_boundary_points(wire):
        """
        Returns the boundary points of a wire.

        Parameters
        ----------
        wire: OCC.TopoDS.TopoDS_Wire
            The wire.

        Returns
        -------
        Vector
            The first boundary point.
        Vector
            The second boundary point.
        """
        vertices = get_shape_vertices(wire)
        return vertices[0], vertices[-1]


    def get_curve_boundary_points(curve):
        """
        Returns the boundary points of a curve.

        Parameters
        ----------
        curve: OCC.Geom.Geom_Curve
            The curve.

        Returns
        -------
        Vector
            The first boundary point.
        Vector
            The second boundary point.
        """
        return get_point_from_curve_parameter(curve, curve.FirstParameter()), \
               get_point_from_curve_parameter(curve, curve.LastParameter())


    def get_point_from_curve_parameter(curve, s):
        """
        Returns a point of a curve from the curve parameter.

        Parameters
        ----------
        curve: OCC.Geom.Geom_Curve
            The curve.
        s: float
            The curve parameter.

        Returns
        -------
        Vector
            The point.
        """
        point = curve.Value(s)
        return point_to_vector(point)


    def get_curve_parameter_from_point(curve, point):
        """
        Returns parameter of the curve for a given point.

        Parameters
        ----------
        curve: OCC.Geom.Geom_Curve
            The curve.
        point: Vector
            The point.

        Returns
        -------
        float
            The curve parameter from the point.
        """
        point_to_project = gp_Pnt(point.x, point.y, point.z)

        projection = GeomAPI_ProjectPointOnCurve(point_to_project, curve)
        if projection.NbPoints() > 0:
            distance = projection.LowerDistance()
            if distance > 1e-2:
                log.warning(f'Unsafe projection from point so curve, distance is {distance}.')
            parameter = projection.LowerDistanceParameter()
        else:
            raise RuntimeError('No projection of the point on the curve is found')

        return parameter


    def get_cc_from_point(curve, point):
        """
        Returns the contour coordinate of the curve for a given point.

        Parameters
        ----------
        curve: OCC.Geom.Geom_Curve
            The curve.
        point: Vector
            The point.

        Returns
        -------
        float
            The contour length from the point.
        """
        parameter = get_curve_parameter_from_point(curve, point)
        curve_adaptor = GeomAdaptor_Curve(curve)
        return GCPnts_AbscissaPoint_Length(
            curve_adaptor, curve_adaptor.FirstParameter(), parameter
        )


    def get_surface_parameters_from_point(surface, point):
        """
        Returns parameter of the curve for a given point.

        Parameters
        ----------
        surface: OCC.Geom.Geom_Surface
            The surface.
        point: Vector
            The point.

        Returns
        -------
        float, float
            The surface parameters of the point.
        """
        point_to_project = gp_Pnt(point.x, point.y, point.z)

        projection = GeomAPI_ProjectPointOnSurf(point_to_project, surface)
        if projection.NbPoints() > 0:
            # distance = projection.LowerDistance()
            # print(distance)
            parameters = projection.LowerDistanceParameters()
        else:
            raise RuntimeError('No projection of the point on the surface is found')

        return parameters


    def is_point_on_curve(curve, point, z_curve, position_blurring):
        """
        Returns parameter of the curve for a given point.

        Parameters
        ----------
        curve: OCC.Geom.Geom_Curve
            The curve.
        point: Vector
            The point.
        z_curve: float
            The z-coordinate of the curve.
        position_blurring: float
            The max distance from the point to the curve at which the point is considered as on the curve.

        Returns
        -------
        bool
            True, if the point is on the curve.
        """
        point_to_project = gp_Pnt(point.x, point.y, z_curve)

        projection = GeomAPI_ProjectPointOnCurve(point_to_project, curve)
        if projection.NbPoints() > 0:
            if projection.LowerDistance() <= position_blurring:
                return True
            else:
                return False
        else:
            return False


    def is_point_on_plane(point: Vector, plane: gp_Pln, position_blurring: float) -> bool:
        """
        Checks if the given point is on the given plane considering the position blurring.

        Parameters
        ----------
        point: Vector
            The point.
        plane: gp_Pln
            The plane.
        position_blurring: float
            The max distance from the point to the plane at which the point is considered as on the curve.

        Returns
        -------
        bool:
            True, if the point is on the plane.
        """
        point = gp_Pnt(point.x, point.y, point.z)
        dist = plane.Distance(point)
        if dist < position_blurring:
            return True
        return False


    def transform_shape(shape, transformation):
        """
        Transforms a shape.

        Parameters
        ----------
        shape: OCC.TopoDS.TopoDS_Shape
            The shape to transform.
        transformation: OCC.gp.gp_Trsf
            Transformation to perform.

        Returns
        -------
        OCC.TopoDS.TopoDS_Shape
            The transformed shape.
        """
        return BRepBuilderAPI_Transform(shape, transformation).Shape()


    def transform_wire(shape, transformation):
        """
        Transforms a wire.

        Parameters
        ----------
        shape: OCC.TopoDS.TopoDS_Shape
            The shape to transform.
        transformation: OCC.gp.gp_Trsf
            Transformation to perform.

        Returns
        -------
        OCC.TopoDS.TopoDS_Wire
            The transformed wire.
        """
        return topods.Wire(transform_shape(shape, transformation))


    def line_plane_intersection(line_origin, line_direction, plane_origin, plane_normal):
        """
        Find the intersection point of a line and a plane in 3D space.

        The line is described by its origin and a direction vector. The plane is described by its origin and a normal vector

        Parameters
        ----------
        line_origin: Vector
            Origin of the line.
        line_direction: Vector
            Direction of the line
        plane_origin: Vector
            Origin of the plane
        plane_normal: Vector
            Normal of the plane
        Returns
        -------
        intersection_point: Vector
            The intersection of line and Plane
        """
        # Transform into OCC objects
        line_origin = gp_Pnt(line_origin.x, line_origin.y, line_origin.z)
        line_direction = gp_Dir(line_direction.x, line_direction.y, line_direction.z)
        line = Geom_Line(line_origin, line_direction)

        plane_origin = gp_Pnt(plane_origin.x, plane_origin.y, plane_origin.z)
        plane_normal = gp_Dir(plane_normal.x, plane_normal.y, plane_normal.z)
        plane = Geom_Plane(plane_origin, plane_normal)

        # Calculate intersection point
        intersection_point = GeomAPI_IntCS(line, plane)

        # Check for successful calculation
        if not intersection_point.IsDone():
            log.warning('No intersection found')

        intersection_point = intersection_point.Point(1)

        # Transform OCC point object into vector object
        intersection_point = point_to_vector(intersection_point)

        return intersection_point


    def is_curve_clockwise(curve, ref_point):
        """
        Returns if a curve is clockwise or counter-clockwise relative to a given point.

        Parameters
        ----------
        curve: OCC.Geom.Geom_Curve
            The curve.
        ref_point: Vector
            The reference point.

        Returns
        -------
        bool
            True, if the curve is clockwise; False, if the curve is counter-clockwise.
        """
        middle_parameter = (curve.LastParameter() - curve.FirstParameter()) / 2 + curve.FirstParameter()
        P = gp_Pnt()
        V1 = gp_Vec()
        curve.D1(middle_parameter, P, V1)
        cross_product = np.cross(point_to_vector(P) - ref_point, point_to_vector(V1))

        if cross_product[2] > 0:
            return False
        elif cross_product[2] < 0:
            return True
        else:
            raise RuntimeError('Can not calculate clockwise of the curve.')


    class WireToCurveParameters(object):
        """
        This class stores the parameters for the conversion of a wire into a b-spline curve.

        Attributes
        ----------
        tolerance: float (default: 1e-7)
            3D tolerance.
        continuity: int (default: 2)
            Continuity of the curve, has to be 0, 1 or 2.
        max_segments: int (default: 200)
            Maximum b-spline segments.
        max_degrees: int (default: 12)
            Maximum b-spline degrees. Has to be lower or equal 25.
        """

        def __init__(self):
            self.tolerance = 1e-7
            self.continuity = 2
            self.max_segments = 200
            self.max_degrees = 12


    # def create_curve_from_curve_adaptor(curve_adaptor, wire_to_curve_parameters=WireToCurveParameters()):
    #     """
    #         Returns if a approximated curve (b-spline) from a wire.
    #
    #         Parameters
    #         ----------
    #         curve_adaptor: OCC.Adaptor3d.Adaptor3d_Curve
    #             The curve adaptor.
    #         wire_to_curve_parameters: WireToCurveParameters
    #             The wire to curve parameters.
    #
    #         Returns
    #         -------
    #         OCC.Geom.Geom_Curve
    #             The curve.
    #     """
    #     log.warning('create_curve_from_curve_adaptor should be avoided, rather use the curve direct.'
    #                 '')
    #     # Approximate curve from curve adaptor
    #     continuity = GeomAbs_C0
    #     if wire_to_curve_parameters.continuity == 1:
    #         continuity = GeomAbs_C1
    #     elif wire_to_curve_parameters.continuity == 2:
    #         continuity = GeomAbs_C2
    #     approx = Approx_Curve3d(curve_adaptor, wire_to_curve_parameters.tolerance,
    #                             continuity,
    #                             wire_to_curve_parameters.max_segments,
    #                             wire_to_curve_parameters.max_degrees)
    #
    #     if approx.IsDone() and approx.HasResult():
    #         return approx.Curve()
    #     else:
    #         raise RuntimeError('Curve adaptor can not approximated by a curve')


    def create_curve_from_wire(wire, wire_to_curve_parameters=WireToCurveParameters()):
        """
            Returns if a approximated curve (b-spline) from a wire.

            Parameters
            ----------
            wire: OCC.TopoDS.TopoDS_Wire
                The wire.
            wire_to_curve_parameters: WireToCurveParameters
                The wire to curve parameters.

            Returns
            -------
            OCC.Geom.Geom_Curve
                The curve.
        """
        # Approximate curve from wire
        curve_adaptor = BRepAdaptor_HCompCurve(BRepAdaptor_CompCurve(wire))
        continuity = GeomAbs_C0
        if wire_to_curve_parameters.continuity == 1:
            continuity = GeomAbs_C1
        elif wire_to_curve_parameters.continuity == 2:
            continuity = GeomAbs_C2
        approx = Approx_Curve3d(curve_adaptor, wire_to_curve_parameters.tolerance,
                                continuity,
                                wire_to_curve_parameters.max_segments,
                                wire_to_curve_parameters.max_degrees)

        if approx.IsDone() and approx.HasResult():
            return approx.Curve()
        else:
            raise RuntimeError('Wire can not approximated by a curve')


    def create_curve_from_edge(edge, wire_to_curve_parameters=WireToCurveParameters()):
        """
            Returns if a approximated curve (b-spline) from a wire.

            Parameters
            ----------
            edge: OCC.TopoDS.TopoDS_Edge
                The edge.
            wire_to_curve_parameters: WireToCurveParameters
                The wire to curve parameters.

            Returns
            -------
            OCC.Geom.Geom_Curve
                The curve.
        """
        # Approximate curve from wire
        curve_adaptor = BRepAdaptor_HCurve(BRepAdaptor_Curve(edge))
        continuity = GeomAbs_C0
        if wire_to_curve_parameters.continuity == 1:
            continuity = GeomAbs_C1
        elif wire_to_curve_parameters.continuity == 2:
            continuity = GeomAbs_C2
        approx = Approx_Curve3d(curve_adaptor, wire_to_curve_parameters.tolerance,
                                continuity,
                                wire_to_curve_parameters.max_segments,
                                wire_to_curve_parameters.max_degrees)

        if approx.IsDone() and approx.HasResult():
            return approx.Curve()
        else:
            raise RuntimeError('Edge can not approximated by a curve')


    def get_shell_area(shell):
        """
        Calculates the area of a shell.

        Parameters
        ----------
        shell: OCC.TopoDS.TopoDS_Shell
            The shell.

        Returns
        -------
        float
            The area of the shell.
        """
        surface_properties = GProp_GProps()
        brepgprop_SurfaceProperties(shell, surface_properties)
        return surface_properties.Mass()


    def calc_cross_section_plane(beam_reference_point, beam_reference_axis, z_cross_section):
        """
        Calculates a cross section plane from the given parameters.

        Parameters
        ----------
        beam_reference_point: Vector
            The reference point of the beam at x_beam = y_beam = z_beam = 0.
        beam_reference_axis: Vector
            The beam reference axis from the beam reference point.
        z_cross_section: float
            The spanwise position where to create the cross section plane. z_beam starts at the beam
            reference point and is orientated in the beam reference axis direction.

        Returns
        -------
        Occ.gp.gp_Pln
            The cross section plane.
        """
        cs_point = beam_reference_point + z_cross_section * beam_reference_axis
        reference_dir = gp_Dir(beam_reference_axis.x, beam_reference_axis.y, beam_reference_axis.z)
        return gp_Pln(gp_Pnt(cs_point.x, cs_point.y, cs_point.z), reference_dir)


    def get_shape_side_lengths(face: TopoDS_Face) -> List[float]:
        """
        Get side length of all sides of the given face.

        Parameters
        ----------
        face: TopoDS_Face
            The face.

        Returns
        -------
        List[float]:
            List of all side lengths of the face.
        """
        side_length = list()
        wire = TopoDS_Iterator(face).Value()
        edges = TopoDS_Iterator(wire)

        while edges.More():
            curve_adapt = BRepAdaptor_Curve(edges.Value())
            side_length.append(GCPnts_AbscissaPoint().Length(curve_adapt, curve_adapt.FirstParameter(),
                                                             curve_adapt.LastParameter(), 1e-6))
            edges.Next()
        return side_length


    def split_face_with_wire(face: TopoDS_Face, wire: TopoDS_Wire) -> List[TopoDS_Shape]:
        """
        Splits the given face into two shapes, seperated by the given wire.

        Parameters
        ----------
        face: TopoDS_Face
            The face.
        wire: TopoDS_Wire
            The wire which splits the face into two shapes.

        Returns
        -------
        List[TopoDS_Shape]:
            List of split shapes from face
        """
        split = BRepFeat_SplitShape(face)
        split.Add(wire, face)
        split.Build()

        return [split.Modified(face).First(), split.Modified(face).Last()]


    def get_normal_on_face(face: TopoDS_Face) -> gp_Dir:
        """
        Gets the normal vector of the given face.

        Parameters
        ----------
        face: TopoDS_Face
            The face.

        Returns
        -------
        gp_Dir:
            Direction of the normal vector.
        """
        adapt = BRepAdaptor_Surface(face)
        geom_face = BRep_Tool.Surface(face)
        uv = ShapeAnalysis_Surface(geom_face).ValueOfUV(get_shell_mid_point(face), 0.01).Coord()
        prop = BRepLProp_SLProps(adapt, uv[0], uv[1], 1, 1.e-3)
        return prop.Normal()


    def get_shell_mid_point(shell: Union[TopoDS_Shell, TopoDS_Compound, TopoDS_Face, TopoDS_Shape]) -> gp_Pnt:
        """
        Gets the coordinates of the midpoint of the given face, shape, shell or compound.

        Parameters
        ----------
        shell: Union[TopoDS_Shell, TopoDS_Compound, TopoDS_Face, TopoDS_Shape]
            Shell, Compound, Face or Shape

        Returns
        -------
        gp_Pnt:
            Midpoint.
        """
        prop = GProp_GProps()
        brepgprop_SurfaceProperties(shell, prop)
        return prop.CentreOfMass()


    def get_shapes_of_type(root_shape, TopAbs_Type: TopAbs_ShapeEnum, TopoDS_class) -> List[TopoDS_Shape]:
        shapes = []
        it = TopExp_Explorer(root_shape, TopAbs_Type)
        while it.More():
            shape = it.Value()
            assert isinstance(shape, TopoDS_class)
            shapes.append(shape)
            it.Next()
        return shapes


    def get_faces_from_shell(shell: Union[TopoDS_Shell, TopoDS_Compound, TopoDS_Shape]) -> List[TopoDS_Face]:
        """
        Gets all the faces from the given shell, compound or shape.

        Parameters
        ----------
        shell: Union[TopoDS_Shell, TopoDS_Compound, TopoDS_Shape]
            Shell, Compound or shape.

        Returns
        -------
        List[TopoDS_Face]:
            List of faces within the given shell.
        """
        if isinstance(shell, TopoDS_Face):
            return [shell]
        else:
            return get_shapes_of_type(shell, TopAbs_FACE, TopoDS_Face)


    def calc_cross_section_wires(component_segment, y_cross_section):
        """
        Calc the cross section wires from the intersection of a plane with a component segment.

        Parameters
        ----------
        component_segment: ComponentSegment
            The component segement.
        y_cross_section: float
            The y-coordinate of the cross section plane (the cross section plane is perpendicular to the y-axis).

        Returns
        -------
        upper_wire: OCC.TopoDS.TopoDS_Wire
            The wire of the upper shell of the component segment.
            Wire direction is from the TE to the LE.
        lower_wire: OCC.TopoDS.TopoDS_Wire
            The wire of the lower shell of the component segment.
            Wire direction is from LE to the lower TE.
        """
        cross_section_plane = calc_cross_section_plane(Vector([0, 0, 0]), Vector([0, 1, 0]),
                                                       y_cross_section)

        upper_shape = component_segment._tigl_object.get_upper_shape().shape()
        lower_shape = component_segment._tigl_object.get_lower_shape().shape()

        upper_wire = get_intersection_wire(upper_shape, cross_section_plane)
        if upper_wire is None:
            raise RuntimeError(
                'No intersection from the shell and the cross section plane for z={}.'.format(y_cross_section))
        lower_wire = get_intersection_wire(lower_shape, cross_section_plane)
        if lower_wire is None:
            raise RuntimeError(
                'No intersection from the shell and the cross section plane for z={}.'.format(y_cross_section))

        return upper_wire, lower_wire


    def calc_cross_section_geometries(component_segment, y_cross_section):
        """
        Calc the cross section geometries (wires, curves, curve adaptors and lengths) from the intersection of a plane
        with a component segment.

        Parameters
        ----------
        component_segment: ComponentSegment
            The component segement.
        y_cross_section: float
            The y-coordinate of the cross section plane (the cross section plane is perpendicular to the y-axis).

        Returns
        -------
        upper_wire: OCC.TopoDS.TopoDS_Wire
            The wire of the upper shell of the component segment.
            Wire direction is from the TE to the LE.
        lower_wire: OCC.TopoDS.TopoDS_Wire
            The wire of the lower shell of the component segment.
            Wire direction is from LE to the lower TE.
        upper_curve: OCC.Geom.Geom_Curve
            The curve of the upper shell of the component segment.
            Curve direction is from the TE to the LE.
        lower_curve: OCC.Geom.Geom_Curve
            The curve of the lower shell of the component segment.
            Curve direction is from LE to the lower TE.
        upper_curve_adaptor: OCC.Core.Adaptor3d.Adaptor3d_Curve
            The curve adaptors of the upper shell of the component segment.
            Curve direction is from the TE to the LE.
        lower_curve_adaptor: OCC.Core.Adaptor3d.Adaptor3d_Curve
            The curve adaptors of the lower shell of the component segment.
            Curve direction is from LE to the lower TE.
        upper_length: float
            Length of the upper curve.
        lower_length: float
            Length of the lower curve.
        length: float
            Total length of the upper and lower curve.
        """
        upper_wire, lower_wire = calc_cross_section_wires(component_segment, y_cross_section)

        # start_point, end_point = get_wire_boundary_points(upper_wire)
        # if start_point.x < end_point.x:
        #     log.debug('Upper wire reversed')
        #     upper_wire.Reverse()
        #
        # start_point, end_point = get_wire_boundary_points(lower_wire)
        # if start_point.x > end_point.x:
        #     log.debug('Lower wire reversed')
        #     lower_wire.Reverse()

        upper_curve = create_curve_from_wire(upper_wire)
        lower_curve = create_curve_from_wire(lower_wire)

        upper_curve_adaptor = BRepAdaptor_CompCurve(upper_wire)
        lower_curve_adaptor = BRepAdaptor_CompCurve(lower_wire)

        assert upper_curve_adaptor.Value(upper_curve_adaptor.FirstParameter()).X() > \
               upper_curve_adaptor.Value(
                   upper_curve_adaptor.LastParameter()).X(), 'Upper curve has to be from the TE to the LE'
        assert lower_curve_adaptor.Value(lower_curve_adaptor.FirstParameter()).X() < \
               lower_curve_adaptor.Value(
                   lower_curve_adaptor.LastParameter()).X(), 'Lower curve has to be from the LE to the TE'

        upper_length = GCPnts_AbscissaPoint_Length(upper_curve_adaptor)
        lower_length = GCPnts_AbscissaPoint_Length(lower_curve_adaptor)
        length = upper_length + lower_length

        return upper_wire, lower_wire, upper_curve, lower_curve, upper_curve_adaptor, lower_curve_adaptor, \
               upper_length, lower_length, length


    def get_point_from_cc(curve_adaptor, cc):
        """
        Gets a point from a curve adaptor by its contour coordinate.

        Parameters
        ----------
        curve_adaptor: OCC.Core.Adaptor3d.Adaptor3d_Curve
            The curve adaptor.
        cc: float
            The contour coordinate of the point.

        Returns
        -------
        Vector
            The point.
        """
        abscissa_point = GCPnts_AbscissaPoint(curve_adaptor, cc, curve_adaptor.FirstParameter())
        if abscissa_point.IsDone():
            return point_to_vector(curve_adaptor.Value(abscissa_point.Parameter()))
        else:
            raise RuntimeError()


    def split_layup_upper_lower(layup, upper_curve_adaptor, lower_curve_adaptor):
        """
        Split a given layup in a layup for the upper and lower shell.

        Parameters
        ----------
        layup: pandas.DataFrame
            The layup as DataFrame. At least the coulums 's_start' and 's_end' are required.
        upper_curve_adaptor: OCC.Core.Adaptor3d.Adaptor3d_Curve
            The curve adaptors of the upper shell of the component segment.
            Curve direction is from the TE to the LE.
        lower_curve_adaptor: OCC.Core.Adaptor3d.Adaptor3d_Curve
            The curve adaptors of the lower shell of the component segment.
            Curve direction is from LE to the lower TE.

        Returns
        -------
        upper_layup: pandas.DataFrame
            The layup of the upper shell.
        lower_layup: pandas.DataFrame
            The layup of the lower shell.
        """
        upper_length = GCPnts_AbscissaPoint_Length(upper_curve_adaptor)
        lower_length = GCPnts_AbscissaPoint_Length(lower_curve_adaptor)
        length = upper_length + lower_length

        upper_lower_split = upper_length / length
        log.debug(f'upper_lower_split: {upper_lower_split}')

        upper_layup_list = []
        lower_layup_list = []
        for i, row in layup.iterrows():
            if not row['s_start'] == row['s_end']:
                log.debug(f"'{row['layer_name']}': row['s_start'] < row['s_end']: {row['s_start']} < {row['s_end']}")
                if row['s_start'] < row['s_end']:
                    log.debug('normal')
                    # Normal definition
                    if row['s_start'] <= upper_lower_split and row['s_end'] <= upper_lower_split:
                        # Only upper
                        # print('normal append')
                        upper_layup_list.append(row)
                    if row['s_start'] >= upper_lower_split and row['s_end'] >= upper_lower_split:
                        # Only lower
                        # print('normal append')
                        lower_layup_list.append(row)
                    if row['s_start'] < upper_lower_split and row['s_end'] > upper_lower_split:
                        # Upper and lower
                        # print('normal append')
                        upper_row = row.copy()
                        upper_row['s_end'] = upper_lower_split
                        lower_row = row.copy()
                        lower_row['s_start'] = upper_lower_split
                        upper_layup_list.append(upper_row)
                        lower_layup_list.append(lower_row)
                else:
                    # "Around the TE" definition
                    if row['s_start'] > upper_lower_split and row['s_end'] < upper_lower_split:
                        # Both points on different sides
                        upper_row = row.copy()
                        upper_row['s_start'] = 0
                        lower_row = row.copy()
                        lower_row['s_end'] = 1
                        upper_layup_list.append(upper_row)
                        lower_layup_list.append(lower_row)
                    if row['s_start'] < upper_lower_split and row['s_end'] < upper_lower_split:
                        # Both points on upper side
                        upper_row1 = row.copy()
                        upper_row1['s_start'] = 0
                        upper_row2 = row.copy()
                        upper_row2['s_end'] = upper_lower_split
                        lower_row = row.copy()
                        lower_row['s_start'] = upper_lower_split
                        lower_row['s_end'] = 1
                        upper_layup_list.append(upper_row1)
                        upper_layup_list.append(upper_row2)
                        lower_layup_list.append(lower_row)
                    if row['s_start'] > upper_lower_split and row['s_end'] > upper_lower_split:
                        # Both points on lower side
                        upper_row = row.copy()
                        upper_row['s_start'] = 0
                        upper_row['s_end'] = upper_lower_split
                        lower_row1 = row.copy()
                        lower_row1['s_start'] = upper_lower_split
                        lower_row2 = row.copy()
                        lower_row2['s_end'] = 1
                        upper_layup_list.append(upper_row)
                        lower_layup_list.append(lower_row1)
                        lower_layup_list.append(lower_row2)

        upper_layup = pd.DataFrame(upper_layup_list)
        lower_layup = pd.DataFrame(lower_layup_list)

        return upper_layup, lower_layup


    def get_cpacs_surface_parameter_from_point(point, segments, side_string):
        """
        Returns the chordwise surface parameter of a given point.

        Parameters
        ----------
        point: Vector
            The point.
        segments: list(tigl3.configuration.CCPACSWingSegment)
            A list of all segments of the wing.
        side_string: str
            Name of the shell side, where point is located ('upper' or 'lower').

        Returns
        -------
        float
            Chordwise surface parameter (0 --> LE; 1 --> TE).
        """
        surface = None
        for segment in segments:
            if segment.get_is_on(vector_to_point(point)):
                if side_string == 'upper':
                    surface = segment.get_upper_surface()
                elif side_string == 'lower':
                    surface = segment.get_lower_surface()
                else:
                    raise RuntimeError(f'side_string "{side_string}" not valid')
                break
        if surface is None:
            raise RuntimeError('Point not on any segment')
        bounds = surface.Bounds()
        bound_u1, bound_u2, bound_v1, bound_v2 = bounds
        su_raw, sv_raw = get_surface_parameters_from_point(surface, point)
        su = (su_raw - bound_u1) / (bound_u2 - bound_u1)
        if side_string == 'upper':
            return su
        elif side_string == 'lower':
            return 1 - su
        else:
            raise RuntimeError(f'side_string "{side_string}" not valid')


    def get_IEA_contour_coordinate_from_shell_coordinate(s_norm, side_string, upper_curve_adaptor, lower_curve_adaptor):
        """
        Gets the IEA contour coordinate (0 --> upper side TE; 1 --> lower side TE) from
        a shell contour coordinate (0 --> upper side TE, 1 --> LE; 0 --> LE, 1 --> lower side TE).

        Parameters
        ----------
        s_norm: float
            The normalised contour coordinate. For the definition see shell_coordinate_definition.
        side_string: str
            Name of the shell side, where to add the cells ('upper' or 'lower').
        upper_curve_adaptor: OCC.Adaptor3d.Adaptor3d_Curve
            Adaptor of the upper shell curve.
        lower_curve_adaptor: OCC.Adaptor3d.Adaptor3d_Curve
            Adaptor of the lower shell curve.

        Returns
        -------
        float
            The IEA contour coordinate (0 --> upper side TE; 1 --> lower side TE).
        """
        tolerance = 1e-5

        upper_length = GCPnts_AbscissaPoint_Length(upper_curve_adaptor)
        lower_length = GCPnts_AbscissaPoint_Length(lower_curve_adaptor)
        length = upper_length + lower_length

        assert 0 <= s_norm <= 1 + tolerance, f's_norm {s_norm} not between 0 and 1'

        if s_norm > 1:
            s_norm = 1

        if side_string == 'upper':
            # upper shell
            s = s_norm * upper_length
        elif side_string == 'lower':
            # lower shell
            s = s_norm * lower_length + upper_length
        else:
            raise RuntimeError(f'side_string "{side_string}" not valid')

        return s / length


    def get_contour_coordinate_from_shell_coordinate(s_norm, side_string, upper_curve_adaptor, lower_curve_adaptor,
                                                     shell_coordinate_definition, tol=1e-3):
        """
        Gets the contour coordinate for the CPACS file (0 --> LE; 1 --> TE) from a shell contour coordinate.

        Parameters
        ----------
        s_norm: float
            The normalised contour coordinate. For the definition see shell_coordinate_definition.
        side_string: str
            Name of the shell side, where to add the cells ('upper' or 'lower').
        upper_curve_adaptor: OCC.Adaptor3d.Adaptor3d_Curve
            Adaptor of the upper shell curve.
        lower_curve_adaptor: OCC.Adaptor3d.Adaptor3d_Curve
            Adaptor of the lower shell curve.
        shell_coordinate_definition: str
            Name of the contour coordinate definition of the wing:
            'IEA': 0 --> upper side TE; 1 --> lower side TE
            'CPACS': -1 --> upper side TE; 0 --> LE; 1 --> lower side TE
        tol: float (default: 1e-3)
            Tolerance for the 'mid' side output at the LE.

        Returns
        -------
        float
            The contour coordinate for the CPACS file (0 --> LE; 1 --> TE).
        """
        upper_length = GCPnts_AbscissaPoint_Length(upper_curve_adaptor)
        lower_length = GCPnts_AbscissaPoint_Length(lower_curve_adaptor)
        length = upper_length + lower_length

        if shell_coordinate_definition == 'CPACS':
            if side_string == 'upper':
                # upper shell
                assert -1 <= s_norm < 0 + tol, f's_norm {s_norm} not on upper side'
                return max(0, -s_norm)
            elif side_string == 'lower':
                # lower shell
                assert 0 - tol <= s_norm <= 1, f's_norm {s_norm} not on lower side'
                return max(0, s_norm)
            else:
                raise RuntimeError(f'side_string "{side_string}" not valid')
        elif shell_coordinate_definition == 'IEA':
            s = s_norm * length
            if side_string == 'upper':
                # upper shell
                assert 0 <= s < upper_length + tol * length, f's_norm {s_norm} not on upper side'
                return max(0, 1 - s / upper_length)
            elif side_string == 'lower':
                # lower shell
                assert upper_length - tol * length <= s <= length, f's_norm {s_norm} not on lower side'
                return max(0, (s - upper_length) / lower_length)
            else:
                raise RuntimeError(f'side_string "{side_string}" not valid')
        else:
            raise RuntimeError(f'shell_coordinate_definition "{shell_coordinate_definition}" not valid.')


    def get_eta_xsi_from_shell_coordinate(s_norm, side_string, component_segment, upper_curve_adaptor, lower_curve_adaptor,
                                          shell_coordinate_definition, tol=1e-3, projection_direction=None):
        """
        Gets a point from a shell contour coordinate.

        Parameters
        ----------
        s_norm: float
            The normalised contour coordinate. For the definition see shell_coordinate_definition.
        side_string: str
            Name of the shell side, where to add the cells ('upper' or 'lower').
        component_segment: ComponentSegment
            Lightworks component segment.
        upper_curve_adaptor: OCC.Adaptor3d.Adaptor3d_Curve
            Adaptor of the upper shell curve.
        lower_curve_adaptor: OCC.Adaptor3d.Adaptor3d_Curve
            Adaptor of the lower shell curve.
        shell_coordinate_definition: str
            Name of the contour coordinate definition of the wing:
            'IEA': 0 --> upper side TE; 1 --> lower side TE
            'CPACS': -1 --> upper side TE; 0 --> LE; 1 --> lower side TE
        tol: float (default: 1e-3)
            Tolerance for the 'mid' side output at the LE.
        projection_direction: Vector (default: Vector([0, 0, 1]))
            The direction in which the points from the contur are projected on the chord face.

        Returns
        -------
        float
            The eta coordinate.
        float
            The xsi coordinate.
        """
        upper_length = GCPnts_AbscissaPoint_Length(upper_curve_adaptor)
        lower_length = GCPnts_AbscissaPoint_Length(lower_curve_adaptor)
        length = upper_length + lower_length

        if shell_coordinate_definition == 'CPACS':
            if side_string == 'upper':
                # upper shell
                assert -1 <= s_norm < 0 + tol, f's_norm {s_norm} not on upper side'
                point = get_point_from_cc(upper_curve_adaptor, min(upper_length, (s_norm + 1)) * upper_length)
            elif side_string == 'lower':
                # lower shell
                assert 0 - tol <= s_norm <= 1, f's_norm {s_norm} not on lower side'
                point = get_point_from_cc(lower_curve_adaptor, max(0, s_norm) * lower_length)
            else:
                raise RuntimeError(f'side_string "{side_string}" not valid')
        elif shell_coordinate_definition == 'IEA':
            s = s_norm * length
            if side_string == 'upper':
                # upper shell
                assert 0 <= s < upper_length + tol * length, f's_norm {s_norm} not on upper side'
                point = get_point_from_cc(upper_curve_adaptor, min(upper_length, s))
            elif side_string == 'lower':
                # lower shell
                assert upper_length - tol * length <= s <= length, f's_norm {s_norm} not on lower side'
                point = get_point_from_cc(lower_curve_adaptor, max(0, s - upper_length))
            else:
                raise RuntimeError(f'side_string "{side_string}" not valid')
        else:
            raise RuntimeError(f'shell_coordinate_definition "{shell_coordinate_definition}" not valid.')

        log.debug(f'side, point: {side_string} {point}')
        if projection_direction is None:
            occ_point = gp_Pnt(point.x, point.y, point.z)
            eta, xsi = component_segment._tigl_object.get_eta_xsi(occ_point)
        else:
            eta, xsi = get_eta_xsi_with_projection_direction(component_segment, point, projection_direction)
        log.debug(f'eta, xsi: {eta} {xsi}')

        return eta, xsi


    def get_eta_xsi_with_projection_direction(component_segment, point, projection_direction):
        """
        Projects a point along a direction to the chord face of a component segment and returns the eta-xsi position.

        Parameters
        ----------
        component_segment
            The component segment.
        point: Vector
            The point.
        projection_direction: Vector
            The projection direction.

        Returns
        -------
        float
            The eta position of the projected point.
        float
            The xsi position of the projected point.
        """
        chord_face = component_segment._tigl_object.get_chordface().get_surface()
        projection_line = Geom_Line(gp_Pnt(point.x, point.y, point.z),
                                    gp_Dir(projection_direction.x, projection_direction.y, projection_direction.z))

        cs_intersection = GeomAPI_IntCS(projection_line, chord_face)
        num_intersections = cs_intersection.NbPoints()
        if num_intersections == 1:
            point_on_chord = cs_intersection.Point(1)
            return component_segment._tigl_object.get_eta_xsi(point_on_chord)
        else:
            raise RuntimeError(f'{num_intersections} intersections with the chord face, not one.')


    def get_layup_at_spanwise_position(layers, eta, with_positioning=False):
        """
        Returns the layup at a given relative spanwise position.

        Parameters
        ----------
        layers: list(Layer)
            The layers.
        eta: float
            Relative spanwise position (0 .. 1).
        with_positioning: bool (default: False)
            If True, the positioning arguments ae incuded in the result.

        Returns
        -------
        list(dict)
            The layup at the given position.
        """
        # print(eta)
        result = []
        for layer in layers:
            if layer.spanwise_borders[0] <= eta <= layer.spanwise_borders[1]:
                layer_dict = {
                    # 'layer': layer,
                    'layer_name': layer.name,
                    'material': layer.material.name,
                    'thickness': float(layer.thickness(eta)),
                    'fiber_direction': float(layer.fibre_orientation(eta))
                }
                if with_positioning:
                    # layer_dict['layer_positioning'] = layer.layer_positioning
                    layer_dict['layer_positioning'] = layer.layer_positioning
                    layer_dict['positioning_arguments'] = layer.positioning_arguments.copy()
                    layer_dict['s_start'] = None
                    layer_dict['s_end'] = None
                result.append(layer_dict)
        # df.thickness.clip(lower=0)
        return result


    def get_cc_from_wire_plane_intersection(wire, cut_plane):
        """
        Returns the curve parameter from the intersection of a wire with a plane.

        Parameters
        ----------
        wire: OCC.TopoDS.TopoDS_Wire
            The wire.
        cut_plane: OCC.Core.gp.gp_Pln
            The cut plane.

        Returns
        -------
        float
            The curve parameter of the intersection.
        """
        cut_points = get_intersection_points(wire, cut_plane)
        assert (len(cut_points) == 1)
        cut_point = cut_points[0]

        curve = create_curve_from_wire(wire)

        return get_cc_from_point(curve, cut_point)


    def get_spar_cell_positions(y_spar_start, y_spar_end, later_analysis_positions_nodes):
        """
        Get the spar cell positions with respect to the later analysis positions of a wing.

        Parameters
        ----------
        y_spar_start: float
            Spanwise position where the spar starts.
        y_spar_end: float
            Spanwise position where the spar ends.
        later_analysis_positions_nodes: list(float)
            Spanwise positions where the analysis is performed.

        Returns
        -------
        numpy.array
            The spanwise positions of the spar cell nodes.
        """
        y_spar_cell_positions = list(
            later_analysis_positions_nodes[np.logical_and(later_analysis_positions_nodes >= y_spar_start,
                                                          later_analysis_positions_nodes <= y_spar_end)])
        if y_spar_start not in y_spar_cell_positions:
            y_spar_cell_positions.insert(0, y_spar_start)
        if y_spar_end not in y_spar_cell_positions:
            y_spar_cell_positions.append(y_spar_end)
        return np.array(y_spar_cell_positions)


    def split_faces(face: Union[TopoDS_Face, TopoDS_Shape],
                    wires: List[TopoDS_Wire],
                    new_faces: List[TopoDS_Face] = None) -> List[TopoDS_Face]:
        """
        Splits the given face into multiple faces each seperated by a wire. The number of returned faces is one higher
        than the number of wires.

        Parameters
        ----------
        face: TopoDS_Face
            Base face.
        wires: List[TopoDS_Wire]
            List of wires which are used to split the base face.
        new_faces: List[TopoDS_Face]
            List of faces. When calling this method, keep this parameter None.

        Returns
        -------
        List[TopoDS_Face]:
            List of split faces.
        """
        wires = wires.copy()
        if new_faces is None:
            new_faces = list()
        if len(wires) and get_intersection_wire(face, wires[0]) is not None:
            tmp_faces = split_face_with_wire(face, wires[0])
            wires.pop(0)
            for face in tmp_faces:
                split_faces(face, wires, new_faces)
        else:
            if face not in new_faces:
                new_faces.append(face)
        return new_faces


    def get_shape_surface_area(shape: TopoDS_Shape) -> float:
        """
        Calculates the area of a shape instance

        Parameters
        ----------
        shape

        Returns
        -------
        float
            the area
        """
        props = GProp_GProps()
        brepgprop_SurfaceProperties(shape, props)
        return props.Mass()


    def get_normal_from_shape(shape: TopoDS_Shape) -> np.ndarray:
        faces = get_faces_from_shell(shape)
        assert len(faces) > 0, 'No faces found for shape.'
        face = faces[0]
        assert isinstance(face, TopoDS_Face)
        return np.asarray(get_normal_on_face(face).Coord())


    # def project_vector_on_surface(surface: TopoDS_Shape, vector: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    #     """
    #     Projects a given vector onto a surface using its normal vector.
    #     Parameters
    #     ----------
    #     surface: TopoDS_Shape
    #         The surface.
    #     vector: np.ndarray
    #         The vector.
    #
    #     Returns
    #     -------
    #     np.ndarray:
    #         The vector projected onto the surface.
    #     """
    #     normal = get_normal_from_shape(surface)
    #     return np.cross(normal, np.cross(vector, normal)), normal


    # def get_buckling_length(surface: TopoDS_Shape, material_orientation: np.ndarray) -> np.ndarray:
    #     """
    #     Calculates the buckling length of the surface. For reference see Hypersizer V7.1 Help "Buckling spans".
    #
    #     Parameters
    #     ----------
    #     surface: TopoDS_Shape
    #         The surface.
    #     material_orientation: np.ndarray
    #         The material orientation of the surface material.
    #
    #     Returns
    #     -------
    #     np.ndarray:
    #         Buckling lengths. First entry is the length in material orientation.
    #     """
    #     # TODO consider orthotropy direction of the material if it is set in the cpacs file
    #     face = get_faces_from_shell(surface)[0]
    #
    #     # project material orientation onto surface.
    #     material_orientation, normal = project_vector_on_surface(surface, material_orientation)
    #     # calculate transverse material orientation
    #     material_transverse_direction = np.cross(material_orientation, normal)
    #
    #     # get center of the surface
    #     center = np.asarray(get_shell_mid_point(surface).Coord())
    #
    #     # get corner points of the surface
    #     corner_points = list()
    #     for point in get_shape_vertices(surface, False):
    #         if point not in corner_points:
    #             corner_points.append(point)
    #
    #     # Calculate buckling length for material and transverse orientation
    #     length_buckling = list()
    #     for orientation in [material_orientation, material_transverse_direction]:
    #         # create plane in selected orientation
    #         cross_sec_plane = calc_cross_section_plane(Vector(center), Vector(orientation), 0)
    #         cross_sec_face = plane_to_face(cross_sec_plane)
    #         x_wire = get_intersection_wire(surface, cross_sec_face)
    #
    #         # cut surface through center point along selected orientation
    #         part_shapes = split_face_with_wire(face, x_wire)
    #
    #         # process each side
    #         cxy_list = list()
    #         XY_list = list()
    #         for xy_face in part_shapes:
    #             # get center of each side
    #             xy_center = np.asarray(get_shell_mid_point(xy_face).Coord())
    #
    #             # calculate the distance between the center of the split surface and the plane which was used to cut the
    #             # surface
    #             cxy_intersection = line_plane_intersection(Vector(xy_center), Vector(orientation),
    #                                                        Vector(center), Vector(orientation))
    #             cxy = np.linalg.norm(cxy_intersection - xy_center)
    #
    #             # get the corner points of the side which are also the corner points of the whole shape
    #             xy_corner_points = list()
    #             for point in get_shape_vertices(xy_face, False):
    #                 if point in corner_points and point not in xy_corner_points:
    #                     xy_corner_points.append(point)
    #
    #             # calculate the distance between the corner points of the split surface and the plane which was used to
    #             # cut the surface. Store the bigger distance.
    #             XY = list()
    #             for corner in xy_corner_points:
    #                 XY1_intersection = line_plane_intersection(Vector(corner), Vector(orientation),
    #                                                            Vector(center), Vector(orientation))
    #                 XY.append(np.linalg.norm(XY1_intersection - corner))
    #             XY = max(XY)
    #             cxy_list.append(cxy)
    #             XY_list.append(XY)
    #
    #         # calculate the buckling lengths
    #         length_buckling.append(
    #             2 * (min([cxy_list[0], XY_list[0] - cxy_list[0]]) + min([cxy_list[1], XY_list[1] - cxy_list[1]])))
    #
    #     return np.array(length_buckling)


    def get_random_color():
        return color(random(), random(), random())
