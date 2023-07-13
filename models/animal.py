class Animal():

    # Class initializer. It has 5 custom parameters, with the
    # special `self` parameter that every method on a class
    # needs as the first parameter.
    def __init__(self, id, name, species, breed, status, locationId, employeeId, customerId):
        self.id = id
        self.name = name
        self.species = species
        self.breed = breed
        self.locationId = locationId
        self.customerId = customerId
        self.employeeId = employeeId
        self.status = status
