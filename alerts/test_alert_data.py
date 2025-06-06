"""Tests for checking plant data for alerts."""

from unittest.mock import MagicMock, patch

from alert_data import temp_alert_required, soil_moisture_alert_required

mock_conn = MagicMock()


@patch("alert_data.recent_alert_sent", return_value=False)
def test_temp_alert_required_temp_too_high(self):
    """Checks that the function identifies a plant as needed
    a temperature alert when the temp is too high."""

    plant = {"plant_id": "", "plant_name": "",
             "avg_temp": 50, "avg_soil_moisture": 5.3}

    assert temp_alert_required(plant, mock_conn)


@patch("alert_data.recent_alert_sent", return_value=False)
def test_temp_alert_required_temp_too_low(self):
    """Checks that the function identifies a plant as needed
    a temperature alert when the temp is too low."""

    plant = {"plant_id": "", "plant_name": "",
             "avg_temp": 10, "avg_soil_moisture": 5.3}

    assert temp_alert_required(plant, mock_conn)


@patch("alert_data.recent_alert_sent", return_value=False)
def test_temp_alert_required_returns_false_temp_in_range(self):
    """Checks that the function identifies a plant as needed
    a temperature alert when the temp is within good range."""

    plant = {"plant_id": "", "plant_name": "",
             "avg_temp": 25, "avg_soil_moisture": 5.3}

    assert not temp_alert_required(plant, mock_conn)


@patch("alert_data.recent_alert_sent", return_value=False)
def test_temp_alert_required_returns_false_temp_at_lower_threshold(self):
    """Checks that the function identifies a plant as needed
    a temperature alert when the temp is at the lower threshold of good range."""

    plant = {"plant_id": "", "plant_name": "",
             "avg_temp": 15.0, "avg_soil_moisture": 5.3}

    assert not temp_alert_required(plant, mock_conn)


@patch("alert_data.recent_alert_sent", return_value=False)
def test_temp_alert_required_returns_true_temp_just_above_good_range(self):
    """Checks that the function identifies a plant as needed
    a temperature alert when the temp is just above upper threshold of good range."""

    plant = {"plant_id": "", "plant_name": "",
             "avg_temp": 30.1, "avg_soil_moisture": 5.3}

    assert temp_alert_required(plant, mock_conn)


@patch("alert_data.recent_alert_sent", return_value=False)
def test_temp_alert_required_returns_true_just_below_good_range(self):
    """Checks that the function identifies a plant as needed
    a temperature alert when the temp is just below lower threshold of good range."""

    plant = {"plant_id": "", "plant_name": "",
             "avg_temp": 14.9, "avg_soil_moisture": 5.3}

    assert temp_alert_required(plant, mock_conn)


@patch("alert_data.recent_alert_sent", return_value=False)
def test_soil_moisture_alert_required_returns_true_just_too_low(self):
    """Checks that the function identifies a plant as needed
    a temperature alert when the soil moisture is just below lower threshold of good range."""

    plant = {"plant_id": "", "plant_name": "",
             "avg_temp": 15.0, "avg_soil_moisture": 19.9}

    assert soil_moisture_alert_required(plant, mock_conn)


@patch("alert_data.recent_alert_sent", return_value=False)
def test_soil_moisture_alert_required_returns_true_zero_reading(self):
    """Checks that the function identifies a plant as needed
    a temperature alert when the soil moisture is at lower threshold of good range."""

    plant = {"plant_id": "", "plant_name": "",
             "avg_temp": 15.0, "avg_soil_moisture": 0}

    assert soil_moisture_alert_required(plant, mock_conn)


@patch("alert_data.recent_alert_sent", return_value=False)
def test_soil_moisture_alert_required_returns_false_in_good_range(self):
    """Checks that the function identifies a plant as needed
    a temperature alert when the soil moisture is just inside good range."""

    plant = {"plant_id": "", "plant_name": "",
             "avg_temp": 15.0, "avg_soil_moisture": 20.1}

    assert not soil_moisture_alert_required(plant, mock_conn)


@patch("alert_data.recent_alert_sent", return_value=False)
def test_soil_moisture_alert_required_returns_false_in_good_range(self):
    """Checks that the function identifies a plant as needed
    a temperature alert when the soil moisture is at lower threshold of good range."""

    plant = {"plant_id": "", "plant_name": "",
             "avg_temp": 15.0, "avg_soil_moisture": 20.0}

    assert not soil_moisture_alert_required(plant, mock_conn)
