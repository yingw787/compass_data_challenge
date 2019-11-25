#!/bin/bash

# Entrypoint to be run as part of Docker container.

PYTHON=$(which python3.7)
echo $PYTHON

$PYTHON $(pwd)/part_1.py

cat schemas.txt

$PYTHON $(pwd)/part_2.py

$PYTHON $(pwd)/part_3_1.py
cat $(pwd)/problem_3_1.csv

$PYTHON $(pwd)/part_3_2.py
cat $(pwd)/problem_3_2.csv

$PYTHON $(pwd)/part_3_3.py
cat $(pwd)/problem_3_3.csv
