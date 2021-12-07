## Created by: Aaron Rezentes, Student ID: 001441915

import csv
import sys
import Package
import myHashtable
import Truck

NUM_PACKAGES = 40

## This method reads the package file to create package objects and then fill my hashtable with them
## It returns the filled out hashtable
def readPackageData():
    file = open("WGUPS Package File.csv")
    reader = csv.reader(file)
    rows = []
    package = None
    packTable = myHashtable.myHashtable(NUM_PACKAGES)
    for item in reader:
        rows.append(item)
    file.close()
    for i in range(1, len(rows)):
        package = Package.Package(int(rows[i][0]), rows[i][1], rows[i][2], rows[i][3], rows[i][4], rows[i][5],
                                  rows[i][6])
        packTable.insert(package)
    return packTable

## This method is used to create a 2d array of addresses and their distances.
## It returns the 2d array.
def readDistanceData():
    file = open("WGUPS Distance Table.csv")
    reader = csv.reader(file)
    rows = []
    for item in reader:
        item = list(filter(lambda x: x, item))
        rows.append(item)
    return rows

## This method loops through the 2d array to find the distance between 2 addresses
## It returns the distance between the 2 addresses
## It has a run time of O(n) which could be reduced if addresses and distances were stored as key value pairs in a hashtable
def getDistance(start, end, distanceTable):
    index1 = 0
    index2 = 0
    for address in distanceTable:## This for loop finds the position of the address to travel to
        if address[1].startswith(end):
            break
        index1 += 1

    for address2 in distanceTable:## This for loop finds the position of the address being traveled from
        if address2[1].startswith(start):
            break
        index2 += 1
    if index1 > index2:
        return float(distanceTable[index1][index2 + 2])
    else:
        return float(distanceTable[index2][index1 + 2])

## This method creates a list by starting with a list of packages at a given start point and adding the closest package until complete
## It return the list of packages (The packages are now in the order they will be delivered in)
def chooseGreedyPath(packages, start, distanceTable):
    currAddress = start
    index = -1
    chosenPath = []
    nextPackage = None
    while len(packages) > 1:
        minDistance = sys.maxsize
        for packIndex, package in enumerate(packages):
            if type(package) == str:
                distance = getDistance(currAddress, package, distanceTable)
            else:
                distance = getDistance(currAddress, package.address, distanceTable)
            if distance < minDistance:
                minDistance = distance
                index = packIndex
        nextPackage = packages.pop(index)
        if type(nextPackage) == str:
            currAddress = nextPackage
        else:
            currAddress = nextPackage.address
        chosenPath.append(nextPackage)
    chosenPath.append(packages.pop(0))
    return chosenPath

## This method takes a truck and a list of packages that haven't been loaded yet. It loads the truck and then calls chooseGreedyPath
## to determine the path. Lastly it adds the HUB as the final destination to ensure it returns after each trip
## It returns True if packages were loaded and False otherwise
def loadTruck(truck, notLoaded, distanceTable, packTable):
    packages = []
    popped = None
    if not notLoaded:
        return False
    while popped != 'HUB' and notLoaded:
        popped = notLoaded.pop(0)
        packages.append(popped)
    if type(packages[len(packages) - 1]) == str:
        packages.pop()
    packages = chooseGreedyPath(packages, 'HUB', distanceTable)
    for package in packages:
        packTable.table[packTable.hash(package.packID)][0].status = "en route"
        truck.addPackage(package)
    truck.addPackage('HUB')
    return True


