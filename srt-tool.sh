#!/bin/bash

HERE="$(dirname ${BASH_SOURCE[0]})"
python "${HERE}/main.py" "${@}"
