import pytest

import petscii_codecs


def test_control():
    assert b'\x08\x09'.decode('petscii_vic20en_uc') == "\uf118\uf119"
    assert b'\x9f'.decode('petscii_vic20en_uc') == "\uf10f"  # cyan

    with pytest.raises(UnicodeDecodeError):
        _ = b'\x95'.decode('petscii_vic20en_uc')  # C64 brown

def test_symbol():
    assert b'\x5c'.decode('petscii_vic20en_uc') == "£"
    assert "£".encode('petscii_vic20en_uc') == b'\x5c'
