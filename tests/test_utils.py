import pytest
from parser import parse_details_from_text
from ocr_utils import clean_post_content
from main import hash_post_content
from constants import STATUS_ALIVE, STATUS_DEAD

def test_parse_details():
    text = "Ali Khan released a green turtle in Jiwani on March 2, 2024"
    result = parse_details_from_text(text)
    assert result['status'] in [STATUS_ALIVE, STATUS_DEAD]
    assert result['province'] in ["Balochistan", "Sindh"]

def test_clean_content():
    noisy = "This is a \x00 noisy\x1F content ™"
    clean = clean_post_content(noisy)
    assert "noisy" in clean and "™" not in clean

def test_hash():
    h = hash_post_content("sample content")
    assert isinstance(h, str) and len(h) == 64
