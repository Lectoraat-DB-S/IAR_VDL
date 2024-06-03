import csv

import numpy
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface, BRepAdaptor_Curve
from OCC.Core.GeomAbs import GeomAbs_Cylinder, GeomAbs_Circle
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import topods

from Hole import Hole


class StepModel:
    def __init__(self, directory):
        self.precision = 4
        self.shape = None
        self.holes = []
        self.name = "Hole_list"

        print("x")

        self.create_shape(directory)
        self.find_holes_in_step()
        self.remove_point_hole_bottom()
        self.write_csv()

    def create_shape(self, directory):
        step_reader = STEPControl_Reader()
        step_reader.ReadFile(directory)
        step_reader.TransferRoots()
        self.shape = step_reader.OneShape()

    def calculate_offset_point(self, point, distance):
        """
        :param point:
        :param self:
        :param distance:
        :return:
        """

        x, y, z, rx, ry, rz = point

        direction = numpy.array([rx, ry, rz])
        norm = numpy.linalg.norm(direction)

        if norm == 0:
            return None

        normalized_direction = direction / norm

        movement_vector = normalized_direction * distance

        new_point = (round(x + movement_vector[0], self.precision),
                     round(y + movement_vector[1], self.precision),
                     round(z + movement_vector[2], self.precision))

        return new_point

    def remove_point_hole_bottom(self):
        holes_to_remove = []
        current_index = 0

        for hole in self.holes:
            current_index += 1
            point = self.calculate_offset_point(hole.location + hole.direction, hole.depth)

            for hole2 in self.holes:
                if hole2.location == point:
                    holes_to_remove.append(current_index)

        for index in sorted(holes_to_remove, reverse=True):
            del self.holes[index]

        print("Found", len(self.holes), "holes.")

    def find_circles_attached_to_cylinder(self):
        circular_edges, surfaces = [], []

        # Explore the shape for faces
        face_explorer = TopExp_Explorer(self.shape, TopAbs_FACE)

        while face_explorer.More():
            face = face_explorer.Current()
            surface_adaptor = BRepAdaptor_Surface(face, True)
            surface_type = surface_adaptor.GetType()

            # Check if the face is a cylinder
            if surface_type == GeomAbs_Cylinder:
                # Explore edges of this cylindrical face
                edge_explorer = TopExp_Explorer(face, TopAbs_EDGE)

                while edge_explorer.More():
                    edge = topods.Edge(edge_explorer.Current())
                    curve_adaptor = BRepAdaptor_Curve(edge)

                    # Check if the edge is circular
                    if curve_adaptor.GetType() == GeomAbs_Circle:
                        circle = curve_adaptor.Circle()
                        start_point = curve_adaptor.Value(0)
                        end_point = curve_adaptor.Value(curve_adaptor.LastParameter())

                        if start_point.IsEqual(end_point, 1e-6):
                            circular_edges.append(edge)
                            surfaces.append(surface_adaptor)

                    edge_explorer.Next()

            face_explorer.Next()

        return circular_edges, surfaces

    def find_holes_in_step(self):

        circles, surfaces = self.find_circles_attached_to_cylinder()

        index = -1

        for circle in circles:
            index += 1
            curve_adaptor = BRepAdaptor_Curve(circle)

            # Check if the edge is circular
            if curve_adaptor.GetType() == GeomAbs_Circle:

                surface = surfaces[index]
                cylinder = surface.Cylinder()
                curve_circle = curve_adaptor.Circle()

                diameter = round(2 * curve_circle.Radius(), self.precision)

                location = (round(curve_circle.Location().X(), self.precision),
                            round(curve_circle.Location().Y(), self.precision),
                            round(curve_circle.Location().Z(), self.precision))

                direction = (-round(cylinder.Axis().Direction().X(), self.precision),
                             -round(cylinder.Axis().Direction().Y(), self.precision),
                             -round(cylinder.Axis().Direction().Z(), self.precision))

                depth = round(abs(surface.LastVParameter() - surface.FirstVParameter()), self.precision)

                hole = Hole(location, direction, diameter, depth)

                if hole not in self.holes:
                    # if diameter == 8:
                    self.holes.append(hole)

        print("Found", str(len(self.holes)), "circles.")

    def write_csv(self):
        with open(f".\\{self.name}.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            for hole in self.holes:
                writer.writerow((hole.location[0], hole.location[1], hole.location[2],
                                 hole.direction[0], hole.direction[1], hole.direction[2]))
