from src.ml_service_client import FoulLanguageDetector, backoff_timeout
from src.mocked_requests import requests

from unittest.mock import patch


@patch("src.ml_service_client._sleep")
def test_detect_foul_language_ok(_sleep):
    fld = FoulLanguageDetector(requests)
    is_foul = fld.predict_foul_language("a not nasty paragraph")

    assert type(is_foul) is bool


def test_backoff_timeout_ok():
    assert 0.6 + 0.5 < backoff_timeout(1) < 0.6 + 1.5
    assert 0.3 + 0.5 < backoff_timeout(0) < 0.3 + 1.5
    assert 9.6 + 0.5 < backoff_timeout(5) < 9.6 + 1.5