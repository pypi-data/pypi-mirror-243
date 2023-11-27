import pytest

import petscii_codecs


def test_upper():
    assert b'ABCDEFG'.decode('petscii_c64en_uc') == "ABCDEFG"
    assert "ABCDEFG".encode('petscii_c64en_uc') == b'ABCDEFG'

def test_control():
    assert b'\x0d'.decode('petscii_c64en_uc') == "\r"
    assert b'\x9f'.decode('petscii_c64en_uc') == "\uf10f"  # cyan
    assert b'\x95'.decode('petscii_c64en_uc') == "\uf106"  # brown

def test_symbol():
    assert b'\x61\x73\x78\x7a'.decode('petscii_c64en_uc') == "♠♥♣♦"
    assert b'\xc1\xd3\xd8\xda'.decode('petscii_c64en_uc') == "♠♥♣♦"
    assert "♠♥♣♦".encode('petscii_c64en_uc') == b'\xc1\xd3\xd8\xda'
    assert b'\x7e\xde\xff'.decode('petscii_c64en_uc') == "πππ"  # 3 different mappings
    assert "π".encode('petscii_c64en_uc') == b'\xff'
    assert b'\x5e'.decode('petscii_c64en_uc') == "↑"
    assert b'\x5f'.decode('petscii_c64en_uc') == "←"

    with pytest.raises(UnicodeEncodeError):
        _ = "^".encode('petscii_c64en_uc')
    with pytest.raises(UnicodeEncodeError):
        _ = "_".encode('petscii_c64en_uc')

def test_line():
    assert b'\x60\xc0'.decode('petscii_c64en_uc') == "──"
    assert "─".encode('petscii_c64en_uc') == b'\xc0'
    assert b'\x7d\xdd'.decode('petscii_c64en_uc') == "││"
    assert "│".encode('petscii_c64en_uc') == b'\xdd'
    assert b'\x6d\x6e\x76'.decode('petscii_c64en_uc') == "╲╱╳"
    assert b'\xcd\xce\xd6'.decode('petscii_c64en_uc') == "╲╱╳"
    assert "╲╱╳".encode('petscii_c64en_uc') == b'\xcd\xce\xd6'
