"""Tests for checking plant data for alerts."""
from alert_data import check_for_alerts


def test_check_for_alerts_when_soil_moisture_too_low():
    """Checks that the function identifies a plant as needed 
    an alert when the soil moisture is too low."""

    plant = [{"plant_id": "", "plant_name": "",
              "avg_temp": 20, "avg_soil_moisture": 8.55}]

    assert check_for_alerts(plant) == [{"plant_id": "", "plant_name": "",
                                       "avg_temp": 20, "avg_soil_moisture": 8.55,
                                        "soil_moisture_alert": True,
                                        "temp_alert": False}]


def test_check_for_alerts_when_soil_moisture_too_high():
    """Checks that the function identifies a plant as needed 
    an alert when the soil moisture is too high."""

    plant = [{"plant_id": "", "plant_name": "",
              "avg_temp": 20, "avg_soil_moisture": 62.3}]

    assert check_for_alerts(plant) == [{"plant_id": "", "plant_name": "",
                                       "avg_temp": 20, "avg_soil_moisture": 62.3,
                                        "soil_moisture_alert": True,
                                        "temp_alert": False}]


def test_check_for_alerts_when_temp_too_high():
    """Checks that the function identifies a plant as needed 
    an alert when the temp is too high."""

    plant = [{"plant_id": "", "plant_name": "",
              "avg_temp": 35.8, "avg_soil_moisture": 15}]

    assert check_for_alerts(plant) == [{"plant_id": "", "plant_name": "",
                                       "avg_temp": 35.8, "avg_soil_moisture": 15,
                                        "soil_moisture_alert": False,
                                        "temp_alert": True}]


def test_check_for_alerts_when_temp_too_low():
    """Checks that the function identifies a plant as needed 
    an alert when the temp is too low."""

    plant = [{"plant_id": "", "plant_name": "",
              "avg_temp": 10.2, "avg_soil_moisture": 15}]

    assert check_for_alerts(plant) == [{"plant_id": "", "plant_name": "",
                                       "avg_temp": 10.2, "avg_soil_moisture": 15,
                                        "soil_moisture_alert": False,
                                        "temp_alert": True}]


def test_check_for_alerts_when_temp_too_high_and_sm_too_high():
    """Checks that the function identifies a plant as needed 
    an alert when the temp is too high and soil moisture is too high."""

    plant = [{"plant_id": "", "plant_name": "",
              "avg_temp": 39.2, "avg_soil_moisture": 80.2}]

    assert check_for_alerts(plant) == [{"plant_id": "", "plant_name": "",
                                       "avg_temp": 39.2, "avg_soil_moisture": 80.2,
                                        "soil_moisture_alert": True,
                                        "temp_alert": True}]


def test_check_for_alerts_when_temp_too_low_and_sm_too_low():
    """Checks that the function identifies a plant as needed 
    an alert when the temp is too low and soil moisture is too low."""

    plant = [{"plant_id": "", "plant_name": "",
              "avg_temp": 10.2, "avg_soil_moisture": 8.3}]

    assert check_for_alerts(plant) == [{"plant_id": "", "plant_name": "",
                                       "avg_temp": 10.2, "avg_soil_moisture": 8.3,
                                        "soil_moisture_alert": True,
                                        "temp_alert": True}]


def test_check_for_alerts_when_temp_too_low_and_sm_too_high():
    """Checks that the function identifies a plant as needed 
    an alert when the temp is too low and soil moisture is too high."""

    plant = [{"plant_id": "", "plant_name": "",
              "avg_temp": 10.2, "avg_soil_moisture": 88.3}]

    assert check_for_alerts(plant) == [{"plant_id": "", "plant_name": "",
                                       "avg_temp": 10.2, "avg_soil_moisture": 88.3,
                                        "soil_moisture_alert": True,
                                        "temp_alert": True}]


def test_check_for_alerts_when_temp_too_high_and_sm_too_low():
    """Checks that the function identifies a plant as needed 
    an alert when the temp is too high and soil moisture is too low."""

    plant = [{"plant_id": "", "plant_name": "",
              "avg_temp": 50.2, "avg_soil_moisture": 5.3}]

    assert check_for_alerts(plant) == [{"plant_id": "", "plant_name": "",
                                       "avg_temp": 50.2, "avg_soil_moisture": 5.3,
                                        "soil_moisture_alert": True,
                                        "temp_alert": True}]
