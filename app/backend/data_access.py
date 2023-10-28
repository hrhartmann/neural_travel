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


def save_to_db():
    trips = create_trips_from_csv()
    rs = ""
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor(dictionary=True)

        # Loop over the list of Trip objects and insert each one into the database
        for trip in trips:
            try:        
                cursor.execute("INSERT INTO trips (id, region, origin_lat, origin_lon, destination_lat, destination_lon, date_time, source) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (
                trip.id, 
                trip.region, 
                trip.origin.lat, 
                trip.origin.long, 
                trip.destination.lat, 
                trip.destination.long, 
                trip.date, 
                trip.source))
            except Exception as error:
                rs += str(error)

        connection.commit()
        cursor.close()
        connection.close()
        return rs
    except Exception as error:
        return str(error)
    
def get_from_db():
    trips = []
    rs = ""
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM trips")
        rows = cursor.fetchall()
        # return str(rows)
        for row in rows:
            trips.append(create_trip_from_row(row))
        cursor.close()
        connection.close()
    except Exception as error:
        rs += str(error)
    finally:
        return rs
        return trips
    
def create_trip_from_row(row):
    return Trip(
        id=int(row["id"]),
        region=row["region"],
        origin=point_from_db(row["origin_lat"], row["origin_lon"]),
        destination=point_from_db(row["destination_lat"], row["destination_lon"]),
        # date=datetime.strptime(row["date_time"], "%d-%m-%y %H:%M"),
        date=row["date_time"],
        source=row["source"]
    )

def point_from_db(db_lat, db_long):
    lat = clean_db_decimal(db_lat)
    long = clean_db_decimal(db_long)
    return Point(lat, long)

def clean_db_decimal(decimal):
    try:
        value = str(decimal).replace("Decimal('", "")
        value = value.replace("')", "")
        return float(value)
    except:
        return None