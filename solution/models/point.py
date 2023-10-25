class Point:
    def __init__(self, lat: float, lng: float):
        self.lat = lat
        self.lng = lng

    def distance_to_origin(self) -> float:
        return (self.lat ** 2 + self.lng ** 2)**.5