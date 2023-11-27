==============
petscii-codecs
==============

The petscii-codecs package provides encodings to represent data from
Commodore 8-bit systems. These computers used a modified form of
ASCII, commonly called PETSCII, which contains graphic symbols as well
as control codes.

Codecs for the following systems are available:

- PET 2001
- later PETs
- VIC-1001
- VIC-20
- C64
- C16
- Plus4

Each system has two codecs, typically one for uppercase and graphics,
one for lowercase and uppercase. The exception is the VIC-1001 which
has a katakana codec instead of the lowercase and uppercase one.


Usage
=====

Codecs are used in the same way as other encodings::

    import petscii_codecs

    with open('example.seq', encoding='petscii_c64en_lc') as f:
        for line in f:
            print(line)
