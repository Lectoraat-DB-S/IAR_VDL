from Hole import Hole
import numpy
from OCC.Core.BRepAdaptor import *
from OCC.Core.STEPControl import *
from OCC.Core.GeomAbs import *
from OCC.Core.TopExp import *
from OCC.Core.TopAbs import *
from OCC.Core.TopoDS import *
from HolesList import HolesList


class CadConverter:
    def __init__(self, step_file_path):
        self.step_file_path = step_file_path
        self.precision = 4
        self.holes_list = HolesList("a")

    def calculate_coordinates(self, point, distance):
        """

        :param point:
        :param self:
        :param distance:
        :return:
        """

        x, y, z, rx, ry, rz = point

        direction = numpy.array([rx, ry, rz])
        # norm = numpy.linalg.norm(direction)
        #
        # if norm == 0:
        #     return None
        #
        # normalized_direction = direction / norm

        movement_vector = direction * distance

        new_point = (round(x + movement_vector[0], self.precision),
                     round(y + movement_vector[1], self.precision),
                     round(z + movement_vector[2], self.precision))

        return new_point

    def remove_bottem_positions(self):
        holes_to_remove = []

        for hole in self.holes_list.holes.values():
            point = self.calculate_coordinates(hole.location + hole.direction, hole.depth)

            if point in self.holes_list.holes:
                holes_to_remove.append(hole.location)

        for hole in holes_to_remove:
            del self.holes_list.holes[hole]
        print("Found", len(self.holes_list.holes), "holes.")

    @staticmethod
    def find_circles_attached_to_cylinder(self, shape):
        circular_edges, surfaces = [], []

        # Explore the shape for faces
        face_explorer = TopExp_Explorer(shape, TopAbs_FACE)

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
        print("Reading file:", self.step_file_path)

        step_reader = STEPControl_Reader()
        step_reader.ReadFile(self.step_file_path)
        step_reader.TransferRoots()
        shape = step_reader.OneShape()

        circles, surfaces = self.find_circles_attached_to_cylinder(shape)

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

                direction = (cylinder.Axis().Direction().X(),
                             cylinder.Axis().Direction().Y(),
                             cylinder.Axis().Direction().Z())

                depth = round(abs(surface.LastVParameter() - surface.FirstVParameter()), self.precision)

                hole = Hole(location, direction, diameter, depth)

                if hole not in self.holes_list.holes:
                    if diameter < 20:
                        self.holes_list.holes[location] = hole

        print("Found", str(len(self.holes_list.holes)), "circles.")
