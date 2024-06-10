import csv
import os
import shutil

import numpy
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface, BRepAdaptor_Curve
from OCC.Core.GeomAbs import GeomAbs_Cylinder, GeomAbs_Circle
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import topods

from Hole import Hole


class StepModel:
    def __init__(self, directory, name, filters):
        self.precision = 4
        self.shape = None
        self.holes = []
        self.filters = filters
        self.name = name

        self.create_shape(directory)
        self.find_holes_in_step()
        self.remove_point_hole_bottom()
        self.export_csv()

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
        if not self.holes:
            print("No holes to remove.")
            return

        holes_to_remove = []

        for i, hole in enumerate(self.holes):
            try:
                point = self.calculate_offset_point(hole.location + hole.direction, hole.depth)
            except Exception as e:
                print(f"Error calculating offset point for hole {i}: {e}")
                continue

            for j, hole2 in enumerate(self.holes):
                if j == i:
                    continue  # Skip comparison with itself
                try:
                    distance = sum((point[k] - hole2.location[k]) ** 2 for k in range(len(point))) ** 0.5
                except IndexError as e:
                    print(f"Error comparing holes {i} and {j}: {e}")
                    continue
                if distance <= 1:
                    break  # Don't remove the hole if it's within the range
            else:
                holes_to_remove.append(i)  # Append only if the inner loop completes without breaking

        for index in sorted(holes_to_remove, reverse=True):
            try:
                del self.holes[index]
            except IndexError as e:
                print(f"Error removing hole at index {index}: {e}")

        print("Remaining holes:", len(self.holes))

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

                direction = (round(cylinder.Axis().Direction().X(), self.precision),
                             round(cylinder.Axis().Direction().Y(), self.precision),
                             round(cylinder.Axis().Direction().Z(), self.precision))

                depth = round(abs(surface.LastVParameter() - surface.FirstVParameter()), self.precision)

                hole = Hole(location, direction, diameter, depth)

                if hole not in self.holes:
                    if self.filters == 0:
                        self.holes.append(hole)
                    elif diameter in self.filters:
                        self.holes.append(hole)

        print("Found", str(len(self.holes)), "circles.")

    def export_csv(self):
        dir_path = f"./{self.name}"
        while os.path.exists(dir_path):
            # Remove the directory and all its contents
            # shutil.rmtree(dir_path)
            dir_path = dir_path + "_new"

        if self.name != "None":
            os.mkdir(dir_path)

        for hole in self.holes:
            size = hole.selected_diameter
            length = hole.selected_length

            if size == "None" or length == "None":
                continue

            file_path = f"./{dir_path}/{size}_{length}"
            line_data = (hole.location[0], hole.location[1], hole.location[2],
                         hole.direction[0], hole.direction[1], hole.direction[2])

            if os.path.exists(file_path):
                # Open the file in append mode
                with open(file_path, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(line_data)
            else:
                # Open the file in write mode
                with open(file_path, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(line_data)