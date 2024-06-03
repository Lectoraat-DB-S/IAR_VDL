class Hole:
    def __init__(self, location, direction, diameter, depth):
        self.location = location
        self.direction = direction
        self.diameter = diameter
        self.depth = depth
        self.insert_type = None
        self.insert_diameter = [None, 2, 3, 4, 5, 6, 8, 10, 12]
        self.insert_length = [None, 1, 1.5, 2]
