from unittest import mock

import pytest
from fastapi.testclient import TestClient

from app.main import SpecialNumber, app


def test_patch_mocked_validate_special_number_0():
    client = TestClient(app)
    response = client.patch("/define-special-number", json={"special_number": 3})

    assert response.status_code == 200
    assert response.json() == {"number": 30}


def test_patch_mocked_validate_special_number_1():
    client = TestClient(app)
    response = client.patch("/define-special-number", json={"special_number": 5})

    assert response.status_code == 200
    assert response.json() == {"number": 75}


def test_patch_mocked_validate_special_number_2():
    # Mock the `__init__` method of the Pydantic model to bypass validation
    with mock.patch.object(SpecialNumber, "__init__", lambda self, **kwargs: None):
        client = TestClient(app)
        response = client.patch("/define-special-number", json={"special_number": 9})

        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid special_number!"


def test_patch_mocked_validate_special_number_3():
    with mock.patch.object(
        SpecialNumber, "validate_special_number", lambda cls, value: value
    ):
        client = TestClient(app)
        # Send a valid request that would normally pass the validation
        response = client.patch("/define-special-number", json={"special_number": 3})
        assert response.status_code == 200
        assert response.json() == {"number": 30}

        # Send a request that would normally fail validation (but won't because we mocked the validator)
        response = client.patch("/define-special-number", json={"special_number": 4})
        assert (
            response.status_code == 400
        )  # It shouldn't raise 422 because we've mocked the validation
        assert response.json()["detail"] == "Invalid special_number!"


def test_patch_mocked_validate_special_number_4():
    with mock.patch.object(SpecialNumber, "validate_special_number", return_value=8):
        client = TestClient(app)
        # Send a valid request that would normally pass the validation
        response = client.patch("/define-special-number", json={"special_number": 3})
        assert response.status_code == 200
        assert response.json() == {"number": 30}

        # Send a request that would normally fail validation (but won't because we mocked the validator)
        response = client.patch("/define-special-number", json={"special_number": 4})
        assert (
            response.status_code == 400
        )  # It shouldn't raise 422 because we've mocked the validation
        assert response.json()["detail"] == "Invalid special_number!"


pytest.main()
