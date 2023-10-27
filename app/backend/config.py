from dotenv import load_dotenv
import os

load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")

MYSQL_CONFIG = {
        "user": "root",
        "password": DB_PASSWORD,
        "host": "db",
        "port": "3306",
        "database": "airportdb"
    }