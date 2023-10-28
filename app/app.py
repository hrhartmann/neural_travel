from flask import Flask, jsonify
import mysql.connector

from data_access import (
    create_trips_from_csv,
    save_to_db,
    get_from_db
)
from logic.number_of_trips import weekly_mean_by_box_and_region
from logic.grouping import (
    group,
    group_by_region,
    group_by_time
)
from config import DB_PASSWORD, MYSQL_CONFIG
from params import REGION

app = Flask(__name__)

save_to_db()
# data = get_from_db()
data = create_trips_from_csv()

def db_data():      
    connection = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM trips")
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

@app.route("/group")
def group_page():
    return jsonify({"Group by time": group(data)})


@app.route("/group/time")
def group_bytime_page():
    return jsonify({"Group by time": group_by_time(data)})


@app.route("/weekly_avg")
def weekly_avg():
    return jsonify(
        {f"The weekly avarage in {REGION} is: ": 
         weekly_mean_by_box_and_region(data)})


@app.route("/save")
def save_to_db_from_file():
    return jsonify({"Data": save_to_db()})


@app.route("/db")
def get_db_data():
    return jsonify({"Data": str(data)})

@app.route("/any")
def any():
    return jsonify({"Data": str(data[3])})


@app.route("/")
def index():
    return jsonify({"Data": "Nothing"})


if __name__ == "__main__":
    app.run(host="0.0.0.0")