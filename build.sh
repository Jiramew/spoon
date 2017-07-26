#!bin/bash
python setup_pypi.py sdist build
python setup_pypi.py bdist_wheel --universal
twine upload dist/*
