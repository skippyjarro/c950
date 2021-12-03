# Truck class
class Truck:
    def __init__(self, name):
        self.name = name
        self.load = []
        self.route = []
        self.currLoc = 'HUB'
        self.mileage = 0
        self.stops = []
        self.route = []
        self.segments = []
        self.distances = {}

    # Method to load packages onto truck and update status to Loaded on truck
    def loadTruck(self, package):
        self.load.append(package)
        package.status = 'Loaded on truck'
        if package.address not in self.stops:
            self.stops.append(package.address)
            return True
        else:
            return False

    # Function to match package addresses to truck current location and remove packages from truck
    # Major Section: O(n)
    def deliverPackage(self, time):
        packagesToBeRemoved = []
        for package in self.load:
            if package.address == self.currLoc:
                packagesToBeRemoved.append(package)
                package.status = 'Delivered at ' + time + ' by ' + self.name
        for pkg in packagesToBeRemoved:
            self.load.remove(pkg)
        return True

    def addSegment(self, vertex1, vertex2):
        self.segments.append([vertex1, vertex2])
        return True

    def addDistance(self, segment, distance):
        self.distances[segment] = distance
        return True
