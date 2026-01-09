import pytest
from datetime import timedelta
from jose import jwt
import os
from unittest.mock import patch

from src.auth.jwt import create_access_token, verify_token, is_token_expired, extract_user_id_from_token
from src.config import settings


def test_create_access_token():
    """Test creating a valid access token."""
    data = {"sub": "test_user_id", "email": "test@example.com"}
    token = create_access_token(data=data)

    # Decode the token to verify its contents
    decoded = jwt.decode(token, settings.better_auth_secret, algorithms=["HS256"])

    assert decoded["sub"] == "test_user_id"
    assert decoded["email"] == "test@example.com"


def test_verify_valid_token():
    """Test verifying a valid token."""
    data = {"sub": "test_user_id", "email": "test@example.com"}
    token = create_access_token(data=data)

    payload = verify_token(token)

    assert payload["sub"] == "test_user_id"
    assert payload["email"] == "test@example.com"


def test_verify_invalid_token():
    """Test verifying an invalid token raises HTTPException."""
    from fastapi import HTTPException

    with pytest.raises(HTTPException) as exc_info:
        verify_token("invalid_token")

    assert exc_info.value.status_code == 401


def test_verify_expired_token():
    """Test verifying an expired token raises HTTPException."""
    from fastapi import HTTPException

    # Create a token that expires immediately
    data = {"sub": "test_user_id", "email": "test@example.com"}
    token = create_access_token(data=data, expires_delta=timedelta(seconds=-1))

    with pytest.raises(HTTPException) as exc_info:
        verify_token(token)

    assert exc_info.value.status_code == 401


def test_is_token_expired_with_valid_token():
    """Test that a valid token is not marked as expired."""
    data = {"sub": "test_user_id", "email": "test@example.com"}
    token = create_access_token(data=data)

    expired = is_token_expired(token)

    assert expired is False


def test_is_token_expired_with_expired_token():
    """Test that an expired token is marked as expired."""
    data = {"sub": "test_user_id", "email": "test@example.com"}
    token = create_access_token(data=data, expires_delta=timedelta(seconds=-1))

    expired = is_token_expired(token)

    assert expired is True


def test_extract_user_id_from_token():
    """Test extracting user ID from a valid token."""
    data = {"sub": "test_user_id", "email": "test@example.com"}
    token = create_access_token(data=data)

    user_id = extract_user_id_from_token(token)

    assert user_id == "test_user_id"


def test_extract_user_id_from_invalid_token():
    """Test extracting user ID from an invalid token raises HTTPException."""
    from fastapi import HTTPException

    with pytest.raises(HTTPException) as exc_info:
        extract_user_id_from_token("invalid_token")

    assert exc_info.value.status_code == 401


def test_validate_user_id_matching():
    """Test that validate_user_id passes when user IDs match."""
    from unittest.mock import patch
    from src.auth.deps import validate_user_id

    # Mock the get_user_id_from_token dependency to return a matching ID
    with patch('src.auth.deps.get_user_id_from_token') as mock_get_user_id:
        mock_get_user_id.return_value = "user123"

        result = validate_user_id("user123")

        assert result == "user123"


def test_validate_user_id_mismatch():
    """Test that validate_user_id raises HTTPException when user IDs don't match."""
    from fastapi import HTTPException
    from src.auth.deps import validate_user_id

    # Mock the get_user_id_from_token dependency to return a different ID
    with patch('src.auth.deps.get_user_id_from_token') as mock_get_user_id:
        mock_get_user_id.return_value = "different_user"

        with pytest.raises(HTTPException) as exc_info:
            validate_user_id("user123")

        assert exc_info.value.status_code == 403
        assert "access your own resources" in str(exc_info.value.detail)