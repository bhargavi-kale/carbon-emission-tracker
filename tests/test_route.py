"""
Unit tests for the Route class using mocking to avoid network dependency.
"""

from unittest.mock import patch, MagicMock
import pytest
from src.route import calculate_distance


@patch("src.route.requests.post")
def test_calculate_distance_mocked(mock_post):
    """
    HAPPY PATH: Test distance calculation without a real network call.
    """
    # 1. Define the hardcoded response shape defined in the test itself
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "routes": [{"distanceMeters": 16093.4}]  # Exactly 10 miles
    }

    # 2. Tell the mock to return this object when requests.post is called
    mock_post.return_value = mock_response

    # 3. Execute the function
    distance = calculate_distance("Manchester, NH", "Boston, MA")

    # 4. Assertions
    # We check if the conversion logic (meters to miles) is correct
    assert pytest.approx(distance, rel=1e-2) == 10.0

    # Ensure the 'network' was actually intercepted and not called for real
    mock_post.assert_called_once()
