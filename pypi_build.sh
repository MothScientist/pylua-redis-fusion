#!/bin/env sh

python -m pip install --upgrade build
python -m pip install --upgrade twine

python -m build
python -m twine upload dist/*