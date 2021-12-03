# Nate Sukhtipyaroge StudentID: 264559
# Complexity of Program: O(n^2)

import csv
import datetime
from hashmap import Hashmap
from package import Package
from distance import Distance
from truck import Truck


# Function to read Package File and load packages into hash table
def loadDepot():
    with open('WGUPS Package File.csv') as packageFile:
        readCSV = csv.reader(packageFile, delimiter=',')
        for row in readCSV:
            packageID = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zipCode = row[4]
            deliveryDeadline = row[5]
            weight = row[6]
            notes = row[7]
            if packageID not in [6, 25, 28, 32]:
                status = 'At the Hub'
            else:
                status = 'Delayed'
            packageList.add(packageID,
                            Package(packageID, address, city, state, zipCode, deliveryDeadline, weight, notes, status))


# Function to read distance table and load into graph data structure
# Major Section: O(n^2)
def loadDistances():
    with open('WGUPS Distance Table.csv') as distanceFile:
        readCSV = csv.reader(distanceFile, delimiter=',')
        tempArray = []
        for row in readCSV:
            tempArray.append(row)
            distance.addVertex(row[0])
        for i in range(0, len(tempArray)):
            for j in range(i, len(tempArray)):
                distance.addDistance((distance.vertices[i], distance.vertices[j]), tempArray[i][j + 1])
                distance.addDistance((distance.vertices[j], distance.vertices[i]), tempArray[i][j + 1])


# Function to load truck 1
# Major Section: O(1)
def loadTruck1():
    # Start route at Hub
    truck1.route.append('HUB')

    # Load packages that have delivery deadlines before EOD and don't have other constraints
    for i in range(1, 41):
        pkg = packageList.getPackage(i)
        if pkg.deliveryDeadline != 'EOD' and pkg.notes is '':
            truck1.loadTruck(pkg)

    # Load packages that need to be delivered together
    truck1.loadTruck(packageList.getPackage(14))
    truck1.loadTruck(packageList.getPackage(16))
    truck1.loadTruck(packageList.getPackage(19))
    truck1.loadTruck(packageList.getPackage(20))

    # Load packages that have the same address as packages already on truck if truck has room
    for i in range(1, 41):
        pkg = packageList.getPackage(i)
        if len(truck1.load) < 16 and pkg.status == 'At the Hub' and pkg.address in truck1.stops and pkg.notes is '':
            truck1.loadTruck(pkg)

    # Generate the shortest route to each stop using nearest neighbor algorithm
    distance.getShortestRoute(truck1, truck1.currLoc)

    # End first run at Hub
    truck1.route.append('HUB')

    # Load segments between stops and distances for each segment
    loadSegmentsDistances(truck1)


# Function to load truck 2
# Major Section: O(1)
def loadTruck2():
    # Start route at the Hub
    truck2.route.append('HUB')

    # Load packages that were delayed or must be on Truck 2
    truck2.loadTruck(packageList.getPackage(3))
    truck2.loadTruck(packageList.getPackage(6))
    truck2.loadTruck(packageList.getPackage(18))
    truck2.loadTruck(packageList.getPackage(25))
    truck2.loadTruck(packageList.getPackage(28))
    truck2.loadTruck(packageList.getPackage(32))
    truck2.loadTruck(packageList.getPackage(36))
    truck2.loadTruck(packageList.getPackage(38))

    # Load packages that have the same address as packages already on the truck
    for i in range(1, 41):
        pkg = packageList.getPackage(i)
        if len(truck2.load) < 16 and pkg.status == 'At the Hub' and pkg.address in truck2.stops and pkg.notes is '':
            truck2.loadTruck(pkg)

    # Load packages if the truck has room
    for i in range(1, 41):
        pkg = packageList.getPackage(i)
        if len(truck2.load) < 16 and pkg.status == 'At the Hub' and pkg.packageID != 9:
            truck2.loadTruck(pkg)

    # Generate the shortest route using the nearest neighbor algorithm
    distance.getShortestRoute(truck2, truck2.currLoc)

    # Load segments between truck stops and distances for each segment
    loadSegmentsDistances(truck2)


# Function to load truck 1 for second trip
# Major Section: O(1)
def loadTruck1Again():

    # Clear stops, route, distances, and segments from previous run
    truck1.stops.clear()
    truck1.route.clear()
    truck1.distances.clear()
    truck1.segments.clear()

    # Start route at Hub
    truck1.route.append('HUB')

    # Load remaining packages
    for i in range(1, 41):
        pkg = packageList.getPackage(i)
        if len(truck1.load) < 16 and pkg.status == 'At the Hub':
            truck1.loadTruck(pkg)

    # Generate the shortest route using the nearest neighbor algorithm
    distance.getShortestRoute(truck1, truck1.currLoc)

    # Load segments between truck stops and distances for each segment
    loadSegmentsDistances(truck1)


# Function to load segments and distances into truck
# Major Section: O(n)
def loadSegmentsDistances(truck):
    # Load segments between each stop of the truck route
    for i in range(0, len(truck.route) - 1):
        truck.addSegment(truck.route[i], truck.route[i + 1])

    # Load distances for each segment of truck route
    for segment in truck.segments:
        truck.addDistance(tuple(segment), distance.getDistance(segment[0], segment[1]))


# Function to deliver packages
# Major Section: O(n)
def deliverPackages(truck, startTime, stopTime):
    # Mark all packages as Out for Delivery
    for package in truck.load:
        package.status = 'Out for Delivery'
    t = startTime

    # For each segment of truck route, calculate time required to travel each segment and add to start time to get
    # arrival time
    for segment in truck.segments:
        travelTime = (truck.distances[tuple(segment)] / 18) * 3600
        dt = datetime.timedelta(seconds=travelTime)
        t += dt

        # if Arrival time is before stop time, add distance traveled to running total of truck mileage,
        # update truck's current location to endpoint of segment, remove package from truck and update status
        if t < stopTime:
            truck.mileage += round((18 / 3600) * travelTime, 2)
            truck.currLoc = segment[1]
            truck.deliverPackage(str(t.time().isoformat()))


