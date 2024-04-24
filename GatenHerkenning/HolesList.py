import csv
from Hole import Hole


class HolesList():
    def __init__(self, name):
        self.name = name
        self.holes = {}

    # def add_hole(self, location, direction, diameter, depth):
    #     self.holes[location] = Hole(location, direction, diameter, depth)
    #
    # def remove_hole(self, location):
    #     del self.holes_list.holes[location]

    def write_csv(self):
        with open(f".\\{self.name}.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            for hole in self.holes.values():
                writer.writerow((hole.location[0], hole.location[1], hole.location[2],
                                hole.direction[0], hole.direction[1],hole.direction[2]))