## The main method runs a loop until the user chooses to exit. Each iteration consists of loading the trucks, choosing the path, delivering up to the given time
## and lastly printing out lots of information, including things about every package and the distance traveled
def main():
    userChoice = "24:00"
    while userChoice.upper() != "EXIT":
        packTable = readPackageData()
        distanceTable = readDistanceData()
        distanceTable.pop(0)
        time = userChoice.split(":")
        maxMiles = int(time[0]) * 18 + ((int(time[1]) * 18) / 60) - 144
        truck1 = Truck.Truck()
        nextAddressTruck1 = None
        ## These 2 long lists are the list of packages not yet loaded or delivered
        truck1NotLoaded = [packTable.search(1), packTable.search(15), packTable.search(16), packTable.search(34),
                           packTable.search(14), packTable.search(20), packTable.search(21), packTable.search(19),
                           packTable.search(13), packTable.search(39), 'HUB', packTable.search(32),
                           packTable.search(31), packTable.search(6), packTable.search(25), packTable.search(26),
                           packTable.search(28), 'HUB', packTable.search(9)]
        loadTruck(truck1, truck1NotLoaded, distanceTable, packTable)
        truck2 = Truck.Truck()
        nextAddressTruck2 = None
        truck2NotLoaded = [packTable.search(29), packTable.search(30), packTable.search(8), packTable.search(5),
                          packTable.search(38), packTable.search(40), packTable.search(4), packTable.search(3),
                          packTable.search(18), packTable.search(36), packTable.search(10), packTable.search(37),
                          packTable.search(27), packTable.search(35), packTable.search(12), packTable.search(7),
                          'HUB', packTable.search(2), packTable.search(17), packTable.search(33), packTable.search(11),
                          packTable.search(24), packTable.search(23), packTable.search(22)]
        loadTruck(truck2, truck2NotLoaded, distanceTable, packTable)
        print("The time being shows is " + userChoice)
        if type(truck1.packages[0]) == str:
            nextAddressTruck1 = 'HUB'
        else:
            nextAddressTruck1 = truck1.packages[0].address

        while getDistance(truck1.address, nextAddressTruck1, distanceTable) + truck1.milesTraveled < maxMiles:## While the time (converted to miles) to stop isn't yet reached
            changed = False
            time = None
            delivered = ""
            delivering = truck1.packages.pop(0)
            if type(delivering) == Package.Package:
                delivering.truck = 1
            if not changed and truck1.milesTraveled > 40:## This changes the address for package 9 at the correct time (converted to miles)
                packTable.search(9).address = "410 S State St"
                changed = True
            if type(delivering) == Package.Package:## these if type() structures are to check if it's a package being delivered or simply the address of the HUB
                truck1.milesTraveled += getDistance(truck1.address, nextAddressTruck1, distanceTable)
                time = truck1.milesTraveled / 18
                if time > 1:
                    delivered += str(int(time) + 8)
                    delivered += ":"
                    if int((time % 1) * 60) < 10:
                        delivered += "0"
                    delivered += str(int((time % 1) * 60))
                else:
                    delivered += "08:"
                    if int((time % 1) * 60) < 10:
                        delivered += "0"
                    delivered += str(int((time % 1) * 60))
                packTable.search(delivering.packID).status = "delivered"
                packTable.search(delivering.packID).timeDelivered = delivered
                truck1.address = nextAddressTruck1
            else:
                truck1.milesTraveled += getDistance(truck1.address, nextAddressTruck1, distanceTable)
                truck1.address = nextAddressTruck1
            if not truck1.packages:
                if not loadTruck(truck1, truck1NotLoaded, distanceTable, packTable):
                    break
            if type(truck1.packages[0]) == str:
                nextAddressTruck1 = 'HUB'
            else:
                nextAddressTruck1 = truck1.packages[0].address

        if type(truck2.packages[0]) == str:
            nextAddressTruck2 = 'HUB'
        else:
            nextAddressTruck2 = truck2.packages[0].address

        while getDistance(truck2.address, nextAddressTruck2, distanceTable) + truck2.milesTraveled < maxMiles:## While the time (converted to miles) to stop isn't yet reached
            time = None
            delivered = ""
            delivering = truck2.packages.pop(0)
            if type(delivering) == Package.Package:## these if type() structures are to check if it's a package being delivered or simply the address of the HUB
                delivering.truck = 2
            if type(delivering) == Package.Package:
                truck2.milesTraveled += getDistance(truck2.address, nextAddressTruck2, distanceTable)
                time = truck2.milesTraveled / 18
                if time > 1:
                    delivered += str(int(time) + 8)
                    delivered += ":"
                    if int((time % 1) * 60) < 10:
                        delivered += "0"
                    delivered += str(int((time % 1) * 60))
                else:
                    delivered += "08:"
                    if int((time % 1) * 60) < 10:
                        delivered += "0"
                    delivered += str(int((time % 1) * 60))
                packTable.search(delivering.packID).status = "delivered"
                packTable.search(delivering.packID).timeDelivered = delivered
                truck2.address = nextAddressTruck2
            else:
                truck2.milesTraveled += getDistance(truck2.address, nextAddressTruck2, distanceTable)
                truck2.address = nextAddressTruck2
            if not truck2.packages:
                if not loadTruck(truck2, truck2NotLoaded, distanceTable, packTable):
                    break
            if type(truck2.packages[0]) == str:
                nextAddressTruck2 = 'HUB'
            else:
                nextAddressTruck2 = truck2.packages[0].address
        packTable.print()
        print("truck 1 miles traveled: " + str(truck1.milesTraveled))
        print("truck 2 miles traveled: " + str(truck2.milesTraveled))
        print("total miles traveled: " + str(truck1.milesTraveled + truck2.milesTraveled))

        print()
        userChoice = input("Please type the 24h time you would like to go to in the format \"hh:mm\" sometime after 08:00 or \"exit\" to end the program: ")


if __name__ == '__main__':
    main()
