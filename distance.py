# Distance class for graph data structure
class Distance:
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.distances = {}

    def addVertex(self, vertex):
        self.vertices.append(vertex)
        return True

    def addEdge(self, vertex1, vertex2):
        self.edges.append([vertex1, vertex2])
        return True

    def addDistance(self, edge, distance):
        self.distances[edge] = distance
        return True

    def getDistance(self, vertex1, vertex2):
        return float(self.distances[(vertex1, vertex2)])

    # Self-adjusting function based on nearest neighbor algorithm to generate optimal route for truck
    # Major Section: O(n)
    def getShortestRoute(self, truck, startLocation):
        currLocation = startLocation
        closestLoc = None
        minDist = 140
        for vertex in self.vertices:
            if self.getDistance(currLocation, vertex) < minDist and \
                                currLocation != vertex and \
                                vertex not in truck.route and \
                                vertex in truck.stops:
                minDist = self.getDistance(currLocation, vertex)
                closestLoc = vertex
        if closestLoc is None:
            return
        else:
            truck.route.append(closestLoc)
            self.getShortestRoute(truck, closestLoc)
