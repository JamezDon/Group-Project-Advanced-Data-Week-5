"""Tests for checking plant data for alerts."""
# from datetime import datetime
# from unittest.mock import MagicMock

# from alert_data import alert_is_required

# mock_cursor = MagicMock()
# mock_cursor.fetchone.return_value = 0
# mock_conn = MagicMock()
# mock_conn.cursor.return_value = mock_cursor
# test_time = datetime.strftime(datetime.now(), "%Y-%m-%d")


# def test_check_for_alerts_when_soil_moisture_too_low():
#     """Checks that the function identifies a plant as needed
#     an alert when the soil moisture is too low."""

#     plant = [{"plant_id": "", "plant_name": "",
#               "avg_temp": 20, "avg_soil_moisture": 8.55}]

#     assert alert_is_required(plant, mock_conn) == [{"plant_id": "", "plant_name": "",
#                                                    "avg_temp": 20, "avg_soil_moisture": 8.55,
#                                                     "alert_sent_at": test_time,
#                                                     "alert_type": ["soil_moisture"]}]


# def test_check_for_alerts_when_temp_too_high():
#     """Checks that the function identifies a plant as needed
#     an alert when the temp is too high."""

#     plant = [{"plant_id": "", "plant_name": "",
#               "avg_temp": 35.8, "avg_soil_moisture": 25}]

#     assert check_for_alerts(plant, mock_conn) == [{"plant_id": "", "plant_name": "",
#                                                    "avg_temp": 35.8, "avg_soil_moisture": 25,
#                                                    "alert_sent_at": test_time,
#                                                    "alert_type": ["temperature"]}]


# def test_check_for_alerts_when_temp_too_low():
#     """Checks that the function identifies a plant as needed
#     an alert when the temp is too low."""

#     plant = [{"plant_id": "", "plant_name": "",
#               "avg_temp": 10.2, "avg_soil_moisture": 25}]

#     assert check_for_alerts(plant, mock_conn) == [{"plant_id": "", "plant_name": "",
#                                                    "avg_temp": 10.2, "avg_soil_moisture": 25,
#                                                    "alert_sent_at": test_time,
#                                                    "alert_type": ["temperature"]}]


# def test_check_for_alerts_when_temp_too_low_and_sm_too_low():
#     """Checks that the function identifies a plant as needed
#     an alert when the temp is too low and soil moisture is too low."""

#     plant = [{"plant_id": "", "plant_name": "",
#               "avg_temp": 10.2, "avg_soil_moisture": 8.3}]

#     assert check_for_alerts(plant, mock_conn) == [{"plant_id": "", "plant_name": "",
#                                                    "avg_temp": 10.2, "avg_soil_moisture": 8.3,
#                                                    "alert_sent_at": test_time,
#                                                    "alert_type": ["temperature", "soil_moisture"]}]


# def test_check_for_alerts_when_temp_too_high_and_sm_too_low():
#     """Checks that the function identifies a plant as needed
#     an alert when the temp is too high and soil moisture is too low."""

#     plant = [{"plant_id": "", "plant_name": "",
#               "avg_temp": 50.2, "avg_soil_moisture": 5.3}]

#     assert check_for_alerts(plant, mock_conn) == [{"plant_id": "", "plant_name": "",
#                                                    "avg_temp": 50.2, "avg_soil_moisture": 5.3,
#                                                    "alert_sent_at": test_time,
#                                                    "alert_type": ["temperature", "soil_moisture"]}]
