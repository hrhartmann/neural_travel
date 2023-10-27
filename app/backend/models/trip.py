from datetime import datetime
from models.point import Point

class Trip:
    def __init__(self, 
                 id: int, 
                 region: str, 
                 origin: Point, 
                 destination: Point, 
                 date: datetime, 
                 source: str):
        self.id = id
        self.region = region
        self.origin = origin
        self.destination = destination
        self.date = date
        self.source = source

    def __str__(self) -> str:
        return f"Trip {self.id} from {self.origin} to {self.destination} on {self.date}."
