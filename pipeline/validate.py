"""Functions for validating the plant data extracted from API."""


def check_status_code(res):
    """Checks the status code of the response."""
    if res.status_code == 404:
        return res.json()
    if res.status_code >= 500:
        raise RuntimeError("Unable to connect to API.")
    if res.status_code == 401:
        raise PermissionError("Invalid API key or not authorised.")
    if res.status_code != 200:
        raise ValueError("Fetching plant data was not successful.")


def get_dict_of_missing_info(plant_dict, keys):

    missing_info = {}
    missing_keys = []
    missing_values = []
    for key in keys:
        if key not in plant_dict:
            missing_keys.append(key)
        else:
            if not plant_dict[key]:
                missing_values.append(key)

    if missing_keys:
        missing_info["missing_keys"] = missing_keys
    if missing_values:
        missing_info["missing_values"] = missing_values

    return missing_info


def check_missing_keys(data):
    """Check that the plant data has all valid keys."""

    required_keys = ["plant_id", "name", "temperature", "origin_location", "botanist",
                     "last_watered", "soil_moisture", "recording_taken"]

    missing_info = get_dict_of_missing_info(data, required_keys)

    return missing_info


def check_missing_location_details(data):
    """Checks that data has all relevant location details."""
    location_details = data["origin_location"]

    required_keys = ["latitude", "longitude", "country", "city"]
    missing_info = get_dict_of_missing_info(location_details, required_keys)
    return missing_info


def check_missing_botanist_details(data):
    """Checks that data has all relevant botanist details."""
    botanist_details = data["botanist"]

    required_keys = ["name", "email", "phone"]
    missing_info = get_dict_of_missing_info(botanist_details, required_keys)
    return missing_info


def validate_plant_data(data):
    """Checks that relevant keys are not missing from the plant data."""
    all_missing_keys = []

    missing_keys = check_missing_keys(data)

    if missing_keys:
        all_missing_keys.append(
            f"Plant data is missing the following: {missing_keys}")
        return all_missing_keys

    missing_location_details = check_missing_location_details(data)
    missing_botanist_details = check_missing_botanist_details(data)

    if missing_location_details:
        all_missing_keys.append(
            f"Missing keys for location: {missing_location_details}")
    if missing_botanist_details:
        all_missing_keys.append(
            f"Missing keys for botanist: {missing_botanist_details}")

    return all_missing_keys
