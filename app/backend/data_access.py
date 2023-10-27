from datetime import datetime
from tkinter import filedialog
import mysql.connector

from models.trip import Trip
from models.point import Point
from config import MYSQL_CONFIG

FILENAME = "trips_data/trips_with_id.csv"


def create_trips_from_csv(filename=FILENAME):
    trips = []
    with open(filename, 'r') as file:
        # data = file.read()
        for line in file: 
            new_trip = create_trip(line)
            if new_trip:
                trips.append(new_trip)
    return trips


def create_trip(trip_line):
    try:
        elements = trip_line.split(",")
        origin = create_point(elements[2])
        destination = create_point(elements[3])
        date = datetime.strptime(elements[4], "%d-%m-%y %H:%M")
        return Trip(
            int(elements[0]),
            elements[1],
            origin,
            destination,
            date,
            elements[5]
        )
    except Exception:
        return 


def create_point(point_element):
    try:
        elements = point_element.split(" ")
        x = float(elements[1].strip("("))
        y = float(elements[2].strip(")"))
        return Point(x, y)
    except:
        return 


def save_to_db(trips):
    return MYSQL_CONFIG["password"]
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor(dictionary=True)

        # Loop over the list of Trip objects and insert each one into the database
        for trip in trips:
            cursor.execute("INSERT INTO trips (id, region, origin_x, origin_y, destination_x, destination_y, date, source) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (
                trip.id, 
                trip.region, 
                trip.origin.lat, 
                trip.origin.long, 
                trip.destination.lat, 
                trip.destination.long, 
                trip.date, 
                trip.source))

        connection.commit()
        cursor.close()
        connection.close()
        return "Success!"
    except Exception as error:
        return str(error)
    



   