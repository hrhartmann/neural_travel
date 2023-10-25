from grouping import get_points_in_bounding_box
from params import ORIGIN_ONLY, DESTINATION_ONLY
from models.point import Point
import statistics

def weekly_mean_by_box_and_region(
        data: list, 
        region: str, 
        point1: Point, 
        point2: Point):
    regional_data = [trip for trip in data if trip.region == region]
    inside_box = get_points_in_bounding_box(regional_data, point1, point2, ORIGIN_ONLY, DESTINATION_ONLY)
    return get_weekly_avg(inside_box)

def get_weekly_avg(data: list):
    weeks = {}
    for trip in data:
        year = trip.date.year
        week = trip.date.isocalendar()[1]
        if week not in weeks:
            weeks[(year, week)] = 0
        weeks[(year, week)] += 1
    weekly_avg = statistics.mean(weeks.values())
    return weekly_avg