#!/bin/env sh

cd tests || exit 1

coverage run -m unittest discover

coverage report -m

coverage html