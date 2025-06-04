"""Testing file for load to database script."""

from load import get_plant_master_data


def test_get_plant_master_data_null_images():

    result = get_plant_master_data({
        "plant_id": 45,
        "name": "Begonia",
        "temperature": 17.35,
        "origin_location": {
            "latitude": 14.31,
            "longitude": 21.89,
            "city": "South Julianview",
            "country": "Heard Island and McDonald Islands"
        },
        "botanist": {
            "name": "Nathan Kuhic",
            "email": "nathan.kuhic@lnhm.co.uk",
            "phone": "(470) 586-3930 x591"
        },
        "last_watered": "2025-06-03T13:32:05.000Z",
        "soil_moisture": 93.86,
        "recording_taken": "2025-06-03T15:18:44.108Z",
        "images": "null",
        "scientific_name": [
            "Begonia 'Art Hodes'"
        ]
    })

    assert not result["image_link"]
    assert all([result["scientific_name"],
               result["plant_name"], result["soil_moisture"]])


def test_get_plant_master_data_no_images_key():

    result = get_plant_master_data({
        "plant_id": 45,
        "name": "Begonia",
        "temperature": 17.35,
        "origin_location": {
            "latitude": 14.31,
            "longitude": 21.89,
            "city": "South Julianview",
            "country": "Heard Island and McDonald Islands"
        },
        "botanist": {
            "name": "Nathan Kuhic",
            "email": "nathan.kuhic@lnhm.co.uk",
            "phone": "(470) 586-3930 x591"
        },
        "last_watered": "2025-06-03T13:32:05.000Z",
        "soil_moisture": 93.86,
        "recording_taken": "2025-06-03T15:18:44.108Z",
        "scientific_name": [
            "Begonia 'Art Hodes'"
        ]
    })

    assert not result["image_link"]
    assert all([result["scientific_name"],
               result["plant_name"], result["soil_moisture"]])


def test_get_plant_master_data_good_images():

    result = get_plant_master_data({
        "plant_id": 5,
        "name": "Pitcher plant",
        "temperature": 16.81,
        "origin_location": {
            "latitude": 82.89,
            "longitude": 0.63,
            "city": "North Felicia",
            "country": "Saint Kitts and Nevis"
        },
        "botanist": {
            "name": "Benny Block",
            "email": "benny.block@lnhm.co.uk",
            "phone": "687-647-1094"
        },
        "last_watered": "2025-06-03T13:57:08.000Z",
        "soil_moisture": 95.51,
        "recording_taken": "2025-06-03T15:18:11.521Z",
        "images": {
            "license": 451,
            "license_name": "CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
            "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
            "original_url": "https://perenual.com/storage/image/upgrade_access.jpg",
            "regular_url": "https://perenual.com/storage/image/upgrade_access.jpg",
            "medium_url": "https://perenual.com/storage/image/upgrade_access.jpg",
            "small_url": "https://perenual.com/storage/image/upgrade_access.jpg",
            "thumbnail": "https://perenual.com/storage/image/upgrade_access.jpg"
        },
        "scientific_name": [
            "Sarracenia catesbaei"
        ]
    })

    assert result["image_link"]
    assert all([result["scientific_name"],
               result["plant_name"], result["soil_moisture"]])
