class Stadium:
    def __init__(self, name, id, city, capacity):
        self.name = name
        self.id = id
        self.city = city
        self.capacity = capacity

    def __str__(self):
        return f'{self.name}, en la ciudad {self.city}.\n'
