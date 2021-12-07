class Package:

    def __init__(self, packID, address, city, state, zipcode, deadline, weight):
        self.packID = packID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.status = "at the hub"
        self.timeDelivered = None
        self.truck = None

    def __repr__(self):
        return ("package ID: " + str(self.packID) + ",   address: " + str(self.address) + ",   delivery deadline: " + str(self.deadline)
        + ",   delivery status: " + self.status + ",   delivered on truck " + str(self.truck) + ",   delivered at: " + str(self.timeDelivered))
