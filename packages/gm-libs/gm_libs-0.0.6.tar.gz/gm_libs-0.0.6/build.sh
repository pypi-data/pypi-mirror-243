#!/bin/bash

rm dist/*
python -m build
python -m twine upload dist/* < __token__