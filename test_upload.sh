#!/usr/bin/env sh

rm -rf build
rm -rf dist

python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository testpypi dist/*
