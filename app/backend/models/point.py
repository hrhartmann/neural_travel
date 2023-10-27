class Point:
    def __init__(self, lat: float, long: float):
        self.lat = lat
        self.long = long

    def distance_to_origin(self) -> float:
        return (self.lat ** 2 + self.long ** 2)**.5
    
    def __str__(self) -> str:
        return f"HHP ({self.lat}, {self.long})"