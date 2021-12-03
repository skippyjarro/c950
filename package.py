# Package class
class Package:
    def __init__(self, packageID, address, city, state, zipCode, deliveryDeadline, weight, notes, status):
        self.packageID = packageID
        self.address = address
        self.city = city
        self.state = state
        self.zipCode = zipCode
        self.deliveryDeadline = deliveryDeadline
        self.weight = weight
        self.notes = notes
        self.status = status