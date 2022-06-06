class City(object):
    def __init__(self, name: str, coordinates: tuple):
        self.name = name
        self.coordinates = coordinates
        self.station = False
        self.station_owner = None

    def __str__(self):
        return f'{self.name}: {self.coordinates}'