# Function to start package loading and delivery
# Major Section: O(1)
def runProgram(stopHour, stopMin):
    # Initialize variables
    time = datetime.datetime(100, 1, 1, 8, 0)
    dt = datetime.timedelta(seconds=1)
    truck1Start = datetime.datetime(100, 1, 1, 8, 0)
    truck2Start = datetime.datetime(100, 1, 1, 9, 5)
    truck1StartAgain = datetime.datetime(100, 1, 1, 10, 30)
    stopTime = datetime.datetime(100, 1, 1, stopHour, stopMin)

    # As long as current time is before stop time, run program
    while time < stopTime:
        # If time is 9:05am, update packages that were delayed in flight to be at the hub
        if time == datetime.datetime(100, 1, 1, 9, 5):
            packageList.getPackage(6).status = 'At the Hub'
            packageList.getPackage(25).status = 'At the Hub'
            packageList.getPackage(28).status = 'At the Hub'
            packageList.getPackage(32).status = 'At the Hub'

        # If time is 10:20am, correct address of package #9
        if time == datetime.datetime(100, 1, 1, 10, 20):
            packageList.getPackage(9).address = '410 S State St'

        # Truck 1 starts first run at 8am
        if time == truck1Start:
            loadTruck1()
            deliverPackages(truck1, truck1Start, stop)

        # Truck 2 starts run at 9:05am after delayed packages arrive
        if time == truck2Start:
            loadTruck2()
            deliverPackages(truck2, truck2Start, stop)

        # Truck 1 start second run at 10:30am
        if time == truck1StartAgain:
            loadTruck1Again()
            deliverPackages(truck1, truck1StartAgain, stop)

        # Increment time by 1 second
        time += dt


# Main method
# Major Section: O(1)
if __name__ == '__main__':
    # Initializing global variables
    packageList = Hashmap(40)
    truck1 = Truck('Truck 1')
    truck2 = Truck('Truck 2')
    distance = Distance()
    totalDistance = 0
    stop = datetime.datetime(100, 1, 1, 17, 0)
    # Load depot and distance table
    loadDepot()
    loadDistances()
    userSelection = -1

    # Command Line Interface
    while userSelection != 0:
        # User Interface Menu
        print('Welcome to WGUPS Delivery Service')
        print('1: Deliver All Packages')
        print('2: Get Package Status at 9am')
        print('3: Get Package Status at 10am')
        print('4: Get Package Status at 12:30pm')
        print('5: Look up a Package ID')
        print('0: Quit')
        userSelection = int(input('Please make a selection: '))

        if userSelection == 1:
            # Initializing global variables
            packageList = Hashmap(40)
            truck1 = Truck('Truck 1')
            truck2 = Truck('Truck 2')
            distance = Distance()

            # Load depot and distance table
            loadDepot()
            loadDistances()

            # Run program with 5pm stop time
            runProgram(17, 0)

            # Print package status
            packageList.printPackageStatus()

            # Total distance traveled for both trucks
            totalDistance = truck1.mileage + truck2.mileage
            print('Total Distance Traveled: ', round(totalDistance, 1), '\n')
        elif userSelection == 2:
            # Initializing global variables
            packageList = Hashmap(40)
            truck1 = Truck('Truck 1')
            truck2 = Truck('Truck 2')
            distance = Distance()

            # Load depot and distance table
            loadDepot()
            loadDistances()

            # Run program with 9am Stop time
            print('Package status as of 9am')
            runProgram(9, 0)

            # Print package status
            packageList.printPackageStatus()

            # Total distance traveled for both trucks
            totalDistance = truck1.mileage + truck2.mileage
            print('Total Distance Traveled: ', round(totalDistance, 1), '\n')
        elif userSelection == 3:
            # Initializing global variables
            packageList = Hashmap(40)
            truck1 = Truck('Truck 1')
            truck2 = Truck('Truck 2')
            distance = Distance()

            # Load depot and distance table
            loadDepot()
            loadDistances()

            # Run program with 10am Stop time
            print('Package status as of 10am')
            runProgram(10, 0)

            # Print package status
            packageList.printPackageStatus()

            # Total distance traveled for both trucks
            totalDistance = truck1.mileage + truck2.mileage
            print('Total Distance Traveled: ', round(totalDistance, 1), '\n')
        elif userSelection == 4:
            # Initializing global variables
            packageList = Hashmap(40)
            truck1 = Truck('Truck 1')
            truck2 = Truck('Truck 2')
            distance = Distance()

            # Load depot and distance table
            loadDepot()
            loadDistances()

            # Run program with 12:30pm Stop time
            print('Package status as of 12:30pm')
            runProgram(12, 30)

            # Print package status
            packageList.printPackageStatus()

            # Total distance traveled for both trucks
            totalDistance = truck1.mileage + truck2.mileage
            print('Total Distance Traveled: ', round(totalDistance, 1), '\n')
        elif userSelection == 5:
            lookupID = -1
            while lookupID < 1 or lookupID > 40:
                lookupID = int(input('Enter a Package ID: '))
                if lookupID < 1 or lookupID > 40:
                    print('Invalid Package ID, Please Try Again')
            packageList.lookupPackage(lookupID)
        elif userSelection == 0:
            print('Thank you for using WGUPS.  Goodbye!')
        else:
            print('Invalid Selection.  Try Again.')
