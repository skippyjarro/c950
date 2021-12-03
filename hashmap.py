# Self-adjusting Custom Hash Table using ZyBooks as reference
class Hashmap:
    def __init__(self, size):
        self.size = size
        self.map = [None] * self.size

    def __get__hash(self, key):
        self.hash = key % self.size
        return self.hash

    def add(self, key, value):
        key_hash = self.__get__hash(key)
        key_value = [key, value]

        if self.map[key_hash] is None:
            self.map[key_hash] = list([key_value])
            return True
        else:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.map[key_hash].append(key_value)
            return True
        return None

    # Method to find package by Package ID and return package object
    def getPackage(self, key):
        key_hash = self.__get__hash(key)

        if self.map[key_hash] is None:
            return False
        else:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    def delete(self, key):
        key_hash = self.__get__hash(key)

        if self.map[key_hash] is None:
            return False
        else:
            for i in range(0, len(self.map[key_hash])):
                if self.map[key_hash][i][0] == key:
                    self.map[key_hash].pop(i)
                    return True

    # Method to print all package information using PackageID
    def lookupPackage(self, packageID):
        package = self.getPackage(packageID)
        print('Package ID:', package.packageID, end=', ')
        print('Address:', package.address, end=', ')
        print('City:', package.city, end=', ')
        print('Zip Code:', package.zipCode, end=', ')
        print('Delivery Deadline:', package.deliveryDeadline, end=', ')
        print('Weight:', package.weight, end=', ')
        print('Status:', package.status)

    def printPackageStatus(self):
        for i in range(1, 41):
            self.lookupPackage(i)

    def clearHashmap(self):
        for i in range(0, 41):
            self.delete(i)
