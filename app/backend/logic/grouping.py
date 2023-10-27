
from models.trip import Point
from params import GRID_BY_REGION, PER_GROUP
from logic.tools import clean_data, show_list


def group_by_time(data: list, per_group: int=PER_GROUP):
    data.sort(key=lambda x: x.date)
    groups = []
    for i in range(0, len(data), per_group):
        try:
            groups.append(data[i:i+per_group])
        except IndexError:
            groups.append(data[i:])
    return show_list(groups)


def group_by_region(data: list):
    groups = {}
    for trip in data:
        if trip.region not in groups:
            groups[trip.region] = []
        groups[trip.region].append(trip)
    return groups


def group_by_location(data: list, x: int=GRID_BY_REGION):
    # Creating a grid
    max_lat, max_long = get_max_lat_long(data)
    section_lat_len =  max_lat / x
    section_long_len = max_long / x
    groups = {}

    # Grouping by section
    for trip in data:
        section = get_section(trip.origin.lat, trip.origin.long, section_lat_len, section_long_len)
        if section not in groups:
            groups[section] = []
        groups[section].append(trip)
    return groups


def group(data, grid=GRID_BY_REGION, per_group=PER_GROUP):
    data = clean_data(data)
    by_region = group_by_region(data)
    for region in by_region:
        by_region[region] = group_by_location(by_region[region], grid)
        for quadrant in by_region[region]:
            by_region[region][quadrant] = group_by_time(by_region[region][quadrant], per_group)
    return by_region
    

def get_section(lat: float, long: float, lat_len: float, long_len: float):
    return (int(lat / lat_len), int(long / long_len))
    

def get_max_lat_long(data: list):
    all_origin_points = [x.origin for x in data]
    all_destination_points = [x.destination for x in data]
    all_points = all_origin_points + all_destination_points
    max_lat = max(all_points, key=lambda x: x.lat).lat
    max_long = max(all_points, key=lambda x: x.long).long
    return max_lat, max_long


def inside_bounding_box(botleft: Point, topright: Point, target: Point):
    return botleft.lat <= target.lat <= topright.lat and botleft.long <= target.long <= topright.long
    

def get_botleft_and_topright(point1: Point, point2: Point):
    origin_distance_p1 = point1.distance_to_origin()
    origin_distance_p2 = point2.distance_to_origin()
    if origin_distance_p1 < origin_distance_p2:
        return point1, point2
    else:
        botleft = point2
        topright = point1
    return botleft, topright


def get_points_in_bounding_box(
        data: list, 
        point1: Point, 
        point2: Point, 
        origin_only: bool = False, 
        destination_only: bool = False):
    botleft, topright = get_botleft_and_topright(point1, point2)
    inside = []
    if origin_only:
        for trip in data:
            if inside_bounding_box(botleft, topright, trip.origin):
                inside.append(trip)
    elif destination_only:
        for trip in data:
            if inside_bounding_box(botleft, topright, trip.destination):
                inside.append(trip)
    else:
        for trip in data:
            if inside_bounding_box(botleft, topright, trip.origin) and inside_bounding_box(botleft, topright, trip.destination):
                inside.append(trip)
    return inside

