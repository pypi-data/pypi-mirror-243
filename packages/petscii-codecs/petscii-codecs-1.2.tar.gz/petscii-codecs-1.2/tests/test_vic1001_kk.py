import pytest

import petscii_codecs


def test_lower():
    with pytest.raises(UnicodeEncodeError):
        _ = "a".encode('petscii_vic1001jp_kk')

def test_katakana():
    assert b'\x79'.decode('petscii_vic1001jp_kk') == "ル"
    assert b'\xa5'.decode('petscii_vic1001jp_kk') == "オ"
    assert b'\xd2'.decode('petscii_vic1001jp_kk') == "メ"

def test_sound_mark():
    assert b'\xaa\xde\xea'.decode('petscii_vic1001jp_kk') == "゛゛゛"
    assert b'\xa1\xaf\xef'.decode('petscii_vic1001jp_kk') == "゜゜゜"

def test_unified():
    assert b'\xf4\xf5\xf6'.decode('petscii_vic1001jp_kk') == "年月日"
