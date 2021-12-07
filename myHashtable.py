class myHashtable:
    ## Because every ID is unique I created the numBuckets variable so that the hastables size can be large enough to fit every item in one bucket.
    def __init__(self, numBuckets):
        self.table = []
        for i in range(numBuckets):
            self.table.append([])

    def hash(self, packID):
        return packID % len(self.table)

    def insert(self, package):
        self.table[self.hash(package.packID)].append(package)

    def remove(self, packID):
        for package in self.table[self.hash(packID)]:
            if package.packID == packID:
                self.table[self.hash(packID)].remove(package)

    def search(self, packID):
        for package in self.table[self.hash(packID)]:
            if package.packID == packID:
                return package
            else:
                return None

    def print(self):
        for i in range(1, 41):
            print(self.search(i))
