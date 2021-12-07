class Truck:
    def __init__(self):
        self.milesTraveled = 0
        self.packages = []
        self.address = 'HUB'

    def addPackage(self, package):
        self.packages.append(package)

