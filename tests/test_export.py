import os
import sys
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from export import MissingAPIKeyError, DefaultFilenameError, validate_api_key, validate_filename, get_headers

def test_missing_api_key():
    with pytest.raises(MissingAPIKeyError):
        validate_api_key(" ")

def test_valid_api_key():
    test_key = "  valid-key-123  "
    cleaned_key = validate_api_key(test_key)
    assert cleaned_key == "valid-key-123"

def test_get_headers():
    test_key = "  valid-key-123  "
    headers = get_headers(test_key)
    assert headers["apikey"] == "valid-key-123"
    assert headers["Content-Type"] == "application/json"

def test_get_headers_empty_key():
    with pytest.raises(MissingAPIKeyError):
        get_headers(" ")

def test_default_filename():
    test_cases = [
        "exported_links_renamethis.csv",
        "exported_links_RENAMETHIS.csv",
        "something_renamethis_else.csv"
    ]
    
    for filename in test_cases:
        with pytest.raises(DefaultFilenameError):
            validate_filename(filename)

def test_valid_filename():
    valid_filenames = [
        "my_exported_links.csv",
        "custom_export_2024.csv",
        "links_backup.csv"
    ]
    
    for filename in valid_filenames:
        validate_filename(filename)  # Should not raise any exception 