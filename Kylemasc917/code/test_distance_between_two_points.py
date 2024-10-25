import pytest
import numpy as np
import math
from distance_between_two_points import (
    haversine_distance,
    read_gps_data,
    calculate_distances,
    process_gps_data
)

# Sample GPS data for testing

SAMPLE_GPS_DATA = """Latitude (°),Longitude (°),Altitude (m)
34.0,-118.0,100
34.1,-118.1,150
34.2,-118.2,200
"""

@pytest.fixture
def sample_csv_file(tmpdir):

    """Create a temporary CSV file for GPS data."""

    csv_file = tmpdir.join("gps_data.csv")
    csv_file.write(SAMPLE_GPS_DATA)
    return str(csv_file)

def test_haversine_distance():

    """Test the haversine distance calculation."""

    EARTH_RADIUS_KM = 6371.0 #radius of Earth
    point1 = (34.0, -118.0, 100)  # Latitude, Longitude, Altitude
    point2 = (34.1, -118.1, 150)

    # Calculate the distance using the function

    distance = haversine_distance(point1, point2)

    # Calculate the expected distance manually
    # Haversine formula for horizontal distance

    lat1, lon1, alt1 = point1
    lat2, lon2, alt2 = point2

    # Convert latitude and longitude from degrees to radians

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Differences in coordinates

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula to calculate horizontal distance

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    horizontal_distance = EARTH_RADIUS_KM * c

    # Calculate the vertical distance and convert to kilometers

    vertical_distance = (alt2 - alt1) / 1000.0

    # Total expected distance

    expected_distance = math.sqrt(horizontal_distance**2 + vertical_distance**2)

    # Print distances for debugging

    print(f"Calculated Distance: {distance}")
    print(f"Expected Distance: {expected_distance}")

    # Use np.isclose to compare distances

    assert np.isclose(distance, expected_distance, atol=1e-4), f"Expected {expected_distance}, got {distance}"

def test_read_gps_data(sample_csv_file):

    """Test reading GPS data from CSV."""

    gps_data = read_gps_data(sample_csv_file)

    expected_data = [
        (34.0, -118.0, 100.0),
        (34.1, -118.1, 150.0),
        (34.2, -118.2, 200.0)
    ]

    assert gps_data == expected_data, f"Expected {expected_data}, got {gps_data}"

def test_calculate_distances(sample_csv_file):

    """Test calculating distances between GPS points."""

    gps_data = read_gps_data(sample_csv_file)
    distances = calculate_distances(gps_data)

    # Expected distances calculated manually or using the haversine distance function

    expected_distances = [
        haversine_distance(gps_data[0], gps_data[1]),
        haversine_distance(gps_data[1], gps_data[2])
    ]

    assert len(distances) == len(expected_distances), "Distance length mismatch."
    for d, expected in zip(distances, expected_distances):
        assert np.isclose(d, expected, atol=1e-4), f"Expected {expected}, got {d}"

def test_process_gps_data(sample_csv_file, tmpdir):

    """Test the entire process of reading GPS data and plotting."""
    
    output_image = str(tmpdir.join("gps_motion.png"))
    distances = process_gps_data(sample_csv_file, output_image)

    assert len(distances) == 2, "Expected two distances from three points."
    assert isinstance(distances, list), "Expected output to be a list."
    assert all(isinstance(d, float) for d in distances), "Expected all distances to be floats."