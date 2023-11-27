import pytest

import petscii_codecs


def test_lower():
    assert b'ABCDEFG'.decode('petscii_c64en_lc') == "abcdefg"
    assert b'abcdefg'.decode('petscii_c64en_lc') == "ABCDEFG"
    assert b'\xc1\xc2\xc3\xc4\xc5\xc6\xc7'.decode('petscii_c64en_lc') == "ABCDEFG"
    assert "ABCDEFG".encode('petscii_c64en_lc') == b'\xc1\xc2\xc3\xc4\xc5\xc6\xc7'
    assert "abcdefg".encode('petscii_c64en_lc') == b'ABCDEFG'

def test_control():
    assert b'\x0d'.decode('petscii_c64en_lc') == "\r"
    assert b'\x9f'.decode('petscii_c64en_lc') == "\uf10f"  # cyan
    assert b'\x95'.decode('petscii_c64en_lc') == "\uf106"  # brown

def test_symbol():
    assert b'\x5e'.decode('petscii_c64en_lc') == "↑"
    assert b'\x5f'.decode('petscii_c64en_lc') == "←"

    with pytest.raises(UnicodeEncodeError):
        _ = "♠".encode('petscii_c64en_lc')
    with pytest.raises(UnicodeEncodeError):
        _ = "π".encode('petscii_c64en_lc')
    with pytest.raises(UnicodeEncodeError):
        _ = "^".encode('petscii_c64en_lc')
    with pytest.raises(UnicodeEncodeError):
        _ = "_".encode('petscii_c64en_lc')

def test_graphic():
    assert b'\x7e\x7f\xa9\xba'.decode('petscii_c64en_lc') == "▒\uf139\uf13a✓"
    assert b'\xde\xdf\xe9\xfa\xff'.decode('petscii_c64en_lc') == "▒\uf139\uf13a✓▒"
