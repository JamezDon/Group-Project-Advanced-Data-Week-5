# Clean the raw data from api

def check_plant_found(data):
    """Checks whether plant was found."""
    return "error" in data


def check_missing_keys(data):
    """Check that the plant data has all valid keys."""

    required_keys = ["plant_id", "name", "temperature", "origin_location", "botanist",
                     "last_watered", "soil_moisture", "recording_taken"]

    missing_key = []
    for key in required_keys:
        if key not in data:
            missing_key.append(key)
    return missing_key


def check_missing_location_details(data):
    """Checks that data has all relevant location details."""
    location_details = data["origin_locations"]

    required_keys = ["latitude", "longitude", "country", "city"]
    missing_key = []
    for key in required_keys:
        if key not in location_details:
            missing_key.append(key)
    return missing_key


def check_missing_botanist_details(data):
    """Checks that data has all relevant botanist details."""
    botanist_details = data["botanist"]

    required_keys = ["name", "email", "phone"]
    missing_key = []
    for key in required_keys:
        if key not in botanist_details:
            missing_key.append(key)
    return missing_key


def validate_data(data):
    """Cleans and validates the plant data."""

    missing_keys = check_missing_keys(data)
    if missing_keys:
        return f"Plant data has the following keys missing: {missing_keys}"

    missing_details = {}
    missing_details["location"] = check_missing_location_details(data)
    missing_details["botanist"] = check_missing_botanist_details(data)
    # missing_location = check_missing_location_details(data)
    # missing_botanist = check_missing_botanist_details(data)
    for key in missing_details:
        if key:
            return f"Mssing details for {key}: {missing_details[key]}"
    return data
