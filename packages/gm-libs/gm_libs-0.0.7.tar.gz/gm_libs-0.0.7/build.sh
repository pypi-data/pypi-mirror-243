#!/bin/bash

rm dist/*
python -m build
python -m twine upload dist/* <<< __token__

pip install gm-libs -U