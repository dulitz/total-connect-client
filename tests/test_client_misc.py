"""Test total_connect_client."""

from unittest.mock import patch
import unittest
import pytest

from common import create_client
from const import (
    LOCATION_INFO_BASIC_NORMAL,
    RESPONSE_ARMED_AWAY,
    RESPONSE_ARMED_STAY,
    RESPONSE_ARMED_STAY_NIGHT,
    RESPONSE_DISARMED,
    RESPONSE_FEATURE_NOT_SUPPORTED,
    RESPONSE_GET_ZONE_DETAILS_NONE,
    RESPONSE_GET_ZONE_DETAILS_SUCCESS,
    RESPONSE_UNKNOWN,
)
from zone import ZONE_STATUS_NORMAL
from exceptions import TotalConnectError, BadResultCodeError, PartialResponseError


class TestTotalConnectClient(unittest.TestCase):
    """Test TotalConnectClient."""

    def setUp(self):
        """Test setup."""
        self.client = create_client()
        self.location_id = LOCATION_INFO_BASIC_NORMAL["LocationID"]

    def tearDown(self):
        """Test cleanup."""
        self.client = None

    def tests_zone_status(self):
        """Test zone_status."""
        responses = [RESPONSE_DISARMED]
        with patch(
            "TotalConnectClient.TotalConnectClient.request", side_effect=responses
        ):
            # should start disarmed
            assert self.client.locations[self.location_id].is_disarmed() is True

            # ask for status of zone 1, which exists
            assert self.client.zone_status(self.location_id, "1") is ZONE_STATUS_NORMAL

            # ask for status of zone 99, which does not exist
            with pytest.raises(TotalConnectError):
                self.client.zone_status(self.location_id, "99")

    def tests_get_armed_status(self):
        """Test get_armed_status."""
        responses = [
            RESPONSE_ARMED_STAY,
            RESPONSE_ARMED_STAY_NIGHT,
            RESPONSE_ARMED_AWAY,
            RESPONSE_DISARMED,
        ]
        with patch(
            "TotalConnectClient.TotalConnectClient.request", side_effect=responses
        ):
            # should start disarmed
            assert self.client.locations[self.location_id].is_disarmed() is True

            # armed_stay
            assert self.client.get_armed_status(self.location_id)
            assert self.client.locations[self.location_id].is_armed_home() is True

            # armed_stay_night
            assert self.client.get_armed_status(self.location_id)
            assert self.client.locations[self.location_id].is_armed_home() is True
            assert self.client.locations[self.location_id].is_armed_night() is True

            # armed_away
            assert self.client.get_armed_status(self.location_id)
            assert self.client.locations[self.location_id].is_armed_away() is True

            # TODO: test alarming states

            # disarmed
            assert self.client.get_armed_status(self.location_id)
            assert self.client.locations[self.location_id].is_disarmed() is True

    def tests_get_zone_details(self):
        """Test get_zone_details."""
        responses = [
            RESPONSE_GET_ZONE_DETAILS_SUCCESS,
            RESPONSE_FEATURE_NOT_SUPPORTED,
            RESPONSE_UNKNOWN,
            RESPONSE_GET_ZONE_DETAILS_NONE,
        ]
        with patch(
            "TotalConnectClient.TotalConnectClient.request", side_effect=responses
        ):
            # first response is SUCCESS
            self.client.get_zone_details(self.location_id)
            # second response is FEATURE_NOT_SUPPORTED
            with pytest.raises(BadResultCodeError):
                self.client.get_zone_details(self.location_id)
            # third response is UNKNOWN
            with pytest.raises(BadResultCodeError):
                self.client.get_zone_details(self.location_id)
            # third response is SUCCESS but with empty ZoneStatus
            # ...which we've seen before in the wild
            with pytest.raises(PartialResponseError):
                self.client.get_zone_details(self.location_id)
