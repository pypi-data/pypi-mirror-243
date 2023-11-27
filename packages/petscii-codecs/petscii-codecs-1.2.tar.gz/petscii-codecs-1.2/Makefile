ALL_MAPPINGS := $(wildcard mappings/*.txt)
ALL_CODECS := $(ALL_MAPPINGS:mappings/%.txt=petscii_codecs/%.py)

.PHONY: install
install: $(ALL_CODECS)
	pip3 install . --upgrade

.PHONY: build
build:
	rm -rf dist
	python3 setup.py sdist bdist_wheel

.PHONY: upload
upload: build
	python3 -m twine upload dist/*

.PHONY: codecs
codecs: $(ALL_CODECS)

.PHONY: unittest
unittest:
	PYTHONPATH=$(PYTHONPATH):petscii_codecs pytest

.PHONY: clean
clean:
	rm -rf $(ALL_CODECS)

petscii_codecs/%.py: mappings/%.txt $(wildcard include/*.txt)
	gen-codec $< $@
