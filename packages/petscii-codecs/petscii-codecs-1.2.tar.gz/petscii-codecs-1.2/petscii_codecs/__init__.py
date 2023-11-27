import glob
import importlib
import os.path

__version__ = '1.0'


for m in glob.glob(os.path.join(os.path.dirname(__file__), '*.py')):
    if m.startswith('__'):
        continue
    importlib.import_module('petscii_codecs.'+os.path.splitext(os.path.basename(m))[0])

del m, glob, importlib, os
